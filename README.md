# Using AI to get feedback on your research

A collection of [Claude Code](https://claude.ai/code) skills for academic research review. Originally developed by [Claes Bäckman](https://claesbackman.com). Adapted for psychology and neuroscience by [Valentin Guigon](https://valentinguigon.substack.com).


The canonical authored workflows live under `Skills/`.

This repository also ships a Codex plugin package at `plugins/ai-research-feedback/`. That package is the Codex-facing install surface, and its bundled skill payloads are derived from `Skills/` rather than authored separately.

To keep those surfaces in sync:

- `scripts/derive_codex_plugin_skills.py` copies the canonical skills from `Skills/` into `plugins/ai-research-feedback/skills/`
- `.github/workflows/derive-codex-plugin-skills.yml` runs that derivation on push
- `.agents/plugins/marketplace.json` exposes the local plugin to Codex as a repo-scoped marketplace

## Using These Workflows

There are two supported ways to use this repository today:

1. Claude Code skills
   Install individual markdown commands from `Skills/*.md` into `~/.claude/commands/` or `.claude/commands/`.
2. Codex plugin
   Use the packaged plugin under `plugins/ai-research-feedback/` through a Codex marketplace.

### Codex Plugin Notes

Codex plugins are not installed by dropping a bare `SKILL.md` file into `~/.agents/`. In the Codex plugin model, `~/.agents/plugins/marketplace.json` is a personal marketplace file, and `$REPO_ROOT/.agents/plugins/marketplace.json` is a repo marketplace file. Those marketplace entries point Codex at a plugin folder that contains `.codex-plugin/plugin.json` plus bundled `skills/`.

For this repo:

- repo-scoped marketplace file: `.agents/plugins/marketplace.json`
- plugin package root: `plugins/ai-research-feedback/`
- plugin manifest: `plugins/ai-research-feedback/.codex-plugin/plugin.json`

If you want the plugin available outside this repo, the Codex docs describe a personal-marketplace pattern using:

- `~/.agents/plugins/marketplace.json`
- a local plugin directory, commonly `~/.codex/plugins/<plugin-name>/`

So the short version is:

- `curl -o ~/.claude/commands/...` makes sense for Claude commands
- `curl -o ~/.agents/plugins/marketplace.json ...` can make sense for Codex marketplace setup
- `~/.agents/` is marketplace wiring, not the place where the skill instructions themselves live

## Maintained Skills

- `Skills/review-paper.md`: Full referee-style paper review command.
- `Skills/review-paper-light.md`: Fast 2-agent paper check.
- `Skills/review-paper-code.md`: Paper-code reproducibility and alignment review.
- `Skills/review-pap.md`: Pre-analysis plan review command.
- `Skills/review-grant.md`: Grant proposal review command.


## Skills

### `review-paper` — Pre-Submission Referee Report

Runs a rigorous pre-submission review of an academic paper, simulating the scrutiny of a specific journal's editorial board. Six specialized review agents run in parallel and consolidate their findings into a single structured report.

**What it reviews:**

| Agent | Focus |
|---|---|
| 1 | Spelling, grammar, and academic style |
| 2 | Internal consistency and cross-reference verification |
| 3 | Unsupported claims and experimental design integrity |
| 4 | Mathematics, equations, and notation |
| 5 | Tables, figures, and their documentation |
| 6 | Contribution evaluation (adversarial journal-specific referee) |

**Installation:**

```bash
curl -o ~/.claude/commands/review-paper.md \
  https://raw.githubusercontent.com/ValentinGuigon/AI-research-feedback/main/Skills/review-paper.md
```

For a project-local install:

```bash
mkdir -p .claude/commands && curl -o .claude/commands/review-paper.md \
  https://raw.githubusercontent.com/ValentinGuigon/AI-research-feedback/main/Skills/review-paper.md
```

**Usage:**

```text
/review-paper
/review-paper PsychSci
/review-paper NatureNeuro path/to/paper.docx
```

**Supported journals:**

| Category | Journals |
|---|---|
| Top-tier neuroscience | `NatureNeuro`, `Neuron`, `eLife`, `CurrBiol` |
| Broad science / Nature family | `NatureHB`, `PNAS` |
| Cognitive and behavioral | `PsychSci`, `JNeurosci` |
| Neuroimaging | `NeuroImage`, `CerebCortex` |
| Computational / open science | `PLoSCB`, `PLoSOne`, `CommsPsych` |

If no journal is specified, the command applies high general standards without a specific journal persona. If no path is provided, it auto-detects the paper in this priority order: `.tex`  `.md`  `.pdf`  `.docx`.

**Output:**

Saves a consolidated report to `PRE_SUBMISSION_REVIEW_[YYYY-MM-DD].md` in the current directory, automatically appending `-v2`, `-v3`, and so on if a file already exists.

**Customization:**

- Add journals or fields by editing the recognized journal names list in the skill file.
- Add project-specific context in your prompt or in a local `CLAUDE.md` file.
- Adjust folder discovery or save paths directly in the skill if your project structure differs from the default assumptions.

**Requirements:**

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with access to the `general-purpose` subagent.
- A paper in `.tex`, `.md`, `.pdf`, or `.docx` format. For `.pdf`, `pdftotext` (poppler-utils) or `pypdf` must be installed. For `.docx`, `pandoc` must be installed.

### `review-paper-light` — Quick Paper Check

Runs a fast 2-agent pre-submission check for a psychology or neuroscience paper. It focuses on contribution, design credibility, causal overclaiming, and unsupported claims, and is designed for quick iteration before a full review.

**Installation:**

```bash
curl -o ~/.claude/commands/review-paper-light.md \
  https://raw.githubusercontent.com/ValentinGuigon/AI-research-feedback/main/Skills/review-paper-light.md
```

For a project-local install:

```bash
mkdir -p .claude/commands && curl -o .claude/commands/review-paper-light.md \
  https://raw.githubusercontent.com/ValentinGuigon/AI-research-feedback/main/Skills/review-paper-light.md
```

**Usage:**

```text
/review-paper-light
/review-paper-light path/to/paper
```

If no path is provided, the command auto-detects the main `.tex` file.

**Output:**

Saves a short prioritized report to `QUICK_REVIEW_[YYYY-MM-DD].md` in the current directory, automatically versioning the filename if one already exists.

**Requirements:**

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with access to the `general-purpose` subagent.
- A paper in `.tex`, `.md`, `.pdf`, or `.docx` format (same extraction dependencies as `review-paper`).

### `review-paper-code` — Paper-Code Reproducibility Review

Runs a paper-code review for empirical research projects. It discovers the main LaTeX paper and analysis code, checks reproducibility and code quality, maps the paper's main empirical claims to the code, and writes a constructive report highlighting strengths, gaps to verify, and concrete next steps.

**What it reviews:**

| Area | Focus |
|---|---|
| Paper discovery | Paper in `.tex`, `.md`, `.pdf`, or `.docx` format |
| Code discovery | Python, R, MATLAB, notebooks, shell scripts, and BIDS pipeline files |
| Reproducibility | Paths, seeds, outputs, dependencies, run order, documentation |
| Code quality | Structure, commented-out code, opaque transforms, major thresholds |
| Paper-code alignment | Tables, variables, contrasts/conditions, methods, BIDS stats model, computational model alignment |

**Usage:**

```text
/review-paper-code
/review-paper-code path/to/paper
/review-paper-code path/to/paper path/to/code_dir
/review-paper-code path/to/paper path/to/code_dir full
```

**Review depth:**

- `main`: default; focuses on main scripts and core outputs
- `full`: reviews all detected code files in scope

**Output:**

Writes a report to `code_review_report.md` in the current working directory.

**Requirements:**

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with access to the `general-purpose` subagent.
- A paper in any supported format plus Python, R, MATLAB, notebook, or BIDS pipeline code (same extraction dependencies as `review-paper`).

### `review-pap` — Pre-Analysis Plan Review

Runs a 6-agent pre-submission review of a pre-analysis plan (PAP). The command auto-detects the main PAP and supporting files, then evaluates writing quality, specification completeness, internal consistency, identification strategy, statistical analysis, implementation details, and registry or journal fit.

**Installation:**

```bash
curl -o ~/.claude/commands/review-pap.md \
  https://raw.githubusercontent.com/ValentinGuigon/AI-research-feedback/main/Skills/review-pap.md
```

For a project-local install:

```bash
mkdir -p .claude/commands && curl -o .claude/commands/review-pap.md \
  https://raw.githubusercontent.com/ValentinGuigon/AI-research-feedback/main/Skills/review-pap.md
```

**Usage:**

```text
/review-pap
/review-pap OSF
/review-pap PsychSci path/to/pap.docx
```

**Supported targets:**

- Trial registries: `OSF`, `AsPredicted`, `ClinicalTrials`, `ISRCTN`
- Journal standards: `PsychSci`, `JNeurosci`, `NatureNeuro`, `eLife`, `NatureHB`, `PNAS`, `NeuroImage`, `CommsPsych`, `PLoSCB`
- General standards: `top-journal`, `working-paper`

If no target is specified, the command defaults to `top-journal`. If no path is provided, it auto-detects the main PAP file.

**Supporting files it can inspect:**

- Power calculations and sample-size worksheets
- Survey instruments and questionnaires
- Randomization protocols and sampling frames
- Code skeletons and mock tables
- Data dictionaries and ethics materials

**Output:**

Saves a consolidated report to `PAP_REVIEW_[YYYY-MM-DD].md` in the current directory.

**Requirements:**

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with access to the `general-purpose` subagent.
- A PAP in `.md`, `.txt`, `.tex`, `.pdf`, or `.docx` format. `.pdf` and `.docx` inputs are extracted automatically (same dependencies as `review-paper`).

### `review-grant` — Grant Proposal Review

Runs a 6-agent pre-submission panel review of a grant proposal. The command auto-detects the main proposal and supporting documents, then evaluates clarity, compliance signals, internal consistency, significance, innovation, research design, feasibility, budget logic, team readiness, and fit to the target funder or program.

**Installation:**

```bash
curl -o ~/.claude/commands/review-grant.md \
  https://raw.githubusercontent.com/ValentinGuigon/AI-research-feedback/main/Skills/review-grant.md
```

For a project-local install:

```bash
mkdir -p .claude/commands && curl -o .claude/commands/review-grant.md \
  https://raw.githubusercontent.com/ValentinGuigon/AI-research-feedback/main/Skills/review-grant.md
```

**Usage:**

```text
/review-grant
/review-grant NSF
/review-grant NIH path/to/proposal.pdf
```

**Supported funders/programs:**

- US federal science and health: `NSF`, `NIH`, `ERC`, `HorizonEurope`
- General proposal standards: `major-funder`, `foundation`

If no target is specified, the command defaults to `major-funder`. If no path is provided, it auto-detects the main proposal file.

**Supporting files it can inspect:**

- Budgets and budget justifications
- Timelines and workplans
- Biosketches, CVs, and personnel documents
- Data-management plans, mentoring plans, and facilities statements
- Letters of support, appendices, and supplementary materials

**Output:**

Saves a consolidated report to `GRANT_PROPOSAL_REVIEW_[YYYY-MM-DD].md` in the current directory.

**Requirements:**

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with access to the `general-purpose` subagent.
- A proposal in `.md`, `.txt`, `.tex`, `.pdf`, or `.docx` format. `.pdf` and `.docx` inputs are extracted automatically (same dependencies as `review-paper`).

## License

MIT — free to use, adapt, and share.
