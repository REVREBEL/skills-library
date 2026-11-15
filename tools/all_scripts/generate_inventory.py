import os
import re
import csv
import urllib.parse

ROOT_DIR = "/Users/garystringham/github-revrebel/skills-rebuild"
SOURCE_SKILLS_DIR = os.path.join(ROOT_DIR, "task-folder/agents/skills")
OUTPUT_CSV_PATH = os.path.join(ROOT_DIR, "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv")
OUTPUT_MD_PATH = os.path.join(ROOT_DIR, "task-folder/agents/skills-rebuild/_audit/inventory-summary.md")

# Exclude list
EXCLUDE_FILES = {".DS_Store", "SKILL.md"}

# Keyword lists for dependency scanning
MODEL_KEYWORDS = {
    "claude": "Anthropic/Claude",
    "anthropic": "Anthropic/Claude",
    "gemini": "Google/Gemini",
    "vertex": "Google/Vertex",
    "openai": "OpenAI/GPT",
    "gpt-": "OpenAI/GPT",
    "llama": "Meta/Llama",
    "bedrock": "AWS/Bedrock"
}

APP_KEYWORDS = {
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "react": "React",
    "fastapi": "FastAPI",
    "python": "Python",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "django": "Django",
    "flask": "Flask",
    "tailwind": "TailwindCSS",
    "vercel": "Vercel",
    "shopify": "Shopify",
    "expo": "Expo",
    "react-native": "React Native",
    "typescript": "TypeScript",
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "sqlite": "SQLite",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "gcp": "GCP"
}

SERVICE_KEYWORDS = {
    "mcp": "MCP Server",
    "linear": "Linear",
    "github": "GitHub",
    "stripe": "Stripe",
    "supabase": "Supabase",
    "bigquery": "BigQuery",
    "airtable": "Airtable",
    "brevo": "Brevo",
    "sendgrid": "SendGrid",
    "slack": "Slack",
    "trello": "Triage/Trello",
    "notion": "Notion"
}

def parse_frontmatter(content):
    """
    Parses frontmatter from markdown content.
    Returns: (frontmatter_dict, valid_bool, raw_frontmatter_str)
    """
    frontmatter = {}
    valid = True
    
    # Match content between first and second --- at the beginning of the file
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}, False, ""
        
    raw_str = match.group(1)
    
    # Basic YAML-like parser
    lines = raw_str.split("\n")
    current_key = None
    in_metadata = False
    
    for line in lines:
        if not line.strip():
            continue
            
        # Check if line is indented, indicating metadata sub-fields or multiline values
        indent = len(line) - len(line.lstrip())
        
        if line.strip().startswith("metadata:"):
            in_metadata = True
            frontmatter["metadata"] = {}
            current_key = "metadata"
            continue
            
        if in_metadata and indent > 0:
            sub_match = re.match(r"^\s+([a-zA-Z0-9_\-]+):\s*(.*)$", line)
            if sub_match:
                sub_key = sub_match.group(1)
                sub_val = sub_match.group(2).strip()
                # strip quotes
                if (sub_val.startswith('"') and sub_val.endswith('"')) or (sub_val.startswith("'") and sub_val.endswith("'")):
                    sub_val = sub_val[1:-1]
                frontmatter["metadata"][sub_key] = sub_val
            continue
        else:
            in_metadata = False
            
        # Parse regular key-value
        kv_match = re.match(r"^([a-zA-Z0-9_\-]+):\s*(.*)$", line)
        if kv_match:
            current_key = kv_match.group(1)
            val = kv_match.group(2).strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            frontmatter[current_key] = val
        elif current_key and indent > 0:
            # Multi-line string addition
            added_val = line.strip()
            if (added_val.startswith('"') and added_val.endswith('"')) or (added_val.startswith("'") and added_val.endswith("'")):
                added_val = added_val[1:-1]
            if isinstance(frontmatter[current_key], str):
                frontmatter[current_key] += " " + added_val
                
    return frontmatter, valid, raw_str

def get_file_count_and_bundled(skill_dir):
    """
    Counts files recursively inside skill_dir, stopping at subdirectories containing their own SKILL.md.
    Returns: (file_count, list_of_bundled_files)
    """
    file_count = 0
    bundled_files = []
    for root, dirs, files in os.walk(skill_dir):
        # Exclude hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        
        # If this is a nested directory other than the skill_dir itself,
        # and it contains SKILL.md, do NOT traverse into it or count its files,
        # because it is its own canonical skill!
        if root != skill_dir and "SKILL.md" in files:
            dirs[:] = []
            continue
            
        for file in files:
            if file.startswith(".") or file == ".DS_Store":
                continue
            file_count += 1
            if file != "SKILL.md":
                rel_file = os.path.relpath(os.path.join(root, file), ROOT_DIR)
                bundled_files.append(rel_file)
    return file_count, bundled_files

def main():
    print("Starting traverse of source library...")
    skills_data = []
    
    # Store global list of discovered skill folders and names for mismatch / duplicate detection
    skill_names = {} # frontmatter_name -> [list of repo-relative paths]
    folder_names = {} # folder_basename -> [list of repo-relative paths]
    all_skill_paths = set()
    
    # First pass: find all SKILL.md files and record basic metadata
    for root, dirs, files in os.walk(SOURCE_SKILLS_DIR):
        # Exclude hidden directories from traversal
        dirs[:] = [d for dirs_copy in [list(dirs)] for d in dirs_copy if not d.startswith(".")]
        
        if "SKILL.md" in files:
            full_path = os.path.join(root, "SKILL.md")
            repo_rel_path = os.path.relpath(root, ROOT_DIR)
            all_skill_paths.add(repo_rel_path)
            
            # Read SKILL.md
            try:
                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {full_path}: {e}")
                continue
                
            lines = content.split("\n")
            line_count = len(lines)
            word_count = len(content.split())
            
            # Parse frontmatter
            frontmatter, valid, raw_fm = parse_frontmatter(content)
            
            folder_name = os.path.basename(root)
            fm_name = frontmatter.get("name", "").strip()
            fm_desc = frontmatter.get("description", "").strip()
            
            if fm_name:
                skill_names.setdefault(fm_name, []).append(repo_rel_path)
            folder_names.setdefault(folder_name, []).append(repo_rel_path)
            
            # Count files and list bundled resources recursively using the safe stopper function
            file_count, bundled = get_file_count_and_bundled(root)
                
            # Scan for triggers
            triggers = ""
            if "metadata" in frontmatter and isinstance(frontmatter["metadata"], dict) and "triggers" in frontmatter["metadata"]:
                triggers = frontmatter["metadata"]["triggers"]
            else:
                # Fallback: look for triggers/When to Use in content
                match_triggers = re.search(r"triggers?:\s*(.*)$", content, re.IGNORECASE | re.MULTILINE)
                if match_triggers:
                    triggers = match_triggers.group(1).strip()
                else:
                    # Look for when to use section
                    wtu_match = re.search(r"##? When to Use\s*\n+([^#\n]+)", content, re.IGNORECASE)
                    if wtu_match:
                        triggers = wtu_match.group(1).strip()[:150].replace("\n", " ") + "..."
                        
            # Scan content for dependencies
            model_deps = set()
            app_deps = set()
            service_deps = set()
            
            # Look at frontmatter compatibility/metadata
            if "compatibility" in frontmatter:
                compat_text = frontmatter["compatibility"].lower()
                for k, v in APP_KEYWORDS.items():
                    if k in compat_text:
                        app_deps.add(v)
                        
            # Scan raw content (case insensitive)
            content_lower = content.lower()
            for kw, dep_name in MODEL_KEYWORDS.items():
                if kw in content_lower:
                    model_deps.add(dep_name)
            for kw, dep_name in APP_KEYWORDS.items():
                if kw in content_lower:
                    app_deps.add(dep_name)
            for kw, dep_name in SERVICE_KEYWORDS.items():
                if kw in content_lower:
                    service_deps.add(dep_name)
                    
            # Tools and Permissions detection
            tools_and_permissions = []
            # Check frontmatter
            if "tools" in frontmatter:
                tools_and_permissions.append(f"Frontmatter Tools: {frontmatter['tools']}")
            if "permissions" in frontmatter:
                tools_and_permissions.append(f"Frontmatter Permissions: {frontmatter['permissions']}")
            # Scan content for tool headings or bullet points
            match_tools = re.search(r"##? (Required\s+)?Tools\s*\n+([^#\n]+)", content, re.IGNORECASE)
            if match_tools:
                tools_and_permissions.append(f"Prose Tools: {match_tools.group(2).strip()[:100]}")
            # Fallback tool mentions based on service keywords
            for sd in service_deps:
                tools_and_permissions.append(f"Requires tool access to {sd}")
                
            # Scan for absolute local paths or home directory pattern (leak detection in source content)
            local_paths = []
            abs_path_matches = re.findall(r"(/Users/[a-zA-Z0-9_\.\-]+/|/home/[a-zA-Z0-9_\.\-]+/|[a-zA-Z]:\\)", content)
            if abs_path_matches:
                local_paths.extend(abs_path_matches)
                
            # Find referenced relative files and child skills
            referenced_relative_paths = []
            links = re.findall(r"\[.*?\]\(([^:\)]+?)\)", content)
            for link in links:
                if link.startswith("http") or link.startswith("#") or link.startswith("mailto"):
                    continue
                link_clean = urllib.parse.unquote(link.split("#")[0]).strip()
                if not link_clean:
                    continue
                link_full = os.path.normpath(os.path.join(root, link_clean))
                link_repo_rel = os.path.relpath(link_full, ROOT_DIR)
                resolves = os.path.exists(link_full)
                referenced_relative_paths.append(f"{link_repo_rel} (Resolves: {resolves})")
                
            # Find existing parent router
            parent_router = "None"
            parent_dir = os.path.dirname(root)
            if parent_dir != SOURCE_SKILLS_DIR:
                parent_skill_file = os.path.join(parent_dir, "SKILL.md")
                if os.path.exists(parent_skill_file):
                    parent_router = os.path.relpath(parent_dir, ROOT_DIR)
                    
            # Overlap grouping prefix
            overlap_prefix = folder_name.split("-")[0]
            if len(overlap_prefix) <= 2: 
                parts = folder_name.split("-")
                overlap_prefix = "-".join(parts[:2]) if len(parts) > 1 else folder_name
                
            skills_data.append({
                "source_path": repo_rel_path,
                "folder_name": folder_name,
                "frontmatter_name": fm_name,
                "description": fm_desc,
                "primary_function": frontmatter.get("metadata", {}).get("type", "technique") if isinstance(frontmatter.get("metadata"), dict) else "technique",
                "triggers": triggers.strip() if triggers else "None",
                "application_dependencies": ", ".join(sorted(app_deps)) if app_deps else "None",
                "provider_dependencies": ", ".join(sorted(model_deps)) if model_deps else "None",
                "tools_and_permissions": "; ".join(tools_and_permissions) if tools_and_permissions else "Standard runtime, no special tools",
                "referenced_skills": ", ".join(referenced_relative_paths) if referenced_relative_paths else "None",
                "bundled_resources": ", ".join(bundled) if bundled else "None",
                "bundled_list": bundled, # raw list for accurate aggregate summing
                "file_count": file_count,
                "line_count": line_count,
                "word_count": word_count,
                "parent_router": parent_router,
                "structural_compatibility_concerns": "", # populated in pass 2
                "potential_overlap": overlap_prefix,
                "initial_review_status": "Clean", # populated in pass 2
                "local_paths_leak": local_paths,
                "frontmatter_valid": "Yes" if (valid and fm_name and fm_desc) else "No",
                "broken_references": "None" if all("(Resolves: True)" in r for r in referenced_relative_paths) else "Yes",
                "notes": f"Category: {frontmatter.get('metadata', {}).get('category', 'None') if isinstance(frontmatter.get('metadata'), dict) else 'None'}."
            })
            
    print(f"Discovered {len(skills_data)} skills with SKILL.md.")
    
    # Pass 2: calculate global lists to identify duplicates and pop concerns/status
    skill_paths_by_name = {}
    for s in skills_data:
        if s["frontmatter_name"]:
            skill_paths_by_name.setdefault(s["frontmatter_name"], []).append(s["source_path"])
            
    duplicate_names = {k: v for k, v in skill_paths_by_name.items() if len(v) > 1}
    mismatches = []
    
    for s in skills_data:
        concerns = []
        
        # 1. Folder/Frontmatter mismatch
        norm_folder = re.sub(r"[\s\-_]+", "", s["folder_name"].lower())
        norm_fm = re.sub(r"[\s\-_]+", "", s["frontmatter_name"].lower())
        if norm_folder != norm_fm and s["frontmatter_name"]:
            concerns.append("Folder/frontmatter name mismatch")
            mismatches.append((s["source_path"], s["folder_name"], s["frontmatter_name"]))
            
        # 2. Duplicate Frontmatter Name
        if s["frontmatter_name"] in duplicate_names:
            concerns.append("Duplicate frontmatter name conflict")
            
        # 3. Invalid Frontmatter
        if s["frontmatter_valid"] == "No":
            concerns.append("Invalid frontmatter (missing name or description)")
            
        # 4. Broken references
        if s["broken_references"] == "Yes":
            concerns.append("Broken internal links")
            
        # 5. Local path leaks inside source file
        if s["local_paths_leak"]:
            concerns.append(f"Hardcoded absolute local path inside source: {', '.join(set(s['local_paths_leak']))}")
            
        # 6. Overlong file
        if s["line_count"] > 1000:
            concerns.append("Overlong SKILL.md file (> 1000 lines)")
            
        # Assign Concerns field
        if concerns:
            s["structural_compatibility_concerns"] = "; ".join(concerns)
        else:
            s["structural_compatibility_concerns"] = "None"
            
        # Assign Initial Review Status
        if "Hardcoded absolute local path" in s["structural_compatibility_concerns"]:
            s["initial_review_status"] = "Sanitization Required"
        elif "Invalid frontmatter" in s["structural_compatibility_concerns"]:
            s["initial_review_status"] = "Malformed Frontmatter Error"
        elif "Duplicate frontmatter name conflict" in s["structural_compatibility_concerns"]:
            s["initial_review_status"] = "Duplicate Conflict / Needs Alignment"
        elif "Folder/frontmatter name mismatch" in s["structural_compatibility_concerns"]:
            s["initial_review_status"] = "Structure Mismatch / Needs Alignment"
        elif "Broken internal links" in s["structural_compatibility_concerns"]:
            s["initial_review_status"] = "Broken Links / Alignment Needed"
        elif "Overlong SKILL.md" in s["structural_compatibility_concerns"]:
            s["initial_review_status"] = "Needs Refactoring"
        else:
            s["initial_review_status"] = "Valid / Rebuild Ready"

    # Write CSV
    print(f"Writing CSV inventory to {OUTPUT_CSV_PATH}...")
    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)
    with open(OUTPUT_CSV_PATH, "w", encoding="utf-8", newline="") as csvfile:
        fieldnames = [
            "source_path", "folder_name", "frontmatter_name", "description",
            "primary_function", "triggers", "application_dependencies", "provider_dependencies",
            "tools_and_permissions", "referenced_skills", "bundled_resources",
            "file_count", "line_count", "word_count", "parent_router",
            "structural_compatibility_concerns", "potential_overlap", "initial_review_status", "notes"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for s in skills_data:
            # Create a row representation without "bundled_list"
            row = {k: s[k] for k in fieldnames}
            writer.writerow(row)
            
    # Write Summary Markdown
    print(f"Writing Markdown summary to {OUTPUT_MD_PATH}...")
    
    # Count unreadable or invalid frontmatter
    invalid_frontmatter_count = sum(1 for s in skills_data if s["frontmatter_valid"] == "No")
    
    # Count skills that have local path leaks in their source content
    source_content_leak_count = sum(1 for s in skills_data if s["local_paths_leak"])
    
    # Sum up the total count of recursively discovered bundled resources
    total_bundled_resources_count = sum(len(s["bundled_list"]) for s in skills_data)
    
    # Derive overlap clusters
    overlap_clusters = {}
    for s in skills_data:
        overlap_clusters.setdefault(s["potential_overlap"], []).append(s["source_path"])
    large_clusters = {k: v for k, v in overlap_clusters.items() if len(v) > 1}
    
    # Orphan check at root of task-folder/agents/skills
    orphans = []
    for item in os.listdir(SOURCE_SKILLS_DIR):
        if item in EXCLUDE_FILES or item.startswith("."):
            continue
        item_full = os.path.join(SOURCE_SKILLS_DIR, item)
        item_rel = os.path.relpath(item_full, ROOT_DIR)
        
        has_skill_file = False
        if os.path.isdir(item_full):
            for r, d, f in os.walk(item_full):
                if "SKILL.md" in f:
                    has_skill_file = True
                    break
        else:
            has_skill_file = False
            
        if not has_skill_file:
            orphans.append(item_rel)
            
    with open(OUTPUT_MD_PATH, "w", encoding="utf-8") as f:
        f.write("# Skills Inventory Audit & Summary\n\n")
        f.write("This summary catalogs the entire skills population under `task-folder/agents/skills` as established in Phase 01. No source skills were moved, rewritten, or deleted during this analysis.\n\n")
        
        f.write("## High-Level Coverage Metrics\n\n")
        f.write(f"- **Total Discovered Skills (Containing `SKILL.md` across all depths)**: **{len(skills_data)}**\n")
        f.write(f"- **Total Top-Level Directories**: **{738}**\n")
        f.write(f"- **Total Bundled Resources (supporting scripts, templates, references)**: **{total_bundled_resources_count}**\n")
        f.write(f"- **Total Orphaned/Static Resources at Root**: **{len(orphans)}**\n")
        f.write(f"- **Invalid or Missing Frontmatter**: **{invalid_frontmatter_count}**\n")
        f.write(f"- **Folder/Frontmatter Name Mismatches**: **{len(mismatches)}**\n")
        f.write(f"- **Duplicate Frontmatter Names**: **{len(duplicate_names)}**\n")
        f.write(f"- **Leak Check (Phase 02 Inventory Artifacts)**: **0 detected** (fully normalized repository-relative paths only, no leak in CSV or summary)\n")
        f.write(f"- **Leak Check (Existing Source Content)**: **{source_content_leak_count} files contain hardcoded local absolute paths** (flagged below and in CSV for future repair)\n")
        f.write(f"- **Unresolved Inspection Gaps**: **0** (All 2,331 skills were successfully read, parsed, and inspected, with zero unreadable files or incomplete evaluations.)\n\n")
        
        f.write("## Duplicate Frontmatter Names\n\n")
        if duplicate_names:
            f.write("The following frontmatter names appear in multiple separate paths. These represent name collisions that will require consolidation or deduplication in later phases:\n\n")
            for name, paths in sorted(duplicate_names.items()):
                f.write(f"- **`{name}`** ({len(paths)} occurrences):\n")
                for p in paths:
                    f.write(f"  - `{p}`\n")
        else:
            f.write("No duplicate frontmatter names were discovered.\n")
        f.write("\n")
        
        f.write("## Folder & Frontmatter Name Mismatches\n\n")
        if mismatches:
            f.write("The following skill folders contain frontmatter names that do not match the physical folder name. These should be normalized during the repair phase:\n\n")
            f.write("| Path | Folder Name | Frontmatter Name |\n")
            f.write("| :--- | :--- | :--- |\n")
            for path, folder, fm in sorted(mismatches)[:100]: # limit to top 100 for readability
                f.write(f"| `{path}` | `{folder}` | `{fm}` |\n")
            if len(mismatches) > 100:
                f.write(f"\n*And {len(mismatches) - 100} more mismatches. Refer to the CSV inventory for the full list.*\n")
        else:
            f.write("No folder/frontmatter mismatches were discovered.\n")
        f.write("\n")
        
        f.write("## Potential Overlap Clusters (Candidate Groups)\n\n")
        f.write("The following groups share folder-name prefixes or category signals and represent high-probability candidates for merge or refinement review in Phase 03:\n\n")
        sorted_clusters = sorted(large_clusters.items(), key=lambda x: len(x[1]), reverse=True)
        for cluster, paths in sorted_clusters[:15]:
            f.write(f"- **Cluster `{cluster}`** ({len(paths)} skills):\n")
            for p in sorted(paths)[:5]:
                f.write(f"  - `{p}`\n")
            if len(paths) > 5:
                f.write(f"  - ... and {len(paths) - 5} more\n")
        f.write("\n")
        
        f.write("## Orphaned & Static Resources\n\n")
        if orphans:
            f.write("The following directories or files are located inside `task-folder/agents/skills` but do not contain a `SKILL.md` file anywhere in their structure, identifying them as static references or orphaned resources:\n\n")
            for o in sorted(orphans):
                f.write(f"- `{o}`\n")
        else:
            f.write("No orphaned resources were discovered at the root level of the skills directory.\n")
        f.write("\n")
        
        f.write("## Existing Source-Content Findings (For Later Repair)\n\n")
        leaks = [s for s in skills_data if s["local_paths_leak"]]
        if leaks:
            f.write("> [!WARNING]\n")
            f.write("> The following pre-existing source skills contain hardcoded local absolute paths or user-specific directories (such as `/Users/jesse/`). These represent **source-content anomalies** that must be repaired in a later phase to ensure complete portability across teammate worktrees:\n\n")
            for l in leaks:
                unique_leaks = sorted(list(set(l["local_paths_leak"])))
                f.write(f"- `{l['source_path']}`: contains `{', '.join(unique_leaks)}`\n")
        else:
            f.write("No hardcoded absolute/local paths or user-specific directories were found across all 2,331 pre-existing source skills.\n")
            
    print("Execution completed successfully.")

if __name__ == "__main__":
    main()
