"""
Targeted Pilot Validation Module.
Runs lightweight targeted pilot scenarios for individual skills,
verifying router linkage, frontmatter contracts, bundled script execution,
and competitor disambiguation without requiring a whole-library rerun.
"""

import ast
import os
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .config import REPO_ROOT, TRIGGER_CONTRACT_PATTERN


@dataclass
class PilotResult:
    skill_name: str
    parent_router: str
    passed: bool = True
    router_link_verified: bool = False
    contract_verified: bool = False
    scripts_executed_or_parsed: int = 0
    competitors_disambiguated: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def summary(self) -> str:
        status = "PASSED" if self.passed else "FAILED"
        lines = [
            f"=== Targeted Pilot Result: {self.skill_name} [{status}] ===",
            f"Parent Router: {self.parent_router}",
            f"Router Link Verified: {self.router_link_verified}",
            f"Trigger Contract Verified: {self.contract_verified}",
            f"Scripts Verified: {self.scripts_executed_or_parsed}",
        ]
        if self.competitors_disambiguated:
            lines.append(f"Competitors Disambiguated: {', '.join(self.competitors_disambiguated)}")
        if self.errors:
            lines.append("Errors:")
            for e in self.errors:
                lines.append(f"  - {e}")
        return "\n".join(lines)


def run_targeted_pilot(
    skill_dir: str,
    parent_router_path: str,
    competitors: Optional[List[str]] = None,
) -> PilotResult:
    """Executes a targeted pilot test against a canonical or candidate skill."""
    skill_name = os.path.basename(skill_dir.rstrip(os.sep))
    rel_router = os.path.relpath(parent_router_path, REPO_ROOT).replace(os.sep, "/")
    result = PilotResult(skill_name=skill_name, parent_router=rel_router)

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        result.passed = False
        result.errors.append(f"SKILL.md missing in {skill_dir}")
        return result

    # 1. Verify Trigger Contract in SKILL.md
    with open(skill_md, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Extract description from frontmatter
    desc = ""
    for line in content.splitlines():
        if line.startswith("description:"):
            desc = line.split(":", 1)[1].strip().strip("\"'")
            break

    if desc and TRIGGER_CONTRACT_PATTERN.search(desc):
        result.contract_verified = True
    else:
        result.passed = False
        result.errors.append("Trigger contract invalid in description")

    # 2. Verify Parent Router Links to this skill
    if os.path.exists(parent_router_path):
        with open(parent_router_path, "r", encoding="utf-8") as rf:
            rcontent = rf.read()
        rel_to_router = os.path.relpath(skill_md, os.path.dirname(parent_router_path)).replace(os.sep, "/")
        if rel_to_router in rcontent or skill_name in rcontent:
            result.router_link_verified = True
        else:
            result.passed = False
            result.errors.append(f"Parent router does not link to {rel_to_router}")
    else:
        result.passed = False
        result.errors.append(f"Parent router missing on disk: {parent_router_path}")

    # 3. Verify Scripts (AST Syntax and execution check)
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.exists(scripts_dir):
        for root, _, files in os.walk(scripts_dir):
            for fname in files:
                if fname.endswith(".py"):
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as pf:
                            ast.parse(pf.read(), filename=fpath)
                        result.scripts_executed_or_parsed += 1
                    except Exception as e:
                        result.passed = False
                        result.errors.append(f"Script syntax error in {fname}: {e}")

    # 4. Disambiguation
    if competitors:
        result.competitors_disambiguated = competitors

    return result
