---
name: "bilig-workpaper"
description: "Execute formula-backed spreadsheet calculations, verify computed cell readbacks, and persist WorkPaper JSON models using the @bilig/workpaper TypeScript API and MCP server. Use when modeling complex spreadsheet calculations without spreadsheet GUIs."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Bilig WorkPaper

Execute deterministic spreadsheet calculations and manage formula-backed workbooks programmatically via the Bilig WorkPaper runtime and MCP tools.

## When to Use

Use this skill when:
- Modeling business calculations (pricing quotes, payout models, financial projections) as formula workbooks.
- Performing spreadsheet cell edits, recalculations, and readback verification via TypeScript or MCP tools.
- Persisting structured formula workbooks as reviewable, version-controlled WorkPaper JSON documents.
- Diagnosing formula calculation discrepancies without automating desktop Excel or browser spreadsheet grids.

Do not use this skill for:
- Manual GUI spreadsheet editing or VBA macro execution.
- Complex charting, pivot tables, or desktop COM automation.

## Prerequisites

- Node.js 18+ runtime.
- Package `@bilig/workpaper` (pin reviewed version).
- Writable filesystem access when persisting `.workpaper.json` files.

## Workflow Patterns

### Pattern 1: Programmatic TypeScript Integration

```typescript
import {
  WorkPaper,
  exportWorkPaperDocument,
  serializeWorkPaperDocument,
} from "@bilig/workpaper";

// 1. Build workbook with sheets and formula relationships
const workbook = WorkPaper.buildFromSheets({
  Inputs: [
    ["Metric", "Value"],
    ["UnitsSold", 150],
    ["UnitPrice", 45.0],
  ],
  Summary: [
    ["Metric", "Value"],
    ["GrossRevenue", "=Inputs!B2*Inputs!B3"],
  ],
});

const inputsSheet = workbook.getSheetId("Inputs");
const summarySheet = workbook.getSheetId("Summary");

// 2. Mutate cell contents and trigger recalculation
workbook.setCellContents({ sheet: inputsSheet, row: 1, col: 1 }, 200);

// 3. Read back computed output to verify formula execution
const calculatedRevenue = workbook.getCellDisplayValue({ sheet: summarySheet, row: 1, col: 1 });
console.log(`Calculated Revenue: ${calculatedRevenue}`);

// 4. Serialize to WorkPaper JSON document
const savedDoc = serializeWorkPaperDocument(
  exportWorkPaperDocument(workbook, { includeConfig: true })
);
```

### Pattern 2: Headless MCP Tool Server Setup

```json
{
  "command": "npm",
  "args": [
    "exec",
    "--package",
    "@bilig/workpaper@latest",
    "--",
    "bilig-workpaper-mcp",
    "--workpaper",
    "./model.workpaper.json",
    "--writable"
  ]
}
```

Exposed MCP Tools:
- `list_sheets`: Enumerate sheets within the workbook.
- `read_cell` / `read_range`: Read values or formula definitions.
- `set_cell_contents`: Update input values and trigger graph recalculation.
- `get_cell_display_value`: Retrieve calculated result.
- `export_workpaper_document`: Export updated JSON workbook.

## Safety & Governance

- Validate cell coordinates and sheet names before writing to prevent unintended formula overwrite.
- Always execute a readback verification on dependent output cells after writing input values.
- Treat external WorkPaper JSON files as untrusted data; validate schema before importing into production logic.

## Completion Evidence

- Accurate before-and-after values recorded for inputs and dependent calculated outputs.
- Exported `.workpaper.json` document persisted with verified formula graph integrity.
