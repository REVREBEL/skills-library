#!/usr/bin/env python3
"""
Catalog-Wide Semantic Role Census & Architecture Stress-Test Tool
Linear Issues: REV-126, REV-150

Performs authoritative census across all 2,087 skills in the library,
evaluating them against the canonical work-order semantic object model:
  - independent_capability
  - family_primitive
  - workflow
  - overlay
  - adapter
  - reference_or_support_candidate
  - alias_candidate
  - manual_review

Outputs:
  - audit/taxonomy-census/semantic-role-census.csv
  - audit/taxonomy-census/semantic-role-census.json
  - audit/taxonomy-census/family-candidate-register.md
  - audit/taxonomy-census/catch-all-bin-analysis.md
  - audit/taxonomy-census/architecture-stress-test-report.md
  - audit/taxonomy-census/manual-review-outliers.md
  - audit/taxonomy-census/census-validation-report.md
"""

import sys
from pathlib import Path

# Ensure tools directory is in sys.path for direct or module execution
_tools_dir = Path(__file__).resolve().parent
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

try:
    from tools import validate_semantic_census
except ImportError:
    import validate_semantic_census

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Regenerate the semantic role census")
    parser.add_argument(
        "--regenerate-skil11",
        action="store_true",
        help="Also rebuild audit/zero-index/SKIL-11/. Off by default: that audit is immutable evidence.",
    )
    args = parser.parse_args()
    validate_semantic_census.main(regenerate_skil11=args.regenerate_skil11)

