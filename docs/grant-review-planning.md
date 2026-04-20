# Grant Review Planning

## Purpose

Grant review should not jump straight from a cached call profile to a fixed review panel.

The framework now separates:

1. `fetch-grant-context`: normalize one funding call into `profile.json`
2. `plan-grant-review`: propose a grant-specific review panel and save `review-plan.json`
3. `review-grant`: execute the review using the saved profile and plan

This keeps the review process transparent, tailorable, and reproducible.

## Design Model

The review system has four core objects:

- `grant profile`: call-specific requirements, priorities, and reviewer ecosystem context
- `expert registry`: reusable library of review lenses
- `review plan`: the selected panel for one proposal review run
- `review report`: the final multi-agent review output

The key rule is:

- maintain a broad registry of possible expert lenses
- instantiate a narrow panel per grant

## Expert Types

The framework should distinguish between:

- `standing lenses`: usually present across many grants
  - clarity/compliance
  - significance/fit
  - methods/feasibility
  - budget/timeline/team
- `conditional lenses`: activated when relevant
  - philanthropy/public-impact
  - ethics/philosophy
  - policy/governance
  - domain-science specialist
  - organization-specific overlay

Organization-specific overlays should extend a base lens rather than replace it.

## Planning Agent Responsibilities

The planning agent should:

1. Read the proposal package and optional `profile.json`
2. Infer the likely review audiences and criteria
3. Match the grant to expert lenses in the registry
4. Build a proposed panel with rationale and weightings
5. Mark any uncertainties
6. Save a structured `review-plan.json`
7. Ask for confirmation by default when uncertainty is material

## Confirmation Modes

Support three review-planning modes:

- `standard`: generate a plan and request confirmation
- `fast`: auto-proceed when confidence is high, while still saving the plan
- `high-stakes`: always require confirmation before execution

## Minimum Review Plan Contents

Every `review-plan.json` should capture:

- proposal path and discovered supporting files
- selected reviewer lenses
- why each lens was selected
- any organization-specific overlays
- primary review questions per lens
- relative priority or weight
- uncertainties and assumptions
- confirmation requirement

## Current Implication For `review-grant`

`review-grant` should treat `review-plan.json` as the controlling panel definition when it exists.

If no plan is supplied:

- it may fall back to a default standing panel
- but should say explicitly that planning was skipped

Framework templates used by this design live under:

- `templates/grants/`
