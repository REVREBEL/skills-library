# Installation Guide

## Prerequisites

- **Python 3.10+** with pip
- **Git** for cloning the repository
- **the agent CLI** installed and configured

Optional:
- **Playwright** for screenshot capabilities

## Quick Install

### Plugin Install (the agent 1.0.33+)

The recommended path. Inside the agent:

```
/plugin marketplace add AgriciDaniel/claude-seo
/plugin install claude-seo@agricidaniel-seo
```

### Manual Install (Unix, macOS, Linux)

```bash
git clone --depth 1 https://github.com/AgriciDaniel/claude-seo.git
bash claude-seo/install.sh
```

Review-then-run alternative:

```bash
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/install.sh > install.sh
cat install.sh        # review
bash install.sh       # run when satisfied
rm install.sh
```

### Manual Install (Windows, PowerShell)

```powershell
git clone --depth 1 https://github.com/AgriciDaniel/claude-seo.git
powershell -ExecutionPolicy Bypass -File claude-seo\install.ps1
```

The Windows path uses `git clone` rather than `irm | iex` because the agent's own security guardrails flag piped remote-script execution. Inspect `install.ps1` before running.

## Manual Installation

1. **Clone the repository**

```bash
git clone https://github.com/AgriciDaniel/claude-seo.git
cd claude-seo
```

2. **Run the installer**

```bash
./install.sh
```

3. **Install Python dependencies** (if not done automatically)

The installer creates a venv at `~/.agents/skills/seo/.venv/`. If that fails, install manually:

```bash
# Option A: Use the venv
~/.agents/skills/seo/.venv/bin/pip install -r ~/.agents/skills/seo/requirements.txt

# Option B: User-level install
pip install --user -r ~/.agents/skills/seo/requirements.txt
```

4. **Install Playwright browsers** (optional, for visual analysis)

```bash
pip install playwright
playwright install chromium
```

Playwright is optional. Without it, visual analysis uses WebFetch as a fallback.

## Installation Paths

The installer copies files to:

| Component | Path |
|-----------|------|
| Main skill | `~/.agents/skills/seo/` |
| Sub-skills | `~/.agents/skills/seo-*/` |
| Subagents | `~/.agents/agents/seo-*.md` |

## Verify Installation

1. Start the agent:

```bash
claude
```

2. Check that the skill is loaded:

```
/seo
```

You should see a help message or prompt for a URL.

## Uninstallation

If installed as a plugin:

```
/plugin uninstall claude-seo@agricidaniel-seo
/plugin marketplace remove AgriciDaniel/claude-seo
```

If installed manually, run the uninstaller from a fresh clone:

```bash
git clone --depth 1 https://github.com/AgriciDaniel/claude-seo.git
bash claude-seo/uninstall.sh
```

`uninstall.sh` removes all installed sub-skills, sub-agents, and the plugin's MCP entries from `~/.agents/settings.json`. Do not maintain a hand-coded `rm` list. The shipped uninstaller is the canonical source.

## Upgrading

To upgrade to the latest version:

```bash
# Uninstall current version
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/uninstall.sh | bash

# Install new version
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/install.sh | bash
```

## Troubleshooting

### "Skill not found" error

Ensure the skill is installed in the correct location:

```bash
ls ~/.agents/skills/seo/SKILL.md
```

If the file doesn't exist, re-run the installer.

### Python dependency errors

Install dependencies manually:

```bash
pip install beautifulsoup4 requests lxml playwright Pillow urllib3 validators
```

### Playwright screenshot errors

Install Chromium browser:

```bash
playwright install chromium
```

### Permission errors on Unix

Make sure scripts are executable:

```bash
chmod +x ~/.agents/skills/seo/scripts/*.py
```