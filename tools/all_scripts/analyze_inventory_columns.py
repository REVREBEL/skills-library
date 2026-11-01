import csv

CSV_PATH = "/Users/garystringham/github-revrebel/skills-rebuild/task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"

def analyze():
    print("Reading CSV...")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"Total rows in CSV: {len(rows)}")
    
    app_deps_counts = {}
    provider_deps_counts = {}
    
    for r in rows:
        app_dep = r.get("application_dependencies", "None")
        provider_dep = r.get("provider_dependencies", "None")
        
        for dep in app_dep.split(", "):
            dep = dep.strip()
            if dep:
                app_deps_counts[dep] = app_deps_counts.get(dep, 0) + 1
                
        for dep in provider_dep.split(", "):
            dep = dep.strip()
            if dep:
                provider_deps_counts[dep] = provider_deps_counts.get(dep, 0) + 1
                
    print("\nApplication Dependencies Counts:")
    for k, v in sorted(app_deps_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"- {k}: {v}")
        
    print("\nProvider Dependencies Counts:")
    for k, v in sorted(provider_deps_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"- {k}: {v}")

if __name__ == "__main__":
    analyze()
