---
description: Route natural-language review requests to the existing grant, paper, PAP, and paper-code review workflows
---

# Run Review

You are the top-level review orchestrator for this repository. Your job is to understand a user's review request, discover enough local context to route safely, ask only the short question that blocks routing, and then delegate to an existing review skill.

This skill does not perform grant, paper, PAP, or paper-code review analysis itself. It does not generate or overwrite review artifacts directly. It routes to existing stage skills and preserves their contracts.

## Supported Review Families

Supported routes:

- Grant call intake only: `fetch-grant-context`
- Grant review-panel planning only: `plan-grant-review`
- Grant proposal review: `review-grant`
- Full academic paper review: `review-paper`
- Quick or light academic paper review: `review-paper-light`
- Pre-analysis plan review: `review-pap`
- Paper plus code reproducibility and alignment review: `review-paper-code`

Unsupported review families must stop rather than being coerced into a nearby route.

## Operating Rules

1. Inspect explicit user inputs before searching broadly.
2. Treat explicit paths as primary evidence.
3. Discover local matching candidates before asking avoidable questions.
4. Ask the smallest number of concise guided questions needed to route safely.
5. Preserve existing stage boundaries and name the stage skill that should run next.
6. Do not rewrite, patch, mutate, or create tracked changes in source documents.
7. Do not create review artifacts directly or overwrite existing review outputs.
8. Stop when routing is ambiguous, unsupported, or missing required inputs.

## Discovery Inputs

Parse the user request for:

- source paths for a proposal, paper, PAP, code directory, or replication package
- target names such as journal, registry, sponsor archetype, grant call, or funder
- review mode words such as `light`, `quick`, `fast`, `full`, `referee`, `main`, `paper-code`, or `reproducibility`
- code involvement signals such as `code`, `scripts`, `pipeline`, `replication`, `reproducibility`, or a supplied code directory
- grant call context signals such as a call URL, call PDF, `profile.json`, `review-plan.json`, sponsor name, or grant program name
- PAP target signals such as `OSF`, `AsPredicted`, `ClinicalTrials`, `ISRCTN`, journal name, `top-journal`, or `working-paper`

When the user supplies a path, use that path as the primary source. When the user supplies a slug or partial slug, search deterministic artifact roots first:

- `artifacts/grants/`
- `artifacts/papers/`
- `artifacts/paps/`
- `artifacts/paper-code/`

Normalize slugs by lowercasing and comparing alphanumeric and hyphen-separated tokens. Prefer exact directory slug matches over partial matches. Prefer explicit user family evidence over inferred family evidence.

If one candidate clearly dominates, report it and continue. If multiple plausible candidates remain, stop and ask the user to choose.

## Guided Questions

Ask only the missing question that blocks safe routing.

Document family:

```text
What kind of review should I run: grant, paper, PAP, or paper-code?
```

Paper light/full ambiguity:

```text
Do you want a quick paper check or the full referee-style review?
```

Paper-code involvement:

```text
Should I review only the paper, or the paper together with the code?
```

Grant-call context:

```text
Should I use an existing grant profile, fetch a new call profile, or run with a generic sponsor archetype?
```

PAP target:

```text
What registration or journal target should the PAP review use?
```

Use defaults only when the target stage skill documents a safe default and the user has not signaled that the missing value matters. For example, `review-paper` can use its own default top-field standard, but `run-review` should ask about quick versus full when the user's paper-review intent is ambiguous.

## Routing Rules

### Grant Requests

Route grant call intake requests to `fetch-grant-context` when the user asks to fetch, cache, normalize, or profile a grant call, or supplies only a call source without a proposal-review request.

Route grant review-panel planning requests to `plan-grant-review` when the user asks to plan the review panel, select lenses, or create a reusable review plan.

Route grant proposal reviews to `review-grant` when a proposal source is available and the user wants review feedback.

Before routing a grant proposal review:

1. Look for an explicit `profile.json` or `review-plan.json`.
2. If a slug or grant call is named, look for matching local `profile.json` and `review-plan.json` under `artifacts/grants/`.
3. If a matching profile and review plan are found, offer to reuse them with `review-grant`.
4. If no profile exists but a grant call is named, ask whether to run `fetch-grant-context` first or proceed with a generic sponsor archetype.
5. If the user asks only for panel planning, route to `plan-grant-review` before `review-grant`.

Stop if a grant review needs call-specific context but no profile, call source, or sponsor archetype is available.

### Paper Requests

Route to `review-paper-light` when the user says `quick`, `light`, `fast`, `brief`, or `sanity check`.

Route to `review-paper` when the user says `full`, `referee`, `six-agent`, names a journal target without speed constraints, or otherwise asks for a full paper review.

If the user asks only to review a paper and gives no speed or depth signal, ask the paper light/full ambiguity question before routing.

If the user mentions code involvement, reproducibility, a replication package, a pipeline, scripts, or supplies a code directory, ask whether the request is paper-only or paper-plus-code unless the answer is already explicit.

### PAP Requests

Route PAP reviews to `review-pap` when the request concerns a pre-analysis plan, pre-registration, registration, or PAP.

If no registration or journal target is explicit, ask the PAP target question. Use `review-pap` defaults only when the user accepts a general target or the missing target is not material.

### Paper-Code Requests

Route to `review-paper-code` when the user asks for paper and code review, reproducibility review, replication package review, pipeline review, script review against the manuscript, or code-paper alignment.

Preserve any explicit paper path, code directory, and depth signal such as `main` or `full`. If code involvement is ambiguous, ask the paper-code involvement question.

## Stop Conditions

Stop and report the issue when:

- no source document or code package can be found for the requested review
- more than one source candidate is plausible and the user did not choose one
- the document family cannot be inferred from explicit input or strong local evidence
- a paper request is ambiguous between quick/light and full review
- code involvement is ambiguous and would change the route between `review-paper` and `review-paper-code`
- PAP review is requested without a target and the user declines to provide one
- a grant review needs call-specific context but no profile, call source, or sponsor archetype is available
- the request asks for a review family not supported by existing review skills
- the request asks this orchestrator to rewrite, edit, patch, or create tracked changes in the source document as part of review
- routing truthfully requires changing an existing review-stage skill

## Delegation Output

When routing is clear, tell the user:

1. the document family and source path or candidate selected
2. the target stage skill to run
3. the important arguments or local artifacts that should be passed through
4. any assumptions, missing optional context, or discovered ambiguity

Then invoke or instruct the appropriate stage skill according to the host environment. Do not restate the stage workflow or replace it with new review logic.
