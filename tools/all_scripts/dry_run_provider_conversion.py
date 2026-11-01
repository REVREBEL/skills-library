import csv
import os
import re

CSV_PATH = "/Users/garystringham/github-revrebel/skills-rebuild/task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
ROOT_DIR = "/Users/garystringham/github-revrebel/skills-rebuild"

# Technical lock-in patterns
PATTERNS = {
    "CLAUDE_MD_OR_DOT_CLAUDE": r"\bCLAUDE\.md\b|\B\.claude\b",
    "PROVIDER_ENV_VARS": r"\bANTHROPIC_API_KEY\b|\bOPENAI_API_KEY\b|\bGEMINI_API_KEY\b",
    "MODEL_LOCK": r"claude-3-5-sonnet|claude-3|gpt-4o|gpt-4|gemini-1\.5-pro|gemini-1\.5|claude-opus|gpt-3\.5|text-davinci",
    "PROPRIETARY_TOOLS": r"\bTodoWrite\b|\bAskUserQuestion\b|\bClaudeCode\b"
}

def analyze_skill_files(source_path):
    skill_md_path = os.path.join(ROOT_DIR, source_path, "SKILL.md")
    content = ""
    if os.path.exists(skill_md_path):
        try:
            with open(skill_md_path, "r", encoding="utf-8", errors="replace") as sf:
                content = sf.read()
        except Exception:
            pass

    all_text = content
    skill_dir = os.path.join(ROOT_DIR, source_path)
    other_files = []
    if os.path.exists(skill_dir):
        for root, dirs, files in os.walk(skill_dir):
            for file in files:
                if file != "SKILL.md":
                    other_files.append(file)
                    if file.endswith((".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh")):
                        try:
                            with open(os.path.join(root, file), "r", encoding="utf-8", errors="replace") as of:
                                all_text += "\n" + of.read()
                        except Exception:
                            pass
    return content, all_text, other_files

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV not found at {CSV_PATH}")
        return

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    retained_rows = [r for r in rows if r.get("compatibility_classification") != "Unsupported application or platform"]
    print(f"Analyzing {len(retained_rows)} active rows for provider coupling decisions...")

    conversions = []
    intrinsic_keeps = []

    for r in retained_rows:
        source_path = r["source_path"]
        folder_name = r["folder_name"]
        frontmatter_name = r["frontmatter_name"]
        description = r["description"]

        # Get file contents
        content, all_text, other_files = analyze_skill_files(source_path)

        # Check for provider mentions or technical lock-ins
        has_provider_name_in_path = any(kw in source_path.lower() for kw in ["claude", "gemini", "openai", "cursor", "codex", "anthropic"])
        
        has_tech_lock = False
        matched_patterns = []
        for name, regex in PATTERNS.items():
            if re.search(regex, all_text, re.IGNORECASE):
                has_tech_lock = True
                matched_patterns.append(name)

        if has_provider_name_in_path or has_tech_lock:
            # Let's decide if it is intrinsic or convertible
            # Intrinsic cases:
            # - Under gemini/ folder
            # - Under codex/ folder (like codex-profiles, codex-subagent, codex-review, codex-fable5)
            # - folder_name contains "gemini" and is explicitly about Gemini (like nerdzao-elite-gemini-high, brand-guidelines-anthropic)
            is_intrinsic = False
            reasons = []

            if "gemini/" in source_path or "codex/" in source_path:
                is_intrinsic = True
                reasons.append("Platform APIs/tools specifically belonging to the platform's namespace")
            elif "brand-guidelines-anthropic" in source_path:
                is_intrinsic = True
                reasons.append("Anthropic brand guidelines and visual assets (brand-specific design)")
            elif "nerdzao-elite-gemini-high" in source_path:
                is_intrinsic = True
                reasons.append("Gemini-specific benchmark configuration and evaluation")

            if is_intrinsic:
                intrinsic_keeps.append({
                    "row": r,
                    "reasons": reasons,
                    "patterns": matched_patterns,
                    "path": source_path
                })
            else:
                # Convertible!
                # E.g. linear-claude-skill, varlock-claude-skill, folder-specific-claude-and-agents-md, planning-with-files, cc-skill-project-guidelines-example, etc.
                conversions.append({
                    "row": r,
                    "patterns": matched_patterns,
                    "path": source_path,
                    "has_name_lock": has_provider_name_in_path
                })

    print(f"\nDry-run analysis complete:")
    print(f"- Total active skills analyzed: {len(retained_rows)}")
    print(f"- To Convert (Neutralize): {len(conversions)} skills")
    print(f"- To Keep as Intrinsic: {len(intrinsic_keeps)} skills")

    print("\n--- TOP CANDIDATES TO CONVERT ---")
    for idx, c in enumerate(conversions[:20]):
        r = c["row"]
        print(f"{idx+1}. Path: {c['path']}")
        print(f"   Name: {r['folder_name']} / FM: {r['frontmatter_name']}")
        print(f"   Has Name Lock: {c['has_name_lock']}")
        print(f"   Tech Locks: {c['patterns']}")
        print("-" * 40)

    print("\n--- INTRINSIC KEEPS ---")
    for idx, ik in enumerate(intrinsic_keeps):
        r = ik["row"]
        print(f"{idx+1}. Path: {ik['path']}")
        print(f"   Name: {r['folder_name']} / FM: {r['frontmatter_name']}")
        print(f"   Reasons: {ik['reasons']}")
        print(f"   Tech Locks: {ik['patterns']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
