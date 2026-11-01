import csv
import os
import re
import shutil
import subprocess

CSV_PATH = "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
ROOT_DIR = "."

# Folders approved for renaming
RENAMED_PATHS_MAP = {
    "task-folder/agents/skills/linear-claude-skill": "task-folder/agents/skills/linear-skill",
    "task-folder/agents/skills/varlock-claude-skill": "task-folder/agents/skills/varlock-skill",
    "task-folder/agents/skills/folder-specific-claude-and-agents-md": "task-folder/agents/skills/folder-specific-agent-context",
    "task-folder/agents/skills/internal-comms-anthropic": "task-folder/agents/skills/internal-comms-guidelines"
}

# Intrinsic platform skills
INTRINSIC_PATHS = {
    "task-folder/agents/skills/gemini/gemini-deep-research",
    "task-folder/agents/skills/gemini/gemini-api-dev",
    "task-folder/agents/skills/gemini/gemini-interactions-api",
    "task-folder/agents/skills/gemini/gemini-api",
    "task-folder/agents/skills/gemini/gemini-omni-flash-api",
    "task-folder/agents/skills/gemini/gemini-api-integration",
    "task-folder/agents/skills/gemini/geminiignore-finops",
    "task-folder/agents/skills/gemini/gemini-live-api-dev",
    "task-folder/agents/skills/codex/codex-profiles",
    "task-folder/agents/skills/codex/codex-subagent",
    "task-folder/agents/skills/codex/codex-fable5",
    "task-folder/agents/skills/codex/codex-review",
    "task-folder/agents/skills/nerdzao-elite-gemini-high",
    "task-folder/agents/skills/brand-guidelines-anthropic"
}

def is_citation_or_code(line):
    """
    Check if a line contains citations, standard research references, arXiv links, 
    proper paper titles, or API initialization code that must NOT be modified.
    """
    line_lower = line.lower()
    
    # Check for citations, papers, standard datasets, or URLs
    citation_indicators = [
        "arxiv", "doi:", "citation", "bibliography", "references", "http://", "https://",
        "g-eval", "mmlu", "human-eval", "gsm8k", "alpaca-eval", "gpqa", "swe-bench"
    ]
    if any(ind in line_lower for ind in citation_indicators):
        return True
        
    # Check for code-like initialization patterns or config paths
    code_indicators = [
        "client = ", "anthropic.", "openai.", "gemini.", "import ", "require(",
        "~/.claude", ".claude/skills", "settings.json", ".claude-plugin", "npm install",
        "npm i ", "yarn add", "pnpm add", "git clone"
    ]
    if any(ind in line_lower for ind in code_indicators):
        return True
        
    return False

def precise_convert_text(text, file_path):
    """
    Applies precise, context-aware conversions line-by-line to instruction/markdown files.
    """
    # Skip code files entirely for model-name or env-var conversions to avoid breaking executables
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".py", ".sh", ".js", ".mjs", ".ts", ".json"]:
        return text

    lines = text.splitlines()
    new_lines = []
    
    for line in lines:
        if is_citation_or_code(line):
            new_lines.append(line)
            continue
            
        # 1. Neutralize model locks (only in instruction/prose lines)
        # We replace specific lock patterns with generic equivalents
        line = re.sub(r"\bdesigned for (the\s+)?claude-3-5-sonnet\b", "designed for a high-capability model", line, flags=re.IGNORECASE)
        line = re.sub(r"\boptimized for (the\s+)?claude-3-5-sonnet\b", "optimized for the active model", line, flags=re.IGNORECASE)
        line = re.sub(r"\brequires (the\s+)?claude-3-5-sonnet\b", "requires a high-capability model", line, flags=re.IGNORECASE)
        line = re.sub(r"\busing (the\s+)?claude-3-5-sonnet\b", "using the active model", line, flags=re.IGNORECASE)
        
        line = re.sub(r"\bdesigned for (the\s+)?claude-3\b", "designed for a high-capability model", line, flags=re.IGNORECASE)
        line = re.sub(r"\boptimized for (the\s+)?claude-3\b", "optimized for the active model", line, flags=re.IGNORECASE)
        line = re.sub(r"\brequires (the\s+)?claude-3\b", "requires a high-capability model", line, flags=re.IGNORECASE)
        line = re.sub(r"\busing (the\s+)?claude-3\b", "using the active model", line, flags=re.IGNORECASE)

        line = re.sub(r"\bdesigned for (the\s+)?gpt-4o\b", "designed for a high-capability model", line, flags=re.IGNORECASE)
        line = re.sub(r"\boptimized for (the\s+)?gpt-4o\b", "optimized for the active model", line, flags=re.IGNORECASE)
        line = re.sub(r"\brequires (the\s+)?gpt-4o\b", "requires a high-capability model", line, flags=re.IGNORECASE)
        line = re.sub(r"\busing (the\s+)?gpt-4o\b", "using the active model", line, flags=re.IGNORECASE)

        # Precise environment variable descriptions in docs
        line = re.sub(r"\bANTHROPIC_API_KEY\b", "LLM_API_KEY", line)
        line = re.sub(r"\bOPENAI_API_KEY\b", "LLM_API_KEY", line)
        
        # CLAUDE_PLUGIN_ROOT and CLAUDE.md generic references (only when not inside path/URL)
        line = re.sub(r"\bCLAUDE_PLUGIN_ROOT\b", "SKILL_ROOT", line)
        line = re.sub(r"\bCLAUDE\.md\b", "AGENTS.md", line)
        
        # Proprietary tool replacements (only inside prose/instructions)
        line = re.sub(r"\bTodoWrite\b", "Write", line)
        line = re.sub(r"\bAskUserQuestion\b", "AskUser", line)
        
        new_lines.append(line)
        
    return "\n".join(new_lines)

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV not found at {CSV_PATH}")
        return

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Starting precise semantic conversion. Total rows loaded: {len(rows)}")

    fieldnames = reader.fieldnames
    # Ensure new columns exist
    new_cols = ["conversion_status", "conversion_decision_basis", "conversion_destination_path"]
    for col in new_cols:
        if col not in fieldnames:
            fieldnames.append(col)

    converted_count = 0
    intrinsic_count = 0
    no_change_count = 0
    quarantined_count = 0

    rebuilt_rows = []

    for idx, r in enumerate(rows):
        source_path = r["source_path"]
        cls = r["compatibility_classification"]

        # Resolve final path
        actual_path = RENAMED_PATHS_MAP.get(source_path, source_path)
        r["conversion_destination_path"] = actual_path
        
        # Handle Quarantined rows separately (separately reported as Not In Scope)
        if cls == "Unsupported application or platform":
            r["conversion_status"] = "Not In Scope (Phase 03 Quarantined)"
            r["conversion_decision_basis"] = "Skipped - Already quarantined in Phase 03"
            quarantined_count += 1
            rebuilt_rows.append(r)
            continue

        # Handle Intrinsic rows separately
        if source_path in INTRINSIC_PATHS:
            r["conversion_status"] = "Retained (Intrinsic)"
            r["conversion_decision_basis"] = "Intrinsically dependent on platform API / brand guideline"
            intrinsic_count += 1
            
            # Add compatibility field to frontmatter if not present
            skill_md_path = os.path.join(ROOT_DIR, actual_path, "SKILL.md")
            if os.path.exists(skill_md_path):
                try:
                    with open(skill_md_path, "r", encoding="utf-8") as sf:
                        content = sf.read()
                    if "compatibility:" not in content:
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            fm = parts[1]
                            body = parts[2]
                            fm += f"compatibility: 'Intrinsic platform/provider dependency: {r['folder_name']}'\n"
                            new_content = "---" + fm + "---" + body
                            with open(skill_md_path, "w", encoding="utf-8") as sf_out:
                                sf_out.write(new_content)
                except Exception as e:
                    print(f"Error adding frontmatter to intrinsic skill: {e}")
            rebuilt_rows.append(r)
            continue

        # Active / Unresolved skills: check for physical files to convert
        skill_dir = os.path.join(ROOT_DIR, actual_path)
        has_physical_change = False
        
        # Check and clean .claude-plugin directory
        claude_plugin_dir = os.path.join(skill_dir, ".claude-plugin")
        if os.path.exists(claude_plugin_dir):
            try:
                shutil.rmtree(claude_plugin_dir)
                has_physical_change = True
                print(f"Removed obsolete .claude-plugin scaffolding from {actual_path}")
            except Exception as e:
                print(f"Error pruning .claude-plugin: {e}")

        # Scan and convert text files in directory
        if os.path.exists(skill_dir):
            for root, dirs, files in os.walk(skill_dir):
                for file in files:
                    if file.endswith((".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh")):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="replace") as f_in:
                                text = f_in.read()
                            new_text = precise_convert_text(text, file_path)
                            if new_text != text:
                                with open(file_path, "w", encoding="utf-8") as f_out:
                                    f_out.write(new_text)
                                has_physical_change = True
                        except Exception as e:
                            print(f"Error converting file {file_path}: {e}")

        if has_physical_change:
            r["conversion_status"] = "Converted"
            r["conversion_decision_basis"] = "Nonessential provider coupling neutralized semantically"
            converted_count += 1
        else:
            r["conversion_status"] = "Reviewed - No Conversion Required"
            r["conversion_decision_basis"] = "Active skill reviewed; no nonessential provider coupling detected or conversion required"
            no_change_count += 1

        rebuilt_rows.append(r)

    # Save CSV
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rebuilt_rows)

    print("\n=== SEMANTIC CONVERSION COMPLETED ===")
    print(f"  - Converted (Neutralized): {converted_count}")
    print(f"  - Retained (Intrinsic): {intrinsic_count}")
    print(f"  - Reviewed (No Conversion Required): {no_change_count}")
    print(f"  - Not In Scope (Phase 03 Quarantined): {quarantined_count}")
    print(f"  - Total Checked Rows: {converted_count + intrinsic_count + no_change_count + quarantined_count}")

if __name__ == "__main__":
    main()
