import csv
import os

CSV_PATH = "/Users/garystringham/github-revrebel/skills-rebuild/task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV not found at {CSV_PATH}")
        return

    keywords = ["claude", "openai", "gpt", "gemini", "anthropic", "cursor", "codex"]
    
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} inventory rows.")
    
    retained_rows = [r for r in rows if r.get("compatibility_classification") != "Unsupported application or platform"]
    print(f"Found {len(retained_rows)} retained / unresolved rows to analyze.")

    matching_rows = []
    for r in retained_rows:
        # Check all fields for keywords (case insensitive)
        found_kw = []
        for col, val in r.items():
            if val:
                val_lower = val.lower()
                for kw in keywords:
                    if kw in val_lower and kw not in found_kw:
                        found_kw.append(kw)
        if found_kw:
            matching_rows.append((r, found_kw))

    print(f"Found {len(matching_rows)} matching rows with provider dependencies:")
    for idx, (r, kws) in enumerate(matching_rows):
        print(f"{idx+1}. Path: {r['source_path']}")
        print(f"   Name: {r['folder_name']} / FM: {r['frontmatter_name']}")
        print(f"   Keywords matched: {kws}")
        print(f"   Classification: {r['compatibility_classification']}")
        print(f"   Model Deps: {r.get('model_dependencies')}")
        print(f"   App Deps: {r.get('application_dependencies')}")
        print(f"   Evidence: {r.get('compatibility_evidence')}")
        print("-" * 50)

if __name__ == "__main__":
    main()
