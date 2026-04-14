---
name: review-paper-light
description: Run a fast pre-submission check for a psychology or neuroscience paper focused on contribution, design credibility, and causal overclaiming. Use when Codex needs a quick paper review from a provided manuscript path or from the current repository contents.
---

Run a fast pre-submission check of an academic paper in psychology or neuroscience.

`Skills/review-paper-light.md` is the workflow source of truth for this skill.
Before taking any action, read that file in full and follow its workflow,
review rubric, report structure, and output expectations.

## Codex-specific execution

Treat the user request as the invocation and pass any provided paper path
through to the source workflow.

When the source workflow calls for 2 reviewer/agent passes:

- If Codex subagents are available and delegation fits the task, run the two
  reviewer passes in parallel using Codex subagents.
- If subagents are not available, complete both reviewer passes yourself and
  keep the reviewer roles separate in the final report.

Do not rewrite or restate the full workflow here. The file at
`Skills/review-paper-light.md` remains authoritative.
