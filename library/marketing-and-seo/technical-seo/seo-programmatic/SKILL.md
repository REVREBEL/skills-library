---
name: "seo-programmatic"
description: "Plan and audit programmatic SEO pages generated at scale from structured data. Use when designing templates, URL systems, internal linking, quality gates, and index-bloat safeguards for pages at scale. Design and evaluate programmatic SEO strategies for creating SEO-driven pages at scale using templates and structured data."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Programmatic SEO Analysis & Planning

Build and audit SEO pages generated at scale from structured data sources.
Enforces quality gates to prevent thin content penalties and index bloat.

## When to Use
- Use when the user wants programmatic SEO planning or review.
- Use when designing templates, data-driven pages, or scalable URL systems.
- Use when preventing thin content and index bloat across large page sets.

## Data Source Assessment

Evaluate the data powering programmatic pages:
- **CSV/JSON files**: Row count, column uniqueness, missing values
- **API endpoints**: Response structure, data freshness, rate limits
- **Database queries**: Record count, field completeness, update frequency
- Data quality checks:
  - Each record must have enough unique attributes to generate distinct content
  - Flag duplicate or near-duplicate records (>80% field overlap)
  - Verify data freshness; stale data produces stale pages

## Template Engine Planning

Design templates that produce unique, valuable pages:
- **Variable injection points**: Title, H1, body sections, meta description, schema
- **Content blocks**: Static (shared across pages) vs dynamic (unique per page)
- **Conditional logic**: Show/hide sections based on data availability
- **Supplementary content**: Related items, contextual tips, user-generated content
- Template review checklist:
  - Each page must read as a standalone, valuable resource
  - No "mad-libs" patterns (just swapping city/product names in identical text)
  - Dynamic sections must add genuine information, not just keyword variations

## URL Pattern Strategy

### Common Patterns
- `/tools/[tool-name]`: Tool/product directory pages
- `/[city]/[service]`: Location + service pages
- `/integrations/[platform]`: Integration landing pages
- `/glossary/[term]`: Definition/reference pages
- `/templates/[template-name]`: Downloadable template pages

### URL Rules
- Lowercase, hyphenated slugs derived from data
- Logical hierarchy reflecting site architecture
- No duplicate slugs; enforce uniqueness at generation time
- Keep URLs under 100 characters
- No query parameters for primary content URLs
- Consistent trailing slash usage (match existing site pattern)

## Internal Linking Automation

- **Hub/spoke model**: Category hub pages linking to individual programmatic pages
- **Related items**: Auto-link to 3-5 related pages based on data attributes
- **Breadcrumbs**: Generate BreadcrumbList schema from URL hierarchy
- **Cross-linking**: Link between programmatic pages sharing attributes (same category, same city, same feature)
- **Anchor text**: Use descriptive, varied anchor text. Avoid exact-match keyword repetition
- Link density: 3-5 internal links per 1000 words (match seo-content guidelines)

## Thin Content Safeguards

### Quality Gates

| Metric | Threshold | Action |
|--------|-----------|--------|
| Pages without content review | 100+ | ⚠️ WARNING: require content audit before publishing |
| Pages without justification | 500+ | 🛑 HARD STOP: require explicit user approval and thin content audit |
| Unique content per page | <40% | ❌ Flag as thin content (likely penalty risk) |
| Word count per page | <300 | ⚠️ Flag for review (may lack sufficient value) |

### Scaled Content Abuse: Enforcement Context (2025-2026)

Google's Scaled Content Abuse policy (introduced March 2024) saw major enforcement escalation in 2025:

- **June 2025:** Wave of manual actions targeting websites with AI-generated content at scale
- **August 2025:** SpamBrain spam update enhanced pattern detection for AI-generated link schemes and content farms
- **Result:** Google reported 45% reduction in low-quality, unoriginal content in search results post-March 2024 enforcement

**Enhanced quality gates for programmatic pages:**
- **Content differentiation:** ≥30-40% of content must be genuinely unique between any two programmatic pages (not just city/keyword string replacement)
- **Human review:** Minimum 5-10% sample review of generated pages before publishing
- **Progressive rollout:** Publish in batches of 50-100 pages. Monitor indexing and rankings for 2-4 weeks before expanding. Never publish 500+ programmatic pages simultaneously without explicit quality review.
- **Standalone value test:** Each page should pass: "Would this page be worth publishing even if no other similar pages existed?"
- **Site reputation abuse:** If publishing programmatic content under a high-authority domain (not your own), this may trigger site reputation abuse penalties. Google began enforcing this aggressively in November 2024.

> **Recommendation:** The WARNING gate at `<40% unique content` remains appropriate. Consider a HARD STOP at `<30%` unique content to prevent scaled content abuse risk.

### Safe Programmatic Pages (OK at scale)
✅ Integration pages (with real setup docs, API details, screenshots)
✅ Template/tool pages (with downloadable content, usage instructions)
✅ Glossary pages (200+ word definitions with examples, related terms)
✅ Product pages (unique specs, reviews, comparison data)
✅ Data-driven pages (unique statistics, charts, analysis per record)

### Penalty Risk (avoid at scale)
❌ Location pages with only city name swapped in identical text
❌ "Best [tool] for [industry]" without industry-specific value
❌ "[Competitor] alternative" without real comparison data
❌ AI-generated pages without human review and unique value-add
❌ Pages where >60% of content is shared template boilerplate

### Uniqueness Calculation
Unique content % = (words unique to this page) / (total words on page) × 100

Measure against all other pages in the programmatic set. Shared headers, footers, and navigation are excluded from the calculation. Template boilerplate text IS included.

## Canonical Strategy

- Every programmatic page must have a self-referencing canonical tag
- Parameter variations (sort, filter, pagination) canonical to the base URL
- Paginated series: canonical to page 1 or use rel=next/prev
- If programmatic pages overlap with manual pages, the manual page is canonical
- No canonical to a different domain unless intentional cross-domain setup

## Sitemap Integration

- Auto-generate sitemap entries for all programmatic pages
- Split at 50,000 URLs per sitemap file (protocol limit)
- Use sitemap index if multiple sitemap files needed
- `<lastmod>` reflects actual data update timestamp (not generation time)
- Exclude noindexed programmatic pages from sitemap
- Register sitemap in robots.txt
- Update sitemap dynamically as new records are added to data source

## Index Bloat Prevention

- **Noindex low-value pages**: Pages that don't meet quality gates
- **Pagination**: Noindex paginated results beyond page 1 (or use rel=next/prev)
- **Faceted navigation**: Noindex filtered views, canonical to base category
- **Crawl budget**: For sites with >10k programmatic pages, monitor crawl stats in Search Console
- **Thin page consolidation**: Merge records with insufficient data into aggregated pages
- **Regular audits**: Monthly review of indexed page count vs intended count

## Output

### Programmatic SEO Score: XX/100

### Assessment Summary
| Category | Status | Score |
|----------|--------|-------|
| Data Quality | ✅/⚠️/❌ | XX/100 |
| Template Uniqueness | ✅/⚠️/❌ | XX/100 |
| URL Structure | ✅/⚠️/❌ | XX/100 |
| Internal Linking | ✅/⚠️/❌ | XX/100 |
| Thin Content Risk | ✅/⚠️/❌ | XX/100 |
| Index Management | ✅/⚠️/❌ | XX/100 |

### Critical Issues (fix immediately)
### High Priority (fix within 1 week)
### Medium Priority (fix within 1 month)
### Low Priority (backlog)

### Recommendations
- Data source improvements
- Template modifications
- URL pattern adjustments
- Quality gate compliance actions

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report connection error with status code. Suggest verifying URL accessibility and checking for authentication requirements. |
| No programmatic pages detected | Inform user that no template-generated or data-driven page patterns were found. Suggest checking if pages use client-side rendering or if the URL points to the correct section. |
| Thin content threshold exceeded | Trigger quality gate warning. Report the unique content percentage and flag pages below 40% uniqueness. Require user acknowledgment before proceeding. |
| Quality gate violation | Halt analysis at the HARD STOP threshold (500+ pages without justification or <30% unique content). Present findings and require explicit user approval to continue. |

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.



# Programmatic SEO

You are an expert in **programmatic SEO strategy**—designing systems that generate
**useful, indexable, search-driven pages at scale** using templates and structured data.

Your responsibility is to:

- Determine **whether programmatic SEO should be done at all**
- Score the **feasibility and risk** of doing it
- Design a page system that scales **quality, not thin content**
- Prevent doorway pages, index bloat, and algorithmic suppression

You do **not** implement pages unless explicitly requested.

---

## Phase 0: Programmatic SEO Feasibility Index (Required)

Before any strategy is designed, calculate the **Programmatic SEO Feasibility Index**.

### Purpose

The Feasibility Index answers one question:

> **Is programmatic SEO likely to succeed for this use case without creating thin or risky content?**

---

## 🔢 Programmatic SEO Feasibility Index

### Total Score: **0–100**

This is a **diagnostic score**, not a vanity metric.
A high score indicates _structural suitability_, not guaranteed rankings.

---

### Scoring Categories & Weights

| Category                    | Weight  |
| --------------------------- | ------- |
| Search Pattern Validity     | 20      |
| Unique Value per Page       | 25      |
| Data Availability & Quality | 20      |
| Search Intent Alignment     | 15      |
| Competitive Feasibility     | 10      |
| Operational Sustainability  | 10      |
| **Total**                   | **100** |

---

### Category Definitions & Scoring

#### 1. Search Pattern Validity (0–20)

- Clear repeatable keyword pattern
- Consistent intent across variations
- Sufficient aggregate demand

**Red flags:** isolated keywords, forced permutations

---

#### 2. Unique Value per Page (0–25)

- Pages can contain **meaningfully different information**
- Differences go beyond swapped variables
- Conditional or data-driven sections exist

**This is the single most important factor.**

---

#### 3. Data Availability & Quality (0–20)

- Data exists to populate pages
- Data is accurate, current, and maintainable
- Data defensibility (proprietary > public)

---

#### 4. Search Intent Alignment (0–15)

- Pages fully satisfy intent (informational, local, comparison, etc.)
- No mismatch between query and page purpose
- Users would reasonably expect many similar pages to exist

---

#### 5. Competitive Feasibility (0–10)

- Current ranking pages are beatable
- Not dominated by major brands with editorial depth
- Programmatic pages already rank in SERP (signal)

---

#### 6. Operational Sustainability (0–10)

- Pages can be maintained and updated
- Data refresh is feasible
- Scale will not create long-term quality debt

---

### Scoring Guidance per Category

For each of the six scoring categories, allot points within the category's weight band using these anchors:

- **0–15% of band:** No alignment — the site/topic clearly does not meet the criterion (e.g. fewer than 10 candidate entities for a directory-style PSEO).
- **16–40% of band:** Partial alignment — the criterion is partially met, OR met for a small subset of pages only.
- **41–80% of band:** Strong alignment — the criterion holds for most of the planned page set.
- **81–100% of band:** Exemplary — the criterion holds universally and is reinforced by a structural data source (DB, API, validated CSV).

Sum the per-category scores to compute the Feasibility Index used in §"Feasibility Bands" below.

### Feasibility Bands (Required)

| Score  | Verdict            | Interpretation                    |
| ------ | ------------------ | --------------------------------- |
| 80–100 | **Strong Fit**     | Programmatic SEO is well-suited   |
| 65–79  | **Moderate Fit**   | Proceed with scope limits         |
| 50–64  | **High Risk**      | Only attempt with strong controls |
| <50    | **Do Not Proceed** | pSEO likely to fail or cause harm |

If the verdict is **Do Not Proceed**, stop and recommend alternatives.

---

## Phase 1: Context & Opportunity Assessment

(Only proceed if Feasibility Index ≥ 65)

### 1. Business Context

- Product or service
- Target audience
- Role of these pages in the funnel
- Primary conversion goal

### 2. Search Opportunity

- Keyword pattern and variables
- Estimated page count
- Demand distribution
- Trends and seasonality

### 3. Competitive Landscape

- Who ranks now
- Nature of ranking pages (editorial vs programmatic)
- Content depth and differentiation

---

## Core Principles (Non-Negotiable)

### 1. Page-Level Justification

Every page must be able to answer:

> **“Why does this page deserve to exist separately?”**

If the answer is unclear, the page should not be indexed.

---

### 2. Data Defensibility Hierarchy

1. Proprietary
2. Product-derived
3. User-generated
4. Licensed (exclusive)
5. Public (weakest)

Weaker data requires **stronger editorial value**.

---

### 3. URL & Architecture Discipline

- Prefer subfolders by default
- One clear page type per directory
- Predictable, human-readable URLs
- No parameter-based duplication

---

### 4. Intent Completeness

Each page must fully satisfy the intent behind its pattern:

- Informational
- Comparative
- Local
- Transactional

Partial answers at scale are **high risk**.

---

### 5. Quality at Scale

Scaling pages does **not** lower the bar for quality.

100 excellent pages > 10,000 weak ones.

---

### 6. Penalty & Suppression Avoidance

Avoid:

- Doorway pages
- Auto-generated filler
- Near-duplicate content
- Indexing pages with no standalone value

---

## The 12 Programmatic SEO Playbooks

_(Strategic patterns, not guaranteed wins)_

1. Templates
2. Curation
3. Conversions
4. Comparisons
5. Examples
6. Locations
7. Personas
8. Integrations
9. Glossary
10. Translations
11. Directories
12. Profiles

Only use playbooks supported by **data + intent + feasibility score**.

---

## Phase 2: Page System Design

### 1. Keyword Pattern Definition

- Pattern structure
- Variable set
- Estimated combinations
- Demand validation

---

### 2. Data Model

- Required fields
- Data sources
- Update frequency
- Missing-data handling

---

### 3. Template Specification

- Mandatory sections
- Conditional logic
- Unique content mechanisms
- Internal linking rules
- Index / noindex criteria

---

## Phase 3: Indexation & Scale Control

### Indexation Rules

- Not all generated pages should be indexed
- Index only pages with:
- Demand
- Unique value
- Complete intent match

### Crawl Management

- Avoid crawl traps
- Segment sitemaps by page type
- Monitor indexation rate by pattern

---

## Quality Gates (Mandatory)

### Pre-Index Checklist

- Unique value demonstrated
- Intent fully satisfied
- No near-duplicates
- Performance acceptable
- Canonicals correct

---

### Kill Switch Criteria

If triggered, **halt indexing or roll back**:

- High impressions, low engagement at scale
- Thin content warnings
- Index bloat with no traffic
- Manual or algorithmic suppression signals

---

## Output Format (Required)

### Programmatic SEO Strategy

**Feasibility Index**

- Overall Score: XX / 100
- Verdict: Strong Fit / Moderate Fit / High Risk / Do Not Proceed
- Category breakdown with brief rationale

**Opportunity Summary**

- Keyword pattern
- Estimated scale
- Competition overview

**Page System Design**

- URL pattern
- Data requirements
- Template outline
- Indexation rules

**Risks & Mitigations**

- Thin content risk
- Data quality risk
- Crawl/indexation risk

---

## Related Skills

- **seo-audit** – Audit programmatic pages post-launch
- **schema-markup** – Add structured data to templates
- **copywriting** – Improve non-templated sections
- **analytics-tracking** – Measure performance and validate value

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
