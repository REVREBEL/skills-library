# Task 13: Build the Reusable Skill Intake, Library, and Runtime Sync Pipeline

## Objective

Convert the completed Agent Skills rebuild machinery into a reusable maintenance system for adding, reviewing, updating, and publishing skills without repeating the original 12-phase rebuild.

The finished system must support a simple operating model:

```text
External install / downloaded skill
            ↓
         intake
            ↓
review / normalize / classify / validate
            ↓
   canonical skills library
            ↓
       symbolic link
            ↓
      .agents/skills
```

The canonical Git repository is the **single source of truth for skill files**.

`.agents/skills` is the **runtime/discovery layer** and should ultimately consist of symbolic links pointing back to canonical skills in the library.

The system must also detect skills installed directly into `.agents/skills` by external tools such as `skills.sh`, ingest them into the canonical library workflow, and then replace the physical runtime copy with the appropriate symbolic link.

---

# Core Operating Model

## Canonical Library

The repository contains the authoritative copies of approved skills.

The existing validated rebuilt library currently under:

```text
task-folder/agents/skills-rebuild/
```

must be used as the starting source for the permanent canonical library.

Do not maintain two physical copies of approved skills.

---

## Intake

Create a dedicated intake location for new or externally discovered skills.

Suggested location:

```text
intake/
```

A skill enters intake when:

1. The user manually places a skill there.
2. An external installer creates a physical skill directory in `.agents/skills`.
3. A skill is imported from another repository or source.
4. An existing canonical skill requires substantial reprocessing.

Intake is temporary.

Approved skills leave intake and become canonical library skills.

Rejected or quarantined skills must not enter the canonical library.

---

## Runtime Layer

`.agents/skills/` should ultimately contain symbolic links for managed skills.

Example:

```text
.agents/skills/cohort-analysis
    ->
<skills-library>/library/data-and-ai/.../cohort-analysis
```

The actual skill files exist only in the canonical library.

Editing the canonical skill therefore immediately updates the runtime skill exposed through `.agents/skills`.

---

# Work

## 1. Establish the Permanent Library Structure

Design and create the permanent repository structure.

Target concept:

```text
skills-library/
├── library/
│   ├── business-and-operations/
│   ├── content-and-documentation/
│   ├── data-and-ai/
│   ├── design-and-experience/
│   ├── development/
│   ├── infrastructure-and-ops/
│   ├── marketing-and-seo/
│   ├── meta-and-agent-skills/
│   ├── quality-and-security/
│   ├── workflow-and-automation/
│   └── SKILL.md
│
├── intake/
│
├── tools/
│   └── skill-library/
│
└── audit/
```

Determine the exact final structure from the validated rebuild rather than blindly applying this example.

Preserve the validated taxonomy and functional routing established during Phases 05–12.

---

## 2. Extract Reusable Logic From the Rebuild

Review the scripts, validators, ledgers, and generators created during the original rebuild.

Identify reusable code covering at minimum:

- package discovery
- inventory
- Agent Skill structural validation
- compatibility checks
- provider-specific coupling detection
- duplicate and overlap analysis
- merge/consolidation analysis
- oversized-skill analysis
- normalization
- bundled-resource validation
- Python/script validation
- dangerous/destructive command safeguards
- secret detection
- absolute workstation path detection
- taxonomy classification
- functional routing
- router link generation
- router traversal validation
- skill-name collision detection
- semantic routing checks
- pilot validation
- Git diff/release validation

Do not rewrite proven logic unnecessarily.

Extract reusable functions into maintainable modules while preserving the original Phase 01–12 scripts as historical rebuild evidence where appropriate.

---

## 3. Remove Frozen Rebuild Assumptions

The original rebuild validators intentionally contain fixed expectations such as:

```text
2,103 active skills
26 routers
2,177 router links
```

These values were valid for the completed rebuild but cannot remain fixed in a living library.

Replace fixed population expectations in the reusable pipeline with derived values.

Example concept:

```text
current canonical population
+ approved additions
- approved removals
= expected resulting population
```

The system must validate changes relative to the current canonical library state rather than assuming the original Phase 12 population forever.

Do not modify historical Phase 01–12 evidence merely to make it dynamic.

---

## 4. Build the Intake Scanner

Create a command that scans:

```text
intake/
```

and identifies every candidate skill package.

It must determine:

- skill name
- source
- package structure
- `SKILL.md` presence
- frontmatter validity
- bundled scripts
- bundled resources
- provider assumptions
- potentially unsafe behavior
- local-machine path dependencies
- likely duplicate/overlap candidates
- likely functional category
- likely functional parent router

The scan must be non-destructive.

---

## 5. Scan `.agents/skills` for External Installs

The pipeline must also inspect:

```text
.agents/skills/
```

and classify each entry.

Minimum classifications:

### Managed Link

A symbolic link pointing to a canonical skill in the skills library.

Action:

```text
PASS / LEAVE UNCHANGED
```

### External Physical Skill

A real directory or file package created directly under `.agents/skills`.

Action:

```text
DISCOVER
→ copy/move safely into intake
→ process through intake pipeline
```

Do not immediately trust it as canonical.

### Broken Managed Link

A symbolic link whose canonical target no longer exists.

Action:

```text
REPORT / REPAIR
```

### External Symbolic Link

A symbolic link that points somewhere outside the canonical skills library.

Action:

```text
REPORT / INSPECT
```

Do not overwrite automatically.

### Collision

An incoming skill conflicts with an existing canonical/runtime name.

Action:

```text
STOP FOR REVIEW
```

---

## 6. Preserve External Installer Compatibility

When an externally installed skill is discovered, inspect how it was exposed to supported agents/applications.

This may include:

- `.agents/skills`
- symbolic links
- agent-specific skill directories
- configuration files
- manifests
- package metadata
- other installer-created references

Record the discovered integration before modifying the installation.

After canonical ingestion, preserve compatibility.

Prefer this topology where possible:

```text
Application-specific location
        ↓
.agents/skills/<runtime-name>
        ↓
canonical skills library
```

If an application uses configuration rather than symbolic links, update only the specific configuration necessary to preserve availability.

Do not blindly rewrite `package.json` or any other configuration merely because it exists.

Determine actual integration behavior first.

---

## 7. Process Each Intake Skill

Each candidate must pass through the reusable equivalents of the original rebuild gates.

For each candidate:

### Validate

Confirm it is a valid Agent Skill package.

### Compatibility Review

Identify unsupported or provider-specific assumptions.

### Duplicate / Overlap Review

Compare against the current canonical library.

Classify as one of:

```text
NEW
MERGE
KEEP_SEPARATE
REPLACE
RENAME
QUARANTINE
REJECT
REVIEW_REQUIRED
```

Do not automatically merge uncertain skills.

### Normalize

Bring the approved package into current canonical standards.

### Classify

Assign its functional category/subcategory.

### Route

Assign exactly one intended functional routing path unless the architecture explicitly requires otherwise.

### Validate Again

Confirm the normalized result is internally valid.

---

## 8. Add Human Approval Gates

The system must stop rather than make irreversible architectural decisions when:

- significant semantic overlap exists
- a merge is recommended
- an existing canonical skill would be replaced
- a runtime-name collision occurs
- a new top-level category appears necessary
- routing is ambiguous
- provider-specific behavior cannot safely be generalized
- destructive functionality is discovered
- provenance is unclear
- external application configuration would need substantial modification

The output should clearly explain:

```text
Candidate
Issue
Recommended decision
Reason
Affected existing skill(s)
Options
```

---

## 9. Install Approved Skills Into the Canonical Library

Once approved:

- move the normalized skill from intake into its canonical library location
- update its canonical registry record
- update functional routing data
- update the appropriate router
- update runtime-name mappings
- preserve provenance
- record the intake transaction

There must be one authoritative physical skill package after installation.

---

## 10. Build the Runtime Manifest

Create a machine-readable manifest mapping runtime names to canonical skill locations.

Example fields:

```text
runtime_name
canonical_name
canonical_path
functional_parent
source
managed
installed_at
last_validated
```

The manifest is the authoritative recipe for creating managed `.agents/skills` links.

It must solve flat-runtime-name collisions deterministically.

Do not rely solely on folder-name inference.

---

## 11. Build `.agents/skills` Symlink Reconciliation

Create a deterministic synchronization command.

For every managed skill:

```text
.agents/skills/<runtime-name>
```

must be a symbolic link to its canonical library package.

The command must:

- create missing managed links
- verify valid managed links
- repair broken managed links
- identify externally installed physical directories
- identify unknown external symlinks
- detect collisions
- never silently overwrite an unmanaged destination

The command must be idempotent.

Running it repeatedly without library changes should produce no changes.

---

## 12. Preserve Single-Source-of-Truth Behavior

After a skill becomes managed:

```text
canonical library skill
```

is the only physical authoritative copy controlled by this system.

`.agents/skills/<runtime-name>` is a pointer.

Do not maintain synchronized physical copies.

---

## 13. Build Library Validation

Create a reusable validation command for the living library.

At minimum verify:

- all canonical skills exist
- all canonical packages have valid `SKILL.md`
- frontmatter contracts pass
- relative links resolve
- bundled resources exist
- qualifying scripts parse
- destructive safeguards remain valid
- no unapproved secrets exist
- no workstation-specific paths exist
- router links resolve
- every canonical active skill has its intended functional routing
- no unintended orphan skills exist
- runtime manifest matches the canonical library
- managed symlinks resolve correctly
- no unmanaged destination would be overwritten

Reuse Phase 11/12 validation logic wherever possible.

---

## 14. Build Targeted Pilot Validation

New skills must not require a complete Phase 12 eight-domain pilot every time.

Instead:

- run representative routing prompts for each new skill
- test its nearest semantic competitors
- verify selected functional routing
- verify required bundled tools/scripts
- verify handoff behavior when relevant

Run broader regression pilots only when taxonomy/router architecture changes.

---

## 15. Create the User-Facing Commands

The normal operating workflow should be simple.

Target interface:

```bash
python3 tools/skill-library.py scan
```

Scans intake and `.agents/skills` without modifying anything.

```bash
python3 tools/skill-library.py intake
```

Processes discovered candidates and produces recommendations.

```bash
python3 tools/skill-library.py apply
```

Applies approved intake decisions to the canonical library.

```bash
python3 tools/skill-library.py sync
```

Reconciles `.agents/skills` symbolic links with the canonical runtime manifest.

```bash
python3 tools/skill-library.py validate
```

Runs full living-library validation.

Optionally:

```bash
python3 tools/skill-library.py status
```

Returns a concise summary such as:

```text
Canonical skills: 2,118
Managed runtime links: 2,118
New external installs: 0
Broken links: 0
Pending intake: 0
Conflicts: 0
Validation: PASS
```

Exact command names may differ if a cleaner implementation is justified.

---

## 16. Create a Permanent Change Ledger

Do not mutate the original rebuild inventory as though new skills existed during the historical rebuild.

Create a new ongoing change ledger.

Record at minimum:

```text
change_id
timestamp
operation
source
source_path
original_name
canonical_name
runtime_name
decision
category
subcategory
canonical_path
functional_parent
overlap_candidates
validation_status
pilot_status
commit
pr
merge_sha
```

Every future add/update/remove operation must be traceable.

---

## 17. Protect Historical Rebuild Evidence

The original rebuild artifacts are historical evidence.

Do not silently rewrite them into the new operating model.

Separate:

```text
historical rebuild evidence
```

from:

```text
living library state
```

Once the reusable pipeline is proven, determine what portions of:

```text
task-folder/agents/skills-rebuild/
```

can be archived or removed.

Do not delete the historical workspace until:

- the canonical production library has been established
- reusable tooling has been extracted
- required audit evidence has been preserved
- `.agents/skills` runtime links have been generated
- complete validation passes without dependency on the rebuild workspace

---

# Required Safety Properties

The pipeline must be:

### Non-destructive by default

Scanning must never change files.

### Idempotent

Repeated sync/validation runs with no changes must result in no changes.

### Conflict-safe

Never overwrite an unmanaged `.agents/skills` entry.

### Auditable

Every accepted library change has provenance and a recorded decision.

### Reversible

Changes should occur through Git and reviewable commits.

### Single-source-of-truth

Canonical skill content exists in one managed physical location.

### External-installer aware

Physical skills newly appearing in `.agents/skills` are treated as intake candidates rather than automatically trusted or deleted.

---

# Representative End-to-End Tests

Test at minimum:

## Scenario A: Manual Intake

Place one valid new skill into:

```text
intake/
```

Expected:

```text
detect
→ analyze
→ approve
→ canonical library
→ router update
→ runtime manifest
→ .agents/skills symlink
→ validation PASS
```

## Scenario B: External Installer

Simulate an external installer creating:

```text
.agents/skills/new-external-skill/
```

Expected:

```text
detect physical directory
→ capture installer/integration state
→ intake
→ normalize
→ canonical library
→ remove temporary runtime physical copy
→ create .agents/skills/new-external-skill symlink
→ verify existing application integrations still work
```

## Scenario C: Existing Managed Skill

Run sync against a valid managed symlink.

Expected:

```text
no changes
```

## Scenario D: Broken Link

Delete/move a canonical target.

Expected:

```text
broken link detected
→ no destructive action
→ actionable repair report
```

## Scenario E: Name Collision

Introduce a candidate sharing a runtime name with an existing canonical skill.

Expected:

```text
conflict detected
→ no overwrite
→ human decision required
```

## Scenario F: Semantic Overlap

Introduce a skill substantially overlapping an existing canonical skill.

Expected:

```text
overlap detected
→ recommended merge/keep-separate decision
→ human approval required
```

---

# Required Artifacts

Create permanent documentation for the new system, including:

```text
docs/skill-library-workflow.md
```

describing:

- where skills live
- where new skills go
- what `.agents/skills` represents
- how external installs are handled
- how symbolic links work
- how to run scan/intake/apply/sync/validate
- how conflicts are handled
- how to recover from broken links

Create machine-readable state artifacts for:

- runtime manifest
- ongoing change ledger
- intake decisions
- validation results

Exact filenames may be selected during implementation if better naming is justified.

---

# Repository Workflow

Perform this work on a dedicated branch from current `main`.

Suggested branch:

```text
feature/reusable-skill-library-pipeline
```

Keep implementation commits logically separated.

Open a reviewable PR against `main`.

Do not merge until:

- end-to-end tests pass
- existing canonical library validation passes
- runtime symlink reconciliation passes
- no existing skills are silently lost
- external-install simulation passes
- conflicts are safely stopped
- the new process has been exercised with at least one real representative skill

---

# Completion Gate

Task 13 is complete only when the following user workflow works:

```text
1. A new skill appears in intake or .agents/skills.
2. The pipeline discovers it.
3. The pipeline evaluates it using the rebuilt library standards.
4. Any material conflict is surfaced for approval.
5. The approved skill is installed once into the canonical library.
6. Routers and manifests are updated.
7. .agents/skills exposes the skill through a symbolic link.
8. Existing application integrations continue to resolve.
9. Validation passes.
10. The change is recorded and reviewable in Git.
```

The final result must eliminate the need to manually repeat the original 12-phase rebuild when adding future skills.

The intended normal instruction to an agent should become:

> **Process the skill intake and sync the library.**

Everything else should be handled by the reusable pipeline or surfaced only when a human decision is genuinely required.