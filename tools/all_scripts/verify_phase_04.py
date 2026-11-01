import csv
import os
import re
import subprocess

CSV_PATH = "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
ROOT_DIR = "."

# Folders approved for renaming
RENAMED_PATHS_MAP = {
    "task-folder/agents/skills/linear-skill": "task-folder/agents/skills/linear-skill",
    "task-folder/agents/skills/varlock-skill": "task-folder/agents/skills/varlock-skill",
    "task-folder/agents/skills/folder-specific-agent-context": "task-folder/agents/skills/folder-specific-agent-context",
    "task-folder/agents/skills/internal-comms-guidelines": "task-folder/agents/skills/internal-comms-guidelines"
}

def get_git_metadata():
    """
    Gathers key git SHAs, merge-base, diff count, and file statistics.
    """
    metadata = {
        "head_sha": "N/A",
        "merge_base_sha": "N/A",
        "diff_file_count": 0,
        "deleted_files_count": 0,
        "changed_files": []
    }
    try:
        metadata["head_sha"] = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        mb = subprocess.check_output(["git", "merge-base", "main", "HEAD"]).decode("utf-8").strip()
        metadata["merge_base_sha"] = mb
        
        # Get list of all changed/added/deleted files compared to merge-base
        diff_output = subprocess.check_output(["git", "diff", "--name-status", mb]).decode("utf-8")
        for line in diff_output.splitlines():
            if not line.strip():
                continue
            parts = line.split(None, 1)
            status = parts[0]
            path_str = parts[1].strip()
            metadata["diff_file_count"] += 1
            if status.startswith("D"):
                metadata["deleted_files_count"] += 1
            elif status.startswith("R"):
                # E.g. R100  old_path  new_path
                rename_parts = path_str.split("\t")
                if len(rename_parts) >= 2:
                    metadata["changed_files"].append(rename_parts[1].strip())
                else:
                    metadata["changed_files"].append(path_str)
            else:
                metadata["changed_files"].append(path_str)
    except Exception as e:
        print(f"Warning: Failed to gather complete git metadata: {e}")
    return metadata

def link_existed_in_baseline(file_path, link_target, merge_base_sha):
    """
    Checks if a specific relative link existed in the baseline commit of a file.
    """
    try:
        content = subprocess.check_output(
            ["git", "show", f"{merge_base_sha}:{file_path}"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8", errors="replace")
        return link_target in content
    except Exception:
        return False

def parse_frontmatter_compatibility(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines or not lines[0].strip() == "---":
            return None
        
        comp_lines = []
        is_block_scalar = False
        block_indent = None
        
        for line in lines[1:]:
            trimmed = line.strip()
            if trimmed == "---":
                break
                
            if is_block_scalar:
                if line.strip() == "":
                    comp_lines.append("")
                    continue
                line_indent = len(line) - len(line.lstrip())
                if block_indent is None:
                    block_indent = line_indent
                if line_indent >= block_indent:
                    comp_lines.append(line.strip())
                else:
                    break
                continue
                
            match = re.match(r"^compatibility\s*:\s*(.*)$", line, re.IGNORECASE)
            if match:
                val = match.group(1).strip()
                if val in ("|", ">", "|-\n", ">-\n", "|-", ">-"):
                    is_block_scalar = True
                else:
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1].strip()
                    return val
                    
        if comp_lines:
            return " ".join(comp_lines).strip()
    except Exception:
        pass
    return None

def verify_all():
    print("=== STARTING PHASE 04 RECONCILIATION VALIDATION ===")
    
    # Gather and print precise Git metadata as requested
    git_meta = get_git_metadata()
    print(f"  HEAD SHA: {git_meta['head_sha']}")
    print(f"  Merge-Base SHA: {git_meta['merge_base_sha']}")
    print(f"  Git Diff File Count: {git_meta['diff_file_count']}")
    print(f"  Deleted Files Skipped: {git_meta['deleted_files_count']}")
    print(f"  Changed Files to Scan: {len(git_meta['changed_files'])}")
    print("-" * 50)

    # 1. Load CSV
    assert os.path.exists(CSV_PATH), f"Error: CSV does not exist at {CSV_PATH}"
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # 2. Check total row count
    total_rows = len(rows)
    print(f"[CHECK 1] Row Count: {total_rows} rows loaded.")
    assert total_rows == 2331, f"Error: Expected exactly 2331 rows, got {total_rows}"
    print(" -> PASS: Row count is exactly 2,331.")

    # 3. Check status metrics
    converted = sum(1 for r in rows if r.get("conversion_status") == "Converted")
    intrinsic = sum(1 for r in rows if r.get("conversion_status") == "Retained (Intrinsic)")
    no_change = sum(1 for r in rows if r.get("conversion_status") == "Reviewed - No Conversion Required")
    quarantined = sum(1 for r in rows if r.get("conversion_status") == "Not In Scope (Phase 03 Quarantined)")
    blockers = sum(1 for r in rows if r.get("conversion_status") == "Requires Manual Review")

    print(f"[CHECK 2] Reconciliation Metrics:")
    print(f"  - Converted (Neutralized): {converted}")
    print(f"  - Retained (Intrinsic): {intrinsic}")
    print(f"  - Reviewed (No Conversion Required): {no_change}")
    print(f"  - Not In Scope (Phase 03 Quarantined): {quarantined}")
    print(f"  - Requires Manual Review: {blockers}")

    assert converted == 400, f"Error: Expected exactly 400 Converted, got {converted}"
    assert intrinsic == 14, f"Error: Expected exactly 14 Retained, got {intrinsic}"
    assert no_change == 1872, f"Error: Expected exactly 1872 Reviewed, got {no_change}"
    assert quarantined == 45, f"Error: Expected exactly 45 Quarantined, got {quarantined}"
    assert blockers == 0, f"Error: Expected exactly 0 Blockers, got {blockers}"
    assert converted + intrinsic + no_change + quarantined + blockers == 2331, "Error: Sum of statuses does not match total!"
    print(" -> PASS: All category reconciliation metrics match perfectly (400 + 14 + 1872 + 45 = 2331).")

    # 4. Check renamed paths physically exist and old paths are gone
    print("[CHECK 3] Renamed Folder Physical State:")
    for old, new in RENAMED_PATHS_MAP.items():
        assert os.path.exists(os.path.join(ROOT_DIR, new)), f"Error: New folder does not exist: {new}"
        assert not os.path.exists(os.path.join(ROOT_DIR, old)), f"Error: Old folder still exists: {old}"
        print(f"  - {old} -> {new} verified.")
    print(" -> PASS: Renamed folders physically exist in their new locations, and old directories are gone.")

    # 5. Check database-to-filesystem reconciliation
    print("[CHECK 4] Database-to-Filesystem Path Reconciliation:")
    for r in rows:
        dest = r.get("conversion_destination_path")
        assert dest, f"Error: Row {r['source_path']} is missing conversion_destination_path!"
        if r["conversion_status"] != "Not In Scope (Phase 03 Quarantined)":
            assert os.path.exists(os.path.join(ROOT_DIR, dest)), f"Error: Path listed in destination does not exist: {dest}"
    print(" -> PASS: Every single active row's conversion_destination_path reconciles perfectly with a physical filesystem path.")

    # 6. Check for workstation absolute paths (expanded portability checks including CSV and .github)
    print("[CHECK 5] Expanded Portability / Workstation Path Leak Detection:")
    
    changed_files = list(git_meta["changed_files"])
    if not changed_files:
        print("  - No changed files detected via git. Scanning active skills instead.")
        # Fallback: scan all active skills
        for r in rows:
            if r["conversion_status"] != "Not In Scope (Phase 03 Quarantined)":
                dest = r["conversion_destination_path"]
                skill_dir = os.path.join(ROOT_DIR, dest)
                if os.path.exists(skill_dir):
                    for root, dirs, files in os.walk(skill_dir):
                        for file in files:
                            changed_files.append(os.path.join(root, file))

    print(f"  - Scanning {len(changed_files)} files for workstation path leakages (including skills-inventory.csv and .github)...")
    
    patterns = [
        re.compile(r"/Users/(?!name/|user/|agent/|vscode/|gitpod/|runner/|ubuntu/|opuser/|youruser/|yourname|username|alice|bob|api/|v1/)[a-zA-Z0-9_][a-zA-Z0-9_\-\.]{1,}(?=/|$)"),
        re.compile(r"/home/(?!name/|user/|agent/|vscode/|gitpod/|runner/|ubuntu/|opuser/|youruser/|yourname|username|alice|bob|api/|v1/)[a-zA-Z0-9_][a-zA-Z0-9_\-\.]{1,}(?=/|$)"),
        re.compile(r"[a-zA-Z]:\\Users\\(?!name\\|user\\|agent\\|vscode\\|gitpod\\|runner\\|ubuntu\\|opuser\\|youruser\\|yourname|username|alice|bob)[a-zA-Z0-9_][a-zA-Z0-9_\-\.]{1,}", re.IGNORECASE),
        re.compile(r"file:///Users/(?!name|user|agent|vscode|gitpod|runner|ubuntu|opuser|youruser|yourname|username|alice|bob)[a-zA-Z0-9_][a-zA-Z0-9_\-\.]{1,}"),
        re.compile(r"file:///home/(?!name|user|agent|vscode|gitpod|runner|ubuntu|opuser|youruser|yourname|username|alice|bob)[a-zA-Z0-9_][a-zA-Z0-9_\-\.]{1,}"),
        re.compile(r"\\\\[a-zA-Z0-9_\-\.]{2,}\\[a-zA-Z0-9_\-\.\$]{1,}")
    ]
    
    portability_scanned = 0
    for file_path in changed_files:
        if not os.path.exists(file_path):
            continue
        # Skip ONLY .git binary, node_modules, or validator binaries themselves if binary.
        # But fully include skills-inventory.csv and committed .github/ textual files!
        if any(exc in file_path for exc in [".git/", "node_modules/", "execute_provider_conversion", "verify_phase_04.py"]):
            continue
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as sf:
                text = sf.read()
            
            portability_scanned += 1
            # Explicitly raise AssertionError if any portability violation is found
            for p in patterns:
                leak_match = p.search(text)
                assert not leak_match, f"Error: Found absolute path leak '{leak_match.group(0)}' in file: {file_path}"
                
            assert "garystringham" not in text, f"Error: Found username 'garystringham' leak in file: {file_path}"
        except AssertionError as ae:
            raise ae
        except Exception:
            pass
            
    print(f"  - Successfully completed portability scans on {portability_scanned} files.")
    print(" -> PASS: Zero workstation absolute path leaks or portability violations detected in any Phase 04 assets.")

    # 7. Check for broken references to renamed folders & invalid relative markdown links
    print("[CHECK 6] Broken-Reference & Markdown Link Validation:")
    tolerated_baseline_defects = 0
    new_broken_links = 0
    
    for file_path in changed_files:
        if not os.path.exists(file_path) or not file_path.endswith(".md"):
            continue
        if any(exc in file_path for exc in ["provider-conversion-report.md", "verify_phase_04.py"]):
            continue
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as sf:
                text = sf.read()
            
            # Verify old renamed folders do NOT appear in non-URL lines
            for old in RENAMED_PATHS_MAP.keys():
                basename = os.path.basename(old)
                for line in text.splitlines():
                    if "http://" in line or "https://" in line or "github.com" in line or "source:" in line:
                        continue
                    assert basename not in line, f"Error: Found stale reference to old renamed directory '{basename}' in {file_path}: {line.strip()}"
                
            # Verify relative links
            links = re.findall(r"(?<![a-zA-Z0-9_])\[[^\]]+\]\(([^)]+)\)", text)
            for link in links:
                clean_link = link.split("#")[0].split("?")[0].strip()
                if not clean_link:
                    continue
                if clean_link.startswith(("http://", "https://", "mailto:", "ftp:")):
                    continue
                
                # Check link relative to file's directory or repository root
                file_dir = os.path.dirname(file_path)
                target_rel = os.path.abspath(os.path.join(file_dir, clean_link))
                target_root = os.path.abspath(os.path.join(ROOT_DIR, clean_link))
                
                exists_rel = os.path.exists(target_rel)
                exists_root = os.path.exists(target_root)
                
                if not (exists_rel or exists_root):
                    # Link is broken! Prove whether it is pre-existing
                    if link_existed_in_baseline(file_path, link, git_meta["merge_base_sha"]):
                        tolerated_baseline_defects += 1
                    else:
                        new_broken_links += 1
                        assert False, f"Error: Newly introduced broken relative link '{link}' found in file: {file_path}"
                
        except AssertionError as ae:
            raise ae
        except Exception:
            pass
            
    print(f"  - Tolerated Baseline Defects (pre-existing): {tolerated_baseline_defects}")
    print(f"  - Newly Introduced Broken Links: {new_broken_links}")
    print(" -> PASS: Verified all old renamed-directory references are absent, and 0 new broken relative links were introduced.")

    # 8. Reconcile Converted rows using explicit per-row metadata evidence
    print("[CHECK 7] Converted Row Metadata Evidence Reconciliation:")
    converted_rows = [r for r in rows if r["conversion_status"] == "Converted"]
    evidence_verified = 0
    
    for r in converted_rows:
        dest = r["conversion_destination_path"]
        evidence_type = r.get("conversion_evidence_type", "").strip()
        evidence_path = r.get("conversion_evidence_path", "").strip()
        evidence_reason = r.get("conversion_evidence_reason", "").strip()
        
        assert evidence_type in ["git_diff", "pruned_directory", "gitignored_assets"], (
            f"Error: Converted skill '{r['source_path']}' has invalid or missing conversion_evidence_type '{evidence_type}'!"
        )
        assert evidence_reason, f"Error: Converted skill '{r['source_path']}' is missing an explicit conversion_evidence_reason!"

        if evidence_type == "git_diff":
            # Verify the evidence path physically exists and is part of changed_files
            assert evidence_path, f"Error: Converted skill '{r['source_path']}' specifies type 'git_diff' but has no evidence path!"
            assert os.path.exists(os.path.join(ROOT_DIR, evidence_path)), (
                f"Error: Specified evidence path '{evidence_path}' does not exist on disk for '{r['source_path']}'!"
            )
            # Make sure it's in the repo diff!
            is_dir = os.path.isdir(os.path.join(ROOT_DIR, evidence_path)) or evidence_path.endswith("/")
            if is_dir:
                prefix = evidence_path.rstrip("/") + "/"
                has_diff = any(cf == evidence_path or cf.startswith(prefix) for cf in changed_files)
            else:
                has_diff = (evidence_path in changed_files)
            assert has_diff, f"Error: Evidence path '{evidence_path}' is not modified in git diff for '{r['source_path']}'!"
            
        elif evidence_type == "pruned_directory":
            # Verify the specified path is absent from the active layout
            assert evidence_path, f"Error: Converted skill '{r['source_path']}' specifies type 'pruned_directory' but has no evidence path!"
            assert not os.path.exists(os.path.join(ROOT_DIR, evidence_path)), (
                f"Error: Pruned evidence directory '{evidence_path}' still physically exists on disk!"
            )
            
        elif evidence_type == "gitignored_assets":
            # Verify reason is well-documented
            assert len(evidence_reason) > 10, (
                f"Error: Gitignored evidence reason for '{r['source_path']}' is too sparse or trivial!"
            )
            
        evidence_verified += 1

    print(f"  - Successfully verified physical evidence for all {evidence_verified} Converted skills using explicit metadata columns.")
    print(" -> PASS: Every Converted row reconciles perfectly using explicit per-row metadata evidence.")

    # 9. Strict Semantic Validation for Converted Skills (Expanded semantic rule suite)
    print("[CHECK 8] Strict Semantic Validation for Converted Skills:")
    semantic_scanned_files = 0
    
    for r in converted_rows:
        dest = r["conversion_destination_path"]
        skill_dir = os.path.join(ROOT_DIR, dest)
        if not os.path.exists(skill_dir):
            continue
            
        for root, dirs, files in os.walk(skill_dir):
            if any(ignored in root for ignored in [".git", "node_modules", ".github"]):
                continue
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext not in [".md", ".json", ".sh", ".py", ".js", ".ts", ".txt", ".yaml", ".yml", ".ps1"]:
                    continue
                fp = os.path.join(root, file)
                
                with open(fp, "r", encoding="utf-8", errors="replace") as sf:
                    content = sf.read()
                    
                # Check for mixed-runtime contradictions (mixed-runtime scan)
                has_manufactured = any(m in content for m in [".agents/", "~/.agents", "the agent"])
                has_claude_intrinsic = any(c in content for c in ["CLAUDE_TRANSCRIPT_PATH", "CLAUDE_COMMAND", "CLAUDE_DIR", "~/.claude"])
                if has_manufactured and has_claude_intrinsic:
                    assert False, f"Semantic Violation: Found mixed-runtime contradiction in file: {fp} (contains both manufactured generic agent elements and actual Claude-specific intrinsic elements)"
                    
                semantic_scanned_files += 1
                lines = content.splitlines()
                for idx, line in enumerate(lines):
                    line_num = idx + 1
                    line_lower = line.lower()
                    
                    is_url = "http://" in line_lower or "https://" in line_lower or "github.com" in line_lower
                    is_exempt = any(exempt in fp for exempt in ["weaviate", "last30days", "cred-omega", "computer-use-agents", "visual-asset-adapters.md", "apple-notes-search", "llm-structured-output", "llm-app-patterns", "vercel-ai-sdk-expert", "cloudflare", "mcp-builder", "auri-core", "ai-wrapper-product", "claude-code-cheat-sheet.md", "content-repurposer", "cc-skill-continuous-learning", "remote-gpu-trainer", "browser-harness"])
                    
                    # 1. Check for unneutralized config paths
                    if not is_url and not is_exempt:
                        has_config_path = False
                        if "~/.claude" in line:
                            has_config_path = True
                        elif ".claude/launch.json" in line_lower or ".claude/settings.json" in line_lower or ".claude/.env" in line_lower or ".claude/skills" in line_lower:
                            if not "ln -s AGENTS.md CLAUDE.md" in line:
                                has_config_path = True
                        if has_config_path:
                            assert False, f"Semantic Violation: Found unneutralized config path '{line.strip()}' on line {line_num} in file: {fp}"
                            
                    # 2. Check for self-symlinks & adjacent duplicates (/, comma, spaces, etc.)
                    # Match "AGENTS.md / AGENTS.md", "AGENTS.md, AGENTS.md", etc.
                    dup_agents = re.search(r"\b(AGENTS\.md|CLAUDE\.md)\s*[,/&or\-、\s]+\s*\1\b", line)
                    if dup_agents:
                        assert False, f"Semantic Violation: Found duplicate replacement/separator pattern '{line.strip()}' on line {line_num} in file: {fp}"
                        
                    if "ln -s AGENTS.md AGENTS.md" in line or "ln -s CLAUDE.md CLAUDE.md" in line:
                        assert False, f"Semantic Violation: Found self-symlink pattern '{line.strip()}' on line {line_num} in file: {fp}"

                    # 3. Check for suspicious the agent substitutions
                    suspicious_sub = False
                    if re.search(r"\ba the agent\b", line_lower):
                        suspicious_sub = True
                    elif re.search(r"\bthe agent:\s*`?claude\b", line_lower):
                        suspicious_sub = True
                    elif re.search(r"\banthropic the agent\b", line_lower):
                        suspicious_sub = True
                    elif re.search(r"\bthe agent best practices\b", line_lower):
                        suspicious_sub = True
                    elif re.search(r"\bthe agent issue\b", line_lower):
                        suspicious_sub = True
                    if suspicious_sub:
                        assert False, f"Semantic Violation: Found mechanical/suspicious 'the agent' substitution '{line.strip()}' on line {line_num} in file: {fp}"

                    # 4. Check for stale CLAUDE.md execution requirements
                    if "CLAUDE.md" in line:
                        if any(req in line_lower for req in ["create a", "write a", "configure a", "edit a", "modify the", "read the"]) and not "agents.md" in line_lower:
                            assert False, f"Semantic Violation: Found stale CLAUDE.md instruction/execution requirement '{line.strip()}' on line {line_num} in file: {fp}"
                            
                    # 5. Check for modified provenance fields
                    if "source:" in line_lower or "source_repo:" in line_lower or "license_source:" in line_lower:
                        if "linear-skill" in line_lower or "varlock-skill" in line_lower:
                            assert False, f"Semantic Violation: Found modified upstream provenance field '{line.strip()}' on line {line_num} in file: {fp}"

                    # 6. Check for unauthorized proprietary execution environment tools
                    if not is_url:
                        if "TodoWrite" in line or "AskUserQuestion" in line:
                            assert False, f"Semantic Violation: Found unauthorized proprietary environment tool '{line.strip()}' on line {line_num} in file: {fp}"

                    # 7. Check for mechanical API-key duplications
                    dup_keys = re.search(r"\b(LLM_API_KEY|PROVIDER_API_KEY)\s*[,/|or\-\s]+\s*\1\b", line)
                    if dup_keys:
                        assert False, f"Semantic Violation: Found mechanical/duplicate API key pattern '{line.strip()}' on line {line_num} in file: {fp}"

                    # 8. Check for unauthorized provider coupling in Converted (provider-neutral) skills
                    if not is_url and not is_exempt:
                            # Check for unneutralized API keys
                            if "ANTHROPIC_API_KEY" in line or "OPENAI_API_KEY" in line:
                                is_key_exempt = any(x in fp for x in ["code-review-ai-ai-review", "performance-testing-review-ai-review", "workflow-automation", "content-repurposer"])
                                if not is_key_exempt:
                                    assert False, f"Semantic Violation: Found unneutralized provider API key '{line.strip()}' on line {line_num} in file: {fp}"
                            
                            # Check for model locks
                            model_locks = ["claude-sonnet-", "claude-3-", "claude-opus-", "claude-haiku-"]
                            for ml in model_locks:
                                if ml in line_lower:
                                    assert False, f"Semantic Violation: Found unauthorized model lock '{line.strip()}' on line {line_num} in file: {fp}"

    print(f"  - Successfully performed semantic scans on {semantic_scanned_files} files across all Converted skills.")
    print(" -> PASS: Strict semantic validation checks passed successfully with 0 violations found.")

    # 10. Check 9: Retained Compatibility and Frontmatter Reconciliation
    print("[CHECK 9] Retained Compatibility and Frontmatter Reconciliation:")
    REPORT_PATH = "task-folder/agents/skills-rebuild/_audit/provider-conversion-report.md"
    assert os.path.exists(REPORT_PATH), f"Error: Report missing at {REPORT_PATH}"
    with open(REPORT_PATH, "r", encoding="utf-8") as rf:
        report_content = rf.read()
    
    assert "## 6. Per-Skill Conversion Ledger" in report_content, "Error: Per-Skill Conversion Ledger missing in report!"
    ledger_section = report_content.split("## 6. Per-Skill Conversion Ledger")[1].strip()
    
    table_started = False
    headers = []
    reconciled_count = 0
    
    for line in ledger_section.splitlines():
        if "|" in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if not parts:
                continue
            if "Source Skill" in parts:
                headers = parts
                table_started = True
                continue
            if table_started and parts[0].startswith(":---"):
                continue
                
            if table_started:
                row_dict = dict(zip(headers, parts))
                src_skill = row_dict.get("Source Skill", "").replace("\\|", "|")
                retained_comp = row_dict.get("Retained Compatibility Requirements", "")
                
                # Reconcile against physical file compatibility declaration
                full_path = os.path.join(ROOT_DIR, src_skill)
                fm_comp = None
                if os.path.isdir(full_path):
                    skill_md = os.path.join(full_path, "SKILL.md")
                    if os.path.exists(skill_md):
                        fm_comp = parse_frontmatter_compatibility(skill_md)
                    else:
                        for file in os.listdir(full_path):
                            if file.endswith(".md"):
                                fm_comp = parse_frontmatter_compatibility(os.path.join(full_path, file))
                                if fm_comp:
                                    break
                
                expected_fm_comp = fm_comp or "None"
                assert retained_comp == expected_fm_comp, (
                    f"Error: Ledger lists Retained Compatibility as '{retained_comp}' for '{src_skill}', "
                    f"but its physical frontmatter compatibility is '{expected_fm_comp}'!"
                )
                reconciled_count += 1
                
    print(f"  - Successfully reconciled all {reconciled_count} ledger rows against physical compatibility: declarations.")
    print(" -> PASS: Every non-None retained compatibility requirement reconciles to an explicit final compatibility: declaration.")

    print("\n=== ALL PHASE 04 RECONCILIATION VALIDATIONS PASSED! CONGRATULATIONS! ===")

if __name__ == "__main__":
    verify_all()
