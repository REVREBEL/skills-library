---
name: "format-revrebel-google-docs"
description: "Format, restyle, create, or quality-check Google Docs according to the current REVREBEL writing and document standards. Use when asked to make a Google Doc follow the REVREBEL way, apply REVREBEL branding or formatting, prepare a REVREBEL report, revise a document against the REVREBEL AI Constitution, or audit an existing Google Doc for REVREBEL compliance."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Format REVREBEL Google Docs

Use the connected Google Drive and Google Docs tools to work from the live source documents on every invocation.

## Live authorities

Read these sources before reviewing or changing the target document:

1. Rules — read tab `t.0`:
   `https://docs.google.com/document/d/1QpGIvzQ_8qvKrccMPfpezgDmlYb-5V-qfEPoQ8P_qto/edit?tab=t.0`
2. Formatting — read tab `t.rohhxzx2gyg`:
   `https://docs.google.com/document/d/1c6TRzMhYEk21Tjzr0V-3lLPN6rTrp3e9LUxxsT0JlMU/edit?tab=t.rohhxzx2gyg`
3. Example report:
   `https://docs.google.com/document/d/1X7e_P5wCG7GYWD8eLOvQ5CPx4EZv-J4mb6M86hj5Qgs/edit`

Do not rely on remembered copies of these documents. Fetch them again each time so later source edits take effect without changing this skill.

Apply authority in this order:

1. The user's explicit instructions for the current document
2. The live Rules document
3. The live Formatting document
4. The example report

Treat the example as a pattern library, not as permission to copy its client-specific content. If the example conflicts with either live standard, follow the live standard.

## Workflow

1. Identify the target Google Doc and the requested outcome. If the user did not provide a target, ask for the document URL or create a new Doc only when requested.
2. Fetch all three live authorities. Record their titles, revision IDs when available, and the tabs read.
3. Read the target document, including all relevant tabs. Preserve tab structure unless the user requests a change.
4. Build a short working checklist from the live sources:
   - writing, reasoning, editing, and prohibited-language rules;
   - page, type, heading, body, color, table, callout, spacing, and hierarchy rules;
   - relevant structural patterns visible in the example.
5. Separate content edits from visual formatting edits. Preserve the author's meaning, facts, links, citations, tables, images, and document structure unless a change is required by the live rules or requested by the user.
6. Apply edits with Google Docs operations. Use named paragraph styles where the standard calls for them, then apply the exact live font, size, color, emphasis, table, border, padding, and page settings.
7. Use the example report to resolve only details the live standards leave open, choosing the closest matching section or document type.
8. Re-read the changed document and verify it against the working checklist. Correct change-related misses before finishing.
9. Report:
   - the document changed or reviewed;
   - the live source revisions used;
   - the main content and formatting changes;
   - anything not applied and why.

## Editing safeguards

- Do not rewrite content merely to make it different.
- Do not invent facts, citations, results, dates, ownership, or recommendations.
- Do not remove comments, suggestions, bookmarks, links, images, tables, footnotes, headers, or footers unless explicitly required.
- Preserve intentional emphasis and accessibility unless the live standard clearly supersedes it.
- Keep heading levels semantic and consistent; do not simulate headings with manual font changes alone.
- Use bullets only when they improve readability.
- Do not claim compliance until the post-edit verification is complete.

## Source failure

If a live authority cannot be read, retry with its document ID and specified tab. If it remains unavailable, stop before changing the target and tell the user which source could not be accessed. Offer a review based on the remaining sources only with the user's approval; label that result as partial rather than fully REVREBEL-compliant.
