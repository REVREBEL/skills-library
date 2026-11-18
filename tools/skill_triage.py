#!/usr/bin/env python3
"""
Structural triage across the four priority domains.

This is the pilot method (audit/quality-pilot) applied at scale. It assigns
each canonical package a triage verdict from measurable structure:

  thin           fewer than 150 words of body
  weak_step      "choose the right tool" style non-guidance
  templated      shares a heading skeleton with 4+ other packages
  duplicate      near-identical name+description to another package
  reference_heavy  more than half its lines are links
  misfiled       path domain has no keyword support, another domain does

Verdicts are proposals for human review, not final decisions. The output is a
ranked queue, not a rewrite.

Usage:
    python3 tools/skill_triage.py
    python3 tools/skill_triage.py --domain design
"""

from __future__ import annotations

import argparse
import csv
import itertools
import os
import re
import sys
from collections import Counter, defaultdict

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from skill_library.config import LIBRARY_DIR, REPO_ROOT


def parse_frontmatter(content: str) -> dict | None:
    """Minimal key: value frontmatter reader (no nested mappings)."""
    if not content:
        return None
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    closing = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing = i
            break
    if closing is None:
        return None
    result = {}
    for line in lines[1:closing]:
        s = line.strip()
        if not s or s.startswith("#") or ":" not in s:
            continue
        k, v = s.split(":", 1)
        if k.strip():
            result[k.strip()] = v.strip().strip("\"'")
    return result

DEFAULT_OUT = os.path.join(REPO_ROOT, "audit", "quality-pilot")

OPERATIONAL_ROOTS = {"github-operations", "skills-create-manage-update"}

DOMAIN_RULES = {
    "design": (
        ("design-and-experience",),
        r"\b(design|ui|ux|figma|typography|layout|color|palette|wireframe|prototype|mockup|style|theme)\b",
    ),
    "content": (
        ("content-and-documentation",),
        r"\b(writing|copy|copywriting|content|blog|article|documentation|doc|editorial|presentation|slide)\b",
    ),
    "data": (
        ("data-and-ai/analytics", "data-and-ai/data-engineering"),
        r"\b(analytics|report|reporting|dashboard|metric|kpi|sql|query|bigquery|pandas|tableau|looker|forecast)\b",
    ),
    "stack": (
        (),
        r"\b(react|npm|node|nodejs|webflow|python|django|flask|fastapi|typescript|next\.?js|tailwind)\b",
    ),
}

WEAK_STEP = re.compile(
    r"choose (the )?(right|correct|appropriate).{0,30}tool"
    r"|choose your .{0,30}tool"
    r"|select (a|the) .{0,20}tool"
    r"|pick (a|the) .{0,20}tool",
    re.IGNORECASE,
)

THIN_WORDS = 150
TEMPLATE_GROUP_MIN = 4
DUPLICATE_THRESHOLD = 0.55
REFERENCE_LINE_RATIO = 0.5

STOP = set(
    "a an the in on of and or for with to at by from is it this that as be use when used using your you".split()
)


def canonical_id(root: str) -> str | None:
    rel = os.path.relpath(root, LIBRARY_DIR).replace(os.sep, "/")
    parts = rel.split("/")
    if not parts or parts[0] == ".":
        return None
    depth = 2 if parts[0] in OPERATIONAL_ROOTS else 3
    if len(parts) != depth:
        return None
    scope = "skills-lifecycle" if parts[0] == "skills-create-manage-update" else parts[0]
    return f"{scope}:{parts[-1]}"


def body_of(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :]
    return text


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2 and w not in STOP}


def skeleton(body: str) -> tuple[str, ...]:
    return tuple(
        re.sub(r"^\d+[.)]\s*", "", line.strip("# ").strip().lower())
        for line in body.splitlines()
        if re.match(r"^#{2,3} ", line)
    )


def features(root: str) -> dict:
    skill_md = os.path.join(root, "SKILL.md")
    text = open(skill_md, encoding="utf-8", errors="replace").read()
    body = body_of(text)
    fm = parse_frontmatter(text) or {}

    lines = [l.strip() for l in body.splitlines() if l.strip()]
    link_lines = sum(1 for l in lines if re.search(r"\[[^\]]*\]\([^)]+\)", l))

    return {
        "name": fm.get("name", os.path.basename(root)),
        "description": fm.get("description", ""),
        "risk": fm.get("risk", ""),
        "words": len(re.findall(r"[A-Za-z0-9]+", body)),
        "headings": len(skeleton(body)),
        "skeleton": skeleton(body),
        "link_ratio": (link_lines / len(lines)) if lines else 0.0,
        "has_weak_step": bool(WEAK_STEP.search(body)),
        "tokens": tokens(f"{fm.get('name','')} {fm.get('description','')}"),
    }


def domain_keywords(text: str) -> dict[str, int]:
    scores = {}
    low = text.lower()
    for domain, (_paths, pattern) in DOMAIN_RULES.items():
        scores[domain] = len(re.findall(pattern, low))
    return scores


def path_domain(root: str) -> str | None:
    rel = os.path.relpath(root, LIBRARY_DIR).replace(os.sep, "/")
    for domain, (paths, _pattern) in DOMAIN_RULES.items():
        if any(rel.startswith(p) for p in paths):
            return domain
    return None


def collect() -> list[dict]:
    records = []
    for root, _dirs, files in os.walk(LIBRARY_DIR):
        if "SKILL.md" not in files:
            continue
        cid = canonical_id(root)
        if not cid:
            continue
        f = features(root)
        f.update(
            {
                "canonical_id": cid,
                "path": os.path.relpath(root, REPO_ROOT).replace(os.sep, "/"),
                "rel": os.path.relpath(root, LIBRARY_DIR).replace(os.sep, "/"),
            }
        )
        records.append(f)
    return records


def assign_domains(records: list[dict]) -> None:
    for r in records:
        scores = domain_keywords(f"{r['canonical_id']} {r['description']}")
        r["keywords"] = scores
        pd = path_domain(os.path.join(REPO_ROOT, r["rel"]))
        r["path_domain"] = pd
        matched = [d for d, s in scores.items() if s > 0]
        if pd and pd in matched:
            r["domains"] = {pd}
        elif matched:
            r["domains"] = set(matched)
        elif pd:
            r["domains"] = {pd}
        else:
            r["domains"] = set()


def find_duplicates(records: list[dict]) -> None:
    index: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(records):
        for t in r["tokens"]:
            index[t].append(i)

    parent = list(range(len(records)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    seen: set[tuple[int, int]] = set()
    for ids in index.values():
        if len(ids) > 60:
            continue
        for a, b in itertools.combinations(ids, 2):
            if (a, b) in seen:
                continue
            seen.add((a, b))
            ta, tb = records[a]["tokens"], records[b]["tokens"]
            if not ta or not tb:
                continue
            if len(ta & tb) / len(ta | tb) >= DUPLICATE_THRESHOLD:
                union(a, b)

    clusters: dict[int, list[int]] = defaultdict(list)
    for i in range(len(records)):
        clusters[find(i)].append(i)

    for i in range(len(records)):
        records[i]["duplicate_group"] = 1
    for members in clusters.values():
        if len(members) > 1:
            for i in members:
                records[i]["duplicate_group"] = len(members)


def find_templates(records: list[dict]) -> None:
    groups: dict[tuple, list[int]] = defaultdict(list)
    for i, r in enumerate(records):
        if r["skeleton"]:
            groups[r["skeleton"]].append(i)

    for i, r in enumerate(records):
        r["template_group"] = 0
    for members in groups.values():
        if len(members) >= TEMPLATE_GROUP_MIN:
            for i in members:
                records[i]["template_group"] = len(members)


def verdict(r: dict) -> tuple[str, str]:
    reasons = []

    if r["duplicate_group"] > 1:
        reasons.append(f"duplicate_cluster:{r['duplicate_group']}")
        return "merge", ";".join(reasons)

    if r["path_domain"] and r["keywords"].get(r["path_domain"], 0) == 0:
        other = {d: s for d, s in r["keywords"].items() if s > 0 and d != r["path_domain"]}
        if other:
            best = max(other, key=other.get)
            reasons.append(f"misfiled:{r['path_domain']}->{best}")
            return "move", ";".join(reasons)

    if r["words"] < THIN_WORDS:
        reasons.append(f"thin:{r['words']}w")
        return "rewrite", ";".join(reasons)

    if r["has_weak_step"]:
        reasons.append("weak_step")
        return "rewrite", ";".join(reasons)

    if r["link_ratio"] > REFERENCE_LINE_RATIO:
        reasons.append(f"reference_heavy:{r['link_ratio']:.0%}")
        return "review", ";".join(reasons)

    if r["template_group"] >= TEMPLATE_GROUP_MIN:
        reasons.append(f"templated:{r['template_group']}")
        return "review", ";".join(reasons)

    return "keep", "distinct"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Structural triage across priority domains")
    parser.add_argument("--domain", action="append", help="Limit to a domain (repeatable)")
    parser.add_argument("--out", default=DEFAULT_OUT)
    args = parser.parse_args(argv)

    records = collect()
    assign_domains(records)
    find_duplicates(records)
    find_templates(records)

    wanted = set(args.domain) if args.domain else set(DOMAIN_RULES)
    rows = []
    for r in records:
        if not (r["domains"] & wanted):
            continue
        v, why = verdict(r)
        r["verdict"], r["reason"] = v, why
        rows.append(r)

    os.makedirs(args.out, exist_ok=True)
    out_path = os.path.join(args.out, "triage-all.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "canonical_id",
                "path",
                "domains",
                "verdict",
                "reason",
                "words",
                "headings",
                "link_ratio",
                "template_group",
                "duplicate_group",
                "risk",
            ],
        )
        w.writeheader()
        for r in sorted(rows, key=lambda x: (x["verdict"], x["canonical_id"])):
            w.writerow(
                {
                    "canonical_id": r["canonical_id"],
                    "path": r["path"],
                    "domains": ";".join(sorted(r["domains"])),
                    "verdict": r["verdict"],
                    "reason": r["reason"],
                    "words": r["words"],
                    "headings": r["headings"],
                    "link_ratio": round(r["link_ratio"], 2),
                    "template_group": r["template_group"],
                    "duplicate_group": r["duplicate_group"],
                    "risk": r["risk"],
                }
            )

    counts = Counter(r["verdict"] for r in rows)
    per_domain = {d: Counter(r["verdict"] for r in rows if d in r["domains"]) for d in sorted(wanted)}

    print(f"triaged: {len(rows)}")
    for k in ("keep", "merge", "move", "rewrite", "review"):
        print(f"  {k:8s} {counts.get(k, 0)}")
    print()
    for d, c in per_domain.items():
        total = sum(c.values())
        print(f"  {d:8s} n={total:4d}  " + "  ".join(f"{k}={c.get(k,0)}" for k in ("keep","merge","move","rewrite","review")))
    print(f"\nWrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())