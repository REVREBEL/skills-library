import csv
import os
import re

CSV_PATH = "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
ROOT_DIR = "."

def clean_file_content(content, file_path):
    lines = content.splitlines()
    new_lines = []
    modified = False

    for line in lines:
        orig_line = line

        # 1. Clean up duplicate AGENTS.md / CLAUDE.md lists
        # E.g., AGENTS.md / AGENTS.md, AGENTS.md, AGENTS.md, AGENTS.md and AGENTS.md, etc.
        line = re.sub(r"\bAGENTS\.md\s*[,/&or\-、\s]+\s*AGENTS\.md\b", "AGENTS.md", line)
        line = re.sub(r"`AGENTS\.md`\s*[,/&or\-、\s]+\s*`AGENTS\.md`", "`AGENTS.md`", line)
        line = re.sub(r"\bCLAUDE\.md\s*[,/&or\-、\s]+\s*CLAUDE\.md\b", "CLAUDE.md", line)
        line = re.sub(r"`CLAUDE\.md`\s*[,/&or\-、\s]+\s*`CLAUDE\.md`", "`CLAUDE.md`", line)

        # 2. Clean up "a the agent" grammatical error
        # Replace "a the agent" with "an agent" (or contextually correct phrasing)
        line = re.sub(r"\ba the agent\b", "an agent", line, flags=re.IGNORECASE)

        # 3. Clean up factual commands and labels where "the agent" was incorrectly substituted
        line = re.sub(r"\bthe agent:\s*`claude\b", "Claude Code: `claude", line, flags=re.IGNORECASE)
        line = re.sub(r"\bthe agent:\s*claude\b", "Claude Code: claude", line, flags=re.IGNORECASE)
        line = re.sub(r"\bStart the agent:\s*claude\b", "Start Claude Code: claude", line, flags=re.IGNORECASE)
        line = re.sub(r"\bStart the agent:\s*`claude\b", "Start Claude Code: `claude", line, flags=re.IGNORECASE)
        line = re.sub(r"\bRun the agent:\s*claude\b", "Run Claude Code: claude", line, flags=re.IGNORECASE)
        line = re.sub(r"\bRun the agent:\s*`claude\b", "Run Claude Code: `claude", line, flags=re.IGNORECASE)

        # 4. Clean up factual citations & proper nouns
        line = re.sub(r"\bFowler,\s*the agent issue\b", "Fowler, Claude issue", line, flags=re.IGNORECASE)
        line = re.sub(r"\bAnthropic\s+the agent\s+best\s+practices\b", "Anthropic Claude best practices", line, flags=re.IGNORECASE)

        if line != orig_line:
            modified = True
        new_lines.append(line)

    return "\n".join(new_lines), modified

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV not found at {CSV_PATH}")
        return

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    converted_dirs = [r["conversion_destination_path"] for r in rows if r["conversion_status"] == "Converted"]
    print(f"Loaded {len(converted_dirs)} Converted skill directories to scan and clean.")

    total_cleaned_files = 0

    for d in converted_dirs:
        full_d = os.path.join(ROOT_DIR, d)
        if not os.path.exists(full_d):
            continue
        
        for root, dirs, files in os.walk(full_d):
            if any(ignored in root for ignored in [".git", "node_modules", ".github"]):
                continue
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext not in [".md", ".json", ".sh", ".py", ".js", ".ts", ".txt", ".yaml", ".yml", ".ps1"]:
                    continue
                fp = os.path.join(root, file)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as sf:
                        content = sf.read()
                    
                    new_content, modified = clean_file_content(content, fp)
                    if modified:
                        with open(fp, "w", encoding="utf-8") as sf:
                            sf.write(new_content)
                        print(f"  [CLEANED] {fp}")
                        total_cleaned_files += 1
                except Exception as e:
                    print(f"  [ERROR] Failed to process {fp}: {e}")

    print(f"Done! Cleaned semantic corruptions in {total_cleaned_files} files across all Converted skills.")

if __name__ == "__main__":
    main()
