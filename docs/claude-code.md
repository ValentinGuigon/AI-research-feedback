# Claude Code

This repo can be used in Claude Code by installing selected files from `Skills/` into `.claude/commands/` or `~/.claude/commands/`.

## Install

Project-local install:

```powershell
New-Item -ItemType Directory -Force .claude\commands | Out-Null
Copy-Item Skills\review-paper.md .claude\commands\review-paper.md
Copy-Item Skills\review-pap.md .claude\commands\review-pap.md
Copy-Item Skills\fetch-grant-context.md .claude\commands\fetch-grant-context.md
Copy-Item Skills\review-grant.md .claude\commands\review-grant.md
```

## Usage

Examples:

```text
/review-paper
/review-paper PsychSci path/to/paper.docx
/review-pap OSF path/to/pap.docx
/fetch-grant-context https://example.org/call-page slug=my-call mode=foundation
/review-grant foundation profile=review/grants/my-call/profile.json path/to/proposal.pdf
```

## Available Commands

- `review-paper`
- `review-paper-light`
- `review-paper-code`
- `review-pap`
- `fetch-grant-context`
- `review-grant`
