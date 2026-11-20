---
name: "hugging-face-cli"
description: "Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing models, datasets, spaces, buckets, repos, papers, jobs, and more — plus the workflows built on it: finding the best model for a task by benchmark leaderboards, exploring datasets via the Dataset Viewer API, creating and SQL-querying datasets, running local or remote evaluations (inspect-ai/lighteval/vLLM), publishing model-index evaluation results, running HF Jobs (CPU/GPU/TPU, scheduled, webhooks), and mounting repos as local filesystems."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
## When to Use

Use this skill when you need the Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing models, datasets, spaces, buckets, repos, papers, jobs, and more on the Hugging Face Hub. Use when: handling authentication; managing local cache; managing Hugging Face Buckets; running or scheduling jobs on Hugging Face; finding the best model for a task; exploring or building datasets; running evaluations; publishing model-index metadata; or mounting repos as local filesystems.

Install by downloading the installer script first, reviewing it, and then running it locally:

```bash
tmpdir="$(mktemp -d)" && trap 'rm -rf "$tmpdir"' EXIT && \
  curl -LsSf https://hf.co/cli/install.sh -o "$tmpdir/hf-install.sh" && \
  less "$tmpdir/hf-install.sh" && bash "$tmpdir/hf-install.sh"
```

The Hugging Face Hub CLI tool `hf` is available. IMPORTANT: the `hf` command replaces the deprecated `huggingface-cli` command. Use `hf --help` to view available functions. Auth commands are all under `hf auth`, e.g. `hf auth whoami`.

Generated with `huggingface_hub v1.21.0`. Run `hf skills add --force` to regenerate.

## CLI Reference

> All commands accept `--format [auto|human|agent|json|quiet]` (or `--json` / `--format table`). Most Hub-scoped commands accept `--namespace TEXT`. See "Common options" at the end for shared flags.

- `hf cp SRC` — Copy files between local paths, repositories, and buckets.
- `hf download REPO_ID` — Download files from the Hub. `[--type [model|dataset|space] --revision TEXT --include TEXT --exclude TEXT --cache-dir TEXT --local-dir TEXT --force-download --dry-run --max-workers INTEGER]`
- `hf env` — Print information about the environment.
- `hf sync` — Sync files between local directory and a bucket. `[--delete --ignore-times --ignore-sizes --plan TEXT --apply TEXT --dry-run --include TEXT --exclude TEXT --filter-from TEXT --existing --ignore-existing --verbose]`
- `hf update` — Update the `hf` CLI to the latest version.
- `hf upload REPO_ID` — Upload a file or folder to the Hub. Recommended for single-commit uploads. `[--type [model|dataset|space] --revision TEXT --private --include TEXT --exclude TEXT --delete TEXT --commit-message TEXT --commit-description TEXT --create-pr --every FLOAT]`
- `hf upload-large-folder REPO_ID LOCAL_PATH` — Upload a large folder to the Hub. Recommended for resumable uploads. `[--type [model|dataset|space] --revision TEXT --private --include TEXT --exclude TEXT --num-workers INTEGER --no-report --no-bars]`
- `hf version` — Print information about the hf version.

### `hf auth` — Manage authentication (login, logout, etc.)

- `hf auth list` — List all stored access tokens.
- `hf auth login` — Login from your browser, or using a token from huggingface.co/settings/tokens. `[--add-to-git-credential --force]`
- `hf auth logout` — Logout from a specific token. `[--token-name TEXT]`
- `hf auth switch` — Switch between access tokens. `[--token-name TEXT --add-to-git-credential]`
- `hf auth token` — Print the current access token to stdout.
- `hf auth whoami` — Find out which huggingface.co account you are logged in as.

### `hf buckets` — Commands to interact with buckets.

- `hf buckets cp SRC` — Copy files between local paths, repositories, and buckets.
- `hf buckets create BUCKET_ID` — Create a new bucket. `[--private --region [us|eu] --exist-ok]`
- `hf buckets delete BUCKET_ID` — Delete a bucket. `[--yes --missing-ok]`
- `hf buckets info BUCKET_ID` — Get info about a bucket.
- `hf buckets list` — List buckets or files in a bucket. `[--human-readable --tree --recursive --search TEXT]`
- `hf buckets move FROM_ID TO_ID` — Move (rename) a bucket to a new name or namespace.
- `hf buckets remove ARGUMENT` — Remove files from a bucket. `[--recursive --yes --dry-run --include TEXT --exclude TEXT]`
- `hf buckets sync` — Sync files between local directory and a bucket. `[--delete --ignore-times --ignore-sizes --plan TEXT --apply TEXT --dry-run --include TEXT --exclude TEXT --filter-from TEXT --existing --ignore-existing --verbose]`

### `hf cache` — Manage local cache directory.

- `hf cache list` — List cached repositories or revisions. `[--cache-dir TEXT --revisions --filter TEXT --sort [accessed|accessed:asc|accessed:desc|modified|modified:asc|modified:desc|name|name:asc|name:desc|size|size:asc|size:desc] --limit INTEGER]`
- `hf cache prune` — Remove detached revisions from the cache. `[--cache-dir TEXT --yes --dry-run]`
- `hf cache rm TARGETS` — Remove cached repositories or revisions. `[--cache-dir TEXT --yes --dry-run]`
- `hf cache verify REPO_ID` — Verify checksums for a single repo revision from cache or a local directory. `[--type [model|dataset|space] --revision TEXT --cache-dir TEXT --local-dir TEXT --fail-on-missing-files --fail-on-extra-files]`

### `hf collections` — Interact with collections on the Hub.

- `hf collections add-item COLLECTION_SLUG ITEM_ID ITEM_TYPE` — Add an item to a collection. `[--note TEXT --exists-ok]`
- `hf collections create TITLE` — Create a new collection on the Hub. `[--namespace TEXT --description TEXT --private --exists-ok]`
- `hf collections delete COLLECTION_SLUG` — Delete a collection from the Hub. `[--missing-ok]`
- `hf collections delete-item COLLECTION_SLUG ITEM_OBJECT_ID` — Delete an item from a collection. `[--missing-ok]`
- `hf collections info COLLECTION_SLUG` — Get info about a collection on the Hub.
- `hf collections list` — List collections on the Hub. `[--owner TEXT --item TEXT --sort [lastModified|trending|upvotes] --limit INTEGER]`
- `hf collections update COLLECTION_SLUG` — Update a collection's metadata on the Hub. `[--title TEXT --description TEXT --position INTEGER --private --theme TEXT]`
- `hf collections update-item COLLECTION_SLUG ITEM_OBJECT_ID` — Update an item in a collection. `[--note TEXT --position INTEGER]`

### `hf datasets` — Interact with datasets on the Hub.

- `hf datasets card DATASET_ID` — Get the dataset card (README) for a dataset on the Hub. `[--metadata --text]`
- `hf datasets info DATASET_ID` — Get info about a dataset on the Hub. `[--revision TEXT --expand TEXT]`
- `hf datasets leaderboard DATASET_ID` — List model scores from a dataset leaderboard. Use `hf datasets ls --filter benchmark:official` to list available leaderboards. `[--limit INTEGER]`
- `hf datasets list` — List datasets on the Hub, or files in a dataset repo. `[--search TEXT --author TEXT --filter TEXT --sort [created_at|downloads|last_modified|likes|trending_score] --limit INTEGER --expand TEXT --human-readable --tree --recursive --revision TEXT]`
- `hf datasets parquet DATASET_ID` — List parquet file URLs available for a dataset. `[--subset TEXT --split TEXT]`
- `hf datasets sql SQL` — Execute a raw SQL query with DuckDB against dataset parquet URLs.

### `hf discussions` — Manage discussions and pull requests on the Hub.

- `hf discussions close REPO_ID NUM` — Close a discussion or pull request. `[--comment TEXT --yes --type [model|dataset|space]]`
- `hf discussions comment REPO_ID NUM` — Comment on a discussion or pull request. `[--body TEXT --body-file PATH --type [model|dataset|space]]`
- `hf discussions create REPO_ID --title TEXT` — Create a new discussion or pull request on a repo. `[--body TEXT --body-file PATH --pull-request --type [model|dataset|space]]`
- `hf discussions diff REPO_ID NUM` — Show the diff of a pull request. `[--type [model|dataset|space]]`
- `hf discussions info REPO_ID NUM` — Get info about a discussion or pull request. `[--type [model|dataset|space]]`
- `hf discussions list REPO_ID` — List discussions and pull requests on a repo. `[--status [open|closed|merged|draft|all] --kind [all|discussion|pull_request] --author TEXT --limit INTEGER --type [model|dataset|space]]`
- `hf discussions merge REPO_ID NUM` — Merge a pull request. `[--comment TEXT --yes --type [model|dataset|space]]`
- `hf discussions rename REPO_ID NUM NEW_TITLE` — Rename a discussion or pull request. `[--type [model|dataset|space]]`
- `hf discussions reopen REPO_ID NUM` — Reopen a closed discussion or pull request. `[--comment TEXT --yes --type [model|dataset|space]]`

### `hf endpoints` — Manage Hugging Face Inference Endpoints.

- `hf endpoints catalog deploy --repo TEXT` — Deploy an Inference Endpoint from the Model Catalog. `[--name TEXT --accelerator TEXT --namespace TEXT]`
- `hf endpoints catalog list` — List available Catalog models.
- `hf endpoints delete NAME` — Delete an Inference Endpoint permanently. `[--namespace TEXT --yes]`
- `hf endpoints deploy NAME --repo TEXT --framework TEXT --accelerator TEXT --instance-size TEXT --instance-type TEXT --region TEXT --vendor TEXT` — Deploy an Inference Endpoint from a Hub repository. `[--namespace TEXT --task TEXT --min-replica INTEGER --max-replica INTEGER --scale-to-zero-timeout INTEGER --scaling-metric [pendingRequests|hardwareUsage] --scaling-threshold FLOAT --revision TEXT --custom-image TEXT --health-route TEXT --port INTEGER --container-command TEXT --container-args TEXT --env TEXT --env-file TEXT --secrets TEXT --secrets-file TEXT --type [public|protected|authenticated|private]]`
- `hf endpoints describe NAME` — Get information about an existing endpoint. `[--namespace TEXT]`
- `hf endpoints list` — Lists all Inference Endpoints for the given namespace. `[--namespace TEXT]`
- `hf endpoints pause NAME` — Pause an Inference Endpoint. `[--namespace TEXT]`
- `hf endpoints resume NAME` — Resume an Inference Endpoint. `[--namespace TEXT --fail-if-already-running]`
- `hf endpoints scale-to-zero NAME` — Scale an Inference Endpoint to zero. `[--namespace TEXT]`
- `hf endpoints update NAME` — Update an existing endpoint. `[--namespace TEXT --repo TEXT --accelerator TEXT --instance-size TEXT --instance-type TEXT --framework TEXT --revision TEXT --task TEXT --min-replica INTEGER --max-replica INTEGER --scale-to-zero-timeout INTEGER --scaling-metric [pendingRequests|hardwareUsage] --scaling-threshold FLOAT]`

### `hf extensions` — Manage hf CLI extensions.

- `hf extensions exec NAME` — Execute an installed extension.
- `hf extensions install REPO_ID` — Install an extension from a public GitHub repository. `[--force]`
- `hf extensions list` — List installed extension commands.
- `hf extensions remove NAME` — Remove an installed extension.
- `hf extensions search` — Search extensions available on GitHub (tagged with 'hf-extension' topic).

### `hf jobs` — Run and manage Jobs on the Hub.

- `hf jobs cancel JOB_ID` — Cancel a Job. `[--namespace TEXT]`
- `hf jobs hardware` — List available hardware options for Jobs.
- `hf jobs inspect JOB_IDS` — Display detailed information on one or more Jobs. `[--namespace TEXT]`
- `hf jobs labels JOB_ID` — Update labels on a Job. Replaces all existing labels. `[--label TEXT --clear --namespace TEXT]`
- `hf jobs list` — List Jobs. `[--all --status [COMPLETED|CANCELED|ERROR|DELETED|SCHEDULING|RUNNING] --label TEXT --limit INTEGER --namespace TEXT --filter TEXT]`
- `hf jobs logs JOB_ID` — Fetch the logs of a Job. `[--follow --tail INTEGER --namespace TEXT]`
- `hf jobs run IMAGE COMMAND` — Run a Job. `[--env TEXT --secrets TEXT --label TEXT --volume TEXT --env-file TEXT --secrets-file TEXT --flavor [cpu-basic|cpu-upgrade|cpu-performance|cpu-xl|t4-small|t4-medium|l4x1|l4x4|l40sx1|l40sx4|l40sx8|a10g-small|a10g-large|a10g-largex2|a10g-largex4|a100-large|a100x4|a100x8|h200|h200x2|h200x4|h200x8|rtx-pro-6000|rtx-pro-6000x2|rtx-pro-6000x4|rtx-pro-6000x8] --timeout TEXT --detach --expose INTEGER --ssh --namespace TEXT]`
- `hf jobs scheduled delete SCHEDULED_JOB_ID` — Delete a scheduled Job. `[--namespace TEXT]`
- `hf jobs scheduled inspect SCHEDULED_JOB_IDS` — Display detailed information on one or more scheduled Jobs. `[--namespace TEXT]`
- `hf jobs scheduled labels SCHEDULED_JOB_ID` — Update labels on a scheduled Job. `[--label TEXT --clear --namespace TEXT]`
- `hf jobs scheduled list` — List scheduled Jobs. `[--all --namespace TEXT --filter TEXT]`
- `hf jobs scheduled resume SCHEDULED_JOB_ID` — Resume (unpause) a scheduled Job. `[--namespace TEXT]`
- `hf jobs scheduled run SCHEDULE IMAGE COMMAND` — Schedule a Job. `[--suspend --concurrency --env TEXT --secrets TEXT --label TEXT --volume TEXT --env-file TEXT --secrets-file TEXT --flavor ... --timeout TEXT --expose INTEGER --namespace TEXT]`
- `hf jobs scheduled suspend SCHEDULED_JOB_ID` — Suspend (pause) a scheduled Job. `[--namespace TEXT]`
- `hf jobs scheduled uv run SCHEDULE SCRIPT` — Run a UV script (local file or URL) on HF infrastructure. `[--suspend --concurrency --image TEXT --flavor ... --env TEXT --secrets TEXT --label TEXT --volume TEXT --env-file TEXT --secrets-file TEXT --timeout TEXT --expose INTEGER --namespace TEXT --with TEXT --python TEXT]`
- `hf jobs ssh JOB_ID` — SSH into a running Job. `[--identity-file PATH --dry-run --namespace TEXT]`
- `hf jobs stats` — Fetch the resource usage statistics and metrics of Jobs. `[--namespace TEXT]`
- `hf jobs uv run SCRIPT` — Run a UV script (local file or URL) on HF infrastructure. `[--image TEXT --flavor ... --env TEXT --secrets TEXT --label TEXT --volume TEXT --env-file TEXT --secrets-file TEXT --timeout TEXT --detach --expose INTEGER --ssh --namespace TEXT --with TEXT --python TEXT]`
- `hf jobs wait JOB_IDS` — Wait for one or more Jobs to reach a terminal state. `[--timeout TEXT --namespace TEXT]`

### `hf models` — Interact with models on the Hub.

- `hf models card MODEL_ID` — Get the model card (README) for a model on the Hub. `[--metadata --text]`
- `hf models info MODEL_ID` — Get info about a model on the Hub. `[--revision TEXT --expand TEXT]`
- `hf models list` — List models on the Hub, or files in a model repo. `[--search TEXT --author TEXT --filter TEXT --num-parameters TEXT --sort [created_at|downloads|last_modified|likes|trending_score] --limit INTEGER --expand TEXT --human-readable --tree --recursive --revision TEXT]`

### `hf papers` — Interact with papers on the Hub.

- `hf papers info PAPER_ID` — Get info about a paper on the Hub.
- `hf papers list` — List daily papers on the Hub. `[--date TEXT --week TEXT --month TEXT --submitter TEXT --sort [publishedAt|trending] --limit INTEGER]`
- `hf papers read PAPER_ID` — Read a paper as markdown.
- `hf papers search QUERY` — Search papers on the Hub. `[--limit INTEGER]`

### `hf repos` — Manage repos on the Hub.

- `hf repos branch create REPO_ID BRANCH` — Create a new branch for a repo on the Hub. `[--revision TEXT --type [model|dataset|space] --exist-ok]`
- `hf repos branch delete REPO_ID BRANCH` — Delete a branch from a repo on the Hub. `[--type [model|dataset|space]]`
- `hf repos cp SRC` — Copy files between local paths, repositories, and buckets.
- `hf repos create REPO_ID` — Create a new repo on the Hub. `[--type [model|dataset|space] --space-sdk TEXT --private --public --protected --exist-ok --resource-group-id TEXT --region [us|eu] --flavor [...] --storage [small|medium|large] --sleep-time INTEGER --secrets TEXT --secrets-file TEXT --env TEXT --env-file TEXT --volume TEXT]`
- `hf repos delete REPO_ID` — Delete a repo from the Hub. This is an irreversible operation. `[--type [model|dataset|space] --missing-ok --yes]`
- `hf repos delete-files REPO_ID PATTERNS` — Delete files from a repo on the Hub. `[--type [model|dataset|space] --revision TEXT --commit-message TEXT --commit-description TEXT --create-pr]`
- `hf repos duplicate FROM_ID` — Duplicate a repo on the Hub (model, dataset, or Space). `[--type [model|dataset|space] --private --public --protected --exist-ok --flavor [...] --storage [small|medium|large] --sleep-time INTEGER --secrets TEXT --secrets-file TEXT --env TEXT --env-file TEXT --volume TEXT]`
- `hf repos list` — List all repos (models, datasets, spaces, buckets) with storage info. `[--namespace TEXT --type [model|dataset|space|bucket] --search TEXT --limit INTEGER --explore]`
- `hf repos move FROM_ID TO_ID` — Move a repository from a namespace to another namespace. `[--type [model|dataset|space]]`
- `hf repos settings REPO_ID` — Update the settings of a repository. `[--gated [auto|manual|false] --private --public --protected --type [model|dataset|space]]`
- `hf repos tag create REPO_ID TAG` — Create a tag for a repo. `[--message TEXT --revision TEXT --type [model|dataset|space]]`
- `hf repos tag delete REPO_ID TAG` — Delete a tag for a repo. `[--yes --type [model|dataset|space]]`
- `hf repos tag list REPO_ID` — List tags for a repo. `[--type [model|dataset|space]]`

### `hf skills` — Manage skills for AI assistants.

- `hf skills add` — Download a Hugging Face skill and install it for an AI assistant. `[--claude --global --dest PATH --force]`
- `hf skills list` — List available skills from the Hugging Face marketplace.
- `hf skills preview` — Print the generated `hf-cli` SKILL.md to stdout.
- `hf skills update` — Update installed Hugging Face marketplace skills. `[--claude --global --dest PATH]`

### `hf spaces` — Interact with spaces on the Hub.

- `hf spaces card SPACE_ID` — Get the Space card (README) for a Space on the Hub. `[--metadata --text]`
- `hf spaces dev-mode SPACE_ID` — Enable or disable dev mode on a Space. `[--stop]`
- `hf spaces hardware` — List available hardware options for Spaces.
- `hf spaces hot-reload SPACE_ID` — Hot-reload any Python file of a Space without a full rebuild + restart. `[--local-file PATH --skip-checks --skip-summary]`
- `hf spaces info SPACE_ID` — Get info about a space on the Hub. `[--revision TEXT --expand TEXT]`
- `hf spaces list` — List spaces on the Hub, or files in a space repo. `[--search TEXT --author TEXT --filter TEXT --sort [created_at|last_modified|likes|trending_score] --limit INTEGER --expand TEXT --human-readable --tree --recursive --revision TEXT]`
- `hf spaces logs SPACE_ID` — Fetch the run or build logs of a Space. `[--build --follow --tail INTEGER]`
- `hf spaces pause SPACE_ID` — Pause a Space.
- `hf spaces restart SPACE_ID` — Restart a Space. `[--factory-reboot]`
- `hf spaces search QUERY` — Search spaces on the Hub using semantic search. `[--filter TEXT --sdk TEXT --include-non-running --description --limit INTEGER]`
- `hf spaces secrets add SPACE_ID` — Add or update secrets for a Space. `[--secrets TEXT --secrets-file TEXT]`
- `hf spaces secrets delete SPACE_ID KEY` — Remove a secret from a Space. `[--yes]`
- `hf spaces secrets list SPACE_ID` — List secrets for a Space. Secret values are write-only and not returned.
- `hf spaces settings SPACE_ID` — Update the settings of a Space. `[--sleep-time INTEGER --hardware [cpu-basic|cpu-upgrade|zero-a10g|t4-small|t4-medium|l4x1|l4x4|l40sx1|l40sx4|l40sx8|a10g-small|a10g-large|a10g-largex2|a10g-largex4|a100-large|a100x4|a100x8]]`
- `hf spaces ssh SPACE_ID` — SSH into a Space's Dev Mode container. `[--identity-file PATH --dry-run --auto]`
- `hf spaces variables add SPACE_ID` — Add or update environment variables for a Space. `[--env TEXT --env-file TEXT]`
- `hf spaces variables delete SPACE_ID KEY` — Remove an environment variable from a Space. `[--yes]`
- `hf spaces variables list SPACE_ID` — List environment variables for a Space.
- `hf spaces volumes delete SPACE_ID` — Remove all volumes from a Space. `[--yes]`
- `hf spaces volumes list SPACE_ID` — List volumes mounted in a Space.
- `hf spaces volumes set SPACE_ID` — Set (replace) volumes for a Space. `[--volume TEXT]`
- `hf spaces wait SPACE_ID` — Wait for a Space to finish building/starting. `[--timeout TEXT]`

### `hf webhooks` — Manage webhooks on the Hub.

- `hf webhooks create --watch TEXT` — Create a new webhook. `[--url TEXT --job-id TEXT --domain [repo|discussions] --secret TEXT]`
- `hf webhooks delete WEBHOOK_ID` — Delete a webhook permanently. `[--yes]`
- `hf webhooks disable WEBHOOK_ID` — Disable an active webhook.
- `hf webhooks enable WEBHOOK_ID` — Enable a disabled webhook.
- `hf webhooks info WEBHOOK_ID` — Show full details for a single webhook.
- `hf webhooks list` — List all webhooks for the current user.
- `hf webhooks update WEBHOOK_ID` — Update an existing webhook. Only provided options are changed. `[--url TEXT --watch TEXT --domain [repo|discussions] --secret TEXT]`

## Common options

- `--format` — Output format: `--format json` (or `--json`) or `--format table` (default).
- `-q / --quiet` — Quiet output (one ID per line).
- `--revision` — Git revision id which can be a branch name, a tag, or a commit hash.
- `--token` — Use a User Access Token. Prefer setting `HF_TOKEN` env var instead of passing `--token`.
- `--type` — The type of repository (model, dataset, or space).

## Mounting repos as local filesystems

To mount Hub repositories or buckets as local filesystems — no download, no copy, no waiting — use `hf-mount`. Files are fetched on demand. GitHub: https://github.com/huggingface/hf-mount

Install by downloading the installer script first, reviewing it, and then running it locally:

```bash
tmpdir="$(mktemp -d)" && trap 'rm -rf "$tmpdir"' EXIT && \
  curl -fsSL https://raw.githubusercontent.com/huggingface/hf-mount/main/install.sh -o "$tmpdir/hf-mount-install.sh" && \
  less "$tmpdir/hf-mount-install.sh" && sh "$tmpdir/hf-mount-install.sh"
```

- `hf-mount start repo openai-community/gpt2 /tmp/gpt2` — mount a repo (read-only)
- `hf-mount start --hf-token $HF_TOKEN bucket myuser/my-bucket /tmp/data` — mount a bucket (read-write)
- `hf-mount status` / `hf-mount stop /tmp/data` — list or unmount

## Tips

- Use `hf <command> --help` for full options, descriptions, usage, and real-world examples.
- Authenticate with `HF_TOKEN` env var (recommended) or with `--token`.
- Update the CLI with `hf update` (uses the correct command for the detected install method).

---

# Workflows

## Finding the Best Model for a Task

Find the best models for a task by querying official HF benchmark leaderboards, enriching results with model size data, filtering for what fits on the user's device, and returning a comparison table with benchmark scores.

### Step 1: Parse the request

Extract from the user's message:

- **Task**: what they want the model to do (coding, math/reasoning, chat, OCR, RAG/retrieval, speech recognition, image classification, multimodal, agents, etc.)
- **Device**: hardware constraints (MacBook M-series 8/16/32/64GB unified memory, RTX GPU with VRAM amount, CPU-only, cloud/no constraint, etc.)

If device is not mentioned, skip filtering entirely and return the highest-performing models regardless of size. If the task is genuinely ambiguous, ask one clarifying question.

**Device → max parameter budget.** When a device is specified, extract its available memory (unified RAM for Apple Silicon, VRAM for discrete GPUs) and apply:

- **fp16 max params (B)** ≈ memory (GB) ÷ 2
- **Q4 max params (B)** ≈ memory (GB) × 2

Examples: 16GB → 8B fp16 / 32B Q4 — 24GB VRAM → 12B fp16 / 48B Q4 — 8GB → 4B fp16 / 16B Q4

### Step 2: Find relevant benchmark datasets

```bash
curl -s -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  "https://huggingface.co/api/datasets?filter=benchmark:official&limit=500" \
  | jq '[.[] | {id, tags, description}]'
```

Select the datasets most relevant to the user's task — match on dataset id, tags, and description. Aim for comprehensive coverage: if 5 benchmarks clearly cover the task, use all 5.

### Step 3: Fetch top models from leaderboards

For each selected benchmark dataset:

```bash
curl -s -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  "https://huggingface.co/api/datasets/<namespace>/<repo>/leaderboard" \
  | jq '[.[:15] | .[] | {rank, modelId, value, verified}]'
```

Collect model IDs and scores across all benchmarks. If a leaderboard returns an error (404, 401, etc.), skip it and note it in the output. The CLI equivalent is `hf datasets leaderboard <dataset_id> --limit 15`.

### Step 4: Enrich with model metadata

For the top 10–15 candidate model IDs:

```bash
# REST API
curl -s -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  "https://huggingface.co/api/models/org/model1" | jq '{safetensors, tags, cardData}'

# CLI
hf models info org/model1 --json | jq '{safetensors, tags, cardData}'
```

Extract: **Parameters** (`safetensors.total` → B, e.g. 7_241_748_480 → "7.2B"), **License** (from tags, e.g. `license:apache-2.0`), or parse size from the model name (7b, 8b, 13b, 70b…) if `safetensors` is absent.

### Step 5: Filter and rank

**With a device:** remove models exceeding the fp16 budget; flag models that fit only with Q4 quantization; keep a slightly-over-budget top model with a "needs Q4" note rather than silently dropping it.

**Without a device:** skip size filtering — rank by benchmark score.

Then rank by benchmark score (descending) and keep the top 5–8 models. Include proprietary models (GPT-4, Claude, Gemini) if they appear, flagged as "API only / not self-hostable". Exclude them if the user asked for local/open models only.

### Step 6: Output

```markdown
| # | Model | Params | [Benchmark 1] | [Benchmark 2] | License | On device |
|---|-------|--------|--------------|--------------|---------|-----------|
| ⭐1 | [org/name](https://huggingface.co/org/name) | 7B | 85.2% | — | Apache 2.0 | Yes (fp16) |
| 2 | [org/name](https://huggingface.co/org/name) | 13B | 83.1% | 71.5% | MIT | Q4 only |
```

- Link model names to `https://huggingface.co/<model_id>`.
- Use `—` for benchmarks where the model wasn't evaluated.
- Star the top pick with ⭐.
- "On device" values: `Yes (fp16)`, `Q4 only`, `Too large`, `API only`.

After presenting the table, ask: "Would you like to run **[top recommended model]**?" If yes, offer **Run locally** (ask about the device if unknown, then give setup instructions) or **Run on HF Jobs** (see the HF Jobs section).

**Error handling:** leaderboard not found → skip and note; model missing metadata → parse size from name; no benchmarks found → fall back to `hf models list --search <task>` by popularity; all leaderboards fail → fall back to popularity search and note it.

## Dataset Viewer (read-only exploration)

The Dataset Viewer API is for read-only exploration and extraction. Base URL: `https://datasets-server.huggingface.co`. Default method `GET`; query params URL-encoded; `offset` is 0-based; `length` max is usually 100. Gated/private datasets require `Authorization: Bearer <HF_TOKEN>`.

Core workflow:

1. Optionally validate dataset availability with `/is-valid`.
2. Resolve `config` + `split` with `/splits`.
3. Preview with `/first-rows`.
4. Paginate content with `/rows` using `offset` and `length` (max 100).
5. Use `/search` for text matching and `/filter` for row predicates.
6. Retrieve parquet links via `/parquet` and totals/metadata via `/size` and `/statistics`.

Endpoints:

- `Validate dataset`: `/is-valid?dataset=<namespace/repo>`
- `List subsets and splits`: `/splits?dataset=<namespace/repo>`
- `Preview first rows`: `/first-rows?dataset=<namespace/repo>&config=<config>&split=<split>`
- `Paginate rows`: `/rows?dataset=<namespace/repo>&config=<config>&split=<split>&offset=<int>&length=<int>`
- `Search text`: `/search?dataset=<namespace/repo>&config=<config>&split=<split>&query=<text>&offset=<int>&length=<int>`
- `Filter with predicates`: `/filter?dataset=<namespace/repo>&config=<config>&split=<split>&where=<predicate>&orderby=<sort>&offset=<int>&length=<int>`
- `List parquet shards`: `/parquet?dataset=<namespace/repo>`
- `Get size totals`: `/size?dataset=<namespace/repo>`
- `Get column statistics`: `/statistics?dataset=<namespace/repo>&config=<config>&split=<split>`
- `Get Croissant metadata`: `/croissant?dataset=<namespace/repo>`

Pagination example:

```bash
curl "https://datasets-server.huggingface.co/rows?dataset=stanfordnlp/imdb&config=plain_text&split=train&offset=0&length=100"
curl "https://datasets-server.huggingface.co/rows?dataset=stanfordnlp/imdb&config=plain_text&split=train&offset=100&length=100"
```

When pagination is partial, use `num_rows_total`, `num_rows_per_page`, and `partial` from the response to drive continuation. For CLI-based parquet discovery or SQL, use `hf datasets parquet` and `hf datasets sql`.

## Creating and Managing Datasets

Two complementary toolchains: the `hf` CLI for quick repo operations, and `uv run` scripts (`dataset_manager.py` / `sql_manager.py`) for structured creation and DuckDB SQL. Both use PEP 723 inline dependencies (run with `uv run`), require `uv`, and need `HF_TOKEN` with write access.

### Create a repo (CLI)

```bash
hf repos create <namespace>/<repo> --type dataset --private --exist-ok
hf upload <namespace>/<repo> ./local/parquet-folder data --type dataset
```

Zero-local-dependency alternative: create at `https://huggingface.co/new-dataset`, upload parquet in the "Files and versions" page, then verify:

```bash
curl -s "https://datasets-server.huggingface.co/parquet?dataset=<namespace>/<repo>"
```

Low-dependency CLI flow (`npx @huggingface/hub` / `hfjs`):

```bash
export HF_TOKEN=<your_hf_token>
npx -y @huggingface/hub upload datasets/<namespace>/<repo> ./local/parquet-folder data
npx -y @huggingface/hub upload datasets/<namespace>/<repo> ./local/parquet-folder data --private
```

After upload, call `/parquet` to discover `<config>/<split>/<shard>` values for querying with `@~parquet`.

### Structured creation (`dataset_manager.py`)

```bash
# Discover existing datasets with the HF MCP server (search_datasets, get_dataset_details)

# Initialize + configure
uv run scripts/dataset_manager.py init --repo_id "your-username/dataset-name" [--private]
uv run scripts/dataset_manager.py config --repo_id "your-username/dataset-name" \
  --system_prompt "$(cat system_prompt.txt)"

# Quick setup with a template
uv run scripts/dataset_manager.py quick_setup \
  --repo_id "your-username/dataset-name" --template classification

# Add rows with template validation
uv run scripts/dataset_manager.py add_rows \
  --repo_id "your-username/dataset-name" --template qa \
  --rows_json "$(cat your_qa_data.json)"

# Stats and template list
uv run scripts/dataset_manager.py stats --repo_id "your-username/dataset-name"
uv run scripts/dataset_manager.py list_templates
```

Templates: `chat` (messages with roles + tool calls), `classification` (text/label/confidence/metadata), `qa` (question/answer/context/answer_type/difficulty), `completion` (prompt/completion/domain/style), `tabular` (columns + data).

Chat template shape:

```json
{
  "messages": [
    {"role": "user", "content": "Natural user request"},
    {"role": "assistant", "content": "Response with tool usage"},
    {"role": "tool", "content": "Tool response", "tool_call_id": "call_123"}
  ],
  "scenario": "Description of use case",
  "complexity": "simple|intermediate|advanced"
}
```

### SQL querying (`sql_manager.py`)

Query, transform, and push datasets with DuckDB SQL over the `hf://` protocol:

```bash
# Query
uv run scripts/sql_manager.py query --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition' LIMIT 10"

# Schema, sample, count
uv run scripts/sql_manager.py describe --dataset "cais/mmlu"
uv run scripts/sql_manager.py sample --dataset "cais/mmlu" --n 5
uv run scripts/sql_manager.py count --dataset "cais/mmlu" --where "subject='nutrition'"

# Unique values / distribution
uv run scripts/sql_manager.py unique --dataset "cais/mmlu" --column "subject"
uv run scripts/sql_manager.py histogram --dataset "cais/mmlu" --column "subject" --bins 20

# Filter and push a subset
uv run scripts/sql_manager.py query --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition'" \
  --push-to "username/mmlu-nutrition-subset" --private

# Export
uv run scripts/sql_manager.py export --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition'" \
  --output "nutrition.parquet" --format parquet

# Config/split control
uv run scripts/sql_manager.py query --dataset "ibm/duorc" --config "ParaphraseRC" --split "test" \
  --sql "SELECT * FROM data LIMIT 5"

# Raw SQL joining datasets
uv run scripts/sql_manager.py raw --sql "
  SELECT a.*, b.*
  FROM 'hf://datasets/dataset1@~parquet/default/train/*.parquet' a
  JOIN 'hf://datasets/dataset2@~parquet/default/train/*.parquet' b
  ON a.id = b.id LIMIT 100
"
```

`hf://` path format: `hf://datasets/{dataset_id}@{revision}/{config}/{split}/*.parquet`. The `@~parquet` revision provides auto-converted Parquet for any dataset format.

Useful DuckDB functions: `LENGTH(col)`, `regexp_replace(col, '\n', '')`, `regexp_matches(col, 'pattern')`, `choices[0]`, `array_length(choices)`, `unnest(choices)`, `USING SAMPLE 10 (RESERVOIR, 42)`, `ROW_NUMBER() OVER (PARTITION BY col ORDER BY col2)`.

Python API: `HFDatasetSQL()` with `query`, `describe`, `sample`, `count`, `histogram`, `filter_and_transform`, `push_to_hub`, `export_to_parquet`, `close`.

### Agent traces

The Hub supports raw agent session traces from the agent, Codex, and Pi Agent. Upload as original JSONL; the Hub auto-detects the trace format, tags the dataset `Traces`, and enables the trace viewer (sessions, turns, tool calls, model responses). Common local dirs: the agent `~/.agents/projects`, Codex `~/.codex/sessions`, Pi `~/.pi/agent/sessions`. Default to private repos (traces may contain prompts, paths, tool outputs, secrets, PII) and preserve raw `.jsonl` nested by project/cwd:

```bash
hf repos create <namespace>/<repo> --type dataset --private --exist-ok
hf upload <namespace>/<repo> ~/.codex/sessions codex/<project-or-cwd> --type dataset
```

## Evaluation

### Local evaluations (inspect-ai / lighteval)

Run evaluations against models on the Hub on local hardware. Frameworks: **inspect-ai** for explicit task control; **lighteval** for leaderboard-style task strings. Backends: **vllm** for throughput on supported architectures; **Transformers (`--backend hf`)** or **accelerate** as compatibility fallbacks.

```bash
# Option A: inspect-ai via Inference Providers (lowest setup overhead)
uv run scripts/inspect_eval_uv.py --model meta-llama/Llama-3.2-1B --task mmlu --limit 20

# Option B: inspect-ai on local GPU
uv run scripts/inspect_vllm_uv.py --model meta-llama/Llama-3.2-1B --task gsm8k --limit 20

# Transformers fallback
uv run scripts/inspect_vllm_uv.py --model microsoft/phi-2 --task mmlu \
  --backend hf --trust-remote-code --limit 20

# Option C: lighteval on local GPU
uv run scripts/lighteval_vllm_uv.py --model meta-llama/Llama-3.2-3B-Instruct \
  --tasks "leaderboard|mmlu|5,leaderboard|gsm8k|5" --max-samples 20 --use-chat-template

# accelerate fallback
uv run scripts/lighteval_vllm_uv.py --model microsoft/phi-2 \
  --tasks "leaderboard|mmlu|5" --backend accelerate --trust-remote-code --max-samples 20
```

Prerequisites: `uv`, `HF_TOKEN` for gated/private models, and for local GPU runs verify with `nvidia-smi`. If `nvidia-smi` is unavailable, use `inspect_eval_uv.py` (provider-backed) or hand off to HF Jobs (below).

**Workflow:** choose framework → choose backend → run a smoke test (`--limit` / `--max-samples`) → scale up only after the smoke test passes → for remote execution, submit the same script + args to HF Jobs.

**inspect-ai tasks:** `mmlu`, `gsm8k`, `hellaswag`, `arc_challenge`, `truthfulqa`, `winogrande`, `humaneval`.

**lighteval task strings** use `suite|task|num_fewshot`: `leaderboard|mmlu|5`, `leaderboard|gsm8k|5`, `leaderboard|arc_challenge|25`, `lighteval|hellaswag|0`. Multiple tasks are comma-separated in `--tasks`. The full task list is at https://github.com/huggingface/lighteval/blob/main/examples/tasks/all_tasks.txt.

**Hardware guidance:** `< 3B` → consumer GPU / Apple Silicon; `3B–13B` → stronger local GPU; `13B+` → high-memory local GPU or HF Jobs.

**Troubleshooting:** CUDA/vLLM OOM → reduce `--batch-size` / `--gpu-memory-utilization`, use a smaller smoke-test model, or hand off to HF Jobs. vLLM doesn't support the model → `--backend hf` (inspect) or `--backend accelerate` (lighteval). Gated repo fails → verify `HF_TOKEN`. Custom model code → `--trust-remote-code`.

### Model card evaluation (model-index)

Add structured evaluation results to Hugging Face model cards. Supports extracting eval tables from README content, importing scores from Artificial Analysis, and running custom model evaluations with vLLM/lighteval.

**⚠️ Before creating ANY pull request with `--create-pr`, check for existing open PRs first:**

```bash
uv run scripts/evaluation_manager.py get-prs --repo-id "username/model-name"
```

If open PRs exist, do NOT create a new one — warn the user, show the PR URLs, and only proceed if they explicitly confirm.

Key workflow: `get-prs` → `inspect-tables` → `extract-readme --table N` (prints YAML by default) → `--apply` (push) or `--create-pr` (PR).

```bash
# Inspect tables to get table numbers and column hints
uv run scripts/evaluation_manager.py inspect-tables --repo-id "username/model"

# Extract a specific table (YAML printed by default)
uv run scripts/evaluation_manager.py extract-readme --repo-id "username/model" --table 1 \
  [--model-column-index <column index shown by inspect-tables>] \
  [--model-name-override "<exact column header/model name>"] \
  [--task-type "text-generation"] [--dataset-name "Custom Benchmarks"]

# Apply
uv run scripts/evaluation_manager.py extract-readme --repo-id "username/model" --table 1 --apply
uv run scripts/evaluation_manager.py extract-readme --repo-id "username/model" --table 1 --create-pr

# Import from Artificial Analysis (AA_API_KEY required)
AA_API_KEY=... uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" --model-name "claude-sonnet-4" --repo-id "username/model-name" \
  [--create-pr]

# View / validate
uv run scripts/evaluation_manager.py show --repo-id "username/model-name"
uv run scripts/evaluation_manager.py validate --repo-id "username/model-name"
```

Model-index format:

```yaml
model-index:
  - name: Model Name
    results:
      - task:
          type: text-generation
        dataset:
          name: Benchmark Dataset
          type: benchmark_type
        metrics:
          - name: MMLU
            type: mmlu
            value: 85.2
        source:
          name: Source Name
          url: https://source-url.com
```

Rules: no markdown in the model name; only URLs in `source.url`. Name matching uses exact normalized token matching (strips markdown, lowercases, replaces `-`/`_` with spaces) — it fails rather than guessing, so use `--model-name-override` with the exact header for comparison tables. For transposed tables (models as rows) ensure only one row is extracted.

**Prerequisites:** `HF_TOKEN` (write), `AA_API_KEY` for Artificial Analysis; `.env` is auto-loaded. Dependencies: huggingface_hub, markdown-it-py, python-dotenv, pyyaml, requests; for vLLM evals: lighteval[accelerate,vllm], vllm, torch, transformers, accelerate.

### Running evaluations on HF Jobs

Submit an evaluation job with `hf jobs uv run`, passing the eval script and a `--` separator before its args:

```bash
# Provider-backed inspect eval
HF_TOKEN=$HF_TOKEN hf jobs uv run hf-evaluation/scripts/inspect_eval_uv.py \
  --flavor cpu-basic --secret HF_TOKEN=$HF_TOKEN \
  -- --model "meta-llama/Llama-2-7b-hf" --task "mmlu"

# GPU (A10G)
HF_TOKEN=$HF_TOKEN hf jobs uv run hf-evaluation/scripts/inspect_eval_uv.py \
  --flavor a10g-small --secret HF_TOKEN=$HF_TOKEN \
  -- --model "meta-llama/Llama-2-7b-hf" --task "gsm8k"

# lighteval with vLLM
hf jobs uv run scripts/lighteval_vllm_uv.py \
  --flavor a10g-small --secrets HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" --tasks "leaderboard|mmlu|5"

# inspect-ai with vLLM
hf jobs uv run scripts/inspect_vllm_uv.py \
  --flavor a10g-small --secrets HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" --task "mmlu"
```

Hardware recommendations for vLLM evals: `< 3B` → `t4-small`; `3B–13B` → `a10g-small`; `13B–34B` → `a10g-large`; `34B+` → `a100-large`. Multi-GPU via `--tensor-parallel-size`. Use `--backend hf` / `--backend accelerate` when vLLM doesn't support the model.

## HF Jobs (managed compute)

Run any workload on fully managed Hugging Face infrastructure — cloud CPUs, GPUs, or TPUs — with no local setup. Use for data processing, batch inference, experiments, model training, synthetic data generation, testing, and scheduled jobs. Jobs require a paid plan (Pro/Team/Enterprise).

### Two submission styles

**UV scripts (recommended)** use PEP 723 inline dependencies:

```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["transformers", "torch"]
# ///
from transformers import pipeline
print(pipeline("sentiment-analysis")("I love Hugging Face!"))
""",
    "flavor": "cpu-basic",
    "timeout": "30m",
})
```

CLI: `hf jobs uv run my_script.py --flavor cpu-basic --timeout 30m`. Python API: `run_uv_job("my_script.py", flavor="cpu-basic", timeout="30m")`.

**Docker jobs** for full image control:

```python
hf_jobs("run", {
    "image": "python:3.12",
    "command": ["python", "-c", "print('Hello from HF Jobs!')"],
    "flavor": "cpu-basic",
    "timeout": "30m",
})
```

CLI: `hf jobs run python:3.12 python -c "print('Hello!')"`. Python API: `run_job(image="python:3.12", command=[...], flavor="cpu-basic")`.

**Script path rules:** with the `hf_jobs()` MCP tool, `script` must be inline code or a URL — a local path won't exist in the remote container. Read and pass contents:

```python
from pathlib import Path
script = Path("hf-jobs/scripts/foo.py").read_text()
hf_jobs("uv", {"script": script})
```

With the `hf jobs uv run` CLI, local file paths work (the CLI uploads the script): `hf jobs uv run ./scripts/foo.py -- --your --args`.

**Extras:** custom image (`"image": "vllm/vllm-openai:latest"`), Python version (`"python": "3.11"`), runtime deps (`"dependencies": ["transformers", "torch>=2.0"]`). Ready-made UV scripts live in the `uv-scripts` org (`dataset_search({"author": "uv-scripts", ...})`).

### Hardware selection

| Workload | Hardware |
|---|---|
| Data processing, testing | `cpu-basic`, `cpu-upgrade` |
| Small models, demos (<1B) | `t4-small` |
| Medium models (1–7B) | `t4-medium`, `l4x1` |
| Large models (7–13B) | `a10g-small`, `a10g-large` |
| Very large (13B+) | `a100-large` |
| Batch inference | `a10g-large`, `a100-large` |
| Multi-GPU / parallel | `l4x4`, `a10g-largex2`, `a10g-largex4` |
| TPU (JAX/Flax) | `v5e-1x1`, `v5e-2x2`, `v5e-2x4` |

Start small and scale up. Full flavor list includes CPU (`cpu-basic`, `cpu-upgrade`), GPU (`t4-small`, `t4-medium`, `l4x1`, `l4x4`, `a10g-small`, `a10g-large`, `a10g-largex2`, `a10g-largex4`, `a100-large`, `a100x4`, `a100x8`, `h200`, `rtx-pro-6000`), and TPU (`v5e-1x1`, `v5e-2x2`, `v5e-2x4`).

### Tokens and persistence

The Jobs environment is **ephemeral** — all files are deleted when the job ends. Persist results or all work is lost:

```python
model.push_to_hub("username/model-name", token=os.environ["HF_TOKEN"])
dataset.push_to_hub("username/dataset-name", token=os.environ["HF_TOKEN"])
api.upload_file(path_or_fileobj="results.json", path_in_repo="results.json",
                repo_id="username/results", token=os.environ["HF_TOKEN"])
# or push to S3/GCS or POST to your own API
```

Token handling (critical):

- **MCP tool:** `secrets={"HF_TOKEN": "$HF_TOKEN"}` — `$HF_TOKEN` is auto-replaced with your logged-in token.
- **Python API (`HfApi().run_uv_job()`):** `secrets={"HF_TOKEN": get_token()}` — you MUST pass the real token; the literal `"$HF_TOKEN"` yields a 9-char invalid token and 401.
- Prefer `secrets` over `env` (secrets are encrypted server-side; env vars appear in logs).
- In scripts, read `os.environ.get("HF_TOKEN")`; verify with `assert "HF_TOKEN" in os.environ` and `hf_whoami()`.

### Timeouts

Default is **30 minutes**. Set a custom timeout: `"2h"`, `"90m"`, `300`, `"1.5h"`, `"1d"`. Guidelines: quick test 10–30m; data processing 1–2h; batch inference 2–4h; experiments 4–8h; long-running 8–24h. Always add 20–30% buffer. On timeout the job is killed immediately and unsaved progress is lost.

### Cost estimation

`Total cost = hours × cost/hour`. Examples: cpu-basic (~$0.10/h) × 0.25h ≈ $0.03; l4x1 (~$2.50/h) × 2h = $5; a10g-large (~$5/h) × 4h = $20. Optimize by starting small, setting timeouts, checkpointing, and not over-provisioning.

### Monitoring

```python
hf_jobs("ps")                                    # list jobs
hf_jobs("inspect", {"job_id": "your-job-id"})    # inspect
hf_jobs("logs", {"job_id": "your-job-id"})       # logs
hf_jobs("cancel", {"job_id": "your-job-id"})     # cancel
```

Python API: `list_jobs()`, `inspect_job(job_id)`, `fetch_job_logs(job_id)`, `cancel_job(job_id)`. CLI: `hf jobs ps` / `hf jobs logs <id>` / `hf jobs cancel <id>`. Monitoring URL: `https://huggingface.co/jobs/username/job-id`. Avoid polling — let the user request status checks.

### Scheduled jobs and webhooks

Schedule with `@annually`, `@monthly`, `@weekly`, `@daily`, `@hourly`, or a CRON expression:

```python
hf_jobs("scheduled uv", {"script": "your_script.py", "schedule": "0 9 * * 1", "flavor": "cpu-basic"})
```

Manage via `hf_jobs("scheduled ps"|"scheduled inspect"|"scheduled suspend"|"scheduled resume"|"scheduled delete", {...})` or Python `list_scheduled_jobs` / `inspect_scheduled_job` / `suspend_scheduled_job` / `resume_scheduled_job` / `delete_scheduled_job`. CLI: `hf jobs scheduled list|inspect|suspend|resume|delete`.

Webhooks trigger jobs when watched repos change; the job receives a `WEBHOOK_PAYLOAD` env var (JSON). CLI: `hf webhooks create --watch ...`; Python: `create_webhook(job_id=..., watched=[...], domains=["repo", "discussion"], secret=...)`.

### Common workload patterns

Prefer shipped scripts in `hf-jobs/scripts/` over new templates:

- `generate-responses.py` — dataset → vLLM responses → push to Hub (GPU + write token).
- `cot-self-instruct.py` — CoT Self-Instruct synthetic data + filtering → push to Hub (GPU + write token).
- `finepdfs-stats.py` — Polars streaming stats over `finepdfs-edu` parquet, optional push (CPU often enough).

### Failure modes

- **OOM** → reduce batch/chunk size; upgrade cpu → t4 → a10g → a100.
- **Timeout** → check logs for actual runtime; raise timeout with buffer; optimize; chunk data.
- **Hub push failures** → add token to secrets (MCP `"$HF_TOKEN"`, Python `get_token()`); verify token and permissions.
- **Missing dependencies** → add to the PEP 723 header.
- **Auth errors** → `hf_whoami()` locally, correct secrets param, re-login `hf auth login`.

### Quick reference: MCP vs CLI vs Python API

| Operation | MCP Tool | CLI | Python API |
|---|---|---|---|
| Run UV script | `hf_jobs("uv", {...})` | `hf jobs uv run script.py` | `run_uv_job("script.py")` |
| Run Docker job | `hf_jobs("run", {...})` | `hf jobs run image cmd` | `run_job(image, command)` |
| List jobs | `hf_jobs("ps")` | `hf jobs ps` | `list_jobs()` |
| View logs | `hf_jobs("logs", {...})` | `hf jobs logs <id>` | `fetch_job_logs(job_id)` |
| Cancel job | `hf_jobs("cancel", {...})` | `hf jobs cancel <id>` | `cancel_job(job_id)` |
| Schedule UV | `hf_jobs("scheduled uv", {...})` | `hf jobs scheduled uv run SCHEDULE script.py` | `create_scheduled_uv_job()` |
| Schedule Docker | `hf_jobs("scheduled run", {...})` | `hf jobs scheduled run SCHEDULE image cmd` | `create_scheduled_job()` |
| List scheduled | `hf_jobs("scheduled ps")` | `hf jobs scheduled ps` | `list_scheduled_jobs()` |
| Delete scheduled | `hf_jobs("scheduled delete", {...})` | `hf jobs scheduled delete <id>` | `delete_scheduled_job()` |

---

## Merged from

- `hugging-face-community-evals` — local inspect-ai/lighteval evaluation workflows, backend selection, hardware guidance
- `hugging-face-dataset-viewer` — Dataset Viewer API endpoints and pagination
- `hugging-face-datasets` — dataset creation (dataset_manager.py) and DuckDB SQL querying (sql_manager.py)
- `hugging-face-evaluation` — model card model-index workflow, README extraction, Artificial Analysis import
- `hugging-face-jobs` — HF Jobs submission, hardware, persistence, timeouts, cost, monitoring, scheduling, webhooks
- `huggingface-best` — benchmark-leaderboard model finder workflow

## Limitations

- Use this skill only when the task clearly matches its upstream product or API scope.
- Verify commands, API behavior, pricing, quotas, credentials, and deployment effects against current official documentation before making changes.
- Do not treat generated examples as a substitute for environment-specific tests, security review, or user approval for destructive or costly actions.