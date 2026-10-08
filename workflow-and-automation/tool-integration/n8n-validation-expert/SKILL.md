---
name: "n8n-validation-expert"
description: "Diagnose, interpret, and remediate n8n workflow validation errors, missing required properties, expression syntax failures, and node connection schema mismatches. Use when diagnosing n8n workflow validation errors or connection schema failures."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# n8n Validation Expert

Systematically diagnose and fix n8n workflow validation errors, parameter mismatches, and expression faults.

## When to Use

Use this skill when:
- An n8n workflow fails to activate or run due to validation errors.
- Troubleshooting `missing_required`, `invalid_value`, `unknown_property`, or `type_mismatch` errors.
- Expression evaluation returns `[Object: null]`, `undefined`, or syntax parsing exceptions.
- Executing automated iterative validation-fix cycles on exported n8n workflow JSON.

Do not use this skill for:
- Writing custom Python scripts (use `n8n-code-python`).
- High-level architectural pattern selection (use `n8n-workflow-patterns`).

## Prerequisites

- n8n error message, error payload, or exported workflow JSON.
- Identification of the failing node and operation.

## Common Validation Errors & Remediation

### 1. `missing_required`
- **Cause**: Node operation requires a parameter that is missing or empty.
- **Fix**: Check the node's active `operation` and populate the mandatory fields. If dynamic, ensure the expression evaluates to a truthy value.

### 2. `invalid_value` / `type_mismatch`
- **Cause**: Expected a specific type (e.g. integer, boolean, array) but received a string or object.
- **Fix**: Use type conversion functions in expressions (e.g., `{{ parseInt($json.id, 10) }}`, `{{ $json.flag === 'true' }}`).

### 3. `expression_syntax_error`
- **Cause**: Unmatched braces, illegal JavaScript expressions, or referring to non-existent nodes.
- **Fix**: Validate node references (`$('ExactNodeName').item.json.key`) and verify matching `{{ ... }}` delimiters.

### 4. `item_list_mismatch`
- **Cause**: Node expects single item output but received array or empty list.
- **Fix**: Place an Item Lists node (Split Out or Aggregate) upstream to normalize item boundaries.

## Validation & Fix Workflow

1. **Extract Error Details**: Isolate `node`, `property`, `message`, and `timestamp`.
2. **Inspect Upstream Output**: Review the exact `$json` output of the preceding node to confirm field presence and casing.
3. **Verify Node Schema**: Confirm parameter requirements for the specific node version.
4. **Apply Surgical Fix**: Modify only the offending parameter or expression.
5. **Re-validate**: Run single-node test execution to verify error clearance.

## Safety & Governance

- When fixing database or API nodes, ensure test runs do not trigger destructive actions against production resources.
- Retain original parameter values when adjusting expressions to avoid accidental loss of configuration intent.

## Completion Evidence

- Node passes validation without warning or error badges.
- Test execution completes with exit code 0 and populates valid output data.
