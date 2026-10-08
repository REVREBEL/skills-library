# Legacy Pyodide Compatibility Guide (Pre-n8n 2.x)

This reference documents legacy Python syntax used in n8n 1.x (Pyodide WebAssembly runner) for teams maintaining older self-hosted instances.

## Syntax Comparison

| Operation | n8n 2.x Native Python (Current) | n8n 1.x Pyodide (Legacy) |
|---|---|---|
| All items variable | `_items` | `_input.all()` |
| First item variable | `_items[0]` | `_input.first()` |
| Per-item variable | `_item` | `_input.item` |
| Execution engine | Native Python / Task Runner Container | WebAssembly Pyodide |

## Legacy Pyodide Example

```python
# Legacy n8n 1.x Pyodide syntax
items = _input.all()
output = []
for item in items:
    output.append({"json": {"id": item.json.id, "processed": True}})
return output
```

## Migration Steps to n8n 2.x

1. Replace `_input.all()` with `_items`.
2. Replace `item.json.field` or `item.json["field"]` with `item.get("json", {}).get("field")`.
3. Replace `_input.item` in per-item mode with `_item`.
4. If running on n8n Cloud, remove all `import` statements and use built-in operations.
