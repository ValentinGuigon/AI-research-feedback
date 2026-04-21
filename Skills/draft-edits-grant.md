---
description: Draft grant-specific post-review edit instructions from a saved contextualized edit plan
---

You are coordinating the grant-specific drafting stage of the post-review editing pipeline.

Your job is to turn one saved `contextualized-edit-plan.json` into deterministic `drafted-edit-instructions.json` that a human can apply to a grant application.

## Goal

Produce a bounded grant drafting artifact that:

- consumes a saved contextualized edit plan rather than re-reading review state ad hoc
- turns each contextualized target into executable grant-edit instructions
- preserves location, constraint, and review-evidence provenance
- may include bounded replacement or insertion text when the source evidence supports it
- does not rewrite the source document directly

This skill is grant-specific. It does not implement paper, PAP, or paper-code drafting.

## Runtime Rules

- Work from local repository files only.
- Produce exactly one drafted edit instructions artifact for one grant source document per run.
- Require a saved `contextualized-edit-plan.json` input.
- Treat the contextualized plan as the controlling source for targets, locations, constraints, and review evidence.
- Use grant-facing wording that is suitable for sponsor, feasibility, budget, public-benefit, and responsible-AI sections.
- Do not add unsupported partners, results, methods, budgets, timelines, beneficiaries, or outcome metrics.
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

For each contextualized target, identify the smallest credible drafting action:

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

## Phase 4: Draft Each Edit Instruction

For every contextualized target, create one drafted instruction with:

- `id`
- `priority`
- `location`
- `action_type`
- `edit_instruction`
- `proposed_text`
- `constraint_checks`
- `provenance`

### `edit_instruction`

Write a human-executable instruction that names the local action and its reason.

### `proposed_text`

Use one of:

- a short insertion or replacement snippet when the contextualized evidence supports wording
- `null` when the correct action is deletion, reconciliation, or source-local verification

When proposing text:

- keep it concise
- avoid invented numerical claims
- mark placeholders with bracketed labels only when a human must supply exact source-local details
- preserve truth constraints from the contextualized plan

### `provenance`

Carry forward:

- `contextualized_target_id`
- `contextualized_edit_plan_path`
- `revision_plan_path` when present
- `writing_constraints_path` when present
- `source_evidence`

## Phase 5: Resolve Deterministic Output Path

Save under the same deterministic grant editing directory as the contextualized plan:

- `review/editing/grants/<source-slug>/drafted-edit-instructions.json`

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
4. Confirm the output path follows `review/editing/grants/<source-slug>/drafted-edit-instructions.json` or the documented `-vN` rule.
5. Confirm `edit_instructions` is non-empty.
6. Confirm every instruction contains location, action type, executable instruction text, constraint checks, and provenance.
7. Confirm no instruction claims to have modified the source document directly.
8. Confirm no proposed text introduces unsupported new facts.
9. Fix the artifact before stopping if any required field is missing or malformed.

## Phase 8: Report Back

After saving and validating, report:

1. the saved drafted edit instructions path
2. the source document path
3. the contextualized edit plan path used
4. how many edit instructions were drafted
5. which instructions include proposed text versus deletion, reconciliation, or verification actions
6. any uncertainty left for final human source editing

## Non-Scope And Guardrails

This skill must not:

- emit a revision plan
- emit writing constraints
- emit a contextualized edit plan
- rewrite the grant application directly
- support papers, PAPs, or paper-code packages
- change shared schemas to make drafting easier
- sync plugin-bundled skill copies unless a separate handoff authorizes plugin sync
