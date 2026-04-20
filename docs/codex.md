# Codex

This repo ships a Codex plugin package under `plugins/ai-research-feedback/`.

Reusable grant-review templates live under `templates/grants/`. Run-specific grant artifacts live under `review/grants/`.

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
Use the AI Research Feedback plugin skill `plan-grant-review` on path/to/proposal.pdf with mode=foundation and context from review/grants/my-call/profile.json.
```

```text
Use the AI Research Feedback plugin skill `review-grant` with foundation profile=review/grants/my-call/profile.json "path/to/proposal.pdf".
```

If Codex seems to ignore the plugin, make the prompt more explicit:

```text
Use the installed AI Research Feedback plugin. Run the `plan-grant-review` skill with foundation profile=review/grants/my-call/profile.json "path/to/proposal.pdf", then run the `review-grant` skill with foundation profile=review/grants/my-call/profile.json plan=review/grants/my-call/review-plan.json "path/to/proposal.pdf".
```
