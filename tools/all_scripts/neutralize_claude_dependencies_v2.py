import csv
import os
import re

CSV_PATH = "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
ROOT_DIR = "."

def neutralize_content(content, file_path):
    # Support all text and script extensions
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in [".md", ".json", ".sh", ".py", ".js", ".ts", ".txt", ".yaml", ".yml", ".ps1"]:
        return content, False

    lines = content.splitlines()
    new_lines = []
    modified = False

    for line in lines:
        line_lower = line.lower()
        
        # Skip URLs and upstream repository links to preserve provenance
        if "http://" in line_lower or "https://" in line_lower or "git@" in line_lower or "github.com" in line_lower:
            new_lines.append(line)
            continue

        # Skip backwards compatibility symlinks
        if "ln -s AGENTS.md CLAUDE.md" in line or "ln -s AGENTS.md CLAUDE.md.bak" in line:
            new_lines.append(line)
            continue

        orig_line = line

        # Replace ~/.claude with ~/.agents (unix-style)
        line = re.sub(r"~/\.claude", "~/.agents", line)
        
        # Replace ~\.claude with ~\.agents (windows-style)
        line = re.sub(r"~\\\.claude", r"~\\.agents", line)

        # Replace .claude/ with .agents/ (unix-style path separators)
        line = re.sub(r"\.claude/", ".agents/", line)

        # Replace .claude\ with .agents\ (windows-style path separators)
        line = re.sub(r"\.claude\\", r".agents\\", line)
        
        # Replace specific string configurations containing .claude
        line = re.sub(r"\.claude\b", ".agents", line)

        # Neutralize proper nouns when not related to pathing/execution environments
        line = re.sub(r"\bClaude Code\b", "the agent", line, flags=re.IGNORECASE)

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
    print(f"Loaded {len(converted_dirs)} Converted skill directories to scan and neutralize.")

    total_modified_files = 0

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
                    
                    new_content, modified = neutralize_content(content, fp)
                    if modified:
                        with open(fp, "w", encoding="utf-8") as sf:
                            sf.write(new_content)
                        print(f"  [MODIFIED] {fp}")
                        total_modified_files += 1
                except Exception as e:
                    print(f"  [ERROR] Failed to process {fp}: {e}")

    print(f"Done! Neutralized {total_modified_files} files across all Converted skills.")

if __name__ == "__main__":
    main()
