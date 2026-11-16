# Non-English Inventory

Fresh scan of every `SKILL.md` under `library/` for non-Latin scripts, run against
`origin/main` rather than trusting the earlier SKIL-11 audit.

## Result

70 files contain non-Latin characters. They are not equivalent:

| Action | Files | Meaning |
|---|---:|---|
| `dump` | 9 | Chinese-dominant body and metadata, no English version |
| `review` | 2 | Substantially bilingual, or Korean inside an English skill |
| `keep_multilingual` | 3 | English skills with intentional Chinese examples or trigger phrases |
| `ignore` | 32 | English skills with a handful of stray Han/Hangul/Cyrillic characters |
| `nested` | 19 | Non-canonical nested packs with Japanese trigger phrases |
| `router` | 5 | Category routers that inherit text from indexed skills |
| **total** | **70** | |

## The correction this makes

"Anything containing Chinese" would be **46 skills**, not 9. The other 37 have between
**4 and 607 Han characters** against thousands of Latin characters — they are English skills
that quote a Chinese term, name a Chinese GPU vendor, or carry a stray character. Deleting
them would remove working content.

The genuinely Chinese-dominant set is 9:

| Skill | Han | Latin |
|---|---:|---:|
| development:mental-health-analyzer | 5,894 | 1,688 |
| development:rehabilitation-analyzer | 3,383 | 1,220 |
| development:oral-health-analyzer | 3,227 | 522 |
| development:tcm-constitution-analyzer | 2,987 | 1,590 |
| development:goal-analyzer | 2,986 | 1,694 |
| development:fitness-analyzer | 2,101 | 905 |
| development:emergency-card | 1,757 | 4,433 |
| marketing-and-seo:ai-analyzer | 1,499 | 1,718 |
| business-and-operations:product-decision-agent | 1,414 | 373 |

## Also worth knowing

The 14 `foreign_language_dominant` skills in the SKIL-11 audit are **9 Chinese and 5
Portuguese**. The Portuguese ones are `context-agent`, `growth-engine`, `matematico-tao`,
`multi-advisor`, and `task-intelligence` — not Chinese, and not covered by this inventory.

`marketing-and-seo:ai-md` is genuinely bilingual (134 separate Han runs, 498 characters) and
needs a split-or-translate decision rather than a straight dump.

## Files

- `non-english-inventory.csv` — 70 rows: path, canonical id, kind, language, character counts, action, reason.