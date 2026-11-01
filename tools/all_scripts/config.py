"""
Configuration and constants for the reusable Agent Skills library pipeline.
"""

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# Repository Root (determined dynamically relative to this module)
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(MODULE_DIR)
REPO_ROOT = os.path.dirname(TOOLS_DIR)

# Core Directories
LIBRARY_DIR = os.path.join(REPO_ROOT, "library")
INTAKE_DIR = os.path.join(REPO_ROOT, "intake")
RUNTIME_DIR = str(Path.home() / ".agents" / "skills")
AUDIT_DIR = os.path.join(REPO_ROOT, "audit")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
CONFIG_DIR = os.path.join(REPO_ROOT, "config")
TARGETS_CONFIG_PATH = os.path.join(CONFIG_DIR, "runtime-targets.json")

# Runtime Publication Branch Name
RUNTIME_BRANCH = "runtime"

@dataclass
class RuntimeTarget:
    name: str
    path: str
    mode: str = "full"  # "full" | "subset"
    include: List[str] = field(default_factory=list)
    accept_external_intake: bool = False
    enabled: bool = True
    remote_url: str = ""

    @property
    def resolved_path(self) -> Path:
        return Path(self.path).expanduser().resolve()


def load_runtime_targets(config_path: Optional[str] = None) -> List[RuntimeTarget]:
    """Load and parse runtime targets from runtime-targets.json."""
    path = config_path or TARGETS_CONFIG_PATH
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    global_remote = data.get("remote_url", "https://github.com/REVREBEL/skills-library.git")
    targets = []
    for item in data.get("targets", []):
        targets.append(
            RuntimeTarget(
                name=item.get("name", ""),
                path=item.get("path", ""),
                mode=item.get("mode", "full"),
                include=item.get("include", []),
                accept_external_intake=item.get("accept_external_intake", False),
                enabled=item.get("enabled", True),
                remote_url=item.get("remote_url") or global_remote,
            )
        )
    return targets


# Audit & Metadata Files
MANIFEST_FILE = os.path.join(AUDIT_DIR, "runtime-manifest.json")
LEDGER_FILE = os.path.join(AUDIT_DIR, "change-ledger.jsonl")
VALIDATION_REPORT_FILE = os.path.join(AUDIT_DIR, "validation-report.md")

# Taxonomy: 10 Top-Level Categories
CATEGORIES = [
    "business-and-operations",
    "content-and-documentation",
    "data-and-ai",
    "design-and-experience",
    "development",
    "infrastructure-and-ops",
    "marketing-and-seo",
    "meta-and-agent-skills",
    "quality-and-security",
    "workflow-and-automation",
]

# Deep Categories (categories that have dedicated subcategory routers)
DEEP_CATEGORIES = {
    "development": [
        "backend",
        "frontend",
        "fullstack",
        "mobile",
        "software-architecture",
        "systems",
    ],
    "marketing-and-seo": [
        "content-and-campaigns",
        "cro",
        "geo-and-local-seo",
        "on-page-seo",
        "technical-seo",
    ],
    "design-and-experience": [
        "design-systems",
        "motion-and-graphics",
        "taste-and-critique",
        "ui-ux",
    ],
}

# Flat Categories (category router routes directly to leaves under subcategory headings)
FLAT_CATEGORIES = {
    "business-and-operations": [
        "legal-and-governance",
        "product-management",
        "startup-finance",
        "strategy",
    ],
    "content-and-documentation": [
        "copywriting",
        "presentations",
        "research-and-synthesis",
        "technical-writing",
    ],
    "data-and-ai": [
        "analytics",
        "data-engineering",
        "llm-and-rag",
        "machine-learning",
        "vector-databases",
    ],
    "infrastructure-and-ops": [
        "ci-cd",
        "cloud-platforms",
        "containers-and-orchestration",
        "observability",
        "server-management",
    ],
    "meta-and-agent-skills": [
        "agent-architecture",
        "skill-lifecycle",
        "skill-validation",
    ],
    "quality-and-security": [
        "compliance",
        "debugging",
        "security",
        "testing",
    ],
    "workflow-and-automation": [
        "git-and-vcs",
        "task-orchestration",
        "tool-integration",
        "web-scraping",
    ],
}

# All 44 Subcategories mapped by category
ALL_SUBCATEGORIES = {**DEEP_CATEGORIES, **FLAT_CATEGORIES}

# Operational System Packages (canonical in library/, symlinked into runtime)
OPERATIONAL_SYSTEM_PACKAGES = {
    "github-operations",
    "skills-create-manage-update",
}

# Protected Runtime Entries in ~/.agents/skills (never overwrite with regular skill sync)
PROTECTED_RUNTIME_ENTRIES = {
    "SKILL.md",
    "github-operations",
    "skills-create-manage-update",
    ".DS_Store",
    ".git",
}

# Regex Patterns for Verification & Safety (aligned with validated Phase 11/12 Gates)
TRIGGER_CONTRACT_PATTERN = re.compile(
    r"\b(use when(?:ever)?|activate when|triggers?|load alongside|when (?:you need|you want|working with|authoring|building|creating|debugging|developing|analyzing|generating|reviewing|managing|configuring|deploying|optimizing|testing|designing))\b",
    re.IGNORECASE,
)

WORKSTATION_PATH_PATTERNS = [
    re.compile(r"(?:^|[\s\"'<`])(/Users/(?!username|name|user|[a-zA-Z0-9_\-.]+\.\.\.)[a-zA-Z0-9_-]+)"),
    re.compile(r"(?:^|[\s\"'<`])(/home/(?!username|user|runner|agent|vscode|opuser|[a-zA-Z0-9_\-.]+\.\.\.)[a-zA-Z0-9_-]+)"),
    re.compile(r"(?:^|[\s\"'<`])([a-zA-Z]:[/\\]Users[/\\](?!username|YourName|user|\.\.\.)[a-zA-Z0-9_-]+)"),
    re.compile(r"(?:^|[\s\"'<`])(\\\\(?!(?:server|cloud|attacker-server\.com)\b)[a-zA-Z0-9_\.\-]+(?:\\[a-zA-Z0-9_\.\-]+)+)"),
    re.compile(r"(?:^|[\s\"'<`])(/(?:mnt|media|Volumes)/(?:Users|home|[a-zA-Z0-9_\.\-]+\s+HD/[Uu]sers)/[a-zA-Z0-9_\.\-]+)"),
]

PROVIDER_COUPLING_PATTERNS = [
    re.compile(r"\bClaude\b", re.IGNORECASE),
    re.compile(r"\bAnthropic\b", re.IGNORECASE),
]

DESTRUCTIVE_COMMAND_PATTERNS = [
    re.compile(r"\brm\s+-[rf]{1,2}\b"),
    re.compile(r"\bDROP\s+(?:TABLE|DATABASE|SCHEMA|VIEW)\b", re.IGNORECASE),
    re.compile(r"\bTRUNCATE\s+(?:TABLE)?\b", re.IGNORECASE),
    re.compile(r"\bgit\s+push\s+.*--force\b"),
    re.compile(r"\bmkfs\b"),
    re.compile(r"\bdd\s+if="),
]

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----\s*[A-Za-z0-9+/]{20,}"),
    re.compile(r"\bghp_[0-9a-zA-Z]{36}\b"),
    re.compile(r"\bgithub_pat_[0-9a-zA-Z_]{82}\b"),
    re.compile(r"\bsk-[0-9a-zA-Z]{32,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
]


def get_all_routers(library_dir: str = LIBRARY_DIR) -> List[str]:
    """Return all 26 router file paths in the canonical library."""
    root_router = os.path.join(library_dir, "SKILL.md")
    cat_routers = [os.path.join(library_dir, c, "SKILL.md") for c in CATEGORIES]
    subcat_routers = [
        os.path.join(library_dir, c, sc, "SKILL.md")
        for c, scs in DEEP_CATEGORIES.items()
        for sc in scs
    ]
    return [root_router] + cat_routers + subcat_routers
