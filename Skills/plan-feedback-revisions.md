---
description: Normalize feedback-bearing sources into selected feedback revision targets and save a deterministic normalized-feedback-plan artifact
---

You are coordinating the feedback-addressed revision-planning stage that sits before writing constraints, contextualization, and drafting.

Your job is to turn one feedback-bearing source into a deterministic `normalized-feedback-plan.json` artifact. This pass defines the shared planning workflow with DOCX comments as the first concrete adapter path.

## Goal

Produce a schema-conformant normalized feedback plan that:

- extracts feedback items from a supported feedback-bearing source
- preserves source-specific provenance, anchors, and uncertainty
- applies an explicit selection policy across `single`, `subset`, or `all`
- converts only selected feedback into normalized revision targets
- stays upstream of writing constraints, object-specific contextualization, and drafting

This skill does not draft edits, rewrite source documents, create tracked changes, or extract PDF annotations.

## Runtime Rules

- Work from local repository files only.
- Produce exactly one normalized-feedback-plan artifact for one source document per run.
- Treat source format as an adapter concern and keep downstream editing stages unchanged.
- Preserve every recovered feedback item, but create normalized revision targets only for selected feedback items.
- Do not silently expand a `single` or `subset` selection into unrelated comments.
- Do not modify the feedback-bearing source document.

## Phase 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- Optional document-type arguments:
  - `type=grant`
  - `type=paper`
  - `type=pap`
  - `type=paper-code`
- Optional source argument:
  - `source=<path>`
- Optional feedback-source argument:
  - `feedback=<path>`
- Optional source-type argument:
  - `source_type=docx-comment`
- Optional selection arguments:
  - `mode=single`
  - `mode=subset`
  - `mode=all`
  - `feedback_id=<id>`
  - `feedback_ids=<id1,id2,...>`
- Optional guideline arguments:
  - `guidelines=<path1,path2,...>`
  - `instruction=<free text guideline or selection instruction>`
- Remaining unresolved path-like token should be treated as the source document path when `source=` is absent.

Resolution rules:

1. Resolve all supplied paths to absolute local paths.
2. If `feedback=` is absent, use `source=` as the feedback-bearing source.
3. If `source_type=` is absent and the feedback source ends in `.docx`, use `docx-comment`.
4. If the source type cannot be resolved to a supported adapter, stop and report the ambiguity.
5. If `type=` is absent, infer `DOCUMENT_TYPE` from the source path and nearby artifact folders using only:
   - `grant`
   - `paper`
   - `pap`
   - `paper-code`
6. If document type cannot be resolved confidently, stop and report the ambiguity instead of guessing.
7. If `mode=` is absent, stop and require an explicit selection mode.
8. For `mode=single`, require exactly one `feedback_id`.
9. For `mode=subset`, require two or more `feedback_ids`.
10. For `mode=all`, select all eligible open feedback items recovered by the adapter.

Store:

- `DOCUMENT_TYPE`
- `SOURCE_DOCUMENT_PATH`
- `FEEDBACK_SOURCE_PATH`
- `SOURCE_TYPE`
- `SELECTION_MODE`
- `SELECTED_SOURCE_FEEDBACK_IDS`
- `GUIDELINE_PATHS`
- `INSTRUCTION`

## Phase 2: Validate Inputs And Contract

1. Confirm that `SOURCE_DOCUMENT_PATH` exists and is a local file.
2. Confirm that `FEEDBACK_SOURCE_PATH` exists and is a local file.
3. Confirm that every supplied guideline path exists before using it.
4. Read `templates/editing/normalized-feedback-plan.schema.json` and treat it as the controlling artifact contract.
5. Validate that the schema requires at minimum:
   - `artifact_version`
   - `document_type`
   - `source_document_path`
   - `generated_at`
   - `feedback_sources`
   - `selection`
   - `feedback_items`
   - `normalized_revision_targets`
   - `downstream_mapping`

Stop if the schema is missing or materially unable to represent the recovered feedback source.

## Phase 3: DOCX Comment Adapter

For `SOURCE_TYPE=docx-comment`, read the DOCX as an Open XML package. Do not use Word automation and do not save the DOCX.

Recover from `word/comments.xml` when available:

- `w:id` as the source-specific comment id
- `w:author` as author or origin
- `w:date` as creation timestamp
- concatenated comment body text
- reply, assignment, or status language as part of the feedback text when it is present in the comment body

Recover anchoring from `word/document.xml` when available:

- text enclosed by matching `w:commentRangeStart` and `w:commentRangeEnd`
- surrounding paragraph text
- paragraph or section hints when visible nearby
- `high` location confidence when a comment range and surrounding paragraph are recovered
- `medium` location confidence when only a paragraph-level reference is recovered
- `unknown` location confidence when comment text exists without a recoverable anchor

If `word/comments.xml` is absent, stop and report that the DOCX contains no extractable comments.

Treat every recovered DOCX comment as eligible unless the adapter can recover an explicit resolved or closed status. If no resolved/closed status is recoverable, record status as `open-or-unknown`.

## Phase 4: Normalize Feedback Items

Create `feedback_items` in deterministic source order.

Each item must include:

- stable normalized `id` using `FB1`, `FB2`, `FB3`
- `source_id` for the feedback source
- `source_specific_id` from the DOCX comment id when recoverable
- `source_type`
- `author_or_origin`
- `created_at`
- `feedback_text`
- `status`
- `tags`
- `anchor`
- `location_confidence`
- `selected`
- `guideline_appraisal`
- `provenance`

Selection rules:

- `selected` is true only when the item's source-specific id or normalized id matches the selection policy.
- `mode=all` selects every eligible open feedback item.
- `mode=single` must produce exactly one selected feedback item.
- `mode=subset` must produce exactly the requested selected feedback items.
- Stop if any requested feedback id is absent.

Guideline appraisal rules:

- Use `verify` when feedback asks for factual or source-local confirmation.
- Use `accept` when the requested change is editorially actionable and does not conflict with supplied guidelines.
- Use `partial` when the concern is valid but should be narrowed before drafting.
- Use `reject` only when the supplied guidelines or source evidence show that acting on the feedback would be harmful or out of scope.
- Set `human_decision_needed` to true for `verify`, unresolved assignments, or ambiguous anchors.

## Phase 5: Build Normalized Revision Targets

Create `normalized_revision_targets` only from selected feedback items.

Target rules:

- Use deterministic identifiers in selected feedback order:
  - `F1`
  - `F2`
  - `F3`
- `feedback_item_ids` must contain only selected normalized feedback ids.
- Do not create a target for an unselected feedback item.
- Map comment language to the smallest fitting `edit_intent`:
  - missing material -> `add`
  - unclear text -> `clarify`
  - move or placement request -> `restructure`
  - word count or overlength concern -> `compress`
  - duplication or not-needed concern -> `remove`
  - consistency concern -> `align`
  - factual check or unresolved assignment -> `verify`
- Preserve source evidence from the feedback item and anchor.
- Candidate locations should carry the recovered section, heading, paragraph, and location confidence without claiming final placement.

## Phase 6: Resolve Deterministic Output Path

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

- `artifacts/<object-folder>/<source-slug>/editing/normalized-feedback-plan.json`

If that file already exists and should be preserved, append `-v2`, `-v3`, and so on to the filename.

## Phase 7: Write The Artifact

Write one JSON artifact at the resolved output path with:

- `artifact_version`: `1.0`
- `document_type`
- `source_document_path`
- `generated_at`: today's date in `YYYY-MM-DD`
- `feedback_guideline_paths` when supplied
- `feedback_sources`
- `selection`
- `feedback_items`
- `normalized_revision_targets`
- `downstream_mapping`

For DOCX comments, the feedback source should include:

- `source_type`: `docx-comment`
- `adapter_name`: `docx-comments`
- `adapter_version`: `1.0`

Set `downstream_mapping.recommended_path` to `emit-compatible-revision-plan` unless a later object-specific contextualizer explicitly supports direct normalized feedback consumption.

## Phase 8: Validate Before Stopping

Before reporting success:

1. Re-open the saved file and verify it parses as JSON.
2. Validate it against `templates/editing/normalized-feedback-plan.schema.json`.
3. Confirm `selection.mode` matches the requested selection mode.
4. Confirm `selection.selected_feedback_ids` equals the selected `feedback_items` ids.
5. For `mode=single`, confirm exactly one selected feedback id and exactly one normalized revision target.
6. For `mode=all`, confirm every eligible open feedback item is selected.
7. Confirm no normalized revision target references an unselected feedback item.
8. Confirm no contextualized edit plan, drafted edit instructions, tracked changes, or rewritten source document was emitted.

Fix the artifact before stopping if any required field is missing or malformed.

## Phase 9: Report Back

After saving and validating, report:

1. the saved normalized-feedback-plan path
2. the resolved document type
3. the feedback source path and source type
4. the selection mode and selected feedback ids
5. how many feedback items were recovered
6. how many normalized revision targets were created
7. any important anchor or guideline uncertainty left for downstream contextualization

## Non-Scope And Guardrails

This skill must not:

- rewrite the DOCX or any other source document
- generate tracked changes
- extract PDF annotations
- emit writing constraints
- emit a contextualized edit plan
- emit drafted edit instructions
- treat a single-comment request as permission to address nearby unrelated comments
- sync plugin-bundled copies
