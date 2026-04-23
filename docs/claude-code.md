# Claude Code

This repo can be used in Claude Code by installing selected files from `Skills/` into `.claude/commands/` or `~/.claude/commands/`.

The guided review command `run-review` is canonical in `Skills/run-review.md`, and the guided editing command `run-editing` is canonical in `Skills/run-editing.md`. Both are exposed through the Codex plugin, but Claude Code still uses local command files, so install them manually if you want slash commands. You can also install and invoke the explicit stage commands below when the exact route is already clear.

## Install

Project-local install:

```powershell
New-Item -ItemType Directory -Force .claude\commands | Out-Null
Copy-Item Skills\review-paper.md .claude\commands\review-paper.md
Copy-Item Skills\review-paper-light.md .claude\commands\review-paper-light.md
Copy-Item Skills\review-paper-code.md .claude\commands\review-paper-code.md
Copy-Item Skills\run-review.md .claude\commands\run-review.md
Copy-Item Skills\run-editing.md .claude\commands\run-editing.md
Copy-Item Skills\review-pap.md .claude\commands\review-pap.md
Copy-Item Skills\fetch-grant-context.md .claude\commands\fetch-grant-context.md
Copy-Item Skills\plan-grant-review.md .claude\commands\plan-grant-review.md
Copy-Item Skills\review-grant.md .claude\commands\review-grant.md
Copy-Item Skills\plan-feedback-revisions.md .claude\commands\plan-feedback-revisions.md
Copy-Item Skills\convert-feedback-plan-to-revision-plan.md .claude\commands\convert-feedback-plan-to-revision-plan.md
Copy-Item Skills\plan-revisions.md .claude\commands\plan-revisions.md
Copy-Item Skills\load-writing-constraints.md .claude\commands\load-writing-constraints.md
Copy-Item Skills\contextualize-revisions-grant.md .claude\commands\contextualize-revisions-grant.md
Copy-Item Skills\draft-edits-grant.md .claude\commands\draft-edits-grant.md
Copy-Item Skills\contextualize-revisions-paper.md .claude\commands\contextualize-revisions-paper.md
Copy-Item Skills\draft-edits-paper.md .claude\commands\draft-edits-paper.md
Copy-Item Skills\review-drafted-edits.md .claude\commands\review-drafted-edits.md
```

## Usage

Examples:

```text
/run-review path/to/document.pdf
/run-editing artifacts/grants/my-proposal/editing/
/review-paper
/review-paper PsychSci path/to/paper.docx
/review-pap OSF path/to/pap.docx
/fetch-grant-context https://example.org/call-page slug=my-call mode=foundation
/plan-grant-review foundation profile=artifacts/grants/my-call/profile.json path/to/proposal.pdf
/review-grant foundation profile=artifacts/grants/my-call/profile.json path/to/proposal.pdf
/plan-feedback-revisions type=grant source=path/to/proposal.docx source_type=docx-comment mode=single feedback_id=1
/convert-feedback-plan-to-revision-plan feedback_plan=artifacts/grants/proposal/editing/normalized-feedback-plan.json
/plan-revisions type=grant source=path/to/proposal.pdf review=artifacts/grants/my-call/grant-review--proposal--2026-04-20.md
/load-writing-constraints type=grant source=path/to/proposal.pdf profile=artifacts/grants/my-call/profile.json
/contextualize-revisions-grant source=path/to/proposal.pdf revision_plan=artifacts/grants/proposal/editing/revision-plan.json writing_constraints=artifacts/grants/proposal/editing/writing-constraints.json
/draft-edits-grant contextualized_plan=artifacts/grants/proposal/editing/contextualized-edit-plan.json
/contextualize-revisions-paper source=path/to/paper.pdf revision_plan=artifacts/papers/paper/editing/revision-plan.json writing_constraints=artifacts/papers/paper/editing/writing-constraints.json
/draft-edits-paper contextualized_plan=artifacts/papers/paper/editing/contextualized-edit-plan.json
/review-drafted-edits drafted_instructions=artifacts/papers/paper/editing/drafted-edit-instructions.json
```

`review-drafted-edits` supports validated grant and paper drafted edit instructions only. It preserves the no-source-rewrite and no-tracked-changes boundaries and must stop for PAP or paper-code loop artifacts until those paths are separately implemented and validated.

## Available Commands

- `review-paper`
- `run-review`
- `run-editing`
- `review-paper-light`
- `review-paper-code`
- `review-pap`
- `fetch-grant-context`
- `plan-grant-review`
- `review-grant`
- `plan-feedback-revisions`
- `convert-feedback-plan-to-revision-plan`
- `plan-revisions`
- `load-writing-constraints`
- `contextualize-revisions-grant`
- `draft-edits-grant`
- `contextualize-revisions-paper`
- `draft-edits-paper`
- `review-drafted-edits`
