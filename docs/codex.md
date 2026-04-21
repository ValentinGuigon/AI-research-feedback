# Codex

This repo ships a Codex plugin package under `plugins/ai-research-feedback/`.

Reusable grant-review templates live under `templates/grants/`. Run-specific grant artifacts live under `artifacts/grants/`.

For repo-local use, Codex reads:

- `.agents/plugins/marketplace.json`
- `plugins/ai-research-feedback/.codex-plugin/plugin.json`

## Install

1. Open this repository in Codex.
2. Make sure the plugin `ai-research-feedback` is enabled for the repo.
3. Start a normal Codex chat.

## Invocation Pattern

Codex does not currently expose these workflows as top-level slash commands. Use normal prompts and name the skill explicitly.

Examples:

```text
Use the AI Research Feedback plugin skill `review-paper` on path/to/paper.docx.
```

```text
Use the AI Research Feedback plugin skill `fetch-grant-context` on https://example.org/call-page with slug=my-call and mode=foundation.
```

```text
Use the AI Research Feedback plugin skill `plan-grant-review` on path/to/proposal.pdf with mode=foundation and context from artifacts/grants/my-call/profile.json.
```

```text
Use the AI Research Feedback plugin skill `review-grant` with foundation profile=artifacts/grants/my-call/profile.json "path/to/proposal.pdf".
```

```text
Use the AI Research Feedback plugin skill `plan-revisions` with type=grant source=path/to/proposal.pdf review=artifacts/grants/my-call/grant-review--proposal--2026-04-20.md.
```

```text
Use the AI Research Feedback plugin skill `plan-feedback-revisions` with type=grant source=path/to/proposal.docx source_type=docx-comment mode=single feedback_id=1.
```

```text
Use the AI Research Feedback plugin skill `convert-feedback-plan-to-revision-plan` with feedback_plan=artifacts/grants/proposal/editing/normalized-feedback-plan.json.
```

```text
Use the AI Research Feedback plugin skill `load-writing-constraints` with type=grant source=path/to/proposal.pdf profile=artifacts/grants/my-call/profile.json.
```

```text
Use the AI Research Feedback plugin skill `contextualize-revisions-grant` with source=path/to/proposal.pdf revision_plan=artifacts/grants/proposal/editing/revision-plan.json writing_constraints=artifacts/grants/proposal/editing/writing-constraints.json.
```

```text
Use the AI Research Feedback plugin skill `draft-edits-grant` with contextualized_plan=artifacts/grants/proposal/editing/contextualized-edit-plan.json.
```

```text
Use the AI Research Feedback plugin skill `contextualize-revisions-paper` with source=path/to/paper.pdf revision_plan=artifacts/papers/paper/editing/revision-plan.json writing_constraints=artifacts/papers/paper/editing/writing-constraints.json.
```

```text
Use the AI Research Feedback plugin skill `draft-edits-paper` with contextualized_plan=artifacts/papers/paper/editing/contextualized-edit-plan.json.
```

If Codex seems to ignore the plugin, make the prompt more explicit:

```text
Use the installed AI Research Feedback plugin. Run the `plan-grant-review` skill with foundation profile=artifacts/grants/my-call/profile.json "path/to/proposal.pdf", then run the `review-grant` skill with foundation profile=artifacts/grants/my-call/profile.json plan=artifacts/grants/my-call/review-plan.json "path/to/proposal.pdf".
```

## Available Skills

- `fetch-grant-context`
- `plan-grant-review`
- `review-paper`
- `review-paper-light`
- `review-paper-code`
- `review-pap`
- `review-grant`
- `plan-feedback-revisions`
- `convert-feedback-plan-to-revision-plan`
- `plan-revisions`
- `load-writing-constraints`
- `contextualize-revisions-grant`
- `contextualize-revisions-paper`
- `draft-edits-grant`
- `draft-edits-paper`
