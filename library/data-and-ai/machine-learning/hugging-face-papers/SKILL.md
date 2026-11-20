---
name: "hugging-face-papers"
description: "Look up, read, publish, and manage Hugging Face paper pages. Read papers as markdown or structured JSON (authors, linked models/datasets/spaces, GitHub, project page); parse arXiv IDs from URLs; search and list daily papers. Also covers publishing: indexing papers from arXiv, linking papers to model/dataset cards, claiming authorship, managing visibility, and generating professional markdown research articles. Use when the user shares a Hugging Face paper page URL, an arXiv URL or ID, asks to summarize/explain/analyze a paper, or wants to publish/manage a paper on the Hub."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Hugging Face Paper Pages

Hugging Face Paper pages (hf.co/papers) is a platform built on top of arXiv (arxiv.org), specifically for research papers in the field of artificial intelligence (AI) and computer science. Hugging Face users can submit their paper at hf.co/papers/submit, which features it on the Daily Papers feed (hf.co/papers). Each day, users can upvote papers and comment on papers. Each paper page allows authors to:
- claim their paper (by clicking their name on the `authors` field). This makes the paper page appear on their Hugging Face profile.
- link the associated model checkpoints, datasets and Spaces by including the HF paper or arXiv URL in the model card, dataset card or README of the Space
- link the Github repository and/or project page URLs
- link the HF organization. This also makes the paper page appear on the Hugging Face organization page.

Whenever someone mentions a HF paper or arXiv abstract/PDF URL in a model card, dataset card or README of a Space repository, the paper will be automatically indexed. Note that not all papers indexed on Hugging Face are also submitted to daily papers. The latter is more a manner of promoting a research paper. Papers can only be submitted to daily papers up until 14 days after their publication date on arXiv.

The Hugging Face team has built an easy-to-use API to interact with paper pages. Content of the papers can be fetched as markdown, or structured metadata can be returned such as author names, linked models/datasets/spaces, linked Github repo and project page.

## When to Use

- User shares a Hugging Face paper page URL (e.g. `https://huggingface.co/papers/2602.08025`)
- User shares a Hugging Face markdown paper page URL (e.g. `https://huggingface.co/papers/2602.08025.md`)
- User shares an arXiv URL (e.g. `https://arxiv.org/abs/2602.08025` or  `https://arxiv.org/pdf/2602.08025`)
- User mentions a arXiv ID (e.g. `2602.08025`)
- User asks you to summarize, explain, or analyze an AI research paper

## Parsing the paper ID

It's recommended to parse the paper ID (arXiv ID) from whatever the user provides:

| Input | Paper ID |
| --- | --- |
| `https://huggingface.co/papers/2602.08025` | `2602.08025` |
| `https://huggingface.co/papers/2602.08025.md` | `2602.08025` |
| `https://arxiv.org/abs/2602.08025` | `2602.08025` |
| `https://arxiv.org/pdf/2602.08025` | `2602.08025` |
| `2602.08025v1` | `2602.08025v1` |
| `2602.08025` | `2602.08025` |

This allows you to provide the paper ID into any of the hub API endpoints mentioned below.

### Fetch the paper page as markdown

The content of a paper can be fetched as markdown like so:

```bash
curl -s "https://huggingface.co/papers/{PAPER_ID}.md"
```

This should return the Hugging Face paper page as markdown. This relies on the HTML version of the paper at https://arxiv.org/html/{PAPER_ID}.

There are 2 exceptions:
- Not all arXiv papers have an HTML version. If the HTML version of the paper does not exist, then the content falls back to the HTML of the Hugging Face paper page.
- If it results in a 404, it means the paper is not yet indexed on hf.co/papers. See [Error handling](#error-handling) for info.

Alternatively, you can request markdown from the normal paper page URL, like so:

```bash
curl -s -H "Accept: text/markdown" "https://huggingface.co/papers/{PAPER_ID}"
```

### Paper Pages API Endpoints

All endpoints use the base URL `https://huggingface.co`.

#### Get structured metadata

Fetch the paper metadata as JSON using the Hugging Face REST API:

```bash
curl -s "https://huggingface.co/api/papers/{PAPER_ID}"
```

This returns structured metadata that can include:

- authors (names and Hugging Face usernames, in case they have claimed the paper)
- media URLs (uploaded when submitting the paper to Daily Papers)
- summary (abstract) and AI-generated summary
- project page and GitHub repository
- organization and engagement metadata (number of upvotes)

To find models linked to the paper, use:

```bash
curl https://huggingface.co/api/models?filter=arxiv:{PAPER_ID}
```

To find datasets linked to the paper, use:

```bash
curl https://huggingface.co/api/datasets?filter=arxiv:{PAPER_ID}
```

To find spaces linked to the paper, use:

```bash
curl https://huggingface.co/api/spaces?filter=arxiv:{PAPER_ID}
```

#### Claim paper authorship

Claim authorship of a paper for a Hugging Face user:

```bash
curl "https://huggingface.co/api/settings/papers/claim" \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $HF_TOKEN" \
  --data '{
    "paperId": "{PAPER_ID}",
    "claimAuthorId": "{AUTHOR_ENTRY_ID}",
    "targetUserId": "{USER_ID}"
  }'
```

- Endpoint: `POST /api/settings/papers/claim`
- Body:
  - `paperId` (string, required): arXiv paper identifier being claimed
  - `claimAuthorId` (string): author entry on the paper being claimed, 24-char hex ID
  - `targetUserId` (string): HF user who should receive the claim, 24-char hex ID
- Response: paper authorship claim result, including the claimed paper ID

#### Get daily papers

Fetch the Daily Papers feed:

```bash
curl -s -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/daily_papers?p=0&limit=20&date=2017-07-21&sort=publishedAt"
```

- Endpoint: `GET /api/daily_papers`
- Query parameters:
  - `p` (integer): page number
  - `limit` (integer): number of results, between 1 and 100
  - `date` (string): RFC 3339 full-date, for example `2017-07-21`
  - `week` (string): ISO week, for example `2024-W03`
  - `month` (string): month value, for example `2024-01`
  - `submitter` (string): filter by submitter
  - `sort` (enum): `publishedAt` or `trending`
- Response: list of daily papers

#### List papers

List arXiv papers sorted by published date:

```bash
curl -s -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/papers?cursor={CURSOR}&limit=20"
```

- Endpoint: `GET /api/papers`
- Query parameters:
  - `cursor` (string): pagination cursor
  - `limit` (integer): number of results, between 1 and 100
- Response: list of papers

#### Search papers

Perform hybrid semantic and full-text search on papers:

```bash
curl -s -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/papers/search?q=vision+language&limit=20"
```

This searches over the paper title, authors, and content.

- Endpoint: `GET /api/papers/search`
- Query parameters:
  - `q` (string): search query, max length 250
  - `limit` (integer): number of results, between 1 and 120
- Response: matching papers

#### Index a paper

Insert a paper from arXiv by ID. If the paper is already indexed, only its authors can re-index it:

```bash
curl "https://huggingface.co/api/papers/index" \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $HF_TOKEN" \
  --data '{
    "arxivId": "{ARXIV_ID}"
  }'
```

- Endpoint: `POST /api/papers/index`
- Body:
  - `arxivId` (string, required): arXiv ID to index, for example `2301.00001`
- Pattern: `^\d{4}\.\d{4,5}$`
- Response: empty JSON object on success

#### Update paper links

Update the project page, GitHub repository, or submitting organization for a paper. The requester must be the paper author, the Daily Papers submitter, or a papers admin:

```bash
curl "https://huggingface.co/api/papers/{PAPER_OBJECT_ID}/links" \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $HF_TOKEN" \
  --data '{
    "projectPage": "https://example.com",
    "githubRepo": "https://github.com/org/repo",
    "organizationId": "{ORGANIZATION_ID}"
  }'
```

- Endpoint: `POST /api/papers/{paperId}/links`
- Path parameters:
  - `paperId` (string, required): Hugging Face paper object ID
- Body:
  - `githubRepo` (string, nullable): GitHub repository URL
  - `organizationId` (string, nullable): organization ID, 24-char hex ID
  - `projectPage` (string, nullable): project page URL
- Response: empty JSON object on success

## Error Handling

- **404 on `https://huggingface.co/papers/{PAPER_ID}` or `md` endpoint**: the paper is not indexed on Hugging Face paper pages yet.
- **404 on `/api/papers/{PAPER_ID}`**: the paper may not be indexed on Hugging Face paper pages yet.
- **Paper ID not found**: verify the extracted arXiv ID, including any version suffix

### Fallbacks

If the Hugging Face paper page does not contain enough detail for the user's question:

- Check the regular paper page at `https://huggingface.co/papers/{PAPER_ID}`
- Fall back to the arXiv page or PDF for the original source:
  - `https://arxiv.org/abs/{PAPER_ID}`
  - `https://arxiv.org/pdf/{PAPER_ID}`

## Notes

- No authentication is required for public paper pages.
- Write endpoints such as claim authorship, index paper, and update paper links require `Authorization: Bearer $HF_TOKEN`.
- Prefer the `.md` endpoint for reliable machine-readable output.
- Prefer `/api/papers/{PAPER_ID}` when you need structured JSON fields instead of page markdown.

---

# Publishing & Managing Papers

Publish, manage, and link research papers on the Hugging Face Hub: create paper pages, link papers to models/datasets, claim authorship, and generate professional markdown-based research articles.

## When to Use

- Publishing a new research paper and linking it to your models/datasets.
- Claiming authorship on a paper where you're an author.
- Generating a markdown research article from a template.
- Managing which verified papers appear on your profile.

## Core capabilities

- **Paper page management** — index papers from arXiv, claim authorship, control visibility, discover papers.
- **Link papers to artifacts** — add citations to model/dataset cards; the Hub auto-generates `arxiv:<PAPER_ID>` tags; maintain attribution.
- **Research article creation** — markdown templates (standard, modern/Distill-style, arxiv, ml-report), dynamic TOC, LaTeX math, standard scientific section structure.
- **Metadata management** — YAML frontmatter, citation tracking, version control, multi-paper support.

## Method 1 — Index a paper from arXiv

Add a paper to HF Paper Pages from arXiv:

```bash
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"   # check if it exists
```

You can also visit `https://huggingface.co/papers/{arxiv-id}` directly to index a paper.

## Method 2 — Link a paper to a model/dataset

```bash
# Model card
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" --repo-type "model" --arxiv-id "2301.12345"

# Dataset card
uv run scripts/paper_manager.py link \
  --repo-id "username/dataset-name" --repo-type "dataset" --arxiv-id "2301.12345"

# Multiple papers
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" --repo-type "model" \
  --arxiv-ids "2301.12345,2302.67890,2303.11111"

# Custom citation
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" --repo-type "model" \
  --arxiv-id "2301.12345" --citation "$(cat citation.txt)"
```

How linking works: the Hub extracts the arXiv ID from the link → adds an `arxiv:<PAPER_ID>` tag → users click the tag to view the Paper Page → the Paper Page shows all models/datasets citing the paper → papers become discoverable via filters and search.

## Method 3 — Claim authorship

```bash
uv run scripts/paper_manager.py claim \
  --arxiv-id "2301.12345" --email "your.email@institution.edu"
uv run scripts/paper_manager.py check-authorship --arxiv-id "2301.12345"
```

Manual process: navigate to `https://huggingface.co/papers/{arxiv-id}` → find your name in the author list → click your name and select "Claim authorship" → wait for admin verification.

## Method 4 — Manage paper visibility

```bash
uv run scripts/paper_manager.py list-my-papers
uv run scripts/paper_manager.py toggle-visibility --arxiv-id "2301.12345" --show true
```

Or manage in account settings → Papers section → toggle "Show on profile".

## Method 5 — Create a research article

```bash
# From a template
uv run scripts/paper_manager.py create \
  --template "standard" --title "Your Paper Title" --output "paper.md"

# Complete paper
uv run scripts/paper_manager.py create \
  --template "modern" --title "Fine-Tuning LLMs with LoRA" \
  --authors "Jane Doe, John Smith" --abstract "$(cat abstract.txt)" --output "paper.md"

# Convert to HTML
uv run scripts/paper_manager.py convert \
  --input "paper.md" --output "paper.html" --style "modern"
```

Templates: `standard` (traditional scientific structure), `modern` (clean, web-friendly, Distill-inspired), `arxiv` (arXiv-style), `ml-report` (ML experiment report). Modern template features: dynamic TOC, responsive design, code highlighting, interactive figures, LaTeX math, citation management, author affiliation linking.

Standard paper sections: Abstract → 1. Introduction → 2. Related Work → 3. Methodology → 4. Experiments → 5. Results → 6. Discussion → 7. Conclusion → References.

## Commands reference

```bash
# Index
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"

# Link
uv run scripts/paper_manager.py link \
  --repo-id "username/repo" --repo-type "model|dataset|space" \
  --arxiv-id "2301.12345" [--citation "..."] [--create-pr]

# Claim / visibility
uv run scripts/paper_manager.py claim --arxiv-id "2301.12345" --email "you@edu"
uv run scripts/paper_manager.py toggle-visibility --arxiv-id "2301.12345" --show true|false

# Create / convert
uv run scripts/paper_manager.py create --template "standard|modern|arxiv|ml-report" \
  --title "Title" [--authors "..."] [--abstract "..."] [--output "file.md"]
uv run scripts/paper_manager.py convert --input "paper.md" --output "paper.html" [--style "modern|classic"]

# Check / list / search
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"
uv run scripts/paper_manager.py list-my-papers
uv run scripts/paper_manager.py search --query "transformer attention"
```

## YAML metadata for linking

**Model card:**

```yaml
---
language:
  - en
license: apache-2.0
tags:
  - text-generation
  - transformers
  - llm
library_name: transformers
---

# Model Name

This model is based on the approach described in [Our Paper](https://arxiv.org/abs/2301.12345).

## Citation

​```bibtex
@article{doe2023paper,
  title={Your Paper Title},
  author={Doe, Jane and Smith, John},
  journal={arXiv preprint arXiv:2301.12345},
  year={2023}
}
​```
```

**Dataset card:**

```yaml
---
language:
  - en
license: cc-by-4.0
task_categories:
  - text-generation
  - question-answering
size_categories:
  - 10K<n<100K
---

# Dataset Name

Dataset introduced in [Our Paper](https://arxiv.org/abs/2301.12345).

For more details, see the [paper page](https://huggingface.co/papers/2301.12345).
```

The Hub automatically extracts arXiv IDs from these links and creates `arxiv:2301.12345` tags.

## Workflows

**Publish new research:** create article → edit → submit to arXiv → index on HF → link to model → claim authorship.

```bash
uv run scripts/paper_manager.py create --template modern --title "Novel Approach" --output paper.md
# (submit to arXiv, get ID)
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"
uv run scripts/paper_manager.py link --repo-id "you/model" --repo-type model --arxiv-id "2301.12345"
uv run scripts/paper_manager.py claim --arxiv-id "2301.12345" --email "you@edu"
```

**Link an existing paper:** check → index if needed → link to multiple repos (model, dataset, space).

**Update a model with a paper reference:** `hf download username/model README.md` → link (the script adds YAML metadata, inserts the arXiv link, adds the citation, and preserves existing content).

## Best practices

- Index papers as soon as they're on arXiv; include full citations in cards; use consistent references across repos.
- Add YAML frontmatter to all model/dataset cards; include licensing; tag with task categories and domains.
- Claim authorship where you're listed; use institutional emails; keep visibility settings updated.
- Link papers to all relevant models, datasets, and Spaces; add BibTeX citations.
- Use templates consistently; include code/data links; generate web-friendly HTML for sharing.

## Advanced usage

```bash
# Batch link
for arxiv_id in "2301.12345" "2302.67890"; do
  uv run scripts/paper_manager.py link --repo-id "user/model" --repo-type model --arxiv-id "$arxiv_id"
done

# Extract info / citation / validate
uv run scripts/paper_manager.py info --arxiv-id "2301.12345" --format json
uv run scripts/paper_manager.py citation --arxiv-id "2301.12345" --format bibtex
uv run scripts/paper_manager.py validate --repo-id "user/model" --repo-type model
```

Python API:

```python
from scripts.paper_manager import PaperManager

pm = PaperManager(hf_token="your_token")
pm.index_paper("2301.12345")
pm.link_paper(repo_id="username/model", repo_type="model",
              arxiv_id="2301.12345", citation="Full citation text")
print(pm.check_paper("2301.12345"))
```

## Error handling & troubleshooting

- **Paper not found** → visit `hf.co/papers/{arxiv-id}` to trigger indexing.
- **Permission denied** → HF_TOKEN lacks write access to the repository.
- **Invalid YAML** → malformed frontmatter in the README.
- **Authorship failed** → email doesn't match paper author records; wait for admin review or contact HF support.
- **arXiv tag not appearing** → ensure the README uses the proper arXiv URL format.
- **Template rendering errors** → check markdown syntax and YAML frontmatter.

## Resources

- [HF Paper Pages](https://huggingface.co/papers)
- [Model Cards](https://huggingface.co/docs/hub/en/model-cards) / [Dataset Cards](https://huggingface.co/docs/hub/en/datasets-cards)
- [Research Article Template](https://huggingface.co/spaces/tfrere/research-article-template) — use for writing, then publish/link with this skill
- [arXiv Format Guide](https://arxiv.org/help/submit)

## Limitations

- Use this skill only when the task clearly matches its upstream product or API scope.
- Verify commands, API behavior, pricing, quotas, credentials, and deployment effects against current official documentation before making changes.
- Do not treat generated examples as a substitute for environment-specific tests, security review, or user approval for destructive or costly actions.

## Merged from

- `hugging-face-paper-publisher` — publishing and managing papers: indexing from arXiv, linking to model/dataset cards, claiming authorship, managing visibility, creating markdown research articles, YAML metadata, workflows, best practices, advanced usage, troubleshooting
