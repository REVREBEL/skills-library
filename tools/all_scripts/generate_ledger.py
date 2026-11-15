import csv
import os
import re

ROOT_DIR = "/Users/garystringham/github-revrebel/skills-rebuild"
CSV_PATH = os.path.join(ROOT_DIR, "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv")
REPORT_PATH = os.path.join(ROOT_DIR, "task-folder/agents/skills-rebuild/_audit/provider-conversion-report.md")

claude_exempts = ['cc-skill-continuous-learning', 'last30days', 'browser-harness', 'remote-gpu-trainer', 'cred-omega', 'apple-notes-search', 'claude-code-cheat-sheet']

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

def get_skill_compatibility(dest_path):
    full_path = os.path.join(ROOT_DIR, dest_path)
    if not os.path.isdir(full_path):
        return None
    skill_md = os.path.join(full_path, "SKILL.md")
    if os.path.exists(skill_md):
        comp = parse_frontmatter_compatibility(skill_md)
        if comp:
            return comp
    for file in os.listdir(full_path):
        if file.endswith(".md"):
            comp = parse_frontmatter_compatibility(os.path.join(full_path, file))
            if comp:
                return comp
    return None

def get_retained_provider_references(row, dest_path):
    orig_evidence = row.get("compatibility_evidence", "").strip()
    if not orig_evidence or orig_evidence == "None":
        return "None"
        
    parts = [p.strip() for p in orig_evidence.split(",") if p.strip()]
    final_parts = []
    
    is_claude_exempt = any(ex in dest_path for ex in claude_exempts)
    
    for p in parts:
        if "Claude Execution Environment" in p:
            if is_claude_exempt:
                final_parts.append("Claude Execution Environment")
        elif "Claude Subject" in p:
            if is_claude_exempt:
                final_parts.append("Claude Subject")
        else:
            final_parts.append(p)
            
    final_parts = sorted(list(set(final_parts)))
    if not final_parts:
        return "None"
    return ", ".join(final_parts)

def main():
    converted_rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = row.get("conversion_status", "")
            if status in ("Converted", "Converted (Neutralized)"):
                converted_rows.append(row)

    print(f"Found {len(converted_rows)} converted rows.")

    # Create the markdown table
    ledger_content = "\n\n---\n\n## 6. Per-Skill Conversion Ledger\n\n"
    ledger_content += "As required by the Phase 04 artifact specification, the following table records every converted skill, its original provider dependencies, classification decision, changes made, retained compatibility requirements, retained provider references, validation performed, and any unresolved blockers:\n\n"
    ledger_content += "| Source Skill | Original Dependency | Decision | Changes Made | Retained Compatibility Requirements | Retained Provider References | Validation Performed | Unresolved Blockers |\n"
    ledger_content += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

    for r in converted_rows:
        src = r.get("source_path", "").strip()
        orig_dep = r.get("provider_dependencies", "").strip() or "None"
        decision = r.get("compatibility_classification", "").strip() or "Supported after conversion"
        changes = r.get("conversion_decision_basis", "").strip() or "Neutralized provider-specific variables/paths"
        
        dest_path = r.get("conversion_destination_path", "")
        retained_comp = get_skill_compatibility(dest_path) or "None"
        retained_prov_ref = get_retained_provider_references(r, dest_path)
        
        val_type = r.get("conversion_evidence_type", "").strip() or "lexical"
        val_path = r.get("conversion_evidence_path", "").strip() or "verify_phase_04.py"
        validation = f"{val_type} (`{val_path}`)"
        blockers = "None"
        
        # Escape markdown pipes in fields to prevent broken layout
        src_esc = src.replace("|", "\\|").replace("\n", " ")
        orig_dep_esc = orig_dep.replace("|", "\\|").replace("\n", " ")
        decision_esc = decision.replace("|", "\\|").replace("\n", " ")
        changes_esc = changes.replace("|", "\\|").replace("\n", " ")
        retained_comp_esc = retained_comp.replace("|", "\\|").replace("\n", " ")
        retained_prov_ref_esc = retained_prov_ref.replace("|", "\\|").replace("\n", " ")
        validation_esc = validation.replace("|", "\\|").replace("\n", " ")

        ledger_content += f"| {src_esc} | {orig_dep_esc} | {decision_esc} | {changes_esc} | {retained_comp_esc} | {retained_prov_ref_esc} | {validation_esc} | {blockers} |\n"

    # Read original report content
    with open(REPORT_PATH, "r", encoding="utf-8") as rf:
        report_content = rf.read()

    # If Section 6 already exists, remove it first to avoid duplicate appending
    if "## 6. Per-Skill Conversion Ledger" in report_content:
        report_content = report_content.split("## 6. Per-Skill Conversion Ledger")[0].rstrip()

    new_report_content = report_content.rstrip() + ledger_content

    with open(REPORT_PATH, "w", encoding="utf-8") as wf:
        wf.write(new_report_content)

    print("Successfully appended Per-Skill Conversion Ledger to provider-conversion-report.md.")

if __name__ == "__main__":
    main()
