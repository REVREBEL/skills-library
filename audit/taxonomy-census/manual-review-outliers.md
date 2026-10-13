# Manual Review & Outlier Register (REV-126 / REV-150)

The following 6 skills were flagged for manual architectural review during the catalog census:

| Canonical ID | Current Path | Flag Reason | Architectural Recommendation |
| :--- | :--- | :--- | :--- |
| `007` | `library/development/fullstack/007` | Persona/agent prompt without concrete technical tasks | Move to agent personas or archive |
| `steve-jobs` | `library/design-and-experience/taste-and-critique/steve-jobs` | Executive persona critique prompt | Move to critique personas or archive |
| `nerdzao-elite-gemini-high` | `library/meta-and-agent-skills/skill-lifecycle/nerdzao-elite-gemini-high` | Non-standard model system prompt configuration | Move to agent prompts or test configs |
| `geminiignore-finops` | `library/infrastructure-and-ops/cloud-platforms/geminiignore-finops` | Tool-specific configuration file generator | Consolidate under cloud FinOps capability |
| `emerging-channels` | `library/marketing-and-seo/cro/emerging-channels` | Vague multi-channel strategic prompt without concrete steps | Refactor into specific social/ad capabilities |
| `integrations` | `library/development/fullstack/integrations` | Ambiguous umbrella name colliding with domain categories | Rename to `third-party-integration-patterns` |

---
All 6 skills are preserved in the catalog census with `confidence = low` and `semantic_role = manual_review` until final triage in REV-127/REV-128.