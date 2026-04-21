---
description: Draft grant-specific post-review edit instructions from a saved contextualized edit plan
---

You are coordinating the grant-specific drafting stage of the post-review editing pipeline.

Your job is to turn one saved `contextualized-edit-plan.json` into deterministic `drafted-edit-instructions.json` that a human can apply to a grant application.

## Goal

Produce a bounded grant drafting artifact that functions as an exact replacement manual:

- consumes a saved contextualized edit plan rather than re-reading review state ad hoc
- turns each contextualized target into field-level, copy/paste-ready grant-edit instructions
- preserves location, constraint, and review-evidence provenance
- records whether each review suggestion is accepted, partially accepted, rejected, or left for factual verification
- gives exact "replace this with that" text whenever the source evidence and constraints support a text edit
- reports word-count or length-limit checks for every proposed replacement when limits are known
- does not rewrite the source document directly

This skill is grant-specific. It does not implement paper, PAP, or paper-code drafting.

## Runtime Rules

- Work from local repository files only.
- Produce exactly one drafted edit instructions artifact for one grant source document per run.
- Require a saved `contextualized-edit-plan.json` input.
- Treat the contextualized plan as the controlling source for targets, locations, constraints, and review evidence.
- Read enough source text to identify the exact field, paragraph, or answer block being changed.
- Use grant-facing wording that is suitable for sponsor, feasibility, budget, public-benefit, and responsible-AI sections.
- Do not add unsupported partners, results, methods, budgets, timelines, beneficiaries, or outcome metrics.
- Do not output only a parallel revised draft. The output must tell the human editor exactly where to apply each change.
- Do not edit the source PDF, DOCX, Markdown, or application file directly.

## Phase 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- Required or inferable contextualized-plan argument:
  - `contextualized_plan=<path>`
  - `plan=<path>`
- Optional source argument:
  - `source=<path>`
- Remaining unresolved path-like token may be treated as the contextualized plan path when `contextualized_plan=` is absent.

Resolution rules:

1. Resolve all supplied paths to absolute local paths.
2. If `contextualized_plan=` is absent, search the resolved source's deterministic grant editing directory for `contextualized-edit-plan.json`.
3. If `source=` is absent, use `source_document_path` from the contextualized plan.
4. Stop if the contextualized plan or source document cannot be resolved.

Store:

- `CONTEXTUALIZED_EDIT_PLAN_PATH`
- `SOURCE_DOCUMENT_PATH`

## Phase 2: Validate Inputs And Contract

1. Confirm that `CONTEXTUALIZED_EDIT_PLAN_PATH` and `SOURCE_DOCUMENT_PATH` exist locally.
2. Parse the contextualized edit plan as JSON.
3. Confirm `document_type = grant`.
4. Confirm `revision_targets` is non-empty.
5. Confirm every target has a non-empty `location.section`, `suggestion`, `motivation`, `constraint_checks`, and `source_evidence`.
6. Confirm the plan points back to saved `revision-plan.json` and `writing-constraints.json` artifacts when those fields exist.

Stop rather than drafting from incompatible or incomplete artifacts.

## Phase 3: Build Grant Drafting Model

For each contextualized target, make an editorial judgment before drafting:

- `accept`: the review suggestion is warranted and should be implemented
- `partial`: the review concern is valid, but the edit should be narrower than the review suggested
- `reject`: the suggestion would weaken accuracy, violate constraints, or overfit a reviewer preference
- `verify`: the suggestion may be warranted, but factual or administrative information is missing

Then identify the smallest credible drafting action:

- `insert`: add missing sponsor-facing material
- `replace`: substitute a better local framing for existing wording
- `delete`: remove duplicate or conflicting text
- `compress`: reduce overload or scope inflation
- `reconcile`: align multiple fields without adding new claims
- `verify`: mark a final human check where source-local structure cannot be safely rewritten

Use grant-specific drafting patterns:

- public-benefit pathway before long-run clinical aspiration
- one final answer per application prompt
- feasibility and budget wording aligned to milestones and staff roles
- explicit minimum viable success path for ambitious methods
- responsible-AI claims framed as research-grade tools with limitations

Reject or narrow suggestions when they would:

- invent new budget amounts, partner commitments, recruitment capacity, evaluation results, or adoption metrics
- exceed a field limit or force removal of higher-priority required content
- overstate clinical, diagnostic, translational, or deployment readiness
- make the application less coherent with the central funding case

## Phase 4: Draft Each Edit Instruction

For every contextualized target, create one drafted instruction with:

- `id`
- `priority`
- `location`
- `editorial_judgment`
- `action_type`
- `edit_instruction`
- `source_text`
- `replacement_text`
- `word_count_check`
- `constraint_checks`
- `provenance`

### `location`

Name the exact grant prompt or field when recoverable. For form-style grants, prefer labels such as:

- `Q18a. Populations or Communities`
- `Q19a. Metrics for Real-World Impact`
- `Milestone 1 - Activities`

When the exact form field cannot be recovered, use the smallest available section plus a `paragraph_hint`, and set the relevant uncertainty in `editorial_judgment`.

### `editorial_judgment`

Include:

- `status`: `accept`, `partial`, `reject`, or `verify`
- `rationale`: one or two sentences explaining the judgment
- `review_suggestion_addressed`: a concise summary of the review suggestion
- `human_decision_needed`: `true` only when factual, budgetary, partner-status, or live-form behavior information is required

### `edit_instruction`

Write a human-executable instruction that names the exact local action and its reason.

Good:

- "In Q19a, replace the full existing answer with the replacement text below."
- "In Q31, do not paste this until partner status is confirmed; use the replacement only after selecting the matching live-form status."

Not acceptable:

- "Make the impact clearer."
- "Consider adding a near-term public benefit."

### `source_text`

Use one of:

- exact current text from the source field or paragraph when available
- a short enough excerpt to identify the block unambiguously when the field is long
- `null` only when the source text cannot be extracted or the action is a pure verification item

### `replacement_text`

Use one of:

- exact full replacement text for `replace`, `compress`, and `reconcile` actions
- exact insertion text for `insert` actions
- `null` only for `delete`, `reject`, or `verify` actions

For `delete` actions, set `replacement_text` to `null` and make `edit_instruction` identify the text or duplicate block to remove.

When drafting replacement text:

- keep it concise
- avoid invented numerical claims
- mark placeholders with bracketed labels only when a human must supply exact source-local details
- preserve truth constraints from the contextualized plan
- preserve known word-count, character-count, and form-field constraints
- write the text so it can be pasted directly into the named field

### `word_count_check`

Include:

- `limit`: the known word or character limit, or `null`
- `unit`: `words`, `characters`, or `unknown`
- `replacement_count`: the count for `replacement_text`, or `null` when no replacement is proposed
- `within_limit`: `true`, `false`, or `null` when no limit is known
- `notes`: short explanation of any uncertainty, especially live-form counting behavior

### `provenance`

Carry forward:

- `contextualized_target_id`
- `contextualized_edit_plan_path`
- `revision_plan_path` when present
- `writing_constraints_path` when present
- `source_evidence`

## Phase 5: Resolve Deterministic Output Path

Save under the same deterministic grant editing directory as the contextualized plan:

- `artifacts/grants/<source-slug>/editing/drafted-edit-instructions.json`

Derive `<source-slug>` from the source document filename:

- lowercase
- remove extension
- replace every run of non-alphanumeric characters with one hyphen
- trim leading and trailing hyphens

If an artifact for the same source already exists and should be preserved, append `-v2`, `-v3`, and so on:

- `drafted-edit-instructions.json`
- `drafted-edit-instructions-v2.json`
- `drafted-edit-instructions-v3.json`

Store the final absolute path as `DRAFTED_EDIT_INSTRUCTIONS_OUTPUT_PATH`.

## Phase 6: Write The Artifact

Write one JSON artifact at `DRAFTED_EDIT_INSTRUCTIONS_OUTPUT_PATH` with at minimum:

- `artifact_version`: `1.0`
- `document_type`: `grant`
- `source_document_path`
- `contextualized_edit_plan_path`
- `generated_at`: today's date in `YYYY-MM-DD`
- `drafting_notes`
- `edit_instructions`

Use absolute paths internally.

## Phase 7: Validate Before Stopping

Before reporting success:

1. Re-open the saved file and verify it parses as JSON.
2. Confirm `document_type` is `grant`.
3. Confirm `contextualized_edit_plan_path` points to the saved contextualized plan used for the run.
4. Confirm the output path follows `artifacts/grants/<source-slug>/editing/drafted-edit-instructions.json` or the documented `-vN` rule.
5. Confirm `edit_instructions` is non-empty.
6. Confirm every instruction contains location, editorial judgment, action type, executable instruction text, source text or a documented reason it is unavailable, replacement text or a documented reason it is unavailable, word-count check, constraint checks, and provenance.
7. Confirm no instruction claims to have modified the source document directly.
8. Confirm every accepted or partially accepted text edit has paste-ready `replacement_text` unless the action is deletion.
9. Confirm rejected suggestions have `replacement_text = null` and a clear rationale.
10. Confirm every proposed replacement has a word-count or length-limit check.
11. Confirm no replacement text introduces unsupported new facts.
12. Fix the artifact before stopping if any required field is missing or malformed.

## Phase 8: Report Back

After saving and validating, report:

1. the saved drafted edit instructions path
2. the source document path
3. the contextualized edit plan path used
4. how many edit instructions were drafted
5. how many suggestions were accepted, partially accepted, rejected, or marked for verification
6. which instructions are paste-ready versus blocked on factual or live-form verification
7. any uncertainty left for final human source editing

## Non-Scope And Guardrails

This skill must not:

- emit a revision plan
- emit writing constraints
- emit a contextualized edit plan
- rewrite the grant application directly
- support papers, PAPs, or paper-code packages
- change shared schemas to make drafting easier
- sync plugin-bundled skill copies unless a separate handoff authorizes plugin sync
