---
name: review-paper
description: Run a 6-agent pre-submission referee report for an academic paper targeting a specified journal.
---

Run a rigorous pre-submission referee review of an academic paper in psychology
or neuroscience.

`Skills/review-paper.md` is the workflow source of truth for this skill.
Before taking any action, read that file in full and follow its discovery,
extraction, agent, consolidation, output, and cleanup behavior.

## Codex-specific execution

Treat the user request as the invocation and pass through any provided paper
path and target journal arguments to the source workflow.

When the source workflow calls for 6 review roles:

- If Codex subagents are available and delegation fits the task, run the six
  review roles in parallel using Codex subagents.
- If subagents are not available, complete all six review roles yourself and
  keep the role outputs separate in the final report before consolidation.

Do not rewrite or restate the full workflow here. The file at
`Skills/review-paper.md` remains authoritative.
