# Skills Inventory Audit & Summary

This summary catalogs the entire skills population under `task-folder/agents/skills` as established in Phase 01. No source skills were moved, rewritten, or deleted during this analysis.

## High-Level Coverage Metrics

- **Total Discovered Skills (Containing `SKILL.md` across all depths)**: **2331**
- **Total Top-Level Directories**: **738**
- **Total Bundled Resources (supporting scripts, templates, references)**: **5004**
- **Total Orphaned/Static Resources at Root**: **0**
- **Invalid or Missing Frontmatter**: **0**
- **Folder/Frontmatter Name Mismatches**: **84**
- **Duplicate Frontmatter Names**: **210**
- **Leak Check (Phase 02 Inventory Artifacts)**: **0 detected** (fully normalized repository-relative paths only, no leak in CSV or summary)
- **Leak Check (Existing Source Content)**: **46 files contain hardcoded local absolute paths** (flagged below and in CSV for future repair)
- **Unresolved Inspection Gaps**: **0** (All 2,331 skills were successfully read, parsed, and inspected, with zero unreadable files or incomplete evaluations.)

## Duplicate Frontmatter Names

The following frontmatter names appear in multiple separate paths. These represent name collisions that will require consolidation or deduplication in later phases:

- **`a-b-test-design`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/a-b-test-design`
  - `task-folder/agents/skills/design/designer/prototyping-testing/skills/a-b-test-design`
- **`ab-testing`** (2 occurrences):
  - `task-folder/agents/skills/ab-testing`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/email-marketing/skills/ab-testing`
- **`accessibility-audit`** (3 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/accessibility-audit`
  - `task-folder/agents/skills/design/designer/design-systems/skills/accessibility-audit`
  - `task-folder/agents/skills/accessibility-audit`
- **`accessibility-test-plan`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/accessibility-test-plan`
  - `task-folder/agents/skills/design/designer/prototyping-testing/skills/accessibility-test-plan`
- **`ad-creative`** (3 occurrences):
  - `task-folder/agents/skills/ads/ad-creative`
  - `task-folder/agents/skills/design/ad-creative`
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/ad-creative`
- **`aesthetic-usability`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/aesthetic-usability`
  - `task-folder/agents/skills/design/designer/ui-design/skills/aesthetic-usability`
- **`affiliate-program`** (2 occurrences):
  - `task-folder/agents/skills/marketing/affiliate-program_02`
  - `task-folder/agents/skills/marketing/affiliate-program`
- **`affinity-diagram`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/affinity-diagram`
  - `task-folder/agents/skills/design/designer/design-research/skills/affinity-diagram`
- **`ai-seo`** (2 occurrences):
  - `task-folder/agents/skills/ai/ai-seo`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/ai-seo`
- **`alert-manager`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/monitor/alert-manager`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/monitor/alert-manager`
- **`animation-principles`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/animation-principles`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/animation-principles`
- **`artifacts-builder`** (3 occurrences):
  - `task-folder/agents/skills/design/artifacts-builder`
  - `task-folder/agents/skills/report-writing/artifacts-builder`
  - `task-folder/agents/skills/writing/artifacts-builder`
- **`backlink-analyzer`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/monitor/backlink-analyzer`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/monitor/backlink-analyzer`
- **`blueprint`** (2 occurrences):
  - `task-folder/agents/skills/design/blueprint`
  - `task-folder/agents/skills/blueprint`
- **`brainstorming`** (3 occurrences):
  - `task-folder/agents/skills/design/designer/ideation/brainstorming`
  - `task-folder/agents/skills/ideation/brainstorming2`
  - `task-folder/agents/skills/ideation/brainstorming`
- **`brand-guidelines`** (2 occurrences):
  - `task-folder/agents/skills/design/brand-guidelines`
  - `task-folder/agents/skills/brand-guidelines`
- **`brandkit`** (2 occurrences):
  - `task-folder/agents/skills/design/brandkit2`
  - `task-folder/agents/skills/design/brandkit`
- **`card-sort-analysis`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/card-sort-analysis`
  - `task-folder/agents/skills/design/designer/design-research/skills/card-sort-analysis`
- **`case-study`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/designer-toolkit/skills/case-study`
  - `task-folder/agents/skills/design/designer/designer-toolkit/skills/case-study`
- **`click-test-plan`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/click-test-plan`
  - `task-folder/agents/skills/design/designer/prototyping-testing/skills/click-test-plan`
- **`co-marketing`** (2 occurrences):
  - `task-folder/agents/skills/marketing/co-marketing`
  - `task-folder/agents/skills/marketing/co-marketing_02`
- **`cohort-analysis`** (2 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/cohort-analysis`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/revenue-analytics/skills/cohort-analysis`
- **`color-system`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/color-system`
  - `task-folder/agents/skills/design/designer/ui-design/skills/color-system`
- **`competitive-analysis`** (3 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/competitive-analysis`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/competitive-analysis`
  - `task-folder/agents/skills/strategy/competitive-analysis`
- **`competitor-analysis`** (5 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/competitor-analysis`
  - `task-folder/agents/skills/marketing/competitor-analysis`
  - `task-folder/agents/skills/seo/competitor-analysis`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/research/competitor-analysis`
  - `task-folder/agents/skills/writing/competitor-analysis`
- **`competitor-monitor`** (2 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/competitor-monitor`
  - `task-folder/agents/skills/seo/seo-skills-main/automation/competitor-monitor`
- **`competitor-profiling`** (2 occurrences):
  - `task-folder/agents/skills/marketing/competitor-profiling`
  - `task-folder/agents/skills/writing/competitor-profiling`
- **`component-spec`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/component-spec`
  - `task-folder/agents/skills/design/designer/design-systems/skills/component-spec`
- **`content-calendar`** (2 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/content-calendar`
  - `task-folder/agents/skills/marketing/content-calendar`
- **`content-commerce`** (2 occurrences):
  - `task-folder/agents/skills/marketing/content-commerce`
  - `task-folder/agents/skills/marketing/content-commerce_02`
- **`content-gap-analysis`** (3 occurrences):
  - `task-folder/agents/skills/marketing/content-gap-analysis`
  - `task-folder/agents/skills/seo/content-gap-analysis`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/research/content-gap-analysis`
- **`content-refresher`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/optimize/content-refresher`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/optimize/content-refresher`
- **`content-research-writer`** (2 occurrences):
  - `task-folder/agents/skills/report-writing/content-research-writer`
  - `task-folder/agents/skills/writing/content-research-writer`
- **`content-strategy`** (5 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/content-strategy`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/content-strategy`
  - `task-folder/agents/skills/content/content-strategy`
  - `task-folder/agents/skills/marketing/content-strategy`
  - `task-folder/agents/skills/seo/seo-skills-main/automation/content/content-strategy`
- **`copy-editing`** (2 occurrences):
  - `task-folder/agents/skills/content/copy-editing`
  - `task-folder/agents/skills/marketing/copy-editing`
- **`copywriting`** (4 occurrences):
  - `task-folder/agents/skills/design/copywriting`
  - `task-folder/agents/skills/content/copywriting`
  - `task-folder/agents/skills/marketing/copywriting`
  - `task-folder/agents/skills/marketing/copywriting/copywriting`
- **`critique-brand-consistency`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/visual-critique/skills/critique-brand-consistency`
  - `task-folder/agents/skills/design/designer/visual-critique/skills/critique-brand-consistency`
- **`critique-composition`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/visual-critique/skills/critique-composition`
  - `task-folder/agents/skills/design/designer/visual-critique/skills/critique-composition`
- **`critique-typography`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/visual-critique/skills/critique-typography`
  - `task-folder/agents/skills/design/designer/visual-critique/skills/critique-typography`
- **`critique-visual-hierarchy`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/visual-critique/skills/critique-visual-hierarchy`
  - `task-folder/agents/skills/design/designer/visual-critique/skills/critique-visual-hierarchy`
- **`cro`** (3 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/cro`
  - `task-folder/agents/skills/marketing/cro`
  - `task-folder/agents/skills/cro`
- **`customer-research`** (2 occurrences):
  - `task-folder/agents/skills/customer-research`
  - `task-folder/agents/skills/marketing/customer-research`
- **`dark-mode-design`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/dark-mode-design`
  - `task-folder/agents/skills/design/designer/ui-design/skills/dark-mode-design`
- **`data-visualization`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/data-visualization`
  - `task-folder/agents/skills/design/designer/ui-design/skills/data-visualization`
- **`design-brief`** (3 occurrences):
  - `task-folder/agents/skills/design/design-brief`
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/design-brief`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/design-brief`
- **`design-critique`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/design-critique`
  - `task-folder/agents/skills/design/designer/design-ops/skills/design-critique`
- **`design-debt-audit`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/design-debt-audit`
  - `task-folder/agents/skills/design/designer/design-ops/skills/design-debt-audit`
- **`design-impact-reporting`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/design-impact-reporting`
  - `task-folder/agents/skills/design/designer/design-ops/skills/design-impact-reporting`
- **`design-md`** (2 occurrences):
  - `task-folder/agents/skills/design/design-md_v1`
  - `task-folder/agents/skills/design/design-md`
- **`design-negotiation`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/designer-toolkit/skills/design-negotiation`
  - `task-folder/agents/skills/design/designer/designer-toolkit/skills/design-negotiation`
- **`design-principles`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/design-principles`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/design-principles`
- **`design-qa-checklist`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/design-qa-checklist`
  - `task-folder/agents/skills/design/designer/design-ops/skills/design-qa-checklist`
- **`design-rationale`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/designer-toolkit/skills/design-rationale`
  - `task-folder/agents/skills/design/designer/designer-toolkit/skills/design-rationale`
- **`design-review`** (2 occurrences):
  - `task-folder/agents/skills/design/design-review_2`
  - `task-folder/agents/skills/design/design-review`
- **`design-review-process`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/design-review-process`
  - `task-folder/agents/skills/design/designer/design-ops/skills/design-review-process`
- **`design-sprint-plan`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/design-sprint-plan`
  - `task-folder/agents/skills/design/designer/design-ops/skills/design-sprint-plan`
- **`design-system-adoption`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/designer-toolkit/skills/design-system-adoption`
  - `task-folder/agents/skills/design/designer/designer-toolkit/skills/design-system-adoption`
- **`design-system-governance`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/design-system-governance`
  - `task-folder/agents/skills/design/designer/design-systems/skills/design-system-governance`
- **`design-taste-frontend`** (3 occurrences):
  - `task-folder/agents/skills/design/deterministic-design/design-audit/taste-skill`
  - `task-folder/agents/skills/design/design-taste-frontend`
  - `task-folder/agents/skills/design/taste-skill`
- **`design-taste-frontend-v1`** (2 occurrences):
  - `task-folder/agents/skills/design/taste-skill-v1`
  - `task-folder/agents/skills/design/deterministic-design/design-audit/taste-skill-v1`
- **`design-token`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/design-token`
  - `task-folder/agents/skills/design/designer/design-systems/skills/design-token`
- **`design-token-audit`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/designer-toolkit/skills/design-token-audit`
  - `task-folder/agents/skills/design/designer/designer-toolkit/skills/design-token-audit`
- **`diary-study-plan`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/diary-study-plan`
  - `task-folder/agents/skills/design/designer/design-research/skills/diary-study-plan`
- **`doc-coauthoring`** (2 occurrences):
  - `task-folder/agents/skills/design/doc-coauthoring`
  - `task-folder/agents/skills/documentation/doc-coauthoring`
- **`documentation-template`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/documentation-template`
  - `task-folder/agents/skills/design/designer/design-systems/skills/documentation-template`
- **`doherty-threshold`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/doherty-threshold`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/doherty-threshold`
- **`ecommerce-seo`** (2 occurrences):
  - `task-folder/agents/skills/marketing/ecommerce-seo`
  - `task-folder/agents/skills/seo/seo-skills-main/ecommerce-seo`
- **`email-list-segmentation`** (2 occurrences):
  - `task-folder/agents/skills/marketing/email-list-segmentation`
  - `task-folder/agents/skills/email/email-list-segmentation`
- **`email-marketing-automation`** (2 occurrences):
  - `task-folder/agents/skills/marketing/email-marketing-automation`
  - `task-folder/agents/skills/email/email-marketing-automation`
- **`email-sequence`** (3 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/email-sequence`
  - `task-folder/agents/skills/email/email-sequence2`
  - `task-folder/agents/skills/email/email-sequence`
- **`empathy-map`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/empathy-map`
  - `task-folder/agents/skills/design/designer/design-research/skills/empathy-map`
- **`enablement-kit`** (3 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/sales-handoff-orchestration/skills/enablement-kit`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/pricing-strategy/skills/enablement-kit`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/design-creative/skills/enablement-kit`
- **`error-handling-ux`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/error-handling-ux`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/error-handling-ux`
- **`experience-map`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/experience-map`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/experience-map`
- **`feedback-patterns`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/feedback-patterns`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/feedback-patterns`
- **`fitts-law`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/fitts-law`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/fitts-law`
- **`form-design`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/form-design`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/form-design`
- **`format-revrebel-google-docs`** (2 occurrences):
  - `task-folder/agents/skills/google/format-revrebel-google-docs`
  - `task-folder/agents/skills/format-revrebel-google-docs`
- **`frontend-design`** (4 occurrences):
  - `task-folder/agents/skills/design/frontend-design`
  - `task-folder/agents/skills/front end/frontend-design2`
  - `task-folder/agents/skills/front end/front-end-design`
  - `task-folder/agents/skills/front end/frontend-design`
- **`frontend-slides`** (2 occurrences):
  - `task-folder/agents/skills/design/frontend-slides`
  - `task-folder/agents/skills/front end/frontend-slides`
- **`full-output-enforcement`** (2 occurrences):
  - `task-folder/agents/skills/design/output-skill`
  - `task-folder/agents/skills/front end/full-output-enforcement`
- **`gesture-patterns`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/gesture-patterns`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/gesture-patterns`
- **`governance`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/personalization-engine/skills/governance`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/customer-journey-orchestration/skills/governance`
- **`gpt-taste`** (2 occurrences):
  - `task-folder/agents/skills/design/gpt-tasteskill`
  - `task-folder/agents/skills/gpt-taste`
- **`handoff-spec`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/handoff-spec`
  - `task-folder/agents/skills/design/designer/design-ops/skills/handoff-spec`
- **`heuristic-evaluation`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/heuristic-evaluation`
  - `task-folder/agents/skills/design/designer/prototyping-testing/skills/heuristic-evaluation`
- **`hicks-law`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/hicks-law`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/hicks-law`
- **`high-end-visual-design`** (2 occurrences):
  - `task-folder/agents/skills/design/high-end-visual-design`
  - `task-folder/agents/skills/design/soft-skill`
- **`icon-system`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/icon-system`
  - `task-folder/agents/skills/design/designer/design-systems/skills/icon-system`
- **`illustration-style`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/illustration-style`
  - `task-folder/agents/skills/design/designer/ui-design/skills/illustration-style`
- **`image-enhancer`** (2 occurrences):
  - `task-folder/agents/skills/report-writing/image-enhancer`
  - `task-folder/agents/skills/writing/image-enhancer`
- **`image-to-code`** (2 occurrences):
  - `task-folder/agents/skills/design/image-to-code-skill`
  - `task-folder/agents/skills/design/ui-skills/image-to-code-skill`
- **`imagegen-frontend-mobile`** (2 occurrences):
  - `task-folder/agents/skills/design/imagegen-frontend-mobile`
  - `task-folder/agents/skills/design/ui-skills/imagegen-frontend-mobile`
- **`imagegen-frontend-web`** (2 occurrences):
  - `task-folder/agents/skills/design/imagegen-frontend-web`
  - `task-folder/agents/skills/design/ui-skills/imagegen-frontend-web`
- **`imagen`** (2 occurrences):
  - `task-folder/agents/skills/design/imagen`
  - `task-folder/agents/skills/images/imagen`
- **`industrial-brutalist-ui`** (2 occurrences):
  - `task-folder/agents/skills/design/brutalist-skill`
  - `task-folder/agents/skills/industrial-brutalist-ui`
- **`influencer-marketplace-integration`** (2 occurrences):
  - `task-folder/agents/skills/marketing/influencer-marketplace-integration_02`
  - `task-folder/agents/skills/marketing/influencer-marketplace-integration`
- **`influencer-tracking`** (2 occurrences):
  - `task-folder/agents/skills/marketing/influencer-tracking`
  - `task-folder/agents/skills/marketing/influencer-tracking_02`
- **`information-architecture`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/information-architecture`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/information-architecture`
- **`internal-linking-optimizer`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/optimize/internal-linking-optimizer`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/optimize/internal-linking-optimizer`
- **`interview-script`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/interview-script`
  - `task-folder/agents/skills/design/designer/design-research/skills/interview-script`
- **`jobs-to-be-done`** (3 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/jobs-to-be-done`
  - `task-folder/agents/skills/design/designer/design-research/skills/jobs-to-be-done`
  - `task-folder/agents/skills/strategy/jobs-to-be-done`
- **`journey-map`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/journey-map`
  - `task-folder/agents/skills/design/designer/design-research/skills/journey-map`
- **`keyword-research`** (4 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/keyword-research`
  - `task-folder/agents/skills/seo/keyword-research`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/research/keyword-research`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/seo/skills/keyword-research`
- **`law-of-common-region`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/law-of-common-region`
  - `task-folder/agents/skills/design/designer/ui-design/skills/law-of-common-region`
- **`law-of-proximity`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/law-of-proximity`
  - `task-folder/agents/skills/design/designer/ui-design/skills/law-of-proximity`
- **`layout-grid`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/layout-grid`
  - `task-folder/agents/skills/design/designer/ui-design/skills/layout-grid`
- **`learn`** (2 occurrences):
  - `task-folder/agents/skills/learn`
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/learn`
- **`lifecycle-marketing-automation`** (2 occurrences):
  - `task-folder/agents/skills/marketing/lifecycle-marketing-automation`
  - `task-folder/agents/skills/marketing/lifecycle-marketing-automation_02`
- **`link-checker`** (2 occurrences):
  - `task-folder/agents/skills/link-checker`
  - `task-folder/agents/skills/seo/seo-skills-main/seo-tools_09/link-checker`
- **`loading-states`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/loading-states`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/loading-states`
- **`localization-design`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/localization-design`
  - `task-folder/agents/skills/design/designer/design-systems/skills/localization-design`
- **`loyalty-program-optimization`** (2 occurrences):
  - `task-folder/agents/skills/marketing/loyalty-program-optimization`
  - `task-folder/agents/skills/marketing/loyalty-program-optimization_02`
- **`marketing-attribution-dashboard`** (2 occurrences):
  - `task-folder/agents/skills/marketing/marketing-attribution-dashboard`
  - `task-folder/agents/skills/marketing/marketing-attribution-dashboard_02`
- **`marketing-ideas`** (2 occurrences):
  - `task-folder/agents/skills/marketing/marketing-ideas`
  - `task-folder/agents/skills/marketing/marketing-ideas_02`
- **`marketing-plan`** (3 occurrences):
  - `task-folder/agents/skills/marketing/marketing-plan`
  - `task-folder/agents/skills/marketing/marketing-plan_02`
  - `task-folder/agents/skills/marketing/marketing-plan_02/evals`
- **`marketing-psychology`** (3 occurrences):
  - `task-folder/agents/skills/design/marketing-psychology`
  - `task-folder/agents/skills/marketing/marketing-psychology`
  - `task-folder/agents/skills/marketing/marketing-psychology_02`
- **`marketplace-advertising`** (2 occurrences):
  - `task-folder/agents/skills/marketing/marketplace-advertising_02`
  - `task-folder/agents/skills/marketing/marketplace-advertising`
- **`metrics-definition`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/metrics-definition`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/metrics-definition`
- **`micro-interaction-spec`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/micro-interaction-spec`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/micro-interaction-spec`
- **`millers-law`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/millers-law`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/millers-law`
- **`minimalist-ui`** (2 occurrences):
  - `task-folder/agents/skills/design/minimalist-skill`
  - `task-folder/agents/skills/design/minimalist-ui`
- **`motion-system`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/motion-system`
  - `task-folder/agents/skills/design/designer/design-systems/skills/motion-system`
- **`naming`** (2 occurrences):
  - `task-folder/agents/skills/design/designer/ideation/naming`
  - `task-folder/agents/skills/ideation/naming`
- **`naming-convention`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/naming-convention`
  - `task-folder/agents/skills/design/designer/design-systems/skills/naming-convention`
- **`navigation-patterns`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/navigation-patterns`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/navigation-patterns`
- **`north-star-vision`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/north-star-vision`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/north-star-vision`
- **`notebooklm`** (2 occurrences):
  - `task-folder/agents/skills/notebook-lm/notebooklm`
  - `task-folder/agents/skills/seo/seo-skills-main/notebooklm/notebooklm`
- **`notebooklm-create`** (2 occurrences):
  - `task-folder/agents/skills/notebook-lm/notebooklm-create`
  - `task-folder/agents/skills/seo/seo-skills-main/notebooklm/notebooklm-create`
- **`on-page-seo-auditor`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/optimize/on-page-seo-auditor`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/optimize/on-page-seo-auditor`
- **`onboarding`** (2 occurrences):
  - `task-folder/agents/skills/marketing/onboarding`
  - `task-folder/agents/skills/onboarding`
- **`onboarding-design`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/onboarding-design`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/onboarding-design`
- **`opportunity-framework`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/opportunity-framework`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/opportunity-framework`
- **`pattern-library`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/pattern-library`
  - `task-folder/agents/skills/design/designer/design-systems/skills/pattern-library`
- **`performance-reporter`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/monitor/performance-reporter`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/monitor/performance-reporter`
- **`positioning`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/product-marketing/skills/positioning`
  - `task-folder/agents/skills/strategy/positioning`
- **`predictive-personalization`** (2 occurrences):
  - `task-folder/agents/skills/marketing/predictive-personalization`
  - `task-folder/agents/skills/marketing/predictive-personalization_02`
- **`presentation-deck`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/designer-toolkit/skills/presentation-deck`
  - `task-folder/agents/skills/design/designer/designer-toolkit/skills/presentation-deck`
- **`pricing`** (2 occurrences):
  - `task-folder/agents/skills/marketing/pricing`
  - `task-folder/agents/skills/pricing`
- **`pricing-strategy`** (2 occurrences):
  - `task-folder/agents/skills/pricing-strategy`
  - `task-folder/agents/skills/strategy/pricing-strategy`
- **`product-launch-campaigns`** (2 occurrences):
  - `task-folder/agents/skills/marketing/product-launch-campaigns`
  - `task-folder/agents/skills/marketing/product-launch-campaigns_02`
- **`product-marketing`** (2 occurrences):
  - `task-folder/agents/skills/marketing/product-marketing`
  - `task-folder/agents/skills/marketing/product-marketing_02`
- **`programmatic-seo`** (3 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/programmatic-seo`
  - `task-folder/agents/skills/seo/seo-skills-main/programmatic-seo`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/programmatic-seo`
- **`prototype-strategy`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/prototype-strategy`
  - `task-folder/agents/skills/design/designer/prototyping-testing/skills/prototype-strategy`
- **`push-notifications`** (2 occurrences):
  - `task-folder/agents/skills/marketing/push-notifications_02`
  - `task-folder/agents/skills/marketing/push-notifications`
- **`rank-tracker`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/monitor/rank-tracker`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/monitor/rank-tracker`
- **`readable-measure`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/readable-measure`
  - `task-folder/agents/skills/design/designer/ui-design/skills/readable-measure`
- **`redesign-existing-projects`** (2 occurrences):
  - `task-folder/agents/skills/design/redesign-skill`
  - `task-folder/agents/skills/redesign-existing-projects`
- **`referral-viral-loops`** (2 occurrences):
  - `task-folder/agents/skills/marketing/referral-viral-loops_02`
  - `task-folder/agents/skills/marketing/referral-viral-loops`
- **`research-repository`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/research-repository`
  - `task-folder/agents/skills/design/designer/design-research/skills/research-repository`
- **`responsive-design`** (3 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/responsive-design`
  - `task-folder/agents/skills/design/designer/ui-design/skills/responsive-design`
  - `task-folder/agents/skills/design/designer/clean-gemini-agents/gemini-agents/skills/ux-design/responsive-design`
- **`review-generation-engine`** (2 occurrences):
  - `task-folder/agents/skills/marketing/review-generation-engine`
  - `task-folder/agents/skills/marketing/review-generation-engine_02`
- **`schema-markup`** (2 occurrences):
  - `task-folder/agents/skills/schema-markup`
  - `task-folder/agents/skills/seo/seo-skills-main/seo-tools_09/schema-markup`
- **`schema-markup-generator`** (2 occurrences):
  - `task-folder/agents/skills/schema-markup-generator`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/build/schema-markup-generator`
- **`search-ux`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/search-ux`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/search-ux`
- **`seasonal-campaign-automation`** (2 occurrences):
  - `task-folder/agents/skills/marketing/seasonal-campaign-automation`
  - `task-folder/agents/skills/marketing/seasonal-campaign-automation_02`
- **`seo`** (4 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo`
  - `task-folder/agents/skills/seo/seo-skills-main/seo`
  - `task-folder/agents/skills/seo/seo`
- **`seo-audit`** (5 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/seo-audit`
  - `task-folder/agents/skills/seo/seo-audit`
  - `task-folder/agents/skills/seo/seo-skills-main/seo-audit`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-audit`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-audit`
- **`seo-competitor-pages`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-competitor-pages`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-competitor-pages`
- **`seo-content`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-content`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-content`
- **`seo-content-brief`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/seo-content-brief`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-content-brief`
- **`seo-content-writer`** (3 occurrences):
  - `task-folder/agents/skills/seo/seo-content-writer`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/build/seo-content-writer`
  - `task-folder/agents/skills/seo/seo-skills-main/automation/content/seo-content-writer`
- **`seo-dataforseo`** (3 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/extensions/dataforseo/skills/seo-dataforseo`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-dataforseo`
  - `task-folder/agents/skills/seo/seo-dataforseo`
- **`seo-drift`** (3 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/seo-drift`
  - `task-folder/agents/skills/seo/seo-drift`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-drift`
- **`seo-geo`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-geo`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-geo`
- **`seo-hreflang`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-hreflang`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-hreflang`
- **`seo-image-gen`** (3 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/extensions/banana/skills/seo-image-gen`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-image-gen`
  - `task-folder/agents/skills/seo/seo-image-gen`
- **`seo-images`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-images`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-images`
- **`seo-page`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-page`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-page`
- **`seo-plan`** (3 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/seo-plan`
  - `task-folder/agents/skills/seo/seo-plan`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-plan`
- **`seo-programmatic`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-programmatic`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-programmatic`
- **`seo-schema`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-schema`
  - `task-folder/agents/skills/seo/seo-schema`
- **`seo-sitemap`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-sitemap`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-sitemap`
- **`seo-technical`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-technical`
  - `task-folder/agents/skills/seo/seo-skills-main/skills/seo-technical`
- **`serp-analysis`** (2 occurrences):
  - `task-folder/agents/skills/seo/serp-analysis`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/research/serp-analysis`
- **`service-blueprint`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/service-blueprint`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/service-blueprint`
- **`shadcn-ui`** (2 occurrences):
  - `task-folder/agents/skills/design/shadcn-ui`
  - `task-folder/agents/skills/shadcn/shadcn-ui`
- **`site-architecture`** (2 occurrences):
  - `task-folder/agents/skills/site-architecture`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/site-architecture`
- **`sms-marketing`** (2 occurrences):
  - `task-folder/agents/skills/marketing/sms-marketing_02`
  - `task-folder/agents/skills/marketing/sms-marketing`
- **`social-commerce`** (2 occurrences):
  - `task-folder/agents/skills/marketing/social-commerce`
  - `task-folder/agents/skills/marketing/social-commerce_02`
- **`social-proof-widgets`** (2 occurrences):
  - `task-folder/agents/skills/marketing/social-proof-widgets_02`
  - `task-folder/agents/skills/marketing/social-proof-widgets`
- **`spacing-system`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/spacing-system`
  - `task-folder/agents/skills/design/designer/ui-design/skills/spacing-system`
- **`stakeholder-alignment`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/stakeholder-alignment`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/stakeholder-alignment`
- **`state-machine`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/interaction-design/skills/state-machine`
  - `task-folder/agents/skills/design/designer/interaction-design/skills/state-machine`
- **`stitch-design-taste`** (2 occurrences):
  - `task-folder/agents/skills/design/stitch-skill`
  - `task-folder/agents/skills/stitch-design-taste`
- **`storytelling`** (3 occurrences):
  - `task-folder/agents/skills/design/storytelling`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/content-marketing/skills/storytelling`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/customer-advocacy-orchestration/skills/storytelling`
- **`summarize-interview`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/summarize-interview`
  - `task-folder/agents/skills/design/designer/design-research/skills/summarize-interview`
- **`survey-design`** (3 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/survey-design`
  - `task-folder/agents/skills/design/designer/design-research/skills/survey-design`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/customer-feedback-orchestration/skills/survey-design`
- **`team-workflow`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/team-workflow`
  - `task-folder/agents/skills/design/designer/design-ops/skills/team-workflow`
- **`technical-seo`** (2 occurrences):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/technical-seo`
  - `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/seo/skills/technical-seo`
- **`technical-seo-checker`** (2 occurrences):
  - `task-folder/agents/skills/seo/seo-skills-main/optimize/technical-seo-checker`
  - `task-folder/agents/skills/seo/seo-skills-main/geo-audit-report/SEO Audit/seo-geo-claude-skills-main 2/optimize/technical-seo-checker`
- **`test-scenario`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/test-scenario`
  - `task-folder/agents/skills/design/designer/prototyping-testing/skills/test-scenario`
- **`theme-factory`** (2 occurrences):
  - `task-folder/agents/skills/theme-factory`
  - `task-folder/agents/skills/report-writing/theme-factory`
- **`theming-system`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/theming-system`
  - `task-folder/agents/skills/design/designer/design-systems/skills/theming-system`
- **`tiktok-ads-integration`** (2 occurrences):
  - `task-folder/agents/skills/marketing/tiktok-ads-integration_02`
  - `task-folder/agents/skills/marketing/tiktok-ads-integration`
- **`tiktok-shop-integration`** (2 occurrences):
  - `task-folder/agents/skills/marketing/tiktok-shop-integration`
  - `task-folder/agents/skills/marketing/tiktok-shop-integration_02`
- **`transilience-report-style`** (2 occurrences):
  - `task-folder/agents/skills/report-writing/formats/transilience-report-style`
  - `task-folder/agents/skills/writing/formats/transilience-report-style`
- **`typography-scale`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/typography-scale`
  - `task-folder/agents/skills/design/designer/ui-design/skills/typography-scale`
- **`ui-skills`** (2 occurrences):
  - `task-folder/agents/skills/ui/ui-skills`
  - `task-folder/agents/skills/design/ui-skills`
- **`usability-test-plan`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/usability-test-plan`
  - `task-folder/agents/skills/design/designer/design-research/skills/usability-test-plan`
- **`user-flow-diagram`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/user-flow-diagram`
  - `task-folder/agents/skills/design/designer/prototyping-testing/skills/user-flow-diagram`
- **`user-persona`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-research/skills/user-persona`
  - `task-folder/agents/skills/design/designer/design-research/skills/user-persona`
- **`ux-writing`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/designer-toolkit/skills/ux-writing`
  - `task-folder/agents/skills/design/designer/designer-toolkit/skills/ux-writing`
- **`version-control-strategy`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/version-control-strategy`
  - `task-folder/agents/skills/design/designer/design-ops/skills/version-control-strategy`
- **`visual-hierarchy`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/visual-hierarchy`
  - `task-folder/agents/skills/design/designer/ui-design/skills/visual-hierarchy`
- **`von-restorff-effect`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/von-restorff-effect`
  - `task-folder/agents/skills/design/designer/ui-design/skills/von-restorff-effect`
- **`web-scraper`** (2 occurrences):
  - `task-folder/agents/skills/web-scraper`
  - `task-folder/agents/skills/seo/seo-skills-main/automation/web-scraper`
- **`win-back-reactivation`** (2 occurrences):
  - `task-folder/agents/skills/marketing/win-back-reactivation_02`
  - `task-folder/agents/skills/marketing/win-back-reactivation`
- **`wireframe-spec`** (2 occurrences):
  - `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/wireframe-spec`
  - `task-folder/agents/skills/design/designer/prototyping-testing/skills/wireframe-spec`
- **`writing-skills`** (2 occurrences):
  - `task-folder/agents/skills/figma/writing-skills`
  - `task-folder/agents/skills/writing/writing-skills`

## Folder & Frontmatter Name Mismatches

The following skill folders contain frontmatter names that do not match the physical folder name. These should be normalized during the repair phase:

| Path | Folder Name | Frontmatter Name |
| :--- | :--- | :--- |
| `task-folder/agents/skills/design/brandkit2` | `brandkit2` | `brandkit` |
| `task-folder/agents/skills/design/brutalist-skill` | `brutalist-skill` | `industrial-brutalist-ui` |
| `task-folder/agents/skills/design/design-md_v1` | `design-md_v1` | `design-md` |
| `task-folder/agents/skills/design/design-review_2` | `design-review_2` | `design-review` |
| `task-folder/agents/skills/design/deterministic-design/design-audit/taste-skill` | `taste-skill` | `design-taste-frontend` |
| `task-folder/agents/skills/design/deterministic-design/design-audit/taste-skill-v1` | `taste-skill-v1` | `design-taste-frontend-v1` |
| `task-folder/agents/skills/design/gpt-tasteskill` | `gpt-tasteskill` | `gpt-taste` |
| `task-folder/agents/skills/design/image-to-code-skill` | `image-to-code-skill` | `image-to-code` |
| `task-folder/agents/skills/design/minimalist-skill` | `minimalist-skill` | `minimalist-ui` |
| `task-folder/agents/skills/design/output-skill` | `output-skill` | `full-output-enforcement` |
| `task-folder/agents/skills/design/redesign-skill` | `redesign-skill` | `redesign-existing-projects` |
| `task-folder/agents/skills/design/soft-skill` | `soft-skill` | `high-end-visual-design` |
| `task-folder/agents/skills/design/stitch-skill` | `stitch-skill` | `stitch-design-taste` |
| `task-folder/agents/skills/design/taste-skill` | `taste-skill` | `design-taste-frontend` |
| `task-folder/agents/skills/design/taste-skill-v1` | `taste-skill-v1` | `design-taste-frontend-v1` |
| `task-folder/agents/skills/design/ui-skills/image-to-code-skill` | `image-to-code-skill` | `image-to-code` |
| `task-folder/agents/skills/email/email-design-eng` | `email-design-eng` | `emil-design-eng` |
| `task-folder/agents/skills/email/email-sequence2` | `email-sequence2` | `email-sequence` |
| `task-folder/agents/skills/figma` | `figma` | `figma-automation` |
| `task-folder/agents/skills/front end/frontend-design2` | `frontend-design2` | `frontend-design` |
| `task-folder/agents/skills/github/actions-advanced` | `actions-advanced` | `github-actions-advanced` |
| `task-folder/agents/skills/github/actions-debugger` | `actions-debugger` | `github-actions-debugger` |
| `task-folder/agents/skills/github/actions-templates` | `actions-templates` | `github-actions-templates` |
| `task-folder/agents/skills/github/advanced-workflows` | `advanced-workflows` | `git-advanced-workflows` |
| `task-folder/agents/skills/github/automation` | `automation` | `github-automation` |
| `task-folder/agents/skills/github/commit` | `commit` | `git-commit` |
| `task-folder/agents/skills/github/flow-branch-creator` | `flow-branch-creator` | `git-flow-branch-creator` |
| `task-folder/agents/skills/github/hooks-automation` | `hooks-automation` | `git-hooks-automation` |
| `task-folder/agents/skills/github/image` | `image` | `gh-image` |
| `task-folder/agents/skills/github/issue-creator` | `issue-creator` | `github-issue-creator` |
| `task-folder/agents/skills/github/llms-create` | `llms-create` | `create-llms` |
| `task-folder/agents/skills/github/llms-update` | `llms-update` | `update-llms` |
| `task-folder/agents/skills/github/pr-review` | `pr-review` | `git-pr-review` |
| `task-folder/agents/skills/github/pr-workflows-onboard` | `pr-workflows-onboard` | `git-pr-workflows-onboard` |
| `task-folder/agents/skills/github/pr-workflows-pr-enhance` | `pr-workflows-pr-enhance` | `git-pr-workflows-pr-enhance` |
| `task-folder/agents/skills/github/pr-workflows-workflow` | `pr-workflows-workflow` | `git-pr-workflows-git-workflow` |
| `task-folder/agents/skills/github/presence` | `presence` | `github-presence` |
| `task-folder/agents/skills/github/pushing` | `pushing` | `git-pushing` |
| `task-folder/agents/skills/github/review-requests` | `review-requests` | `gh-review-requests` |
| `task-folder/agents/skills/github/security-review` | `security-review` | `gha-security-review` |
| `task-folder/agents/skills/github/workflow-automation` | `workflow-automation` | `github-workflow-automation` |
| `task-folder/agents/skills/github/workflow-versioning` | `workflow-versioning` | `git-workflow-and-versioning` |
| `task-folder/agents/skills/ideation/brainstorming2` | `brainstorming2` | `brainstorming` |
| `task-folder/agents/skills/marketing/affiliate-program_02` | `affiliate-program_02` | `affiliate-program` |
| `task-folder/agents/skills/marketing/co-marketing_02` | `co-marketing_02` | `co-marketing` |
| `task-folder/agents/skills/marketing/content-commerce_02` | `content-commerce_02` | `content-commerce` |
| `task-folder/agents/skills/marketing/influencer-marketplace-integration_02` | `influencer-marketplace-integration_02` | `influencer-marketplace-integration` |
| `task-folder/agents/skills/marketing/influencer-tracking_02` | `influencer-tracking_02` | `influencer-tracking` |
| `task-folder/agents/skills/marketing/lifecycle-marketing-automation_02` | `lifecycle-marketing-automation_02` | `lifecycle-marketing-automation` |
| `task-folder/agents/skills/marketing/loyalty-program-optimization_02` | `loyalty-program-optimization_02` | `loyalty-program-optimization` |
| `task-folder/agents/skills/marketing/marketing-attribution-dashboard_02` | `marketing-attribution-dashboard_02` | `marketing-attribution-dashboard` |
| `task-folder/agents/skills/marketing/marketing-ideas_02` | `marketing-ideas_02` | `marketing-ideas` |
| `task-folder/agents/skills/marketing/marketing-plan_02` | `marketing-plan_02` | `marketing-plan` |
| `task-folder/agents/skills/marketing/marketing-plan_02/evals` | `evals` | `marketing-plan` |
| `task-folder/agents/skills/marketing/marketing-psychology_02` | `marketing-psychology_02` | `marketing-psychology` |
| `task-folder/agents/skills/marketing/marketplace-advertising_02` | `marketplace-advertising_02` | `marketplace-advertising` |
| `task-folder/agents/skills/marketing/predictive-personalization_02` | `predictive-personalization_02` | `predictive-personalization` |
| `task-folder/agents/skills/marketing/product-launch-campaigns_02` | `product-launch-campaigns_02` | `product-launch-campaigns` |
| `task-folder/agents/skills/marketing/product-marketing_02` | `product-marketing_02` | `product-marketing` |
| `task-folder/agents/skills/marketing/push-notifications_02` | `push-notifications_02` | `push-notifications` |
| `task-folder/agents/skills/marketing/referral-viral-loops_02` | `referral-viral-loops_02` | `referral-viral-loops` |
| `task-folder/agents/skills/marketing/review-generation-engine_02` | `review-generation-engine_02` | `review-generation-engine` |
| `task-folder/agents/skills/marketing/seasonal-campaign-automation_02` | `seasonal-campaign-automation_02` | `seasonal-campaign-automation` |
| `task-folder/agents/skills/marketing/sms-marketing_02` | `sms-marketing_02` | `sms-marketing` |
| `task-folder/agents/skills/marketing/social-commerce_02` | `social-commerce_02` | `social-commerce` |
| `task-folder/agents/skills/marketing/social-proof-widgets_02` | `social-proof-widgets_02` | `social-proof-widgets` |
| `task-folder/agents/skills/marketing/tiktok-ads-integration_02` | `tiktok-ads-integration_02` | `tiktok-ads-integration` |
| `task-folder/agents/skills/marketing/tiktok-shop-integration_02` | `tiktok-shop-integration_02` | `tiktok-shop-integration` |
| `task-folder/agents/skills/marketing/win-back-reactivation_02` | `win-back-reactivation_02` | `win-back-reactivation` |
| `task-folder/agents/skills/report-writing` | `report-writing` | `olakai-reports` |
| `task-folder/agents/skills/seo/seo-skills-main` | `seo-skills-main` | `seo` |
| `task-folder/agents/skills/seo/seo-skills-main/frontend` | `frontend` | `techstack-frontend` |
| `task-folder/agents/skills/webflow/webflow-cli-cloud` | `webflow-cli-cloud` | `webflow-cli:cloud` |
| `task-folder/agents/skills/webflow/webflow-cli-code-component` | `webflow-cli-code-component` | `webflow-cli:code-component` |
| `task-folder/agents/skills/webflow/webflow-cli-designer-extension` | `webflow-cli-designer-extension` | `webflow-cli:designer-extension` |
| `task-folder/agents/skills/webflow/webflow-cli-devlink` | `webflow-cli-devlink` | `webflow-cli:devlink` |
| `task-folder/agents/skills/webflow/webflow-cli-troubleshooter` | `webflow-cli-troubleshooter` | `webflow-cli:troubleshooter` |
| `task-folder/agents/skills/webflow/webflow-code-component-component-audit` | `webflow-code-component-component-audit` | `webflow-code-component:component-audit` |
| `task-folder/agents/skills/webflow/webflow-code-component-component-scaffold` | `webflow-code-component-component-scaffold` | `webflow-code-component:component-scaffold` |
| `task-folder/agents/skills/webflow/webflow-code-component-convert-component` | `webflow-code-component-convert-component` | `webflow-code-component:convert-component` |
| `task-folder/agents/skills/webflow/webflow-code-component-deploy-guide` | `webflow-code-component-deploy-guide` | `webflow-code-component:deploy-guide` |
| `task-folder/agents/skills/webflow/webflow-code-component-local-dev-setup` | `webflow-code-component-local-dev-setup` | `webflow-code-component:local-dev-setup` |
| `task-folder/agents/skills/webflow/webflow-code-component-pre-deploy-check` | `webflow-code-component-pre-deploy-check` | `webflow-code-component:pre-deploy-check` |
| `task-folder/agents/skills/webflow/webflow-code-component-troubleshoot-deploy` | `webflow-code-component-troubleshoot-deploy` | `webflow-code-component:troubleshoot-deploy` |

## Potential Overlap Clusters (Candidate Groups)

The following groups share folder-name prefixes or category signals and represent high-probability candidates for merge or refinement review in Phase 03:

- **Cluster `seo`** (85 skills):
  - `task-folder/agents/skills/design/seo-optimizer`
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/seo-audit`
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/seo-drift`
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/seo-implement`
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/seo-plan`
  - ... and 80 more
- **Cluster `design`** (50 skills):
  - `task-folder/agents/skills/design/design-an-interface`
  - `task-folder/agents/skills/design/design-brief`
  - `task-folder/agents/skills/design/design-consultation`
  - `task-folder/agents/skills/design/design-it`
  - `task-folder/agents/skills/design/design-loop`
  - ... and 45 more
- **Cluster `content`** (27 skills):
  - `task-folder/agents/skills/content/content-creator`
  - `task-folder/agents/skills/content/content-marketer`
  - `task-folder/agents/skills/content/content-strategy`
  - `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/content-strategy`
  - `task-folder/agents/skills/design/designer/ux-strategy/skills/content-strategy`
  - ... and 22 more
- **Cluster `frontend`** (24 skills):
  - `task-folder/agents/skills/design/frontend-design`
  - `task-folder/agents/skills/design/frontend-dev`
  - `task-folder/agents/skills/design/frontend-enhancer`
  - `task-folder/agents/skills/design/frontend-skill`
  - `task-folder/agents/skills/design/frontend-slides`
  - ... and 19 more
- **Cluster `code`** (18 skills):
  - `task-folder/agents/skills/code/code-documentation`
  - `task-folder/agents/skills/code/code-documentation-code-explain`
  - `task-folder/agents/skills/code/code-documentation-doc-generate`
  - `task-folder/agents/skills/code/code-polish`
  - `task-folder/agents/skills/code/code-refactoring-context-restore`
  - ... and 13 more
- **Cluster `data`** (17 skills):
  - `task-folder/agents/skills/data-analytics/data-profiling`
  - `task-folder/agents/skills/data-analytics/data-storytelling`
  - `task-folder/agents/skills/data/data-engineer`
  - `task-folder/agents/skills/data/data-engineering-data-driven-feature`
  - `task-folder/agents/skills/data/data-engineering-data-pipeline`
  - ... and 12 more
- **Cluster `api`** (17 skills):
  - `task-folder/agents/skills/api/api-analyzer`
  - `task-folder/agents/skills/api/api-and-interface-design`
  - `task-folder/agents/skills/api/api-design-principles`
  - `task-folder/agents/skills/api/api-designer`
  - `task-folder/agents/skills/api/api-documentation`
  - ... and 12 more
- **Cluster `brand`** (16 skills):
  - `task-folder/agents/skills/brand-guidelines`
  - `task-folder/agents/skills/brand-guidelines-anthropic`
  - `task-folder/agents/skills/brand-guidelines-community`
  - `task-folder/agents/skills/brand-perception-psychologist`
  - `task-folder/agents/skills/design/brand-analyzer`
  - ... and 11 more
- **Cluster `webflow`** (16 skills):
  - `task-folder/agents/skills/webflow/webflow-automation`
  - `task-folder/agents/skills/webflow/webflow-cli-cloud`
  - `task-folder/agents/skills/webflow/webflow-cli-code-component`
  - `task-folder/agents/skills/webflow/webflow-cli-designer-extension`
  - `task-folder/agents/skills/webflow/webflow-cli-devlink`
  - ... and 11 more
- **Cluster `social`** (15 skills):
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/social-strategy`
  - `task-folder/agents/skills/marketing/social`
  - `task-folder/agents/skills/marketing/social-commerce`
  - `task-folder/agents/skills/marketing/social-commerce_02`
  - `task-folder/agents/skills/marketing/social-proof-widgets`
  - ... and 10 more
- **Cluster `context`** (14 skills):
  - `task-folder/agents/skills/context/context-agent`
  - `task-folder/agents/skills/context/context-compression`
  - `task-folder/agents/skills/context/context-degradation`
  - `task-folder/agents/skills/context/context-driven-development`
  - `task-folder/agents/skills/context/context-engineering`
  - ... and 9 more
- **Cluster `competitor`** (14 skills):
  - `task-folder/agents/skills/marketing/competitor-analysis`
  - `task-folder/agents/skills/marketing/competitor-profiling`
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/competitor-alerts`
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/competitor-analysis`
  - `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/competitor-monitor`
  - ... and 9 more
- **Cluster `agent`** (13 skills):
  - `task-folder/agents/skills/agents/agent-creator`
  - `task-folder/agents/skills/agents/agent-evaluation`
  - `task-folder/agents/skills/agents/agent-manager-skill`
  - `task-folder/agents/skills/agents/agent-memory`
  - `task-folder/agents/skills/agents/agent-memory-mcp`
  - ... and 8 more
- **Cluster `product`** (13 skills):
  - `task-folder/agents/skills/data-analytics/data-analytics/product-analytics`
  - `task-folder/agents/skills/marketing/product-launch-campaigns`
  - `task-folder/agents/skills/marketing/product-launch-campaigns_02`
  - `task-folder/agents/skills/marketing/product-marketing`
  - `task-folder/agents/skills/marketing/product-marketing-context`
  - ... and 8 more
- **Cluster `hugging`** (13 skills):
  - `task-folder/agents/skills/hugging face/hugging-face-cli`
  - `task-folder/agents/skills/hugging face/hugging-face-community-evals`
  - `task-folder/agents/skills/hugging face/hugging-face-dataset-viewer`
  - `task-folder/agents/skills/hugging face/hugging-face-datasets`
  - `task-folder/agents/skills/hugging face/hugging-face-evaluation`
  - ... and 8 more

## Orphaned & Static Resources

No orphaned resources were discovered at the root level of the skills directory.

## Existing Source-Content Findings (For Later Repair)

> [!WARNING]
> The following pre-existing source skills contain hardcoded local absolute paths or user-specific directories (such as `~/`). These represent **source-content anomalies** that must be repaired in a later phase to ensure complete portability across teammate worktrees:

- `task-folder/agents/skills/using-git-worktrees`: contains `~/`
- `task-folder/agents/skills/audio-transcriber`: contains `o:\`
- `task-folder/agents/skills/design/designer/ce-plan`: contains `~/`
- `task-folder/agents/skills/webflow/webflow-cli-code-component`: contains `~/`
- `task-folder/agents/skills/webflow/webflow-cli-devlink`: contains `~/`
- `task-folder/agents/skills/earllm-build`: contains `C:\`
- `task-folder/agents/skills/llm/llm/llm-app-patterns`: contains `e:\, s:\`
- `task-folder/agents/skills/context/context-guardian`: contains `C:\`
- `task-folder/agents/skills/context/context-agent`: contains `C:\`
- `task-folder/agents/skills/embedding-strategies`: contains `e:\`
- `task-folder/agents/skills/python/pydantic-ai`: contains `e:\, h:\`
- `task-folder/agents/skills/images/image-studio`: contains `C:\`
- `task-folder/agents/skills/conversation-memory`: contains `r:\, s:\`
- `task-folder/agents/skills/privilege-escalation-methods`: contains `~/, C:\, z:\`
- `task-folder/agents/skills/007`: contains `C:\`
- `task-folder/agents/skills/front end/frontend-slides-frontend-slides`: contains `~/`
- `task-folder/agents/skills/rclone-cli`: contains `~/`
- `task-folder/agents/skills/leiloeiro-avaliacao`: contains `C:\`
- `task-folder/agents/skills/speckit-updater`: contains `C:\`
- `task-folder/agents/skills/cloud-penetration-testing`: contains `~/, C:\`
- `task-folder/agents/skills/agents/agentic-eval`: contains `k:\`
- `task-folder/agents/skills/agents/multi-agent-architect`: contains `h:\, s:\, y:\`
- `task-folder/agents/skills/blockrun`: contains `~/`
- `task-folder/agents/skills/auri-core`: contains `~/`
- `task-folder/agents/skills/autonomous-agent-patterns`: contains `s:\`
- `task-folder/agents/skills/n8n/n8n-multi-instance`: contains `e:\`
- `task-folder/agents/skills/social/social-networks/instagram`: contains `C:\`
- `task-folder/agents/skills/social/social-metadata-hardening`: contains `g:\`
- `task-folder/agents/skills/networks/network-101`: contains `C:\`
- `task-folder/agents/skills/ai/ai-studio-image`: contains `C:\`
- `task-folder/agents/skills/linux/linux-privilege-escalation`: contains `~/`
- `task-folder/agents/skills/unslop-file`: contains `C:\`
- `task-folder/agents/skills/prompts/prompt-engineering-patterns`: contains `L:\`
- `task-folder/agents/skills/files/file-path-traversal`: contains `~/, C:\`
- `task-folder/agents/skills/api/api-fuzzing-bug-bounty`: contains `C:\`
- `task-folder/agents/skills/api/api-security-best-practices`: contains `r:\`
- `task-folder/agents/skills/advogado-criminal`: contains `C:\`
- `task-folder/agents/skills/antigravity/antigravity-agent-manager`: contains `~/`
- `task-folder/agents/skills/statsmodels`: contains `s:\`
- `task-folder/agents/skills/computer-use-agents`: contains `~/`
- `task-folder/agents/skills/react/react-flow-architect`: contains `d:\, s:\`
- `task-folder/agents/skills/devcontainer-setup`: contains `~/`
- `task-folder/agents/skills/langchain-architecture`: contains `e:\`
- `task-folder/agents/skills/1password`: contains `~/`
- `task-folder/agents/skills/pm2`: contains `C:\`
- `task-folder/agents/skills/writing/competitor-analysis`: contains `h:\`
