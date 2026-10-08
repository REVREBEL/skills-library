# Phase 08 Batch Audit Record: `batch-02-business-and-operations-legal-and-governance`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-02-business-and-operations-legal-and-governance`
- **Category / Subcategory**: `business-and-operations` / `legal-and-governance`
- **Member Skill Count**: 11
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `3fa77c40941210020fcb89e2c36d8d07042bd2c3e308e9fa399b33d9a42df04a`
- **Approved Task 08 Cohesion Waiver**: Batch 02 was grouped mechanically under `legal-and-governance` per inherited Phase 05 paths; 10 members are recognized as cross-domain exceptions rather than a cohesive single-domain batch. Physical paths are preserved to maintain Phase 05/06/07 audit lineage.

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `ai-native-cli` | `task-folder/agents/skills/ai/ai-native-cli` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `api-and-interface-design` | `task-folder/agents/skills/api/api-and-interface-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `aria` | `task-folder/agents/skills/agents/agent-squad/aria` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `blockchain-developer` | `task-folder/agents/skills/blockchain-developer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `data-quality-frameworks` | `task-folder/agents/skills/data/data-quality-frameworks` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ddd-context-mapping` | `task-folder/agents/skills/ddd-context-mapping` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `employment-contract-templates` | `task-folder/agents/skills/employment-contract-templates` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `frontend-data-contracts` | `task-folder/agents/skills/front end/frontend-data-contracts` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-error-handling` | `task-folder/agents/skills/n8n/n8n-error-handling` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `options-flow-analyzer` | `task-folder/agents/skills/options-flow-analyzer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pydantic-models-py` | `task-folder/agents/skills/python/pydantic-models-py` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `ai-native-cli` | User asks to design or refactor a CLI command to output agent-friendly JSON schemas, handle exit codes deterministically, or provide structured error payloads. | User asks to write a visual desktop GUI in Electron or build a browser web dashboard. | User asks 'How do I build a CLI for my tool?' -> Disambiguate: Check if the CLI is intended for human interactive shell use (standard argparse) or autonomous AI agent invocation (ai-native-cli spec). |
| `api-and-interface-design` | User asks to design OpenAPI 3.1 REST API specifications, establish semantic versioning, and standardize HTTP error payloads. | User asks to debug frontend CSS z-index stacking context or flexbox alignment. | User asks 'How do I design a clean interface?' -> Disambiguate: Clarify whether they mean a backend HTTP/gRPC API interface or a visual UI/UX layout. |
| `aria` | User asks to orchestrate a squad of specialized autonomous subagents to collaboratively research, design, and implement a complex feature. | User asks for a simple single-line shell command to list directory files. | User asks 'How do I coordinate multiple agents?' -> Disambiguate: Check if they want multi-agent squad orchestration (Aria) or a single specialized subagent invocation. |
| `blockchain-developer` | User asks to author an ERC-20/ERC-721 Solidity smart contract, implement reentrancy guards, or connect via ethers.js/viem RPC. | User asks to configure a traditional centralized PostgreSQL database or Redis cache layer. | User asks 'How do I build a decentralized app?' -> Disambiguate: Determine if they need smart contract architecture (Solidity/EVM) or frontend Web3 wallet integration (wagmi/viem). |
| `data-quality-frameworks` | User asks to implement automated data validation assertions, null-rate checks, and Great Expectations / Soda suites across data pipelines. | User asks to train an image classification convolutional neural network in PyTorch. | User asks 'How do I validate my data?' -> Disambiguate: Determine if they need tabular data pipeline quality assertions or web form input validation. |
| `ddd-context-mapping` | User asks to map relationships (Shared Kernel, Customer-Supplier, Anti-Corruption Layer) between domain bounded contexts in a microservices system. | User asks to write unit test assertions for an individual helper utility function. | User asks 'How should I divide my system architecture?' -> Disambiguate: Determine if they need strategic DDD context mapping or low-level folder organization. |
| `employment-contract-templates` | User asks to draft a standard offer letter, NDA, IP assignment clause, or contractor services agreement template. | User asks to configure continuous integration build runners in GitHub Actions. | User asks 'How do I create a contract?' -> Disambiguate: Confirm whether they need a legal workforce agreement template or a technical software API data contract. |
| `frontend-data-contracts` | User asks to define TypeScript interfaces and Zod schemas that validate backend API payloads before passing them to UI components. | User asks to optimize CSS Grid layouts, Tailwind animations, or responsive typography. | User asks 'How do I manage data contracts in my app?' -> Disambiguate: Verify if they need frontend TypeScript API types or backend database schema definitions. |
| `n8n-error-handling` | User asks to build an n8n Error Trigger sub-workflow that captures execution failures, formats stack traces, and sends alerts to Slack. | User asks to write Python machine learning training scripts outside workflow automation engines. | User asks 'How do I handle workflow errors?' -> Disambiguate: Clarify if errors occur inside an n8n automation pipeline or within custom backend application code. |
| `options-flow-analyzer` | User asks to scan options chain data for unusual block trades, calculate call/put ratios, and detect institutional flow divergence. | User asks to prepare annual corporate balance sheets or file SEC 10-K tax compliance documents. | User asks 'How do I analyze market volume?' -> Disambiguate: Check if they are analyzing options flow derivatives or standard equity stock volume. |
| `pydantic-models-py` | User asks to implement multi-model Pydantic v2 schemas (Base, Create, Update, Response) for a REST API endpoint in Python. | User asks to define database table migrations with Alembic or write raw SQL schema DDL. | User asks 'How should I structure my data validation models?' -> Disambiguate: Confirm whether validation occurs at the Python application layer (Pydantic) or database schema constraint layer (SQL DDL). |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/business-and-operations/legal-and-governance/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `3fa77c40941210020fcb89e2c36d8d07042bd2c3e308e9fa399b33d9a42df04a` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `data-quality-frameworks` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `ddd-context-mapping` | `references/context-map-patterns.md` | Created or preserved in canonical package |
| `employment-contract-templates` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `n8n-error-handling` | `references/API_WORKFLOWS.md` | Created or preserved in canonical package |
| `n8n-error-handling` | `references/ERROR_WORKFLOWS.md` | Created or preserved in canonical package |
| `n8n-error-handling` | `references/NODE_ERROR_OUTPUTS.md` | Created or preserved in canonical package |
| `n8n-error-handling` | `references/RESPONSE_SHAPES.md` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- Approved Task 08 Cohesion Waiver: 10 cross-domain skills inherited from Phase 05 keyword placement (`ai-native-cli`, `pydantic-models-py`, `blockchain-developer`, etc.) cataloged as inherited taxonomy exceptions for Phase 10 router dispatch.
