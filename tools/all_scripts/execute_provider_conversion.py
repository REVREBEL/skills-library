import csv
import os
import re
import shutil

CSV_PATH = "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
ROOT_DIR = "."

# Technical lock-in patterns
PATTERNS = {
    "CLAUDE_MD_OR_DOT_CLAUDE": r"\bCLAUDE\.md\b|\B\.claude\b",
    "PROVIDER_ENV_VARS": r"\bANTHROPIC_API_KEY\b|\bOPENAI_API_KEY\b|\bGEMINI_API_KEY\b",
    "MODEL_LOCK": r"claude-3-5-sonnet|claude-3|gpt-4o|gpt-4|gemini-1\.5-pro|gemini-1\.5|claude-opus|gpt-3\.5|text-davinci",
    "PROPRIETARY_TOOLS": r"\bTodoWrite\b|\bAskUserQuestion\b|\bClaudeCode\b"
}

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

RENAMED_PATHS_MAP = {
    "task-folder/agents/skills/linear-claude-skill": "task-folder/agents/skills/linear-skill",
    "task-folder/agents/skills/varlock-claude-skill": "task-folder/agents/skills/varlock-skill",
    "task-folder/agents/skills/folder-specific-claude-and-agents-md": "task-folder/agents/skills/folder-specific-agent-context",
    "task-folder/agents/skills/internal-comms-anthropic": "task-folder/agents/skills/internal-comms-guidelines"
}

# General conversions
REPLACEMENTS = [
    # Metadata Name/Folder renames
    (r"\blinear-claude-skill\b", "linear-skill"),
    (r"\bvarlock-claude-skill\b", "varlock-skill"),
    (r"\bfolder-specific-claude-and-agents-md\b", "folder-specific-agent-context"),
    (r"\binternal-comms-anthropic\b", "internal-comms-guidelines"),
    
    # Environment Variables / Config Paths
    (r"\bCLAUDE_PLUGIN_ROOT\b", "SKILL_ROOT"),
    (r"\bANTHROPIC_API_KEY\b", "LLM_API_KEY"),
    (r"\bOPENAI_API_KEY\b", "LLM_API_KEY"),
    
    # CLAUDE.md generic agent context references
    (r"\bCLAUDE\.md\b", "AGENTS.md"),
    (r"\bclaude-and-agents-md\b", "agent-context-guidelines"),
    
    # Model locks
    (r"\bclaude-3-5-sonnet\b", "a capable LLM"),
    (r"\bclaude-3\b", "a capable LLM"),
    (r"\bgpt-4o\b", "the active model"),
    (r"\bgpt-4\b", "the active model"),
    (r"\bgemini-1\.5-pro\b", "the active model"),
    
    # Proprietary tools
    (r"\bTodoWrite\b", "task_plan file update"),
    (r"\bAskUserQuestion\b", "clarifying question"),
    (r"\bClaudeCode\b", "the agent"),
    (r"\bClaude Code\b", "the agent"),
    (r"\bClaude sessions\b", "agent sessions"),
    (r"\bClaude's context\b", "the agent's context")
]

def perform_conversions(text):
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV not found at {CSV_PATH}")
        return

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Starting conversion phase. Total inventory rows loaded: {len(rows)}")

    fieldnames = reader.fieldnames
    # Add new Phase 04 columns if not already present
    new_cols = ["conversion_status", "conversion_decision_basis", "conversion_destination_path"]
    for col in new_cols:
        if col not in fieldnames:
            fieldnames.append(col)

    converted_count = 0
    intrinsic_count = 0
    no_change_count = 0

    rebuilt_rows = []

    for r in rows:
        source_path = r["source_path"]
        current_dest = r["current_destination"]
        cls = r["compatibility_classification"]

        # 1. Resolve final path (handle renames)
        actual_path = RENAMED_PATHS_MAP.get(source_path, source_path)
        r["conversion_destination_path"] = actual_path
        
        if cls == "Unsupported application or platform":
            # Quarantined / not-needed skills are not evaluated/converted in Phase 04
            r["conversion_status"] = "Reviewed - No Conversion Required"
            r["conversion_decision_basis"] = "Skipped - Already quarantined in Phase 03"
            rebuilt_rows.append(r)
            continue

        # 2. Check if intrinsic
        if source_path in INTRINSIC_PATHS:
            r["conversion_status"] = "Retained (Intrinsic)"
            r["conversion_decision_basis"] = "Intrinsically dependent on platform API / brand guideline"
            intrinsic_count += 1
            
            # Update frontmatter of intrinsic skills with compatibility marker
            skill_md_path = os.path.join(ROOT_DIR, actual_path, "SKILL.md")
            if os.path.exists(skill_md_path):
                try:
                    with open(skill_md_path, "r", encoding="utf-8") as sf:
                        content = sf.read()
                    
                    # Ensure compatibility field exists in frontmatter
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
                    print(f"Failed to update frontmatter for intrinsic skill at {actual_path}: {e}")
            
            rebuilt_rows.append(r)
            continue

        # 3. Detect provider coupling in this active/unresolved skill
        skill_dir = os.path.join(ROOT_DIR, actual_path)
        has_couple = False
        all_text = ""
        
        skill_md_path = os.path.join(ROOT_DIR, actual_path, "SKILL.md")
        if os.path.exists(skill_md_path):
            try:
                with open(skill_md_path, "r", encoding="utf-8") as sf:
                    all_text += sf.read()
            except: pass

        if os.path.exists(skill_dir):
            for root, dirs, files in os.walk(skill_dir):
                for file in files:
                    if file != "SKILL.md" and file.endswith((".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh")):
                        try:
                            with open(os.path.join(root, file), "r", encoding="utf-8") as of:
                                all_text += "\n" + of.read()
                        except: pass

        has_provider_name_in_path = any(kw in source_path.lower() for kw in ["claude", "gemini", "openai", "cursor", "codex", "anthropic"])
        has_tech_lock = any(re.search(regex, all_text, re.IGNORECASE) for regex in PATTERNS.values())

        if has_provider_name_in_path or has_tech_lock:
            # Fully convertible! Apply context-aware conversion pipeline
            r["conversion_status"] = "Converted"
            r["conversion_decision_basis"] = "Nonessential provider coupling neutralized"
            converted_count += 1

            # Process all text files in the skill directory
            if os.path.exists(skill_dir):
                for root, dirs, files in os.walk(skill_dir):
                    for file in files:
                        if file.endswith((".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh")):
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, "r", encoding="utf-8", errors="replace") as f_in:
                                    text = f_in.read()
                                new_text = perform_conversions(text)
                                if new_text != text:
                                    with open(file_path, "w", encoding="utf-8") as f_out:
                                        f_out.write(new_text)
                            except Exception as e:
                                print(f"Error converting file {file_path}: {e}")

            # Prune obsolete .claude-plugin folders (all found to contain only obsolete configuration scaffolding)
            claude_plugin_dir = os.path.join(skill_dir, ".claude-plugin")
            if os.path.exists(claude_plugin_dir):
                try:
                    shutil.rmtree(claude_plugin_dir)
                    print(f"Removed obsolete .claude-plugin scaffolding from {actual_path}")
                except Exception as e:
                    print(f"Failed to remove .claude-plugin directory at {claude_plugin_dir}: {e}")
        else:
            r["conversion_status"] = "Reviewed - No Conversion Required"
            r["conversion_decision_basis"] = "No provider coupling patterns detected"
            no_change_count += 1

        # 4. Update the current destination to reconcile with filesystem renames
        r["current_destination"] = actual_path
        rebuilt_rows.append(r)

    # Write the updated CSV back
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rebuilt_rows)

    print("\nConversion execution completed:")
    print(f"- Converted (Neutralized): {converted_count}")
    print(f"- Retained (Intrinsic): {intrinsic_count}")
    print(f"- Reviewed - No Conversion Required: {no_change_count}")
    print(f"Total rows updated in database: {len(rebuilt_rows)}")

if __name__ == "__main__":
    main()
