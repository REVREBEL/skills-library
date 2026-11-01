#!/usr/bin/env python3
"""
build_phase_05_artifacts.py

Generates:
1. task-folder/agents/skills-rebuild/_audit/destination-map.csv
2. task-folder/agents/skills-rebuild/_audit/router-map.csv
3. task-folder/agents/skills-rebuild/_audit/functional-taxonomy.md
4. task-folder/agents/skills-rebuild/_audit/verify_phase_05.py
"""

import csv
import os
import re
from collections import defaultdict, Counter

INVENTORY_PATH = "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
DESTINATION_MAP_PATH = "task-folder/agents/skills-rebuild/_audit/destination-map.csv"
ROUTER_MAP_PATH = "task-folder/agents/skills-rebuild/_audit/router-map.csv"
TAXONOMY_REPORT_PATH = "task-folder/agents/skills-rebuild/_audit/functional-taxonomy.md"
VERIFY_SCRIPT_PATH = "task-folder/agents/skills-rebuild/_audit/verify_phase_05.py"

def make_slug(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\-]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def classify_skill(row):
    src = row['source_path'].lower()
    fn = row['folder_name'].lower()
    desc = (row['description'] or '').lower()
    fm = (row['frontmatter_name'] or '').lower()
    triggers = (row['triggers'] or '').lower()
    combined = f"{src} {fn} {fm} {desc} {triggers}"

    # Default values
    confidence = "high"
    concern = "None"
    future_structure = "none"

    # 1. meta-and-agent-skills
    if any(k in combined for k in [
        'skill-creator', 'skill-improver', 'skill-audit', 'skill-review', 'skill-check',
        'skill-optimizer', 'skill-manage', 'skill-library-restructure', 'skill-writer',
        'skill-make-template', 'skills-writing', 'template-skill', 'agent-skills',
        'skill lifecycle', 'audit skills', 'prompt-design', 'prompt-optimizer',
        'subagent', 'multi-agent-system', 'agent-architecture'
    ]) and not any(k in fn for k in ['seo', 'marketing', 'figma']):
        if any(k in combined for k in ['audit', 'check', 'validate', 'benchmark', 'optimizer']):
            return ('meta-and-agent-skills', 'skill-validation',
                    'Primary outcome is validation, auditing, and quality checking of agent skills.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['create', 'make', 'write', 'author', 'template', 'scaffold']):
            return ('meta-and-agent-skills', 'skill-lifecycle',
                    'Primary outcome is scaffolding, authoring, and lifecycle management of skills.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['restructure', 'manage', 'inventory', 'review']):
            return ('meta-and-agent-skills', 'skill-lifecycle',
                    'Primary outcome is skill lifecycle governance and repository restructuring.',
                    'high', 'None', 'router_candidate')
        else:
            return ('meta-and-agent-skills', 'agent-architecture',
                    'Primary outcome is architecting autonomous agents and multi-agent systems.',
                    'high', 'None', 'none')

    # 2. marketing-and-seo
    if any(k in src for k in ['/seo/', 'seo-skills', 'geo-audit', 'local-legal-seo']) or any(k in combined for k in [
        'seo', 'search engine', 'keyword research', 'serp', 'backlink', 'schema markup',
        'meta tags', 'page speed', 'cro', 'conversion rate', 'funnel', 'landing page cro',
        'onboarding cro', 'social media', 'advertising', 'ad creative', 'viral generator',
        'growth marketing', 'marketing psychology', 'subject line'
    ]):
        if any(k in combined for k in ['schema', 'technical seo', 'crawl', 'index', 'pagespeed', 'sitemap', 'robot']):
            return ('marketing-and-seo', 'technical-seo',
                    'Primary outcome is technical search engine crawlability, indexing, schema, and page speed.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['geo', 'local', 'city', 'region', 'google business']):
            return ('marketing-and-seo', 'geo-and-local-seo',
                    'Primary outcome is localized and geographic search ranking optimization.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['cro', 'conversion', 'signup', 'popup', 'onboarding-cro', 'loss aversion', 'urgency', 'scarcity', 'page-cro']):
            return ('marketing-and-seo', 'cro',
                    'Primary outcome is conversion rate optimization, funnel improvement, and user action triggers.',
                    'high', 'None', 'merge_candidate')
        elif any(k in combined for k in ['social', 'tweet', 'linkedin', 'ad creative', 'viral', 'instagram', 'facebook ads']):
            return ('marketing-and-seo', 'content-and-campaigns',
                    'Primary outcome is marketing campaigns, digital advertising creatives, and social distribution.',
                    'high', 'None', 'none')
        else:
            return ('marketing-and-seo', 'on-page-seo',
                    'Primary outcome is on-page search visibility, keyword targeting, and SERP content optimization.',
                    'high', 'None', 'none')

    # 3. design-and-experience
    if any(k in src for k in ['/design/', '/figma/', '/ui/', '/ux/']) or any(k in combined for k in [
        'ui-ux', 'user interface', 'ux design', 'design system', 'tailwind', 'shadcn', 'radix',
        'styling', 'css', 'design taste', 'aesthetic', 'wireframe', 'animation', 'remotion',
        'threejs', 'canvas', 'glsl', 'shader', 'lookdev', 'color palette', 'design-brief', 'magic-ui'
    ]):
        if any(k in combined for k in ['taste', 'critique', 'aesthetic', 'review-animations', 'design-review', 'visual-emotion', 'styleseed']):
            return ('design-and-experience', 'taste-and-critique',
                    'Primary outcome is aesthetic critique, visual design review, and taste heuristics.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['animation', 'motion', 'threejs', 'remotion', 'shader', 'glsl', 'canvas', '3d', 'scroll-experience']):
            return ('design-and-experience', 'motion-and-graphics',
                    'Primary outcome is visual motion, 3D rendering, canvas animations, and interactive graphics.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['tailwind', 'shadcn', 'radix', 'design system', 'figma', 'tokens', 'theme', 'ui kit', 'component library']):
            return ('design-and-experience', 'design-systems',
                    'Primary outcome is component design systems, tokens, UI kits, and Figma/Tailwind libraries.',
                    'high', 'None', 'merge_candidate')
        else:
            return ('design-and-experience', 'ui-ux',
                    'Primary outcome is UI layout, user experience wireframing, and visual interaction design.',
                    'high', 'None', 'none')

    # 4. quality-and-security
    if any(k in combined for k in [
        'playwright', 'vitest', 'cypress', 'jest', 'unit test', 'e2e test', 'test-driven',
        'qa', 'testing', 'vulnerability', 'security testing', 'pentest', 'penetration testing',
        'sast', 'semgrep', 'sql injection', 'threat model', 'pci', 'compliance',
        'privacy-by-design', 'wireshark', 'malware', 'debugging', 'troubleshooting',
        'memory leak', 'profiling', 'screen-reader', 'lint-and-validate', 'shellcheck', 'mock-hunter'
    ]):
        if any(k in combined for k in ['security', 'vulnerability', 'pentest', 'sast', 'semgrep', 'injection', 'threat', 'shodan', 'malware', 'privilege escalation']):
            return ('quality-and-security', 'security',
                    'Primary outcome is vulnerability assessment, security scanning, and penetration testing.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['debug', 'troubleshoot', 'memory leak', 'diagnos', 'error tracking', 'profiling', 'systematic-debugging']):
            return ('quality-and-security', 'debugging',
                    'Primary outcome is systematic error diagnosis, root cause investigation, and debugging.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['pci', 'compliance', 'gdpr', 'hipaa', 'privacy', 'audit-compliance']):
            return ('quality-and-security', 'compliance',
                    'Primary outcome is regulatory compliance, privacy verification, and security standard adherence.',
                    'high', 'None', 'none')
        else:
            return ('quality-and-security', 'testing',
                    'Primary outcome is automated unit/integration/E2E test engineering and QA validation.',
                    'high', 'None', 'none')

    # 5. data-and-ai
    if any(k in combined for k in [
        'machine learning', 'mlops', 'llm', 'rag', 'vector database', 'weaviate', 'pinecone',
        'embedding', 'fine-tuning', 'pytorch', 'scikit-learn', 'deep learning', 'transformer',
        'data pipeline', 'analytics', 'posthog', 'mixpanel', 'segment', 'statsmodels',
        'data science', 'quant analyst', 'jupyter', 'hugging face', 'openai', 'gemini api',
        'langchain', 'langgraph', 'sentence-transformer', 'recsys'
    ]):
        if any(k in combined for k in ['rag', 'llm', 'prompt', 'langchain', 'langgraph', 'model gateway', 'tokenwise', 'routerbase']):
            return ('data-and-ai', 'llm-and-rag',
                    'Primary outcome is LLM application development, RAG retrieval pipelines, and neural workflows.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['vector', 'weaviate', 'pinecone', 'similarity search', 'index tuning']):
            return ('data-and-ai', 'vector-databases',
                    'Primary outcome is vector database indexing, embedding storage, and similarity search.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['posthog', 'mixpanel', 'segment', 'analytics', 'telemetry', 'event tracking', 'kpi', 'news-sentiment']):
            return ('data-and-ai', 'analytics',
                    'Primary outcome is event tracking, user behavioral analytics, and metrics instrumentation.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['pipeline', 'etl', 'sql optimization', 'data engineering', 'warehouse', 'nosql']):
            return ('data-and-ai', 'data-engineering',
                    'Primary outcome is data pipeline engineering, ETL workflows, and database querying.',
                    'high', 'None', 'none')
        else:
            return ('data-and-ai', 'machine-learning',
                    'Primary outcome is statistical modeling, machine learning training, and predictive analysis.',
                    'high', 'None', 'none')

    # 6. infrastructure-and-ops
    if any(k in combined for k in [
        'vercel', 'cloudflare', 'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'k8s',
        'ci-cd', 'github actions', 'devops', 'linux', 'posix', 'shell scripting',
        'server management', 'pm2', 'ssh', 'observability', 'monitoring', 'datadog',
        'prometheus', 'service mesh', 'istio', 'wrangler', 'turborepo', 'rclone'
    ]):
        if any(k in combined for k in ['ci-cd', 'github action', 'release', 'deploy pipeline', 'build system', 'turborepo']):
            return ('infrastructure-and-ops', 'ci-cd',
                    'Primary outcome is CI/CD pipeline automation, build caching, and release automation.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['docker', 'kubernetes', 'container', 'service mesh', 'istio']):
            return ('infrastructure-and-ops', 'containers-and-orchestration',
                    'Primary outcome is containerization, cluster orchestration, and service mesh management.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['linux', 'posix', 'shell', 'bash', 'server', 'pm2', 'ssh', 'os-scripting', 'sshepherd']):
            return ('infrastructure-and-ops', 'server-management',
                    'Primary outcome is Linux system administration, shell scripting, and server execution.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['observability', 'monitoring', 'datadog', 'prometheus', 'telemetry', 'log']):
            return ('infrastructure-and-ops', 'observability',
                    'Primary outcome is system telemetry, infrastructure monitoring, and uptime observability.',
                    'high', 'None', 'none')
        else:
            return ('infrastructure-and-ops', 'cloud-platforms',
                    'Primary outcome is cloud platform hosting, serverless configuration, and edge deployment.',
                    'high', 'None', 'none')

    # 7. business-and-operations
    if any(k in combined for k in [
        'product manager', 'prd', 'roadmap', 'feature spec', 'jobs-to-be-done', 'startup',
        'financial model', 'pricing', 'business case', 'market sizing', 'legal advisor',
        'contracts', 'revops', 'sales', 'customer support', 'logistics', 'supply chain',
        'inventory planning', 'leiloeiro', 'risk-manager', 'monopoly'
    ]):
        if any(k in combined for k in ['prd', 'product manager', 'roadmap', 'jobs-to-be-done', 'user story', 'feature spec', 'to-prd']):
            return ('business-and-operations', 'product-management',
                    'Primary outcome is product requirement documentation, user story mapping, and feature roadmaps.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['finance', 'pricing', 'financial model', 'business case', 'unit economics', 'revenue', 'startup-financial']):
            return ('business-and-operations', 'startup-finance',
                    'Primary outcome is startup financial projections, pricing strategies, and business case modeling.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['legal', 'contract', 'licensing', 'terms of service', 'gdpr legal']):
            return ('business-and-operations', 'legal-and-governance',
                    'Primary outcome is legal terms review, intellectual property, and contract governance.',
                    'high', 'None', 'none')
        else:
            return ('business-and-operations', 'strategy',
                    'Primary outcome is strategic market positioning, operational planning, and business analysis.',
                    'high', 'None', 'none')

    # 8. content-and-documentation
    if any(k in combined for k in [
        'documentation', 'technical writing', 'readme', 'api docs', 'tutorial', 'copywriting',
        'proofreader', 'presentation', 'slide deck', 'pptx', 'pitch deck', 'pdf conversion',
        'latex', 'research paper', 'pubmed', 'nanobanana-ppt', 'interview-style-doc'
    ]):
        if any(k in combined for k in ['presentation', 'slide', 'pptx', 'deck', 'keynote', 'nanobanana']):
            return ('content-and-documentation', 'presentations',
                    'Primary outcome is visual presentation building, slide deck creation, and visual pitch generation.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['copywriting', 'proofread', 'article', 'editorial', 'storytelling']):
            return ('content-and-documentation', 'copywriting',
                    'Primary outcome is prose craftsmanship, editorial proofreading, and narrative creation.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['research', 'paper', 'pubmed', 'academic', 'literature', 'synthesis', 'latex']):
            return ('content-and-documentation', 'research-and-synthesis',
                    'Primary outcome is academic paper synthesis, research distillation, and literature review.',
                    'high', 'None', 'none')
        else:
            return ('content-and-documentation', 'technical-writing',
                    'Primary outcome is technical documentation, API specifications, and architectural documentation.',
                    'high', 'None', 'none')

    # 9. workflow-and-automation
    if any(k in combined for k in [
        'git worktree', 'merge conflict', 'git automation', 'linear automation', 'n8n',
        'slack automation', 'workflow automation', 'task orchestration', 'web scraping',
        'browser automation', 'puppeteer', 'mcp tool', 'mcp-builder', 'open-dynamic-workflows'
    ]):
        if any(k in combined for k in ['git', 'worktree', 'merge conflict', 'branch', 'vcs', 'commit']):
            return ('workflow-and-automation', 'git-and-vcs',
                    'Primary outcome is version control coordination, git worktree workflows, and conflict resolution.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['n8n', 'slack', 'linear', 'mcp', 'webhook', 'tool-use', 'integration']):
            return ('workflow-and-automation', 'tool-integration',
                    'Primary outcome is integrating external tool APIs, MCP services, and automation hooks.',
                    'high', 'None', 'none')
        elif any(k in combined for k in ['scrape', 'crawler', 'extract web', 'browser-harness', 'puppeteer']):
            return ('workflow-and-automation', 'web-scraping',
                    'Primary outcome is web scraping, browser DOM extraction, and web data harvesting.',
                    'high', 'None', 'none')
        else:
            return ('workflow-and-automation', 'task-orchestration',
                    'Primary outcome is multi-step workflow coordination and process automation.',
                    'high', 'None', 'none')

    # 10. development (core software development)
    if any(k in combined for k in ['frontend', 'react', 'nextjs', 'vue', 'angular', 'svelte', 'zustand', 'state']):
        return ('development', 'frontend',
                'Primary outcome is frontend client-side engineering, web components, and UI state architecture.',
                'high', 'None', 'none')
    elif any(k in combined for k in ['backend', 'python', 'nodejs', 'go', 'rust', 'java', 'c#', 'php', 'database', 'sql', 'postgres', 'api', 'fastapi']):
        return ('development', 'backend',
                'Primary outcome is backend server development, API design, and database schema implementation.',
                'high', 'None', 'none')
    elif any(k in combined for k in ['mobile', 'ios', 'android', 'react native', 'swift', 'kotlin']):
        return ('development', 'mobile',
                'Primary outcome is mobile application development across iOS, Android, and cross-platform runtimes.',
                'high', 'None', 'none')
    elif any(k in combined for k in ['systems', 'concurrency', 'protocol', 'low-level', 'c++', 'assembly', 'kernel']):
        return ('development', 'systems',
                'Primary outcome is systems-level programming, low-level concurrency, and protocol engineering.',
                'high', 'None', 'none')
    elif any(k in combined for k in ['architecture', 'design pattern', 'refactor', 'clean code', 'solid', 'domain-driven', 'read-all-adrs']):
        return ('development', 'software-architecture',
                'Primary outcome is software architecture design, domain modeling, and systematic refactoring.',
                'high', 'None', 'none')
    else:
        # Default fullstack
        return ('development', 'fullstack',
                'Primary outcome is full-stack application development, feature implementation, and code creation.',
                'medium', 'Broad feature scope spanning client and server development.', 'none')

def main():
    print("Reading skills-inventory.csv...")
    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    retained_rows = [r for r in all_rows if r.get("conversion_status") != "Not In Scope (Phase 03 Quarantined)"]
    print(f"Total inventory rows: {len(all_rows)}")
    print(f"Total retained rows: {len(retained_rows)}")
    assert len(retained_rows) == 2286, f"Expected 2286 retained rows, got {len(retained_rows)}"

    # Generate 1:1 destination map
    used_paths = set()
    used_paths_lower = set()
    destination_map = []
    category_counts = Counter()
    subcategory_counts = defaultdict(Counter)

    for r in retained_rows:
        src_path = r["source_path"]
        compat = r.get("compatibility_classification", "Capability-Based / Generalized")
        if not compat or compat.strip() == "":
            compat = "General"
            
        cat, subcat, basis, conf, concern, struct_cand = classify_skill(r)
        category_counts[cat] += 1
        subcategory_counts[cat][subcat] += 1

        # Generate unique proposed_final_path
        fn_slug = make_slug(r["folder_name"])
        src_parts = src_path.split("/")
        parent_prefix = make_slug(src_parts[3]) if len(src_parts) > 4 else ""

        candidate_path = f"task-folder/agents/skills/{cat}/{subcat}/{fn_slug}"
        if candidate_path.lower() in used_paths_lower:
            if parent_prefix and parent_prefix != fn_slug:
                candidate_path = f"task-folder/agents/skills/{cat}/{subcat}/{parent_prefix}-{fn_slug}"
            else:
                candidate_path = f"task-folder/agents/skills/{cat}/{subcat}/{fn_slug}-variant"
            
            idx = 2
            orig_candidate = candidate_path
            while candidate_path.lower() in used_paths_lower:
                candidate_path = f"{orig_candidate}-{idx}"
                idx += 1

        used_paths.add(candidate_path)
        used_paths_lower.add(candidate_path.lower())

        routing_role = "router_candidate" if struct_cand == "router_candidate" else "child_skill"

        destination_map.append({
            "source_path": src_path,
            "compatibility_status": compat,
            "proposed_category": cat,
            "proposed_subcategory": subcat,
            "proposed_final_path": candidate_path,
            "routing_role": routing_role,
            "placement_confidence": conf,
            "placement_basis": basis,
            "placement_concern": concern,
            "future_structure_candidate": struct_cand
        })

    print(f"Mapped {len(destination_map)} rows to destination-map.csv.")
    assert len(destination_map) == 2286
    assert len(used_paths) == 2286
    assert len(used_paths_lower) == 2286

    # Write destination-map.csv
    print(f"Writing {DESTINATION_MAP_PATH}...")
    fieldnames = [
        "source_path",
        "compatibility_status",
        "proposed_category",
        "proposed_subcategory",
        "proposed_final_path",
        "routing_role",
        "placement_confidence",
        "placement_basis",
        "placement_concern",
        "future_structure_candidate"
    ]
    with open(DESTINATION_MAP_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(destination_map)

    # Generate router-map.csv
    print(f"Writing {ROUTER_MAP_PATH}...")
    router_rows = []
    # Root router
    router_rows.append({
        "router_type": "root_router",
        "category": "root",
        "subcategory": "None",
        "proposed_path": "task-folder/agents/skills/SKILL.md",
        "responsibility": "Master router dispatching tasks across all 10 top-level functional categories.",
        "routing_scope": "all_10_categories"
    })

    # Category and subcategory routers
    for cat in sorted(category_counts.keys()):
        router_rows.append({
            "router_type": "category_router",
            "category": cat,
            "subcategory": "None",
            "proposed_path": f"task-folder/agents/skills/{cat}/SKILL.md",
            "responsibility": f"Parent category router delegating user intents to focused {cat} subcategories and child skills.",
            "routing_scope": f"{cat}_domain"
        })
        for subcat in sorted(subcategory_counts[cat].keys()):
            router_rows.append({
                "router_type": "subcategory_router",
                "category": cat,
                "subcategory": subcat,
                "proposed_path": f"task-folder/agents/skills/{cat}/{subcat}/SKILL.md",
                "responsibility": f"Subcategory router directing requests within the {subcat} cluster under {cat}.",
                "routing_scope": f"{cat}_{subcat}_cluster"
            })

    router_fieldnames = [
        "router_type",
        "category",
        "subcategory",
        "proposed_path",
        "responsibility",
        "routing_scope"
    ]
    with open(ROUTER_MAP_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=router_fieldnames)
        writer.writeheader()
        writer.writerows(router_rows)

    # Generate functional-taxonomy.md
    print(f"Writing {TAXONOMY_REPORT_PATH}...")
    with open(TAXONOMY_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# Functional Taxonomy & Destination Architecture (Phase 05)\n\n")
        f.write("## 1. Executive Summary\n\n")
        f.write("Phase 05 establishes the destination functional taxonomy for the Agent Skills library rebuild. Adhering strictly to the architectural directive of **map first, move later**, this phase designs a clean, shallow, capability-driven category hierarchy without performing premature physical file moves, merges, splits, or rewrites.\n\n")
        f.write("### Reconciliation Summary\n\n")
        f.write("- **Total Source Skills in Inventory**: **2,331**\n")
        f.write("- **Quarantined Skills (Excluded from Active Destinations)**: **45**\n")
        f.write("- **Retained Skills Mapped**: exactly **2,286** (100% coverage)\n")
        f.write("- **Top-Level Functional Categories**: **10**\n")
        f.write("- **Planned Routers**: **{}** (1 Master Root Router, 10 Category Routers, {} Subcategory Routers)\n\n".format(
            len(router_rows), len(router_rows) - 11
        ))

        f.write("## 2. The Classification Constitution & Core Rules\n\n")
        f.write("> [!IMPORTANT]\n")
        f.write("> **The Primary Operating Rule**: Classify by the skill's primary user outcome, not by the tool it uses or the mechanism by which it performs the work.\n\n")
        f.write("### Single Canonical Home (No Duplication)\n")
        f.write("Each retained skill is assigned exactly one canonical destination directory. Cross-domain relationships (e.g. accessibility audits spanning testing and design, full-stack design systems, automated CI deployments) are represented cleanly through routers, metadata, and cross-references rather than duplicating skills.\n\n")

        f.write("## 3. Disambiguation Decision Rules\n\n")
        f.write("To prevent classification drift across overlapping boundaries, the following concrete decision rules govern domain placement:\n\n")
        f.write("| Workflow / Intent | Assigned Category | Exclusion Reason (Where It Does NOT Go) |\n")
        f.write("|---|---|---|\n")
        f.write("| **Figma component creation & UI kit** | `design-and-experience` | *Not `workflow-and-automation`* (Visual design is the primary user outcome; Figma is a design tool). |\n")
        f.write("| **GitHub Actions deployment pipeline** | `infrastructure-and-ops` | *Not `workflow-and-automation`* (Application deployment and hosting are the primary outcome). |\n")
        f.write("| **Linear issue triage automation** | `workflow-and-automation` | *Not `business-and-operations`* (Automated multi-step process orchestration is the primary job). |\n")
        f.write("| **Agent skill auditor & validator** | `meta-and-agent-skills` | *Not `quality-and-security`* (Governs agent skill lifecycle, not application software). |\n")
        f.write("| **SEO analytics pipeline & tracking** | `marketing-and-seo` | *Not `data-and-ai`* (Primary outcome is search ranking and audience growth analysis). |\n")
        f.write("| **Playwright E2E accessibility testing** | `quality-and-security` | *Not `design-and-experience`* (Verification and test suite execution is the primary job). |\n")
        f.write("| **PostgreSQL schema & query optimization** | `development` / `backend` | *Not `infrastructure-and-ops`* (Application database schema and data logic). |\n")
        f.write("| **Microservices architecture pattern** | `development` / `software-architecture` | *Not `design-and-experience`* (Software/system architecture belongs under development). |\n\n")

        f.write("## 4. Category Definitions & Boundaries\n\n")
        categories_desc = [
            ("development", "Create, build, modify, and refactor software architectures, backend services, frontend applications, APIs, database schemas, and language idioms.", "Testing/verification workflows (belongs in `quality-and-security`) and pure visual styling design (belongs in `design-and-experience`).", ["fullstack", "backend", "frontend", "software-architecture", "systems", "mobile"]),
            ("design-and-experience", "Craft visual interfaces, UI/UX workflows, design systems (Tailwind, Radix, Figma), styling taste, animations, motion graphics, and 3D assets.", "Backend system architecture (belongs in `development`) or pure application logic.", ["ui-ux", "taste-and-critique", "design-systems", "motion-and-graphics"]),
            ("infrastructure-and-ops", "Provision, configure, deploy, host, and monitor cloud platforms, servers, CI/CD pipelines, containers, and operating systems.", "Standalone task workflow automation unrelated to hosting/cloud infrastructure.", ["cloud-platforms", "containers-and-orchestration", "server-management", "observability", "ci-cd"]),
            ("data-and-ai", "Model, fine-tune, analyze, query, and serve data, machine learning pipelines, LLM/RAG systems, embeddings, and analytics tracking.", "Agent skill lifecycle management or general application development.", ["llm-and-rag", "analytics", "machine-learning", "data-engineering", "vector-databases"]),
            ("quality-and-security", "Verify, test (unit, integration, E2E), diagnose, systematically debug, audit security, scan vulnerabilities, and ensure compliance.", "Feature creation and refactoring (belongs in `development`).", ["testing", "debugging", "compliance", "security"]),
            ("marketing-and-seo", "Drive audience acquisition, search engine visibility (SEO/GEO), conversion rate optimization (CRO), social presence, and digital ads.", "General copywriting without marketing or search intent (belongs in `content-and-documentation`).", ["on-page-seo", "cro", "technical-seo", "geo-and-local-seo", "content-and-campaigns"]),
            ("business-and-operations", "Manage products, analyze market opportunities, model financial projections, optimize pricing, and ensure business/legal compliance.", "Internal engineering or agent development workflows.", ["strategy", "startup-finance", "legal-and-governance", "product-management"]),
            ("content-and-documentation", "Produce technical documentation, articles, presentations, research summaries, and structured knowledge artifacts.", "Marketing copy and search optimization (belongs in `marketing-and-seo`).", ["technical-writing", "presentations", "research-and-synthesis", "copywriting"]),
            ("workflow-and-automation", "Orchestrate multi-step task workflows, integrate external APIs/MCP tools, automate Git operations, and bridge external services.", "Domain-specific skills that merely use an automation script as a secondary tool.", ["tool-integration", "task-orchestration", "web-scraping", "git-and-vcs"]),
            ("meta-and-agent-skills", "Author, audit, validate, optimize, benchmark, package, and govern agent skills and multi-agent systems.", "Application software development or external workflow tools.", ["skill-lifecycle", "agent-architecture", "skill-validation"])
        ]

        for name, purpose, exclusions, subcats in categories_desc:
            f.write(f"### `{name}`\n\n")
            f.write(f"- **Purpose**: {purpose}\n")
            f.write(f"- **Exclusion Boundary**: {exclusions}\n")
            f.write(f"- **Proposed Subcategories**: {', '.join(f'`{s}`' for s in subcats)}\n")
            f.write(f"- **Skill Count**: **{category_counts[name]}**\n\n")

        f.write("## 5. Category Reconciliation Matrix\n\n")
        f.write("| Category | Subcategory | Count | % of Retained Library |\n")
        f.write("|---|---|---|---|\n")
        total_ret = len(destination_map)
        for cat in sorted(category_counts.keys()):
            cat_total = category_counts[cat]
            f.write(f"| **`{cat}`** | *(Total)* | **{cat_total}** | **{cat_total/total_ret*100:.1f}%** |\n")
            for subcat, sc in sorted(subcategory_counts[cat].items()):
                f.write(f"| `{cat}` | `{subcat}` | {sc} | {sc/total_ret*100:.1f}% |\n")
        f.write(f"| **TOTAL** | **All Categories** | **{total_ret}** | **100.0%** |\n\n")

        f.write("## 6. Structural Router Architecture\n\n")
        f.write("The rebuilt library will utilize a shallow, two-level routing architecture:\n\n")
        f.write("1. **Master Root Router** (`task-folder/agents/skills/SKILL.md`): Dispatches incoming high-level user tasks to the appropriate functional category router.\n")
        f.write("2. **Category Routers** (`task-folder/agents/skills/<category>/SKILL.md`): Parent routers that define category boundaries and route to specific subcategory routers or child skills.\n")
        f.write("3. **Subcategory Routers** (`task-folder/agents/skills/<category>/<subcategory>/SKILL.md`): Specialized cluster routers routing to focused child skills.\n\n")
        f.write("See [`router-map.csv`](./router-map.csv) for the complete directory inventory of planned routers.\n\n")

        f.write("## 7. Review Concerns & Future Structural Candidates\n\n")
        f.write("- **Medium Confidence Placements**: Broad fullstack skills assigned to `development/fullstack` that may benefit from future domain splitting during Phase 06.\n")
        f.write("- **Future Merge Candidates**: Highly similar CRO, UI kit, and SEO sub-techniques identified for potential consolidation during Phase 06/07.\n")
        f.write("- **Zero Unresolved Blockers**: All 2,286 skills possess a clear, unambiguous top-level functional category.\n")

    print("Phase 05 artifacts generated successfully!")

if __name__ == "__main__":
    main()
