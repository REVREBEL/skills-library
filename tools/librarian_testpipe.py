#!/usr/bin/env python3
"""
Librarian Test Pipe

Runs the full Librarian pipeline on a set of candidate skills in intake/,
writes approved skills to a test library folder, generates routers and a
manifest, and prints a summary of what happened.

Usage:
    python3 tools/librarian_testpipe.py                    # process all candidates
    python3 tools/librarian_testpipe.py --candidate NAME   # process one
    python3 tools/librarian_testpipe.py --dry-run          # evaluate only, no writes
    python3 tools/librarian_testpipe.py --reset            # wipe test library first

The test library is written to test-library/ (gitignored). It is a
self-contained output: library/<category>/<subcategory>/<skill>/ plus
routers and a manifest. It never touches the real library/.
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.librarian import (
    retrieve_candidates,
    rerank_candidates,
    extract_claims,
    diff_claims,
    decide_merge,
)
from skill_library.librarian_ai import (
    extract_claims_opencode,
    decide_merge_opencode,
    rerank_with_openrouter,
    CLAIM_MODEL,
    DECISION_MODEL,
)
from skill_library.scanner import scan_intake, scan_candidate_directory

TEST_INTAKE = REPO_ROOT / "test-intake"
TEST_LIBRARY = REPO_ROOT / "test-library"
TEST_MANIFEST = TEST_LIBRARY / "runtime-manifest.json"
TEST_LEDGER = TEST_LIBRARY / "change-ledger.jsonl"


def reset_test_library():
    """Wipe the test library and start fresh."""
    if TEST_LIBRARY.exists():
        shutil.rmtree(TEST_LIBRARY)
    TEST_LIBRARY.mkdir(parents=True, exist_ok=True)
    TEST_MANIFEST.write_text(json.dumps({"version": "1.0", "skills": {}}, indent=2))
    TEST_LEDGER.write_text("")
    print(f"Test library reset: {TEST_LIBRARY}")


def build_catalog_index():
    """Build a catalog index from the real library for retrieval."""
    from skill_library.intake import tokenize, _extract_body_for_similarity

    catalog = []
    for skill_md in sorted((REPO_ROOT / "library").glob("**/**/SKILL.md")):
        rel = skill_md.relative_to(REPO_ROOT).as_posix()
        parts = rel.split("/")
        if len(parts) < 4:
            continue
        skill_dir = skill_md.parent
        try:
            content = skill_md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fm = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not fm:
            continue
        fm_text = fm.group(1)
        name = ""
        desc = ""
        m = re.search(r'^name:\s*"?(.*?)"?\s*$', fm_text, re.MULTILINE)
        if m:
            name = m.group(1)
        m = re.search(r'^description:\s*"?(.*?)"?\s*$', fm_text, re.MULTILINE | re.DOTALL)
        if m:
            desc = m.group(1).strip().strip('"')
        if not name:
            name = skill_dir.name
        body = _extract_body_for_similarity(content)
        catalog.append({
            "name": name,
            "canonical_path": str(skill_dir.relative_to(REPO_ROOT)),
            "tokens": tokenize(name + " " + desc + " " + body),
            "description": desc,
            "body_sample": body,
        })
    return catalog


def write_skill_to_test_library(skill_name, body, description, category, subcategory, role, source_path):
    """Write a skill to the test library with proper frontmatter."""
    if subcategory:
        dest_dir = TEST_LIBRARY / category / subcategory / skill_name
    else:
        dest_dir = TEST_LIBRARY / category / skill_name
    dest_dir.mkdir(parents=True, exist_ok=True)

    skill_md = dest_dir / "SKILL.md"
    skill_md.write_text(body, encoding="utf-8")

    # Record in manifest
    manifest = json.loads(TEST_MANIFEST.read_text())
    rel_path = str(dest_dir.relative_to(TEST_LIBRARY))
    manifest["skills"][skill_name] = {
        "canonical_path": rel_path,
        "category": category,
        "subcategory": subcategory,
        "role": role,
        "source": source_path,
    }
    TEST_MANIFEST.write_text(json.dumps(manifest, indent=2))

    # Record in ledger
    from datetime import datetime, timezone
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "INSTALL",
        "skill": skill_name,
        "path": rel_path,
        "source": source_path,
        "role": role,
    }
    with open(TEST_LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    return dest_dir


def merge_claims_into_skill(target_name, include_claims):
    """Append included claims to the target skill's body in the test library.

    For SUPPLEMENT verdicts, the included claims are appended as a new
    section in the target skill's SKILL.md. Claims that are already
    covered by the existing body are skipped — the diff already identified
    restatements, so we only add genuinely new claims.
    """
    # Find the target skill in the test library
    target_md = None
    for p in TEST_LIBRARY.glob(f"**/{target_name}/SKILL.md"):
        target_md = p
        break
    if not target_md or not target_md.exists():
        return None

    content = target_md.read_text(encoding="utf-8")

    # Filter out claims already covered by the existing body
    from skill_library.intake import tokenize, compute_dice_similarity
    body_tokens = tokenize(content)
    new_claims = []
    for c in include_claims:
        claim_tokens = tokenize(c.text)
        sim = compute_dice_similarity(body_tokens, claim_tokens)
        if sim < 0.5:  # Only add claims that aren't already covered
            new_claims.append(c)

    if not new_claims:
        return None  # Nothing new to add

    # Build the merge section
    claims_text = "\n".join(f"- {c.text}" for c in new_claims)
    merge_section = f"\n\n## Merged Capabilities\n\n{claims_text}\n"

    target_md.write_text(content + merge_section, encoding="utf-8")
    return target_md


def generate_routers():
    """Generate a root -> category -> subcategory -> skill router tree.

    Walks up from each real skill (a SKILL.md with a `name:` field), so
    category routers are discovered even when their subcategory routers
    do not exist yet. Generates deepest routers first so category routers
    can then link to them. All paths are relative to the router.
    """
    from skill_library.config import CATEGORIES

    test_lib = TEST_LIBRARY.resolve()

    def _has_name_frontmatter(skill_md: Path) -> bool:
        try:
            head = skill_md.read_text(encoding="utf-8")[:500]
        except Exception:
            return False
        if not head.startswith("---"):
            return False
        parts = head.split("---", 2)
        return len(parts) >= 2 and "name:" in parts[1]

    # Collect every ancestor of a skill as a router directory.
    router_dirs = set()
    for skill_md in test_lib.rglob("SKILL.md"):
        if not _has_name_frontmatter(skill_md):
            continue
        parent = skill_md.parent.parent.resolve()
        while parent != test_lib and parent != parent.parent:
            router_dirs.add(parent)
            parent = parent.parent

    # Deepest first: subcategory routers appear before category routers.
    for router_dir in sorted(router_dirs, key=lambda p: len(p.parts), reverse=True):
        entries = []
        for child in sorted(router_dir.iterdir()):
            if not child.is_dir():
                continue
            child_md = child / "SKILL.md"
            if not child_md.exists():
                continue
            if _has_name_frontmatter(child_md):
                entries.append(f"- [`{child.name}`]({child.name}/SKILL.md)")
            else:
                entries.append(f"- [{child.name}]({child.name}/SKILL.md)")
        if entries:
            (router_dir / "SKILL.md").write_text(
                f"# {router_dir.name} Router\n\n" + "\n".join(entries) + "\n",
                encoding="utf-8",
            )
            print(f"  router: {router_dir.relative_to(test_lib)} ({len(entries)} entries)")

    # Root router lists top-level categories.
    root_links = []
    for cat in CATEGORIES:
        if (test_lib / cat).exists():
            root_links.append(f"- [{cat}]({cat}/SKILL.md)")
    (test_lib / "SKILL.md").write_text(
        "# Test Library Root\n\n" + "\n".join(root_links) + "\n",
        encoding="utf-8",
    )


def process_candidate(candidate, catalog, dry_run=False, max_matches=1):
    """Run the Librarian pipeline on a single candidate. Returns the proposal."""
    print(f"\n{'='*60}")
    print(f"Processing: {candidate.name}")
    print(f"Description: {candidate.description[:80]}...")
    print(f"{'='*60}")

    # Step 1: Deterministic scan (already done by scan_intake)
    print(f"[1/6] Deterministic scan: PASSED")

    # Step 2: Dice retrieval
    retrieved = retrieve_candidates(
        candidate_name=candidate.name,
        candidate_description=candidate.description,
        candidate_body=candidate.body_sample,
        catalog=catalog,
    )
    print(f"[2/6] Dice retrieval: {len(retrieved)} candidates")
    for i, rc in enumerate(retrieved[:5]):
        print(f"  [{i+1}] {rc.name} (sim={rc.similarity:.3f})")

    if not retrieved:
        print("\n=== Recommendation: NEW ===")
        return {"verdict": "NEW", "proposals": []}

    # Step 3: Rerank
    print(f"[3/6] Rerank: {len(retrieved)} candidates")
    try:
        reranked = rerank_candidates(
            query=candidate.description,
            candidates=retrieved,
            rerank_fn=rerank_with_openrouter,
        )
        for i, rc in enumerate(reranked[:5]):
            print(f"  [{i+1}] {rc.name} (rerank={rc.rerank_score:.3f}, dice={rc.dice_similarity:.3f})")
    except Exception as e:
        print(f"  Rerank failed: {e}")
        print(f"  Falling back to Dice order")
        from skill_library.librarian import RerankedCandidate
        reranked = [
            RerankedCandidate(
                name=c.name, canonical_path=c.canonical_path,
                rerank_score=c.similarity, dice_similarity=c.similarity,
                description=c.description,
            )
            for c in retrieved
        ]

    # Step 4: Claim extraction
    print(f"[4/6] Claim extraction: {CLAIM_MODEL}")
    print(f"  Extracting claims from {candidate.name} (candidate)...", flush=True)
    try:
        candidate_claims = extract_claims(
            skill_name=candidate.name,
            skill_body=candidate.body_sample,
            extract_fn=extract_claims_opencode,
        )
        print(f"  Extracted {len(candidate_claims)} claims from candidate")
    except Exception as e:
        print(f"  Claim extraction failed: {e}")
        candidate_claims = []

    # Dedupe by name (the catalog contains nested copies of some skills,
    # e.g. two `brutalism` entries). Keep the highest-ranked copy.
    seen_names = set()
    unique_reranked = []
    for rc in reranked:
        if rc.name in seen_names:
            continue
        seen_names.add(rc.name)
        unique_reranked.append(rc)
    reranked = unique_reranked

    # Step 5: Claim diff + Step 6: Merge decision
    proposals = []
    for rc in reranked[:max_matches]:
        print(f"[5/6] Claim diff vs {rc.name}")
        print(f"  Extracting claims from {rc.name} (existing)...", flush=True)
        print(f"[6/6] Merge decision: {DECISION_MODEL}")
        try:
            # Self-match optimization: if the top catalog hit is the same
            # skill at (nearly) identical similarity, reuse the candidate's
            # claims instead of paying for another extraction call.
            if rc.name == candidate.name and rc.dice_similarity >= 0.99:
                print(f"  Self-match detected; reusing candidate claims")
                existing_claims = candidate_claims
            else:
                existing_claims = extract_claims(
                    skill_name=rc.name,
                    skill_body=rc.body_sample if hasattr(rc, 'body_sample') else "",
                    extract_fn=extract_claims_opencode,
                )
            claim_diff = diff_claims(existing_claims, candidate_claims)
            print(f"  Added: {len(claim_diff.added)}, Restatement: {len(claim_diff.restatement)}, Unchanged: {claim_diff.unchanged}")

            print(f"  Deciding merge against {rc.name}...", flush=True)
            proposal = decide_merge(
                skill1_name=rc.name,
                skill2_name=candidate.name,
                claim_diff=claim_diff,
                decide_fn=decide_merge_opencode,
            )
            proposals.append(proposal)
            print(f"\n{proposal.summary()}\n")
        except Exception as e:
            print(f"  Merge decision failed: {e}")

    return {"verdict": proposals[0].verdict if proposals else "REVIEW", "proposals": proposals}


def main():
    parser = argparse.ArgumentParser(description="Librarian Test Pipe")
    parser.add_argument("--candidate", help="Process a single candidate by name")
    parser.add_argument("--dry-run", action="store_true", help="Evaluate only, no writes")
    parser.add_argument("--reset", action="store_true", help="Wipe test library first")
    parser.add_argument("--max-matches", type=int, default=1,
                        help="How many deduplicated catalog matches to evaluate (default: 1)")
    args = parser.parse_args()

    if args.reset:
        reset_test_library()

    if not TEST_INTAKE.exists():
        TEST_INTAKE.mkdir(parents=True, exist_ok=True)
        print(f"Created {TEST_INTAKE}")
        print(f"Add candidate skills to {TEST_INTAKE}/<skill-name>/SKILL.md")
        return 0

    candidates = scan_intake(str(TEST_INTAKE))
    if not candidates:
        print(f"No candidates found in {TEST_INTAKE}")
        print(f"Add candidate skills to {TEST_INTAKE}/<skill-name>/SKILL.md")
        return 0

    if args.candidate:
        candidates = [c for c in candidates if c.name == args.candidate]
        if not candidates:
            print(f"Candidate '{args.candidate}' not found in {TEST_INTAKE}")
            return 1

    catalog = build_catalog_index()
    print(f"Catalog: {len(catalog)} skills indexed from library/")
    print(f"Test intake: {len(candidates)} candidates")
    print(f"Test library: {TEST_LIBRARY}")

    # Build the category taxonomy for placement
    from skill_library.config import CATEGORIES, DEEP_CATEGORIES, OPERATIONAL_SYSTEM_PACKAGES
    taxonomy = {}
    for cat in CATEGORIES:
        taxonomy[cat] = DEEP_CATEGORIES.get(cat, [])
    for root in OPERATIONAL_SYSTEM_PACKAGES:
        taxonomy[root] = []

    results = []
    for candidate in candidates:
        result = process_candidate(
            candidate, catalog, dry_run=args.dry_run,
            max_matches=args.max_matches,
        )
        results.append({"candidate": candidate.name, **result})

        if args.dry_run:
            continue

        verdict = result["verdict"]
        proposals = result.get("proposals", [])

        # Place the skill (NEW, SUPPLEMENT, EXTEND, ALIAS all need placement)
        if verdict in ("NEW", "SUPPLEMENT", "EXTEND"):
            from skill_library.librarian_ai import propose_placement_opencode
            print(f"  Placing: {candidate.name}")
            try:
                placement = propose_placement_opencode(
                    candidate.name,
                    candidate.description,
                    taxonomy,
                )
                print(f"    -> {placement['category']}/{placement['subcategory'] or '(root)'} — {placement['reasoning'][:80]}")
            except Exception as e:
                print(f"    Placement failed: {e}, defaulting to uncategorized")
                placement = {"category": "uncategorized", "subcategory": "", "reasoning": str(e)}

            # Read the FULL body from the candidate's SKILL.md, not the
            # truncated body_sample used for similarity scoring.
            skill_md_path = Path(candidate.source_dir) / "SKILL.md"
            full_body = skill_md_path.read_text(encoding="utf-8") if skill_md_path.exists() else candidate.body_sample

            # Generate the rich metadata block (role, applications, keywords, ...)
            from skill_library.librarian_ai import generate_metadata_opencode, render_frontmatter
            print(f"  Generating metadata: {candidate.name}")
            try:
                metadata = generate_metadata_opencode(
                    candidate.name,
                    candidate.description,
                    placement["category"],
                    placement["subcategory"],
                    candidate.body_sample,
                )
                print(f"    role={metadata['role']}  applications={metadata['applications']}")
            except Exception as e:
                print(f"    Metadata generation failed: {e}, using defaults")
                metadata = {
                    "role": "capability", "applications": [], "keywords": [], "tags": [],
                    "depends_on": [], "composed_of": [], "extends": None, "adapts": None,
                    "aliased_to": None,
                    "execution_provider": {"default": "prompt_template", "supported": []},
                    "risk": "low", "side_effects": "read-only",
                }

            # Build the body with generated frontmatter replacing the original.
            # Preserve the candidate's license when available.
            body_only = re.sub(r"^---\s*\n.*?\n---\s*\n", "", full_body, count=1, flags=re.DOTALL)
            license_id = "MIT"
            lic_match = re.search(r'^license:\s*"?([^"\n]+)"?', full_body, re.MULTILINE)
            if lic_match:
                license_id = lic_match.group(1).strip()
            canonical_id = f"{placement['category']}:{candidate.name}"
            new_fm = render_frontmatter(
                candidate.name, candidate.description, metadata, canonical_id,
                license_id=license_id,
            )
            new_body = f"{new_fm}\n{body_only.strip()}\n"

            dest = write_skill_to_test_library(
                skill_name=candidate.name,
                body=new_body,
                description=candidate.description,
                category=placement["category"],
                subcategory=placement["subcategory"],
                role=metadata.get("role", "capability"),
                source_path=str(candidate.source_dir),
            )
            print(f"  -> Written to test library: {dest}")

            # For SUPPLEMENT/EXTEND, merge the claims into the target
            if verdict in ("SUPPLEMENT", "EXTEND") and proposals:
                target = proposals[0].target
                include = proposals[0].include_claims
                if include:
                    merged = merge_claims_into_skill(target, include)
                    if merged:
                        print(f"  -> Merged {len(include)} claims into {target}")
                    else:
                        print(f"  -> Target {target} not in test library; skipping merge")

    # Generate routers
    if not args.dry_run:
        generate_routers()
        print(f"\n{'='*60}")
        print(f"Test library generated: {TEST_LIBRARY}")
        print(f"  Skills: {len(list(TEST_LIBRARY.glob('**/**/SKILL.md')))}")
        print(f"  Routers: {len(list(TEST_LIBRARY.glob('*/SKILL.md')))}")
        print(f"  Manifest: {TEST_MANIFEST}")
        print(f"{'='*60}")

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for r in results:
        verdict = r["verdict"]
        proposals = r.get("proposals", [])
        if proposals:
            p = proposals[0]
            print(f"  {r['candidate']:30} -> {verdict:12} (target: {p.target}, confidence: {p.confidence})")
        else:
            print(f"  {r['candidate']:30} -> {verdict}")

    return 0


if __name__ == "__main__":
    sys.exit(main())