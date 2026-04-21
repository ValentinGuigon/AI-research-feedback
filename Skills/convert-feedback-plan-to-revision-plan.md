---
description: Convert a normalized feedback plan into a schema-compatible revision-plan artifact for downstream editing stages
---

You are coordinating the compatibility bridge from feedback-addressed planning into the existing post-review editing pipeline.

Your job is to turn one `normalized-feedback-plan.json` artifact into one schema-conformant `revision-plan.json` artifact without changing downstream contracts.

## Goal

Produce a `templates/editing/revision-plan.schema.json` compatible artifact that:

- consumes one normalized feedback plan
- converts only `normalized_revision_targets` from selected feedback
- preserves target order
- maps feedback target ids such as `F1` to revision target ids such as `R1`
- preserves feedback provenance in schema-allowed fields
- stops before writing constraints, contextualization, drafting, tracked changes, or source rewriting

## Runtime Rules

- Work from local repository files only.
- Produce exactly one revision-plan artifact for one normalized feedback plan per run.
- Treat `templates/editing/revision-plan.schema.json` as the controlling output contract.
- Do not modify the normalized feedback plan.
- Do not emit writing constraints, contextualized edit plans, drafted edit instructions, tracked changes, or rewritten source documents.
- Do not sync plugin-bundled copies in this workflow.

## Phase 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- Optional normalized feedback plan argument:
  - `feedback_plan=<path>`
  - `normalized_feedback_plan=<path>`
- Optional output argument:
  - `output=<path>`
- Optional document-type argument:
  - `type=grant`
  - `type=paper`
  - `type=pap`
  - `type=paper-code`
- Remaining unresolved `.json` path-like token should be treated as the normalized feedback plan path when `feedback_plan=` is absent.

Resolution rules:

1. Resolve the normalized feedback plan path to an absolute local path.
2. Confirm the normalized feedback plan exists and parses as JSON.
3. If `type=` is supplied, confirm it matches the plan `document_type`.
4. If `output=` is supplied, resolve it to an absolute local path and preserve any existing file unless explicitly authorized to overwrite.
5. If `output=` is absent, resolve the deterministic editing directory from the normalized plan `document_type` and `source_document_path`.

Store:

- `NORMALIZED_FEEDBACK_PLAN_PATH`
- `REVISION_PLAN_OUTPUT_PATH`
- `DOCUMENT_TYPE`
- `SOURCE_DOCUMENT_PATH`

## Phase 2: Validate Inputs And Contract

1. Read `templates/editing/normalized-feedback-plan.schema.json`.
2. Read `templates/editing/revision-plan.schema.json`.
3. Confirm the normalized feedback plan has:
   - `document_type`
   - `source_document_path`
   - `selection.selected_feedback_ids`
   - `feedback_items`
   - `normalized_revision_targets`
   - `downstream_mapping.target_id_map`
4. Confirm every normalized revision target references only selected feedback item ids.
5. Stop if the revision-plan schema cannot represent provenance using `review_path`, `finding_id`, `quote_or_summary`, and `notes`.

## Phase 3: Resolve Deterministic Output Path

Save under `artifacts/` using the normalized object folder for `DOCUMENT_TYPE` and the `editing` stage folder:

- `grant` -> `artifacts/grants/<source-slug>/editing/`
- `paper` -> `artifacts/papers/<source-slug>/editing/`
- `pap` -> `artifacts/paps/<source-slug>/editing/`
- `paper-code` -> `artifacts/paper-code/<source-slug>/editing/`

Derive `<source-slug>` from the source document filename:

- lowercase
- remove extension
- replace every run of non-alphanumeric characters with one hyphen
- trim leading and trailing hyphens

Default output path:

- `artifacts/<object-folder>/<source-slug>/editing/revision-plan.json`

If that file already exists and should be preserved, append `-v2`, `-v3`, and so on:

- `revision-plan.json`
- `revision-plan-v2.json`
- `revision-plan-v3.json`

## Phase 4: Map Targets

Convert every item in `normalized_revision_targets`, in order, into one `revision_targets` entry.

### `id`

Use deterministic revision ids in normalized target order:

- `R1`
- `R2`
- `R3`

If the normalized feedback plan already has `downstream_mapping.target_id_map`, preserve that mapping when it matches target order. Otherwise, record the inferred mapping in `plan_notes`.

### Direct Fields

Copy the following fields directly when present:

- `priority`
- `issue`
- `edit_intent`
- `motivation`
- `dependencies`

### `source_evidence`

Every revision target must carry at least one evidence object with:

- `review_path`: the absolute or repo-local path to the normalized feedback plan
- `review_section`: `normalized_revision_targets`
- `finding_id`: a compact provenance string containing the normalized target id, feedback item id, and source-specific feedback id when recoverable
- `quote_or_summary`: a concise summary containing the feedback text, guideline appraisal state, and anchor or candidate-location evidence

Do not put unsupported keys inside `source_evidence`; the revision-plan schema sets `additionalProperties` to false.

### `candidate_locations`

Copy only schema-allowed location fields:

- `section_hint`
- `heading_hint`
- `paragraph_hint`
- `reason`

Move normalized feedback `location_confidence` into target `notes`.

### `notes`

Use target notes to preserve recoverable provenance that does not fit in the revision-plan schema:

- normalized feedback target id
- selected feedback item ids
- source-specific feedback ids such as DOCX comment ids
- source type and source path
- guideline appraisal state and rationale
- author or origin
- anchor source text or surrounding text summary
- location confidence

Keep notes concise and deterministic.

## Phase 5: Write The Artifact

Write one JSON artifact at `REVISION_PLAN_OUTPUT_PATH` with:

- `artifact_version`: `1.0`
- `document_type`
- `source_document_path`
- `review_paths`: a one-item array containing `NORMALIZED_FEEDBACK_PLAN_PATH`
- `generated_at`: today's date in `YYYY-MM-DD`
- `plan_notes`
- `revision_targets`

Recommended plan notes:

- state that the artifact is a compatibility conversion from normalized feedback
- record the selected feedback ids
- record the normalized target id to revision target id mapping
- state that downstream stages still own writing constraints, contextualization, and drafting

## Phase 6: Validate Before Stopping

Before reporting success:

1. Re-open the saved file and verify it parses as JSON.
2. Validate it against `templates/editing/revision-plan.schema.json`.
3. Confirm `review_paths` contains the normalized feedback plan path.
4. Confirm the number of `revision_targets` equals the number of `normalized_revision_targets`.
5. Confirm every revision target has source evidence pointing back to the normalized feedback plan.
6. Confirm every feedback item id and source-specific feedback id is recoverable from evidence or notes.
7. For a single-comment normalized plan, confirm exactly one target and no unselected feedback id appears in targets.
8. For an all-comment normalized plan, confirm all selected feedback items are represented in target order.
9. Confirm no writing constraints, contextualized edit plan, drafted edit instructions, tracked changes, or rewritten source document was emitted.

Fix the artifact before stopping if any required field is missing or malformed.

## Phase 7: Report Back

After saving and validating, report:

1. the saved revision-plan path
2. the normalized feedback plan path used as review evidence
3. the resolved document type
4. the target count
5. the feedback-to-revision target id mapping
6. the provenance fields used for feedback ids, source-specific ids, anchor evidence, and guideline appraisal
7. any uncertainty left for downstream contextualization

## Non-Scope And Guardrails

This skill must not:

- draft replacement text
- emit writing constraints
- emit contextualized edit plans
- emit drafted edit instructions
- rewrite or patch source documents
- generate tracked changes
- extract DOCX comments or PDF annotations directly
- modify schemas
- sync plugin-bundled copies
