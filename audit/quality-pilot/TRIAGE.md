# Structural Triage — Four Priority Domains

**Scope:** 910 canonical skills across design, content, data, and core stack
**Method:** `tools/skill_triage.py`, the pilot rubric applied at scale
**Mode:** Read-only. No library content changed.

---

## 1. Headline

| Verdict | Skills | Share |
|---|---:|---:|
| keep | 655 | 72% |
| review | 139 | 15% |
| rewrite | 67 | 7% |
| merge | 49 | 5% |
| move | 0 | 0% |
| **total** | **910** | |

Structural triage leaves **72% marked keep**. That is the same ratio the 37-skill pilot
predicted (~60% surviving), and it means **structural triage does not get the library to 100**.
It gets it to roughly 650.

## 2. The classifier is not trustworthy for verdicts

The rubric was checked against the 37 manual verdicts from the data-analytics pilot:

| | |
|---|---:|
| Overlapping skills | 18 |
| Agreed | 5 |
| **Agreement** | **28%** |

Disagreements run in both directions:

| Skill | Manual | Automatic | Why the classifier missed it |
|---|---|---|---|
| analytics | merge | keep | Needs reading to see the overlap with `analytics-tracking` |
| analytics-tracking | merge | keep | Same |
| customer-analytics | merge | rewrite | Overlap with `unit-economics` is semantic, not textual |
| financial-analytics-dashboard | merge | rewrite | Similarity is 0.32 — below the 0.55 threshold |
| custom-code-management | move | keep | Substantial English skill; misfiling needs domain knowledge |
| instagram | move | keep | Portuguese content, not caught by a Han/Hangul scan |
| pricing-strategy | move | keep | Marketing content filed under data |
| product-analytics | keep | rewrite | Flagged for "weak step" wording that is actually fine |
| sendgrid-automation | review | keep | Provider coupling is invisible to structure |

**Conclusion:** the automated verdicts are a **prioritisation queue, not decisions**. 28% agreement
is not a tool you can act on without reading.

## 3. Two rules that do not work

**`move` never fires.** The misfiled check compares a skill's path domain against its keyword
score in that same domain. Skills filed under a domain almost always mention that domain's words,
so the condition is never met. Detecting misfiling needs a semantic comparison against *other*
domains, not an absence check.

**`duplicate` only catches near-identical text.** At a 0.55 Jaccard threshold on name plus
description, it finds 49 merge candidates — but the pilot's real merges (analytics +
analytics-tracking, financial-analytics-dashboard + financial-reporting-dashboard) score 0.22–0.32
because the domain nouns differ. Text similarity systematically underestimates semantic duplicates.

## 4. What the triage is actually good for

Ranking, not deciding. The useful output is the **139 `review` + 67 `rewrite` = 206 skills** that
structure flags as worth a human look. That is a tractable reading list instead of 910.

The 655 `keep` verdicts should be treated as "no structural objection", not "approved".

## 5. Recommendation

1. **Do not run a mass merge from this output.** 5% merge is plausible but the classifier misses
   most real pairs; acting on it would merge the wrong things.
2. **Use the 206 flagged skills as the review queue.** Start with `review`, then `rewrite`.
3. **Review the 655 in domain batches**, not one at a time — read a category's skills together and
   ask which single skill would replace the others.
4. **Fix the two broken rules** before the next run: semantic misfiling (compare against all four
   domains, not an absence check) and a lower duplicate threshold with body-text shingles rather
   than name+description tokens.

## 6. Files

- `triage-all.csv` — 910 rows: canonical id, path, domains, verdict, reason, size, structure metrics.
- `tools/skill_triage.py` — the classifier.