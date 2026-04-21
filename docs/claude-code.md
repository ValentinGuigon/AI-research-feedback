# Claude Code

This repo can be used in Claude Code by installing selected files from `Skills/` into `.claude/commands/` or `~/.claude/commands/`.

## Install

Project-local install:

```powershell
New-Item -ItemType Directory -Force .claude\commands | Out-Null
Copy-Item Skills\review-paper.md .claude\commands\review-paper.md
Copy-Item Skills\review-pap.md .claude\commands\review-pap.md
Copy-Item Skills\fetch-grant-context.md .claude\commands\fetch-grant-context.md
Copy-Item Skills\plan-grant-review.md .claude\commands\plan-grant-review.md
Copy-Item Skills\review-grant.md .claude\commands\review-grant.md
Copy-Item Skills\plan-revisions.md .claude\commands\plan-revisions.md
Copy-Item Skills\load-writing-constraints.md .claude\commands\load-writing-constraints.md
Copy-Item Skills\contextualize-revisions-grant.md .claude\commands\contextualize-revisions-grant.md
Copy-Item Skills\draft-edits-grant.md .claude\commands\draft-edits-grant.md
```

## Usage

Examples:

```text
/review-paper
/review-paper PsychSci path/to/paper.docx
/review-pap OSF path/to/pap.docx
/fetch-grant-context https://example.org/call-page slug=my-call mode=foundation
/plan-grant-review foundation profile=review/grants/my-call/profile.json path/to/proposal.pdf
/review-grant foundation profile=review/grants/my-call/profile.json path/to/proposal.pdf
/plan-revisions type=grant source=path/to/proposal.pdf review=review/grants/my-call/grant-review--proposal--2026-04-20.md
/load-writing-constraints type=grant source=path/to/proposal.pdf profile=review/grants/my-call/profile.json
/contextualize-revisions-grant source=path/to/proposal.pdf revision_plan=review/editing/grants/proposal/revision-plan.json writing_constraints=review/editing/grants/proposal/writing-constraints.json
/draft-edits-grant contextualized_plan=review/editing/grants/proposal/contextualized-edit-plan.json
```

## Available Commands

- `review-paper`
- `review-paper-light`
- `review-paper-code`
- `review-pap`
- `fetch-grant-context`
- `plan-grant-review`
- `review-grant`
- `plan-revisions`
- `load-writing-constraints`
- `contextualize-revisions-grant`
- `draft-edits-grant`
