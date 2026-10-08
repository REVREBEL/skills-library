"""
Permanent Change Ledger Management.
Records every add, update, remove, and sync operation to audit/change-ledger.jsonl
ensuring full traceability and provenance.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .config import AUDIT_DIR, LEDGER_FILE


def get_current_iso_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ChangeLedger:
    """Manages appending and querying audit records in audit/change-ledger.jsonl."""

    def __init__(self, ledger_path: str = LEDGER_FILE):
        self.ledger_path = ledger_path
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        if not os.path.exists(self.ledger_path):
            with open(self.ledger_path, "w", encoding="utf-8") as f:
                pass  # create empty file

    def record_change(
        self,
        operation: str,
        source: str,
        source_path: str,
        original_name: str,
        canonical_name: str,
        runtime_name: str,
        decision: str,
        category: str,
        subcategory: str,
        canonical_path: str,
        functional_parent: str,
        overlap_candidates: Optional[List[str]] = None,
        validation_status: str = "PASS",
        pilot_status: str = "PASS",
        commit: Optional[str] = None,
        pr: Optional[str] = None,
        merge_sha: Optional[str] = None,
    ) -> dict:
        """Append a new change record to the ledger."""
        record = {
            "change_id": f"CHG-{uuid.uuid4().hex[:12].upper()}",
            "timestamp": get_current_iso_timestamp(),
            "operation": operation,
            "source": source,
            "source_path": source_path.replace(os.sep, "/") if source_path else "",
            "original_name": original_name,
            "canonical_name": canonical_name,
            "runtime_name": runtime_name,
            "decision": decision,
            "category": category,
            "subcategory": subcategory,
            "canonical_path": canonical_path.replace(os.sep, "/") if canonical_path else "",
            "functional_parent": functional_parent.replace(os.sep, "/") if functional_parent else "",
            "overlap_candidates": overlap_candidates or [],
            "validation_status": validation_status,
            "pilot_status": pilot_status,
            "commit": commit or "",
            "pr": pr or "",
            "merge_sha": merge_sha or "",
        }

        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        return record

    def list_changes(self) -> List[dict]:
        """Read all change records from the ledger."""
        records = []
        if not os.path.exists(self.ledger_path):
            return records
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return records

    def get_history(self, limit: Optional[int] = None) -> List[dict]:
        """Return change records in reverse chronological order."""
        changes = self.list_changes()
        changes.reverse()
        if limit:
            return changes[:limit]
        return changes

