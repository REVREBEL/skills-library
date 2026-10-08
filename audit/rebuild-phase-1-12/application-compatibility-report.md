# Phase 03: Application Compatibility Report

This report details the systematic evaluation of the 2,331 recursively cataloged source skills under `task-folder/agents/skills` against the approved application, platform, and environment requirements. All quarantine operations were executed using a graph-aware, filesystem-authoritative surgical file-by-file move protocol.

## 1. High-Level Compatibility Metrics

- **Total Inventoried Skills Audited**: **2331**
- **Total Retained Skills**: **1855**
- **Total Quarantined Skills**: **45**
- **Total Unresolved Skills (Manual Review)**: **431**
- **Total Unique Exclusive Files Moved (Quarantined Footprint)**: **123**

### Complete 8-Category Classification Count Breakdown

| Compatibility Classification | Count | Retention Status |
| :--- | :--- | :--- |
| `Approved and supported` | **1561** | Retained |
| `Supported after conversion` | **293** | Retained |
| `Optional dependency with a supported replacement` | **0** | Retained |
| `Unsupported application or platform` | **45** | Quarantined |
| `Unsupported tool or permission dependency` | **0** | Quarantined |
| `Provider-specific but potentially reusable` | **1** | Retained |
| `Unrelated to the target library` | **0** | Quarantined |
| `Ambiguous and requiring manual review` | **431** | Unresolved (Manual Review Required) |

## 2. Quarantined Technologies Breakdown

The following is the count of quarantined skills grouped by the specific excluded technology that made them incompatible with the approved environment:

| Excluded Technology | Occurrences in Quarantined Skills |
| :--- | :--- |
| `Expo` | **14** |
| `Ruby` | **12** |
| `Rails` | **9** |
| `AWS Secrets Manager` | **6** |
| `AWS Lambda` | **6** |
| `HashiCorp Vault` | **3** |
| `Azure Key Vault` | **2** |
| `GDB workflows` | **2** |
| `Ditto session-mining` | **1** |
| `Windows-specific admin` | **1** |
| `GDB-cli` | **1** |
| `EAS Update` | **1** |

## 3. Unresolved Skills Requiring Human Alignment

The following is the complete list of ambiguous, mixed, or borderline skills that have been routed for manual verification. Their folders and files remain at their active locations, flagged with `Requires Manual Review` in the master database:

| Source Path | Folder Name | Compatibility Evidence | Decision Basis |
| :--- | :--- | :--- | :--- |
| `task-folder/agents/skills/3d-web-experience` | `3d-web-experience` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, React, provider_deps=None |
| `task-folder/agents/skills/accessibility-audit` | `accessibility-audit` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Expo, provider_deps=None |
| `task-folder/agents/skills/agents/agent-squad/luna` | `luna` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, provider_deps=None |
| `task-folder/agents/skills/agents/agents-sdk` | `agents-sdk` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Node.js, React, SQLite, TypeScript, provider_deps=None |
| `task-folder/agents/skills/agents/agents-v2-py` | `agents-v2-py` | `Excluded Tech: Azure Key Vault, GPT/OpenAI Subject` | Contains excluded technology keyword but dependency may be optional or non-intrinsic: Excluded Tech: Azure Key Vault, GPT/OpenAI Subject |
| `task-folder/agents/skills/ai/ai-native-cli` | `ai-native-cli` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/alternatives-pages` | `alternatives-pages` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/analytics-tracking` | `analytics-tracking` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/anti-reversing-techniques` | `anti-reversing-techniques` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, provider_deps=None |
| `task-folder/agents/skills/api/api-and-interface-design` | `api-and-interface-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, TypeScript, provider_deps=None |
| `task-folder/agents/skills/api/api-documentation-generator` | `api-documentation-generator` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, TypeScript, provider_deps=None |
| `task-folder/agents/skills/api/api-endpoint-builder` | `api-endpoint-builder` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/api/api-integration` | `api-integration` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, provider_deps=None |
| `task-folder/agents/skills/api/api-patterns` | `api-patterns` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, TypeScript, provider_deps=None |
| `task-folder/agents/skills/api/api-sdk-generator` | `api-sdk-generator` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, TypeScript, provider_deps=None |
| `task-folder/agents/skills/api/api-security-best-practices` | `api-security-best-practices` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Node.js, provider_deps=None |
| `task-folder/agents/skills/api/app-builder` | `app-builder` | `Excluded Tech: Expo` | Multi-stack builder containing optional Expo template (non-intrinsic dependency). |
| `task-folder/agents/skills/api/app-builder/templates` | `templates` | `Excluded Tech: Expo` | Multi-stack builder containing optional Expo template (non-intrinsic dependency). |
| `task-folder/agents/skills/architecture/architect-review` | `architect-review` | `Excluded Tech: HashiCorp Vault` | Contains excluded technology keyword but dependency may be optional or non-intrinsic: Excluded Tech: HashiCorp Vault |
| `task-folder/agents/skills/architecture/architecture-decision-records` | `architecture-decision-records` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, MySQL, PostgreSQL, React, TypeScript, provider_deps=None |
| `task-folder/agents/skills/auri-core` | `auri-core` | `Gemini Subject, Claude Subject, Excluded Tech: Azul tooling, Excluded Tech: AWS Lambda, GPT/OpenAI Subject, Claude Execution Environment` | Contains excluded technology keyword but dependency may be optional or non-intrinsic: Gemini Subject, Claude Subject, Excluded Tech: Azul tooling, Excluded Tech: AWS Lambda, GPT/OpenAI Subject, Claude Execution Environment |
| `task-folder/agents/skills/backend/backend-dev-guidelines` | `backend-dev-guidelines` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Node.js, TypeScript, provider_deps=None |
| `task-folder/agents/skills/bash/bash-linux` | `bash-linux` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/bash/bash-pro` | `bash-pro` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Docker, Expo, provider_deps=None |
| `task-folder/agents/skills/behavioral-modes` | `behavioral-modes` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, TypeScript, provider_deps=None |
| `task-folder/agents/skills/binary-analysis-patterns` | `binary-analysis-patterns` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, provider_deps=None |
| `task-folder/agents/skills/broken-authentication` | `broken-authentication` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, provider_deps=None |
| `task-folder/agents/skills/browser-automation` | `browser-automation` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/bugs-are-annoying` | `bugs-are-annoying` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, provider_deps=None |
| `task-folder/agents/skills/building-components` | `building-components` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=TypeScript, provider_deps=None |
| `task-folder/agents/skills/canva-automation` | `canva-automation` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/carrier-relationship-management` | `carrier-relationship-management` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/cc-skill-backend-patterns` | `cc-skill-backend-patterns` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Next.js, Node.js, TypeScript, provider_deps=None |
| `task-folder/agents/skills/cc-skill-clickhouse-io` | `cc-skill-clickhouse-io` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=PostgreSQL, TypeScript, provider_deps=None |
| `task-folder/agents/skills/cc-skill-frontend-patterns` | `cc-skill-frontend-patterns` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Next.js, React, TypeScript, provider_deps=None |
| `task-folder/agents/skills/cc-skill-security-review` | `cc-skill-security-review` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Next.js, React, TypeScript, Vercel, provider_deps=OpenAI/GPT |
| `task-folder/agents/skills/cdk-patterns` | `cdk-patterns` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Expo, Node.js, Python, TypeScript, provider_deps=None |
| `task-folder/agents/skills/changelog-automation` | `changelog-automation` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/ci-cd-and-automation` | `ci-cd-and-automation` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=PostgreSQL, TypeScript, Vercel, provider_deps=None |
| `task-folder/agents/skills/citation-management` | `citation-management` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, provider_deps=None |
| `task-folder/agents/skills/claimable-postgres` | `claimable-postgres` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Expo, Node.js, PostgreSQL, TypeScript, Vercel, provider_deps=None |
| `task-folder/agents/skills/clean-code` | `clean-code` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Python, provider_deps=None |
| `task-folder/agents/skills/clerk-auth` | `clerk-auth` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Next.js, PostgreSQL, React, TypeScript, provider_deps=None |
| `task-folder/agents/skills/clerk-nextjs-patterns` | `clerk-nextjs-patterns` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Next.js, TypeScript, provider_deps=None |
| `task-folder/agents/skills/cloud-architect` | `cloud-architect` | `Excluded Tech: HashiCorp Vault` | Contains excluded technology keyword but dependency may be optional or non-intrinsic: Excluded Tech: HashiCorp Vault |
| `task-folder/agents/skills/cloud-devops` | `cloud-devops` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Docker, GCP, Kubernetes, provider_deps=None |
| `task-folder/agents/skills/cloudflare` | `cloudflare` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, MySQL, Node.js, PostgreSQL, SQLite, provider_deps=None |
| `task-folder/agents/skills/cloudformation-best-practices` | `cloudformation-best-practices` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Expo, provider_deps=None |
| `task-folder/agents/skills/cms-best-practices` | `cms-best-practices` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/coda-automation` | `coda-automation` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/code/code-documentation` | `code-documentation` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=MySQL, PostgreSQL, TypeScript, provider_deps=None |
| `task-folder/agents/skills/code/code-documentation-doc-generate` | `code-documentation-doc-generate` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/code/code-polish` | `code-polish` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, provider_deps=None |
| `task-folder/agents/skills/code/code-refactoring-tech-debt` | `code-refactoring-tech-debt` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Python, React, provider_deps=None |
| `task-folder/agents/skills/code/code-review-checklist` | `code-review-checklist` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/code/code-reviewer` | `code-reviewer` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Kubernetes, Python, React, TypeScript, provider_deps=None |
| `task-folder/agents/skills/code/codebase-audit-pre-push` | `codebase-audit-pre-push` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, TypeScript, provider_deps=None |
| `task-folder/agents/skills/code/codebase-cleanup-deps-audit` | `codebase-cleanup-deps-audit` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/code/codebase-cleanup-tech-debt` | `codebase-cleanup-tech-debt` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Python, React, provider_deps=None |
| `task-folder/agents/skills/code/codebase-to-wordpress-converter` | `codebase-to-wordpress-converter` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Next.js, React, TailwindCSS, provider_deps=None |
| `task-folder/agents/skills/comprehensive-review-full-review` | `comprehensive-review-full-review` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Django, Python, React, TypeScript, provider_deps=None |
| `task-folder/agents/skills/computer-vision-expert` | `computer-vision-expert` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/container-security-hardening` | `container-security-hardening` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Docker, Expo, GCP, Kubernetes, Node.js, PostgreSQL, Python, React, provider_deps=None |
| `task-folder/agents/skills/content/content-marketer` | `content-marketer` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, Shopify, provider_deps=None |
| `task-folder/agents/skills/context/context-compression` | `context-compression` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/context/context-driven-development` | `context-driven-development` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Python, TypeScript, provider_deps=None |
| `task-folder/agents/skills/conversation-memory` | `conversation-memory` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/core-components` | `core-components` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/cost-optimization` | `cost-optimization` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, GCP, provider_deps=None |
| `task-folder/agents/skills/customer-support` | `customer-support` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Shopify, provider_deps=None |
| `task-folder/agents/skills/cv-generator` | `cv-generator` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Kubernetes, React, provider_deps=None |
| `task-folder/agents/skills/data/data-engineer` | `data-engineer` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Docker, GCP, Kubernetes, MySQL, PostgreSQL, Python, provider_deps=None |
| `task-folder/agents/skills/data/data-engineering-data-pipeline` | `data-engineering-data-pipeline` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Docker, Expo, PostgreSQL, Python, provider_deps=None |
| `task-folder/agents/skills/data/data-scientist` | `data-scientist` | `Excluded Tech: AWS Lambda, Excluded Tech: Azure Functions` | Contains excluded technology keyword but dependency may be optional or non-intrinsic: Excluded Tech: AWS Lambda, Excluded Tech: Azure Functions |
| `task-folder/agents/skills/data/data-structure-protocol` | `data-structure-protocol` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, provider_deps=None |
| `task-folder/agents/skills/databases/database-admin` | `database-admin` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, GCP, Kubernetes, MySQL, PostgreSQL, provider_deps=None |
| `task-folder/agents/skills/databases/database-architect` | `database-architect` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Django, GCP, MySQL, PostgreSQL, provider_deps=None |
| `task-folder/agents/skills/databases/database-cloud-optimization-cost-optimize` | `database-cloud-optimization-cost-optimize` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, GCP, provider_deps=None |
| `task-folder/agents/skills/databases/database-migration` | `database-migration` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, MySQL, PostgreSQL, TypeScript, provider_deps=None |
| `task-folder/agents/skills/databases/database-migrations-sql-migrations` | `database-migrations-sql-migrations` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=MySQL, PostgreSQL, provider_deps=None |
| `task-folder/agents/skills/databases/database-optimizer` | `database-optimizer` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Django, GCP, MySQL, PostgreSQL, provider_deps=None |
| `task-folder/agents/skills/ddd-tactical-patterns` | `ddd-tactical-patterns` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=TypeScript, provider_deps=None |
| `task-folder/agents/skills/debugging/debugging-and-error-recovery` | `debugging-and-error-recovery` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, TypeScript, provider_deps=None |
| `task-folder/agents/skills/debugging/debugging-code` | `debugging-code` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Node.js, Python, TypeScript, provider_deps=Anthropic/Claude |
| `task-folder/agents/skills/debugging/debugging-toolkit-smart-debug` | `debugging-toolkit-smart-debug` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=TypeScript, provider_deps=None |
| `task-folder/agents/skills/debugging/error-diagnostics-smart-debug` | `error-diagnostics-smart-debug` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=TypeScript, provider_deps=None |
| `task-folder/agents/skills/dependency-management-deps-audit` | `dependency-management-deps-audit` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/dependency-upgrade` | `dependency-upgrade` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, TypeScript, provider_deps=None |
| `task-folder/agents/skills/deployment-engineer` | `deployment-engineer` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Docker, GCP, Kubernetes, provider_deps=None |
| `task-folder/agents/skills/deployment-validation-config-validate` | `deployment-validation-config-validate` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Expo, Python, TypeScript, provider_deps=None |
| `task-folder/agents/skills/deprecation-and-migration` | `deprecation-and-migration` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=TypeScript, provider_deps=None |
| `task-folder/agents/skills/design/design-an-interface` | `design-an-interface` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/design-brief` | `design-brief` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/design-it/ai-native-ui` | `ai-native-ui` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/aurora-ui` | `aurora-ui` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/brutalism` | `brutalism` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/brutalist-typography` | `brutalist-typography` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, React, React Native, Shopify, provider_deps=None |
| `task-folder/agents/skills/design/design-it/card-based-design` | `card-based-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/color-blocking` | `color-blocking` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, React, provider_deps=None |
| `task-folder/agents/skills/design/design-it/cyber-y2k` | `cyber-y2k` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, Shopify, provider_deps=None |
| `task-folder/agents/skills/design/design-it/cyberpunk-ui` | `cyberpunk-ui` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/dark-mode` | `dark-mode` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/dashboard-design` | `dashboard-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, Shopify, provider_deps=None |
| `task-folder/agents/skills/design/design-it/duotone-design` | `duotone-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, Shopify, provider_deps=None |
| `task-folder/agents/skills/design/design-it/frutiger-aero` | `frutiger-aero` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/glassmorphism` | `glassmorphism` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/material-design` | `material-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/maximalism` | `maximalism` | `Excluded Tech: Ruby` | Contains excluded technology keyword but dependency may be optional or non-intrinsic: Excluded Tech: Ruby |
| `task-folder/agents/skills/design/design-it/neo-brutalism` | `neo-brutalism` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/neumorphism` | `neumorphism` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/retro-design` | `retro-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/retro-futurism` | `retro-futurism` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/sci-fi-interface` | `sci-fi-interface` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/spatial-computing-ui` | `spatial-computing-ui` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/spatial-design` | `spatial-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-it/synthwave` | `synthwave` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, React, provider_deps=None |
| `task-folder/agents/skills/design/design-it/typography-first` | `typography-first` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, React, provider_deps=None |
| `task-folder/agents/skills/design/design-it/vaporwave` | `vaporwave` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, React, provider_deps=None |
| `task-folder/agents/skills/design/design-it/y2k-design` | `y2k-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=React, React Native, provider_deps=None |
| `task-folder/agents/skills/design/design-spatial` | `design-spatial` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Python, Vercel, provider_deps=None |
| `task-folder/agents/skills/design/design-system` | `design-system` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, React, provider_deps=Meta/Llama |
| `task-folder/agents/skills/design/design-ux` | `design-ux` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Vercel, provider_deps=None |
| `task-folder/agents/skills/design/designer-skills-main/design-research/skills/research-repository` | `research-repository` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/motion-system` | `motion-system` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/onboarding-design` | `onboarding-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/von-restorff-effect` | `von-restorff-effect` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, provider_deps=None |
| `task-folder/agents/skills/design/designer/analysis/ebook-analysis` | `ebook-analysis` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer/ce-polish` | `ce-polish` | `Claude Execution Environment, Excluded Tech: Rails, Claude Subject` | Contains excluded technology keyword but dependency may be optional or non-intrinsic: Claude Execution Environment, Excluded Tech: Rails, Claude Subject |
| `task-folder/agents/skills/design/designer/design-research/skills/research-repository` | `research-repository` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer/design-systems/skills/motion-system` | `motion-system` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer/interaction-design/skills/onboarding-design` | `onboarding-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer/layers-skills-main/skills/layers-conceptual-model` | `layers-conceptual-model` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer/layers-skills-main/skills/layers-product-strategy` | `layers-product-strategy` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer/layers-skills-main/skills/layers-user-needs` | `layers-user-needs` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/designer/ui-design/skills/von-restorff-effect` | `von-restorff-effect` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, provider_deps=None |
| `task-folder/agents/skills/design/fortify` | `fortify` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/frontend-design` | `frontend-design` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, React, provider_deps=Anthropic/Claude |
| `task-folder/agents/skills/design/frontend-enhancer` | `frontend-enhancer` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Next.js, React, TailwindCSS, TypeScript, provider_deps=None |
| `task-folder/agents/skills/design/image-to-code-skill` | `image-to-code-skill` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/include` | `include` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, provider_deps=None |
| `task-folder/agents/skills/design/intent` | `intent` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/localize` | `localize` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Expo, provider_deps=None |
| `task-folder/agents/skills/design/pitch-deck` | `pitch-deck` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, Python, provider_deps=None |
| `task-folder/agents/skills/design/specify` | `specify` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/design/strategize` | `strategize` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, provider_deps=None |
| `task-folder/agents/skills/design/ui-skills/image-to-code-skill` | `image-to-code-skill` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, provider_deps=None |
| `task-folder/agents/skills/dev-to-hashnode` | `dev-to-hashnode` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Python, React, provider_deps=None |
| `task-folder/agents/skills/development` | `development` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Docker, FastAPI, Next.js, Node.js, PostgreSQL, Python, React, React Native, TailwindCSS, TypeScript, Vercel, provider_deps=None |
| `task-folder/agents/skills/development/developer/developer-advocacy` | `developer-advocacy` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=AWS, Kubernetes, React, Vercel, provider_deps=None |
| `task-folder/agents/skills/development/developer/developer-churn` | `developer-churn` | `None` | Unclear dependency or provider coupling pattern: evidence=[], app_deps=Expo, React, provider_deps=None |

*And 281 more ambiguous rows. Refer to the CSV database for the full list.*

## 4. Reconciliation Checklist & Invariants Proof

To ensure complete technical verification and trace accuracy, the following mathematical invariants were checked and proved during execution:

- [x] **Classification Total Equality**: All 8 individual classification counts sum to exactly 2,331.
- [x] **Disposition Total Equality**: Retained Count (including conversions and reusables) + Quarantined Count + Unresolved Count = exactly 2,331.
- [x] **Database Row Reconciliation**: Total rows written to `skills-inventory.csv` = exactly 2,331 rows. Every source path remains unique and accounted for, with exactly 0 unclassified or omitted rows.
- [x] **Surgical Movement & Footprint Verification**:
  - Calculated the **unique union of exclusive footprints** to be exactly **123 files**.
  - Reconciled filesystem renames/moves; exactly 123 physical files were relocated into quarantine.
  - Every quarantined skill's source `SKILL.md` file has been traceably moved and no longer exists at its active source path.
  - All files in each quarantined skill's calculated exclusive filesystem footprint were successfully moved to `task-folder/agents/not-needed`.
  - The quarantine manifest `moved-to-not-needed.csv` matches the count of physically quarantined skills.
  - No moved file appears simultaneously in both the active `skills/` and quarantined `not-needed/` directories.
  - **Crucial Invariant**: Every sub-nested retained or unresolved descendant skill (and its respective sub-SKILL.md) remains 100% untouched and active in its original location, completely unaffected by the quarantine of an ancestor folder.
  - **README Preservation**: Preserved `task-folder/agents/not-needed/README.md` perfectly without any destructive overwrite.
- [x] **Portability Rule Enforcement**: Audited all updated CSVs, reports, and manifests to confirm they contain zero workstation-specific absolute paths (no `/Users/` or `/home/` leaks). All references are strictly repository-relative.
