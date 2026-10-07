---
name: "n8n-code-python"
description: "Write, debug, and optimize Python transformations in n8n 2.x native Python Code nodes using _items and _item data structures, handling Cloud sandbox constraints and self-hosted runner environments. Use when writing Python transformations or debugging n8n 2.x Python Code nodes."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# n8n Native Python Code Node (n8n 2.x)

Write reliable, performant data transformations in n8n 2.x native Python Code nodes across n8n Cloud and self-hosted environments.

## When to Use

Use this skill when:
- Writing custom Python transformation logic inside n8n Code nodes (Language: Python).
- Processing workflow items using n8n 2.x native Python data structures (`_items` and `_item`).
- Navigating runtime constraints between n8n Cloud (pure built-in execution) and self-hosted n8n (task runner images with custom packages).
- Debugging Python syntax errors, item key access, or return format rejections in n8n.

Do not use this skill for:
- Writing schema-constrained AI Custom Code Tools for LangChain/AI Agent nodes (use `n8n-code-tool`).
- Writing JavaScript Code nodes or utilizing n8n JS-specific helpers (`$helpers`, Luxon, `$jmespath`).

## Prerequisites

- n8n version 2.0+ with Native Python execution mode active.
- Defined input dataset from upstream trigger or action node.

## Execution Model & Data Structures

In n8n 2.x native Python, data is exposed via two built-in variables depending on the selected execution mode:

| Mode | Variable | Description |
|---|---|---|
| **Run Once for All Items** | `_items` | List of item dictionaries: `[{"json": {...}}, ...]` |
| **Run Once for Each Item** | `_item` | Current item dictionary: `{"json": {...}}` |

> [!NOTE]
> Native Python in n8n 2.x does **not** support legacy Pyodide objects (`_input.all()`, `_input.first()`, `_input.item`) or global `$node` helpers. For legacy Pyodide instances (n8n 1.x), see the [Legacy Pyodide Compatibility Guide](./references/LEGACY_PYODIDE_COMPATIBILITY.md).

### Return Format Contract

- **Run Once for All Items Mode**: Must return a list of dictionaries with `"json"` keys (e.g. `[{"json": {...}}]`) or a list of flat dictionaries (n8n will wrap them into `{"json": ...}`).
- **Run Once for Each Item Mode**: Must return a single dictionary with a `"json"` key (e.g. `{"json": {...}}`) or a single flat dictionary.

---

## Code Examples

### Example 1: Batch Processing & Normalization (All Items Mode)

```python
# Mode: Run Once for All Items
results = []

for item in _items:
    data = item.get("json", {})
    cleaned_record = {
        "user_id": str(data.get("id", "")).strip().upper(),
        "email": str(data.get("email", "")).strip().lower(),
        "gross_amount": round(float(data.get("amount", 0.0)), 2),
        "is_active": bool(data.get("status") == "active"),
    }
    results.append({"json": cleaned_record})

return results
```

### Example 2: Per-Item Transformation (Each Item Mode)

```python
# Mode: Run Once for Each Item
data = _item.get("json", {})
raw_tags = data.get("tags", "")

# Transform comma-separated string to deduplicated sorted list
tag_list = sorted(list(set(t.strip().lower() for t in raw_tags.split(",") if t.strip())))

return {
    "json": {
        "product_id": data.get("product_id"),
        "normalized_tags": tag_list,
        "tag_count": len(tag_list)
    }
}
```

---

## Cloud vs Self-Hosted Environment Constraints

### n8n Cloud
- Runs in a strict sandbox where `import` statements are disabled (even standard library modules like `re`, `math`, `json`, `datetime` cannot be imported).
- All transformations must use pure built-in Python syntax, string manipulation, dictionary/list methods, and mathematical operators.

### Self-Hosted n8n
- Runs Python via dedicated task runner sidecar containers (`n8n-task-runners`).
- Importing standard library or external packages (e.g. `pandas`, `requests`, `numpy`) requires:
  1. Installing packages into the runner container image.
  2. Setting Python runner allowlist environment variables on the task runner:
     - `N8N_RUNNERS_STDLIB_ALLOW=*` (or specific standard-library modules like `re,math,json,datetime`)
     - `N8N_RUNNERS_EXTERNAL_ALLOW=pandas,numpy,requests` (for third-party installed packages)

---

## Progressive Disclosure & Reference

- [Legacy Pyodide Compatibility Guide](./references/LEGACY_PYODIDE_COMPATIBILITY.md): Reference for legacy n8n 1.x / Pyodide syntax migration (`_input.all()`).

---

## Safety & Governance

- Always use `.get()` with safe defaults when accessing dictionary keys to prevent unhandled `KeyError` crashes.
- Never execute dynamic untrusted string code using `eval()` or `exec()`.

## Completion Evidence

- Code node executes cleanly in n8n 2.x without runtime syntax errors.
- Output matches the required `[{"json": {...}}]` or `{"json": {...}}` contract.
