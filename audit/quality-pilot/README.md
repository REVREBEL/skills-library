# Quality Pilot — Data Analytics & Reporting

**Scope:** `library/data-and-ai/analytics/` — 37 canonical skills
**Purpose:** test whether structural triage can get the library to a defensible size before
scaling to the other three domains.
**Method limitation:** this is triage from headings, descriptions and file structure. It is
**not** a full read of every body. It identifies which skills need deep review; it does not
replace that review.

---

## 1. Headline

Structural triage alone removes about **40%** of this domain:

| Verdict | Skills |
|---|---:|
| keep | 15 |
| merge | 8 → 4 |
| rewrite | 3 |
| review | 3 |
| move out | 8 |
| **total** | **37** |

After triage the domain holds roughly **25 in-domain skills**, of which 3 still need a
provider decision and 3 need rewriting. Net: **37 → ~22**.

## 2. What the pilot actually found

The initial hypothesis was duplication. That was wrong, and the correction matters.

**The 13 ecommerce skills are not duplicates.** They share a template skeleton —
`Overview / When to Use / Core Instructions / Steps / Best Practices / Common Pitfalls` —
but their content is genuinely different: budgeting is not margin analysis, and margin
analysis is not revenue recognition. Mean pairwise text similarity is only **0.22**.

What they actually share is a **weak step**:

> "Step 1: Choose the right tool for your platform"

That is not guidance. It pushes the decision back to the user in a section that should be
opinionated. Thirteen skills with the same non-answer is what makes them feel interchangeable.

**Real duplication is small.** Only four merge groups:

| Group | Skills | Basis |
|---|---|---|
| analytics + analytics-tracking | 2 | same measurement-setup ground |
| financial-analytics-dashboard + financial-reporting-dashboard | 2 | highest similarity in the set (0.32) |
| email-list-segmentation + lifecycle-marketing-automation | 2 | same lifecycle segmentation |
| customer-analytics + unit-economics-tracking | 2 | same RFM and segmentation |

**Misfiled skills are the bigger win.** 8 of 37 are not analytics at all:

- `computer-vision-expert`, `hugging-face-vision-trainer` → machine learning
- `custom-code-management` → development/frontend (Webflow)
- `four-core-documents` → business-and-operations/strategy
- `positioning`, `pricing-strategy`, `stp-framework` → marketing
- `instagram` → marketing, and non-English (Portuguese description)

These are not quality problems. They are **routing** problems, and they make the analytics
category look broader and thinner than it is.

## 3. What this implies for the four domains

The four requested domains hold about **957** canonical skills:

| Domain | Candidate pool |
|---|---:|
| design | 473 |
| content | 338 |
| data | 153 |
| core stack (React, npm, Webflow, Python) | 155 |
| **union** | **957** |

If this pilot's ratio holds — 60% surviving structural triage — the four domains would land
around **570 skills, not 100**.

Closing that gap requires a second pass that structural triage cannot do: reading each
surviving skill and asking whether the guidance is correct, current and opinionated. That is
the expensive part, and it is the only part that produces a genuinely small library.

## 4. Recommendation

1. **Run structural triage across all four domains first.** It is cheap, mechanical, and
   produces a defensible list of what to merge, move, rewrite and drop.
2. **Then run a quality pass on the survivors**, domain by domain, against an explicit rubric.
3. **Do not promise a number before step 2.** Structural triage gives ~570. The quality pass
   is what gets to 100, and its yield is unknown until it runs on a real domain.

## 5. Files

- `data-analytics-triage.csv` — 37 rows: skill, size, verdict, reason.