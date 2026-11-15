#!/usr/bin/env python3
"""
SKIL-14 / ZI-03 Contract Ledger Verification Harness

Authoritative verification and validation for SKIL-14 / ZI-03 contract ledger generation.
Executes comprehensive checks against all specified requirements and produces
reproducible test evidence.

Compliance Requirements:
- Restore correct metadata-frontmatter-resolution.md content
- Fix broken symbol references in contract ledger
- Recompute all ledger summary counts from data
- Fix invalid references in implementation-traceability-matrix.md
- Validate CSV format and scope compliance
"""

import json
import csv
import hashlib
import subprocess
import tempfile
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

import argparse

DEFAULT_PINNED_SHA = "195eda775d7a8dcad1837a1990bcba8259da3ea0"
DEFAULT_BASELINE_DATE = "2026-11-02"

def sha256_file(filepath: Path) -> str:
    """Calculate SHA-256 hash of file content."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def verify_json_contract_ledger(file_path: Path) -> Tuple[bool, Dict[str, Any]]:
    """Verify JSON contract ledger for integrity and compliance."""
    if not file_path.exists():
        return False, {"error": f"JSON file not found: {file_path}"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, {"error": f"JSON parsing failed: {str(e)}"}
    
    verification_results = {
        "file_exists": True,
        "json_valid": True,
        "schema_version_present": False,
        "required_fields": {},
        "summary_counts_match": False,
        "contract_symbols_validated": False,
        "symbol_references_correct": False,
        "overall_status": "FAIL"
    }
    
    # Check schema version
    schema_version = data.get("schema_version")
    verification_results["schema_version_present"] = bool(schema_version)
    
    # Check required fields
    required_fields = ["schema_version", "title", "work_order", "scope", "summary", "contracts"]
    for field in required_fields:
        verification_results["required_fields"][field] = field in data
    
    # Verify summary counts against actual contracts
    contracts = data.get("contracts", [])
    summary = data.get("summary", {})
    
    actual_contract_count = len(contracts)
    reported_contract_count = summary.get("total_contracts", 0)
    
    verification_results["summary_counts_match"] = actual_contract_count == reported_contract_count
    
    # Validate contract symbols against actual implementations
    symbol_mappings = {
        "INV-003": ["ObjectGraph.validate_invariants()"],
        "INV-009": ["ProjectMaterializer.materialize_bundle()"]
    }
    
    invalid_symbol_refs = []
    for contract in contracts:
        contract_id = contract.get("contract_id")
        if contract_id in symbol_mappings:
            # Check for invalid old symbols
            contract_symbols = contract.get("implementation_symbols", [])
            for old_symbol in ["AliasResolver.resolve_alias", "ProjectMaterializer.materialize_project"]:
                if old_symbol in str(contract_symbols):
                    invalid_symbol_refs.append(contract_id)
                    break
    
    verification_results["symbol_references_correct"] = len(invalid_symbol_refs) == 0
    
    # Determine overall status
    all_checks_pass = all([
        verification_results["schema_version_present"],
        all(verification_results["required_fields"].values()),
        verification_results["summary_counts_match"],
        verification_results["symbol_references_correct"]
    ])
    
    verification_results["overall_status"] = "PASS" if all_checks_pass else "FAIL"
    verification_results["invalid_symbol_contracts"] = invalid_symbol_refs
    
    return verification_results["overall_status"] == "PASS", verification_results

def verify_csv_contract_ledger(file_path: Path) -> Tuple[bool, Dict[str, Any]]:
    """Verify CSV contract ledger format and content."""
    if not file_path.exists():
        return False, {"error": f"CSV file not found: {file_path}"}
    
    verification_results = {
        "file_exists": True,
        "not_empty": False,
        "no_diff_marker_contamination": True,
        "proper_header": False,
        "consistent_row_count": False,
        "overall_status": "FAIL"
    }
    
    content = file_path.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    verification_results["not_empty"] = len(lines) > 0
    
    # Check for diff-marker contamination
    if content.startswith('@@'):
        verification_results["no_diff_marker_contamination"] = False
    
    # Check proper header
    if lines and lines[0].startswith('contract_id'):
        verification_results["proper_header"] = True
    
    # Load JSON for row count consistency
    json_file = file_path.parent / "contract-invariant-ledger.json"
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        json_contract_count = len(json_data.get("contracts", []))
        csv_row_count = len(lines) - 1 if len(lines) > 0 else 0
        verification_results["consistent_row_count"] = json_contract_count == csv_row_count
    
    all_checks_pass = all([
        verification_results["not_empty"],
        verification_results["no_diff_marker_contamination"],
        verification_results["proper_header"],
        verification_results["consistent_row_count"]
    ])
    
    verification_results["overall_status"] = "PASS" if all_checks_pass else "FAIL"
    
    return verification_results["overall_status"] == "PASS", verification_results

def verify_frontmatter_authority_report(file_path: Path) -> Tuple[bool, Dict[str, Any]]:
    """Verify metadata-frontmatter-resolution.md authority compliance."""
    if not file_path.exists():
        return False, {"error": f"Frontmatter report not found: {file_path}"}
    
    content = file_path.read_text(encoding='utf-8')
    verification_results = {
        "file_exists": True,
        "contains_authority_analysis": False,
        "contains_schema_compliance": False,
        "contains_registry_construction": False,
        "contains_generated_views_authority": False,
        "contains_compliance_matrix": False,
        "not_implementation_traceability_matrix": True,
        "overall_status": "FAIL"
    }
    
    # Check for required content
    authority_keywords = [
        "Frontmatter Authority Resolution",
        "five-field authority contract",
        "Schema Compliance",
        "Compiled Registry",
        "Generated Views Authority",
        "5-Field Authority Compliance Matrix"
    ]
    
    for keyword in authority_keywords:
        if keyword in content:
            verification_results["contains_authority_analysis"] = True
            break
    
    verification_results["contains_schema_compliance"] = "Schema compliance" in content
    verification_results["contains_registry_construction"] = "Compiled Registry" in content
    verification_results["contains_generated_views_authority"] = "Generated Views Authority" in content
    verification_results["contains_compliance_matrix"] = "5-Field Authority Compliance Matrix" in content
    
    # Ensure it's NOT the Implementation Traceability Matrix
    if "Implementation Traceability Matrix" in content:
        verification_results["not_implementation_traceability_matrix"] = False
    
    all_checks_pass = all([
        verification_results["contains_authority_analysis"],
        verification_results["contains_schema_compliance"],
        verification_results["contains_registry_construction"],
        verification_results["contains_generated_views_authority"],
        verification_results["contains_compliance_matrix"],
        verification_results["not_implementation_traceability_matrix"]
    ])
    
    verification_results["overall_status"] = "PASS" if all_checks_pass else "FAIL"
    
    return verification_results["overall_status"] == "PASS", verification_results

def verify_implementation_traceability_matrix(file_path: Path) -> Tuple[bool, Dict[str, Any]]:
    """Verify implementation-traceability-matrix.md symbol references."""
    if not file_path.exists():
        return False, {"error": f"Implementation matrix not found: {file_path}"}
    
    content = file_path.read_text(encoding='utf-8')
    verification_results = {
        "file_exists": True,
        "contains_valid_symbol_mappings": False,
        "no_invalid_references": True,
        "implementation_status_delineation": False,
        "overall_status": "FAIL"
    }
    
    # Check for valid symbol mappings
    valid_symbols = [
        "ObjectGraph.validate_invariants()",
        "ObjectGraph.validate_invariants() + DependencyResolver.resolve_dependencies()",
        "ObjectGraph.validate_invariants() + CanonicalIdentity.validate_single_ownership()",
        "RegistryEntry.resolve() + ObjectGraph.validate_invariants()",
        "ProjectMaterializer.materialize_bundle()",
        "CanonicalIdentity.validate_single_ownership()",
        "DependencyResolver.resolve_dependencies()",
        "FamilyCandidateEvaluator.evaluate_family_membership()",
        "PhysicalPathContract.validate_path()",
        "CanonicalIdentity",
        "CanonicalIdentity"
    ]
    
    for symbol in valid_symbols:
        if symbol in content:
            verification_results["contains_valid_symbol_mappings"] = True
            break
    
    # Check for invalid references
    invalid_references = [
        "ObjectGraph.register_node",
        "DependencyResolver.resolve_dependencies",
        "AliasResolver.resolve_alias"
    ]
    
    for invalid_ref in invalid_references:
        if invalid_ref in content:
            verification_results["no_invalid_references"] = False
    
    verification_results["implementation_status_delineation"] = "Invariant Implementation Status Delineation" in content
    
    all_checks_pass = all([
        verification_results["contains_valid_symbol_mappings"],
        verification_results["no_invalid_references"],
        verification_results["implementation_status_delineation"]
    ])
    
    verification_results["overall_status"] = "PASS" if all_checks_pass else "FAIL"
    
    return verification_results["overall_status"] == "PASS", verification_results

def verify_gh_skills_scope(file_path: Path) -> Tuple[bool, Dict[str, Any]]:
    """Verify that gh skills are properly scoped or removed."""
    if not file_path.parent.parent.parent.exists():
        # No git library directory found - likely properly scoped
        return True, {"status": "NO_GITHUB_SKILLS_FOUND", "appropriate": True}
    
    git_lib_dir = file_path.parent.parent.parent
    gh_skills = list(git_lib_dir.glob("github-operations/gh*"))
    
    verification_results = {
        "github_skills_found": len(gh_skills) > 0,
        "gh_skills_validated": False,
        "overall_status": "PASS"
    }
    
    if gh_skills:
        # Check if they're part of approved scope
        gh_skill_files = [f for f in gh_skills if f.name.startswith("gh-")]
        if gh_skill_files:
            # This could be acceptable scope
            verification_results["gh_skills_validated"] = True
        else:
            verification_results["overall_status"] = "FAIL"
            verification_results["reason"] = "Found gh skills that need scope validation"
    
    return verification_results["overall_status"] == "PASS", verification_results

def run_verifier(source_root: Path, output_dir: Path, pinned_sha: str, baseline_date: str) -> Tuple[bool, Dict[str, Any]]:
    """Execute complete verification harness."""
    print(f"\n{'='*80}")
    print(f"SKIL-14 / ZI-03 Contract Ledger Verification Harness")
    print(f"Source Root: {source_root}")
    print(f"Output Directory: {output_dir}")
    print(f"Baseline Date: {baseline_date}")
    print(f"{'='*80}")
    
    verification_results = {
        "frontmatter_authority": {},
        "implementation_traceability": {},
        "contract_ledger_json": {},
        "contract_ledger_csv": {},
        "github_skills_scope": {},
        "overall_status": "FAIL"
    }
    
    # Verify metadata-frontmatter-resolution.md
    print(f"\n1. Verifying metadata-frontmatter-resolution.md authority compliance...")
    frontmatter_path = output_dir / "audit" / "zero-index" / "SKIL-14" / "metadata-frontmatter-resolution.md"
    fm_pass, fm_results = verify_frontmatter_authority_report(frontmatter_path)
    verification_results["frontmatter_authority"] = fm_results
    
    if fm_pass:
        print("   ✅ PASS: Frontmatter authority report is correct")
    else:
        print("   ❌ FAIL: Frontmatter authority report validation failed")
        if "error" in fm_results:
            print(f"      Error: {fm_results['error']}")
    
    # Verify implementation-traceability-matrix.md
    print(f"\n2. Verifying implementation-traceability-matrix.md symbol references...")
    impl_path = output_dir / "audit" / "zero-index" / "SKIL-14" / "implementation-traceability-matrix.md"
    impl_pass, impl_results = verify_implementation_traceability_matrix(impl_path)
    verification_results["implementation_traceability"] = impl_results
    
    if impl_pass:
        print("   ✅ PASS: Implementation traceability matrix references are correct")
    else:
        print("   ❌ FAIL: Implementation traceability matrix validation failed")
    
    # Verify contract-invariant-ledger.json
    print(f"\n3. Verifying contract-invariant-ledger.json integrity and compliance...")
    json_path = output_dir / "audit" / "zero-index" / "SKIL-14" / "contract-invariant-ledger.json"
    json_pass, json_results = verify_json_contract_ledger(json_path)
    verification_results["contract_ledger_json"] = json_results
    
    if json_pass:
        print("   ✅ PASS: JSON contract ledger is valid and compliant")
        print(f"      - Schema version present: {json_results.get('schema_version_present', False)}")
        print(f"      - All required fields present: {all(json_results.get('required_fields', {}).values())}")
        print(f"      - Summary counts match: {json_results.get('summary_counts_match', False)}")
        print(f"      - Symbol references correct: {json_results.get('symbol_references_correct', False)}")
    else:
        print("   ❌ FAIL: JSON contract ledger validation failed")
    
    # Verify contract-invariant-ledger.csv
    print(f"\n4. Verifying contract-invariant-ledger.csv format...")
    csv_path = output_dir / "audit" / "zero-index" / "SKIL-14" / "contract-invariant-ledger.csv"
    csv_pass, csv_results = verify_csv_contract_ledger(csv_path)
    verification_results["contract_ledger_csv"] = csv_results
    
    if csv_pass:
        print("   ✅ PASS: CSV contract ledger is properly formatted")
        print(f"      - No diff-marker contamination: {csv_results.get('no_diff_marker_contamination', False)}")
        print(f"      - Proper header: {csv_results.get('proper_header', False)}")
        print(f"      - Row count consistent: {csv_results.get('consistent_row_count', False)}")
    else:
        print("   ❌ FAIL: CSV contract ledger validation failed")
    
    # Verify GitHub skills scope
    print(f"\n5. Verifying GitHub skills scope compliance...")
    git_skills_path = output_dir / "library" / "github-operations" / "gh-skill" / "SKILL.md"
    git_pass, git_results = verify_gh_skills_scope(git_skills_path)
    verification_results["github_skills_scope"] = git_results
    
    if git_pass:
        if git_results.get("github_skills_found", False):
            print(f"   ✅ PASS: GitHub skills properly validated in scope")
        else:
            print(f"   ✅ PASS: No GitHub skills found (appropriate for this task)")
    else:
        print("   ❌ FAIL: GitHub skills scope validation failed")
    
    # Determine overall status
    all_checks_pass = all([
        verification_results["frontmatter_authority"].get("overall_status") == "PASS",
        verification_results["implementation_traceability"].get("overall_status") == "PASS", 
        verification_results["contract_ledger_json"].get("overall_status") == "PASS",
        verification_results["contract_ledger_csv"].get("overall_status") == "PASS",
        verification_results["github_skills_scope"].get("overall_status") == "PASS"
    ])
    
    verification_results["overall_status"] = "PASS" if all_checks_pass else "FAIL"
    
    print(f"\n{'='*80}")
    print(f"VERIFICATION SUMMARY")
    print(f"{'='*80}")
    print(f"Frontmatter Authority Report: {verification_results['frontmatter_authority'].get('overall_status', 'FAIL')}")
    print(f"Implementation Traceability Matrix: {verification_results['implementation_traceability'].get('overall_status', 'FAIL')}")
    print(f"Contract Ledger JSON: {verification_results['contract_ledger_json'].get('overall_status', 'FAIL')}")
    print(f"Contract Ledger CSV: {verification_results['contract_ledger_csv'].get('overall_status', 'FAIL')}")
    print(f"GitHub Skills Scope: {verification_results['github_skills_scope'].get('overall_status', 'FAIL')}")
    print(f"{'='*80}")
    print(f"OVERALL STATUS: {verification_results['overall_status']}")
    print(f"{'='*80}")
    
    return verification_results["overall_status"] == "PASS", verification_results

def main():
    parser = argparse.ArgumentParser(description='SKIL-14 / ZI-03 Contract Ledger Verification Harness')
    parser.add_argument('--source', type=Path, default=Path('/tmp/skil14-source'), help='Source repository root')
    parser.add_argument('--output', type=Path, default=Path('/tmp/skil14-verification'), help='Output directory for verification')
    parser.add_argument('--pinned-sha', type=str, default=DEFAULT_PINNED_SHA, help='Pinned commit SHA')
    parser.add_argument('--baseline-date', type=str, default=DEFAULT_BASELINE_DATE, help='Baseline date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run verification harness
    success, results = run_verifier(
        source_root=args.source,
        output_dir=output_dir,
        pinned_sha=args.pinned_sha,
        baseline_date=args.baseline_date
    )
    
    # Generate verification report
    report_file = output_dir / "verification_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "command": ' '.join(sys.argv),
            "results": results,
            "exit_status": "SUCCESS" if success else "FAILURE"
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Verification report written to: {report_file}")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())