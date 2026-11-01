import csv
import os
import re

CSV_PATH = "/Users/garystringham/github-revrebel/skills-rebuild/task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
ROOT_DIR = "/Users/garystringham/github-revrebel/skills-rebuild"

# Technical lock-in patterns
PATTERNS = {
    "CLAUDE_MD_OR_DOT_CLAUDE": r"\bCLAUDE\.md\b|\B\.claude\b",
    "PROVIDER_ENV_VARS": r"\bANTHROPIC_API_KEY\b|\bOPENAI_API_KEY\b|\bGEMINI_API_KEY\b",
    "SLASH_COMMANDS": r"\s/\w+\b", # e.g. /bug, /search, /explain but let's narrow it down or analyze
    "MODEL_LOCK": r"claude-3|gpt-4|gemini-1\.5|claude-opus|gpt-3\.5|text-davinci",
    "PROPRIETARY_TOOLS": r"\bTodoWrite\b|\bAskUserQuestion\b|\bClaudeCode\b|\bCursor\b|\bCodex\b",
}

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV not found at {CSV_PATH}")
        return

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    retained_rows = [r for r in rows if r.get("compatibility_classification") != "Unsupported application or platform"]
    print(f"Analyzing {len(retained_rows)} retained / unresolved rows for technical coupling...")

    stats = {k: 0 for k in PATTERNS}
    results = []

    for r in retained_rows:
        source_path = r["source_path"]
        folder_name = r["folder_name"]
        
        # Read SKILL.md content
        skill_md_path = os.path.join(ROOT_DIR, source_path, "SKILL.md")
        content = ""
        if os.path.exists(skill_md_path):
            try:
                with open(skill_md_path, "r", encoding="utf-8", errors="replace") as sf:
                    content = sf.read()
            except Exception as e:
                print(f"Failed to read {skill_md_path}: {e}")

        # Walk through files in the skill folder to check for CLAUDE.md or other files
        all_text = content
        skill_dir = os.path.join(ROOT_DIR, source_path)
        other_files = []
        if os.path.exists(skill_dir):
            for root, dirs, files in os.walk(skill_dir):
                for file in files:
                    if file != "SKILL.md":
                        other_files.append(file)
                        # Read other text files
                        if file.endswith((".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh")):
                            try:
                                with open(os.path.join(root, file), "r", encoding="utf-8", errors="replace") as of:
                                    all_text += "\n" + of.read()
                            except Exception:
                                pass

        matched_patterns = {}
        for name, regex in PATTERNS.items():
            matches = re.findall(regex, all_text, re.IGNORECASE)
            if matches:
                # Deduplicate matches
                matched_patterns[name] = list(set(matches))
                stats[name] += 1

        if matched_patterns:
            results.append({
                "row": r,
                "matches": matched_patterns,
                "other_files": other_files
            })

    print(f"\nSummary of Matches:")
    for k, v in stats.items():
        print(f"- {k}: {v} skills")

    print(f"\nDetailed match list (first 50):")
    for idx, res in enumerate(results[:50]):
        r = res["row"]
        print(f"{idx+1}. Path: {r['source_path']}")
        print(f"   Name: {r['folder_name']}")
        print(f"   Matches: {res['matches']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
