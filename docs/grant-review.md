# Grant Review

## Start Here

Grant review is a 3-step process:

1. Fetch the grant call context and save it as a local profile.
2. Plan the grant-specific review panel and save it as a local review plan.
3. Review your proposal against that saved profile and review plan.

If you skip step 1, `review-grant` falls back to a generic sponsor archetype such as `foundation` or `NSF`.

If you skip step 2, `review-grant` should fall back to a default standing panel and record that no tailored review plan was used.

## Fastest Copy-Paste Pattern

### Claude Code

```text
/fetch-grant-context https://example.org/call-page slug=my-call mode=foundation
/plan-grant-review foundation profile=review/grants/my-call/profile.json path/to/proposal.pdf
/review-grant foundation profile=review/grants/my-call/profile.json plan=review/grants/my-call/review-plan.json path/to/proposal.pdf
```

### Codex

```text
Use the AI Research Feedback plugin skill `fetch-grant-context` on https://example.org/call-page with slug=my-call and mode=foundation.
Use the AI Research Feedback plugin skill `plan-grant-review` on path/to/proposal.pdf with mode=foundation and context from review/grants/my-call/profile.json.
Use the AI Research Feedback plugin skill `review-grant` on path/to/proposal.pdf with mode=foundation, context from review/grants/my-call/profile.json, and plan from review/grants/my-call/review-plan.json.
```

## Google.org Example

If your proposal file is:

- `./tests/fixtures/google_org/Google Impact Challenge_ AI for Science application.pdf`

then the intended pattern is:

### Claude Code

```text
/fetch-grant-context "Google.org Impact Challenge AI for Science" slug=google-impact-challenge-ai-for-science mode=foundation
/plan-grant-review foundation profile=review/grants/google-impact-challenge-ai-for-science/profile.json ./tests/fixtures/google_org/Google Impact Challenge_ AI for Science application.pdf
/review-grant foundation profile=review/grants/google-impact-challenge-ai-for-science/profile.json plan=review/grants/google-impact-challenge-ai-for-science/review-plan.json ./tests/fixtures/google_org/Google Impact Challenge_ AI for Science application.pdf
```

### Codex

```text
Use the AI Research Feedback plugin skill `fetch-grant-context` on "Google.org Impact Challenge AI for Science" with slug=google-impact-challenge-ai-for-science and mode=foundation.
Use the AI Research Feedback plugin skill `plan-grant-review` on ./tests/fixtures/google_org/Google Impact Challenge_ AI for Science application.pdf with mode=foundation and context from review/grants/google-impact-challenge-ai-for-science/profile.json.
Use the AI Research Feedback plugin skill `review-grant` on ./tests/fixtures/google_org/Google Impact Challenge_ AI for Science application.pdf with mode=foundation, context from review/grants/google-impact-challenge-ai-for-science/profile.json, and plan from review/grants/google-impact-challenge-ai-for-science/review-plan.json.
```

## What Each Step Produces

`fetch-grant-context` writes:

- `review/grants/<slug>/profile.json`
- `review/grants/<slug>/sources.md`

Framework templates live under:

- `templates/grants/`

`plan-grant-review` writes:

- `review/grants/<slug>/review-plan.json`

`review-grant` reads:

- your proposal file
- optional supporting documents it discovers automatically
- the cached `profile.json` from step 1
- optional `review-plan.json` from step 2

`review-grant` writes:

- if a profile is provided: the report is saved next to that `profile.json`
- otherwise: the report is saved under `review/`
- filename pattern: `grant-review--<proposal-slug>--YYYY-MM-DD.md`

## Workflows

### `fetch-grant-context`

Fetches and normalizes one funding call into a reusable local profile.

Examples:

```text
/fetch-grant-context https://example.org/call-page
/fetch-grant-context "Google.org Generative AI Accelerator" slug=google-genai-accelerator
/fetch-grant-context path/to/guidelines.pdf mode=foundation
```

Accepted grant identifiers:

- URL
- local PDF path
- local folder path
- free-text grant/program name

Optional arguments:

- `slug=<slug>`
- `out=<path>`
- `mode=NSF|NIH|ERC|HorizonEurope|major-funder|foundation`

Output:

- `review/grants/<slug>/profile.json`
- `review/grants/<slug>/sources.md`

### `plan-grant-review`

Builds a proposal-specific review panel from the cached grant profile and the expert registry.

Examples:

```text
/plan-grant-review
/plan-grant-review foundation
/plan-grant-review profile=review/grants/my-call/profile.json path/to/proposal.pdf
/plan-grant-review foundation profile=review/grants/my-call/profile.json mode=standard path/to/proposal.pdf
```

Accepted arguments:

- sponsor archetype: `NSF|NIH|ERC|HorizonEurope|major-funder|foundation`
- `profile=<path>`
- `grant-profile=<path>`
- `mode=standard|fast|high-stakes`
- optional proposal path

Output:

- if a profile is provided: `<profile-dir>/review-plan.json`
- otherwise: `review/review-plan--<proposal-slug>--YYYY-MM-DD.json`

### `review-grant`

Runs a proposal review using a sponsor archetype, optional cached grant profile, and optional cached review plan.

Examples:

```text
/review-grant
/review-grant NSF
/review-grant profile=review/grants/my-call/profile.json path/to/proposal.pdf
/review-grant foundation profile=review/grants/my-call/profile.json plan=review/grants/my-call/review-plan.json path/to/proposal.pdf
/review-grant NIH path/to/proposal.pdf
```

Supported sponsor archetypes:

- `NSF`
- `NIH`
- `ERC`
- `HorizonEurope`
- `major-funder`
- `foundation`

Optional plan arguments:

- `plan=<path>`
- `review-plan=<path>`

Supporting files it can inspect:

- budgets
- budget justifications
- timelines
- workplans
- biosketches
- CVs
- personnel documents
- data-management plans
- mentoring plans
- facilities statements
- letters of support
- appendices
- supplementary materials

Output:

- if a profile is provided: `<profile-dir>/grant-review--<proposal-slug>--YYYY-MM-DD.md`
- otherwise: `review/grant-review--<proposal-slug>--YYYY-MM-DD.md`

## Rule of Thumb

Use this pattern:

- first: fetch the grant
- second: plan the review panel
- third: review the proposal with the saved profile and plan

Template:

```text
fetch-grant-context -> review/grants/<slug>/profile.json -> plan-grant-review -> review/grants/<slug>/review-plan.json -> review-grant
```
