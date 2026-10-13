#!/usr/bin/env python3
"""
Catalog-Wide Semantic Role Census & Architecture Stress-Test Tool
Linear Issues: REV-126, REV-150

Performs authoritative census across all 2,133 skills in the library,
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

# Run the validated engine from validate_semantic_census
import validate_semantic_census

if __name__ == "__main__":
    validate_semantic_census.main()
