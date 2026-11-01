"""
Runtime Manifest Management.
Maintains audit/runtime-manifest.json mapping flat runtime names in .agents/skills
to canonical skill paths in library/, resolving name collisions deterministically.
"""

import json
import os
from collections import Counter
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from .config import (
    AUDIT_DIR,
    DEEP_CATEGORIES,
    FLAT_CATEGORIES,
    LIBRARY_DIR,
    MANIFEST_FILE,
    REPO_ROOT,
)


def get_current_iso_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class RuntimeManifest:
    """Manages the mapping between runtime symlink names and canonical skills."""

    def __init__(self, manifest_path: str = MANIFEST_FILE):
        self.manifest_path = manifest_path
        self.version = "1.0.0"
        self.generated_at = ""
        self.skills: Dict[str, dict] = {}
        if os.path.exists(self.manifest_path):
            self.load()

    def load(self) -> None:
        """Load manifest from JSON file."""
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.version = data.get("version", "1.0.0")
        self.generated_at = data.get("generated_at", "")
        self.skills = data.get("skills", {})

    def save(self, output_path: Optional[str] = None) -> None:
        """Save manifest to JSON file."""
        dest = output_path or self.manifest_path
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        data = {
            "version": self.version,
            "generated_at": get_current_iso_timestamp(),
            "total_managed_skills": len(self.skills),
            "skills": dict(sorted(self.skills.items())),
        }
        with open(dest, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_skill(
        self,
        runtime_name: str,
        canonical_name: str,
        canonical_path: str,
        functional_parent: str,
        source: str = "intake",
        managed: bool = True,
    ) -> None:
        """Add or update a skill in the manifest."""
        now = get_current_iso_timestamp()
        existing = self.skills.get(runtime_name)
        installed_at = existing.get("installed_at", now) if existing else now
        self.skills[runtime_name] = {
            "runtime_name": runtime_name,
            "canonical_name": canonical_name,
            "canonical_path": canonical_path.replace(os.sep, "/"),
            "functional_parent": functional_parent.replace(os.sep, "/"),
            "source": source,
            "managed": managed,
            "installed_at": installed_at,
            "last_validated": now,
        }

    def remove_skill(self, runtime_name: str) -> bool:
        """Remove a skill from the manifest."""
        if runtime_name in self.skills:
            del self.skills[runtime_name]
            return True
        return False

    def get_skill(self, runtime_name: str) -> Optional[dict]:
        return self.skills.get(runtime_name)

    def find_by_canonical_path(self, canonical_path: str) -> Optional[dict]:
        norm = canonical_path.replace(os.sep, "/").strip("/")
        for s in self.skills.values():
            if s["canonical_path"].strip("/") == norm:
                return s
        return None

    def find_by_canonical_name(self, name: str) -> List[dict]:
        return [s for s in self.skills.values() if s["canonical_name"] == name]

    @classmethod
    def build_from_library(
        cls,
        library_dir: str = LIBRARY_DIR,
        manifest_path: str = MANIFEST_FILE,
    ) -> "RuntimeManifest":
        """
        Builds a complete runtime manifest by traversing the 26 routers in library/.
        Resolves flat-runtime-name collisions deterministically.
        """
        manifest = cls(manifest_path=manifest_path)
        manifest.skills.clear()

        # Step 1: Collect all canonical leaf skills from the router hierarchy
        leaf_records: List[dict] = []
        # Discover all routers
        root_router = os.path.join(library_dir, "SKILL.md")
        category_routers: List[str] = []
        subcategory_routers: List[str] = []

        for cat, subcats in DEEP_CATEGORIES.items():
            category_routers.append(os.path.join(library_dir, cat, "SKILL.md"))
            for sc in subcats:
                subcategory_routers.append(os.path.join(library_dir, cat, sc, "SKILL.md"))
        for cat in FLAT_CATEGORIES.keys():
            category_routers.append(os.path.join(library_dir, cat, "SKILL.md"))

        all_routers = [root_router] + category_routers + subcategory_routers
        norm_routers = {os.path.normpath(r) for r in all_routers}

        import re
        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

        seen_leaf_paths = set()

        for r_path in all_routers:
            r_dir = os.path.dirname(r_path)
            rel_router = os.path.relpath(r_path, REPO_ROOT).replace(os.sep, "/")
            with open(r_path, "r", encoding="utf-8") as f:
                content = f.read()

            for m in link_pattern.finditer(content):
                target = m.group(2).split("#")[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                abs_target = os.path.normpath(os.path.join(r_dir, target))
                if os.path.basename(abs_target) == "SKILL.md" and abs_target not in norm_routers:
                    skill_dir = os.path.dirname(abs_target)
                    if skill_dir in seen_leaf_paths:
                        continue
                    seen_leaf_paths.add(skill_dir)

                    canonical_path = os.path.relpath(skill_dir, REPO_ROOT).replace(os.sep, "/")
                    # Extract category and subcategory from path
                    rel_to_lib = os.path.relpath(skill_dir, library_dir).split(os.sep)
                    category = rel_to_lib[0]
                    subcategory = rel_to_lib[1] if len(rel_to_lib) > 2 else "general"
                    folder_name = rel_to_lib[-1]

                    # Parse frontmatter name if available
                    name = folder_name
                    try:
                        with open(abs_target, "r", encoding="utf-8") as sf:
                            for line in sf:
                                if line.startswith("name:"):
                                    name = line.split(":", 1)[1].strip().strip("\"'")
                                    break
                    except Exception:
                        pass

                    leaf_records.append({
                        "canonical_name": name,
                        "folder_name": folder_name,
                        "category": category,
                        "subcategory": subcategory,
                        "canonical_path": canonical_path,
                        "functional_parent": rel_router,
                    })

        # Step 2: Deterministic runtime name assignment & collision resolution
        name_counts = Counter(r["canonical_name"] for r in leaf_records)
        used_runtime_names = set()

        for r in leaf_records:
            cname = r["canonical_name"]
            cat = r["category"]
            subcat = r["subcategory"]

            if name_counts[cname] == 1 and cname not in used_runtime_names:
                runtime_name = cname
            else:
                # Collision resolution: prefix with category
                candidate = f"{cat}-{cname}"
                if candidate not in used_runtime_names:
                    runtime_name = candidate
                else:
                    # Still colliding: prefix with category-subcategory
                    candidate = f"{cat}-{subcat}-{cname}"
                    runtime_name = candidate

            used_runtime_names.add(runtime_name)
            manifest.add_skill(
                runtime_name=runtime_name,
                canonical_name=cname,
                canonical_path=r["canonical_path"],
                functional_parent=r["functional_parent"],
                source="canonical_rebuild",
                managed=True,
            )

        manifest.save()
        return manifest
