# AI Research Feedback

Research-review workflows for papers, pre-analysis plans, and grant proposals.

This repo supports two surfaces:

- Claude Code commands authored from `Skills/*.md`
- a Codex plugin packaged under `plugins/ai-research-feedback/`

The canonical authored workflows live in `Skills/`. The Codex plugin bundles derived copies under `plugins/ai-research-feedback/skills/`.

## Quick Start

### Claude Code

Copy a workflow into `.claude/commands/`, then run it as a slash command.

Example:

```powershell
New-Item -ItemType Directory -Force .claude\commands | Out-Null
Copy-Item Skills\review-paper.md .claude\commands\review-paper.md
```

Then in Claude Code:

```text
/review-paper
```

### Codex

Install the repo-local plugin, then invoke a workflow in normal chat by naming the skill explicitly.

Example:

```text
Use the AI Research Feedback plugin skill `fetch-grant-context` on https://example.org/call-page with slug=my-call and mode=foundation.
```

```text
Use the AI Research Feedback plugin skill `review-paper` on ./paper/my-paper-to-review.pdf with journal=PNAS.
```

## Workflows

- `review-paper`: full referee-style paper review
- `review-paper-light`: quick paper check
- `review-paper-code`: paper-code reproducibility review
- `review-pap`: pre-analysis plan review
- `fetch-grant-context`: grant call intake and normalization
- `plan-grant-review`: reviewer-panel planning and confirmation before grant review
- `review-grant`: proposal review against a sponsor archetype and optional cached grant profile
- `plan-revisions`: shared post-review revision planning from saved review reports
- `load-writing-constraints`: shared writing-constraint extraction for revision passes
- `contextualize-revisions-grant`: grant-specific post-review contextualization from saved editing artifacts
- `draft-edits-grant`: grant-specific drafted edit instructions from a saved contextualized edit plan
- `contextualize-revisions-paper`: paper-specific post-review contextualization from saved editing artifacts
- `draft-edits-paper`: paper-specific drafted edit instructions from a saved contextualized edit plan

Planned next layer:

- post-review editing as a staged architecture, documented in `docs/post-review-editing.md`
- shared editing schemas under `templates/editing/`
- PAP or paper-code editing workflow specs

## Output Locations

Review reports save to deterministic locations:

- `review-paper` -> `review/papers/paper-review--<paper-slug>--YYYY-MM-DD.md`
- `review-paper-light` -> `review/papers/paper-light-review--<paper-slug>--YYYY-MM-DD.md`
- `review-paper-code` -> `review/code/paper-code-review--<subject-slug>--YYYY-MM-DD.md`
- `review-pap` -> `review/paps/pap-review--<pap-slug>--YYYY-MM-DD.md`
- `plan-grant-review` with profile -> next to the profile as `review-plan.json`
- `review-grant` with profile -> next to the profile as `grant-review--<proposal-slug>--YYYY-MM-DD.md`
- `review-grant` without profile -> `review/grant-review--<proposal-slug>--YYYY-MM-DD.md`

If a filename already exists, the workflow appends `-v2`, `-v3`, and so on.

Planned post-review editing artifacts save under deterministic per-source folders:

- `revision-plan` -> `review/editing/<object-folder>/<source-slug>/revision-plan.json`
- `writing-constraints` -> `review/editing/<object-folder>/<source-slug>/writing-constraints.json`
- `contextualized-edit-plan` -> `review/editing/<object-folder>/<source-slug>/contextualized-edit-plan.json`
- `drafted-edit-instructions` -> `review/editing/<object-folder>/<source-slug>/drafted-edit-instructions.json`

Current object folders are:

- `grants`
- `papers`
- `paps`
- `paper-code`

Shared post-review editing stages now specified:

- `plan-revisions` -> `review/editing/<object-folder>/<source-slug>/revision-plan.json`
- `load-writing-constraints` -> `review/editing/<object-folder>/<source-slug>/writing-constraints.json`
- `contextualize-revisions-grant` -> `review/editing/grants/<source-slug>/contextualized-edit-plan.json`
- `draft-edits-grant` -> `review/editing/grants/<source-slug>/drafted-edit-instructions.json`
- `contextualize-revisions-paper` -> `review/editing/papers/<source-slug>/contextualized-edit-plan.json`
- `draft-edits-paper` -> `review/editing/papers/<source-slug>/drafted-edit-instructions.json`

Representative runtime validation artifacts now exist for the Google.org grant fixture under:

- `review/editing/grants/google-impact-challenge-ai-for-science-application-1/`

Representative paper contextualization validation artifacts now exist for the Communications Psychology paper fixture under:

- `review/editing/papers/s44271-024-00170-w/`

Representative paper drafting validation artifacts now exist for the same fixture under:

- `review/editing/papers/s44271-024-00170-w/`

## Grant Review In One Glance

Grant review is a 3-step flow:

1. Fetch the grant call into `review/grants/<slug>/profile.json`
2. Plan the review panel in `review/grants/<slug>/review-plan.json`
3. Review the proposal using that saved profile and review plan

When you use `review-grant` with a profile, the review report is saved next to that profile using:

- `grant-review--<proposal-slug>--YYYY-MM-DD.md`

Claude Code example:

```text
/fetch-grant-context "Google.org Impact Challenge AI for Science" slug=google-impact-challenge-ai-for-science mode=foundation
/plan-grant-review foundation profile=review/grants/google-impact-challenge-ai-for-science/profile.json ./tests/fixtures/google_org/Google Impact Challenge_ AI for Science application.pdf
/review-grant foundation profile=review/grants/google-impact-challenge-ai-for-science/profile.json plan=review/grants/google-impact-challenge-ai-for-science/review-plan.json ./tests/fixtures/google_org/Google Impact Challenge_ AI for Science application.pdf
```

Codex example:

```text
Use the AI Research Feedback plugin skill `fetch-grant-context` on "Google.org Impact Challenge AI for Science" with slug=google-impact-challenge-ai-for-science and mode=foundation.
Use the AI Research Feedback plugin skill `plan-grant-review` on ./tests/fixtures/google_org/Google Impact Challenge_ AI for Science application.pdf with mode=foundation and context from review/grants/google-impact-challenge-ai-for-science/profile.json.
Use the AI Research Feedback plugin skill `review-grant` on ./tests/fixtures/google_org/Google Impact Challenge_ AI for Science application.pdf with mode=foundation, context from review/grants/google-impact-challenge-ai-for-science/profile.json, and plan from review/grants/google-impact-challenge-ai-for-science/review-plan.json.
```

## Repo Structure

- `Skills/`: canonical workflow definitions
- `plugins/ai-research-feedback/`: Codex plugin package
- `.agents/plugins/marketplace.json`: repo-local Codex marketplace entry
- `scripts/derive_codex_plugin_skills.py`: syncs canonical workflows into the plugin bundle
- `review/grants/`: run-specific grant profiles and review plans
- `templates/grants/`: reusable grant schemas and expert-registry templates
- `templates/editing/`: shared post-review editing artifact schemas

## Docs

- [docs/claude-code.md](docs/claude-code.md)
- [docs/codex.md](docs/codex.md)
- [docs/paper-review.md](docs/paper-review.md)
- [docs/pap-review.md](docs/pap-review.md)
- [docs/grant-review.md](docs/grant-review.md)
- [docs/grant-review-planning.md](docs/grant-review-planning.md)
- [docs/post-review-editing.md](docs/post-review-editing.md)
