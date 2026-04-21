# Feedback-Addressed Editing Architecture

## Purpose

This document specifies a generalized editing entry layer for feedback-bearing sources.

The goal is to turn DOCX comments, PDF annotations, review reports, inline notes, and direct user instructions into normalized feedback targets that can reuse the existing staged editing pipeline:

```text
feedback-bearing source + feedback guidelines + selection policy
-> normalized-feedback-plan.json
-> revision-plan-compatible targets
-> writing-constraints.json
-> contextualized-edit-plan.json
-> drafted-edit-instructions.json
```

This is a specification for the shared architecture. The first bounded DOCX-comment planning path is implemented as `Skills/plan-feedback-revisions.md`, with representative single-comment and all-comment normalized feedback artifacts under `artifacts/grants/benrimoh-research-vision/editing/`. The compatibility bridge into the existing `revision-plan.json` contract is implemented as `Skills/convert-feedback-plan-to-revision-plan.md`, with representative Benrimoh revision-plan artifacts in the same editing directory. A later validation pass also proves the selected single-comment `FB2` path can continue through writing constraints, grant contextualization, and drafted edit instructions while preserving feedback provenance. PDF extraction, tracked changes, and direct source-document rewriting remain out of scope.

## Design Boundary

Feedback-addressed editing has one new upstream normalization layer and keeps the downstream stages unchanged.

The adapter layer is responsible for reading source-specific feedback formats and preserving provenance. The shared editing layer is responsible for selecting feedback items, appraising them against guidelines, and emitting normalized revision targets. The existing downstream stages remain responsible for writing constraints, object-specific contextualization, and drafting.

The architecture should not create separate skill families for single-comment, multiple-comment, and all-comment workflows. Those are selection modes over the same normalized contract.

## Input Adapter Responsibilities

Adapters convert one feedback-bearing source into normalized feedback items. They do not draft edits and do not modify source documents.

### DOCX Comments

A DOCX-comments adapter should recover, when available:

- source comment id
- comment author and timestamp
- commented text range or anchor
- comment body and replies
- surrounding paragraph or heading context
- extraction confidence

DOCX tracked-changes generation and source DOCX rewriting are out of scope for this architecture pass.

The first DOCX-comment adapter path is defined in:

- `Skills/plan-feedback-revisions.md`

It reads DOCX Open XML comment parts, preserves recovered comment ids and anchors, applies `single`, `subset`, or `all` selection policies, and emits only `normalized-feedback-plan.json` artifacts. It does not emit contextualized edit plans, drafted edit instructions, tracked changes, or rewritten DOCX files.

### PDF Annotations

A PDF-annotations adapter should recover, when available:

- annotation id or deterministic fallback id
- page number and annotation type
- highlighted or annotated text
- annotation body
- coordinates or page-local location hints
- surrounding text recovered from extraction
- location confidence

PDF anchoring is expected to be weaker than DOCX anchoring. The normalized contract therefore records `location_confidence` and `anchor_recovery_notes`.

### Review Reports

A review-report adapter should recover:

- report path
- reviewer section or finding id when present
- issue text or recommendation
- severity language when present
- candidate location hints named by the reviewer

Review reports may already feed `revision-plan.json`. Under this generalized architecture they can also be represented as feedback items so selection and guideline appraisal are shared with comment and annotation workflows.

### Inline Notes

An inline-notes adapter should recover:

- note id or deterministic fallback id
- source path
- note text
- inline marker or nearby quoted text
- section, heading, or paragraph hints
- uncertainty caused by ambiguous note placement

Inline notes are treated as feedback, not as already-approved replacement text.

### Direct User Instructions

A direct-user-instruction adapter should recover:

- instruction id
- instruction text
- user-supplied target span or location hint
- source path
- selection status
- guideline or constraint source if supplied

Direct instructions still pass through guideline appraisal and downstream constraints unless the user explicitly frames them as non-negotiable constraints.

## Selection Modes

The normalized feedback plan must support three selection modes:

- `single`: exactly one feedback item is selected.
- `subset`: two or more feedback items are selected by id, author, location, status, tag, source, or another recorded selector.
- `all`: all open or eligible feedback items from the normalized source set are selected.

Selection is explicit. Downstream stages must use `selected_feedback_ids` and must not silently expand a single or subset selection into unrelated feedback.

## Guideline Appraisal

Each selected feedback item carries a guideline appraisal. The appraisal records whether the feedback should be acted on as written, narrowed, rejected, or verified before drafting.

Allowed states:

- `accept`: the feedback is warranted and should be implemented.
- `partial`: the concern is valid, but the edit should be narrower than requested.
- `reject`: the feedback would weaken accuracy, violate constraints, duplicate other work, or overfit a preference.
- `verify`: the feedback may be warranted, but factual, administrative, source-local, or methodological confirmation is needed.

The appraisal is not final drafting. It constrains how the normalized feedback item maps into revision targets and later edit instructions.

## Normalized Feedback Artifact

The canonical artifact name is:

- `normalized-feedback-plan.json`

The schema lives at:

- `templates/editing/normalized-feedback-plan.schema.json`

The artifact is saved under the same deterministic editing directory as the existing staged artifacts:

- `artifacts/grants/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/papers/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/paps/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/paper-code/<source-slug>/editing/normalized-feedback-plan.json`

If an artifact for the same source should be preserved, append `-v2`, `-v3`, and so on:

- `normalized-feedback-plan.json`
- `normalized-feedback-plan-v2.json`
- `normalized-feedback-plan-v3.json`

The artifact must include:

- `artifact_version`
- `document_type`
- `source_document_path`
- `feedback_sources`
- `selection`
- `feedback_items`
- `normalized_revision_targets`
- `downstream_mapping`
- `generated_at`

Each feedback item must include:

- stable normalized `id`
- source-specific id when recoverable
- `source_type`
- `feedback_text`
- author or origin when recoverable
- anchoring data
- `location_confidence`
- selected status
- guideline appraisal
- provenance

The allowed source types are:

- `docx-comment`
- `pdf-annotation`
- `review-report`
- `inline-note`
- `direct-user-instruction`

## Anchoring And Location Confidence

Adapters must preserve enough anchoring evidence for later object-specific contextualization to find the target without pretending the adapter has final edit placement.

Anchoring fields distinguish:

- exact quote or selected source text
- surrounding text
- section, heading, paragraph, page, or coordinate hints
- source-local ids such as DOCX comment ids or PDF annotation ids
- `location_confidence`: `high`, `medium`, `low`, or `unknown`
- `anchor_recovery_notes`

Low-confidence anchoring does not block normalization. It must be surfaced so contextualization and drafting can use `verify` or request human placement checks.

## Downstream Mapping

The recommended compatibility path is:

1. Produce `normalized-feedback-plan.json`.
2. Convert selected and appraised feedback into `normalized_revision_targets` that are compatible with `revision-plan.json` targets.
3. Emit a compatible `revision-plan.json` with `Skills/convert-feedback-plan-to-revision-plan.md`.
4. Feed the compatible revision plan into the existing staged pipeline.

This preserves the existing downstream contracts:

- `writing-constraints.json` remains first-class and is not replaced by feedback guidelines.
- `contextualized-edit-plan.json` remains responsible for source-local placement and constraint checks.
- `drafted-edit-instructions.json` remains responsible for human-applied edit instructions and paste-ready text when supported.
- provenance must carry feedback source ids, adapter evidence, guideline appraisal, and any revision-plan compatibility id.

The normalized target id should use a stable prefix such as `F1`, `F2`, and `F3`. When converted into `revision-plan.json`, those ids are mapped to `R1`, `R2`, and `R3`; the bridge preserves the mapping in plan notes and keeps feedback ids, source-specific comment ids, guideline appraisal, and anchor evidence recoverable through schema-allowed evidence and notes fields.

The Benrimoh validation chain demonstrates this downstream mapping for the single selected feedback item `FB2`: `F1` maps to `R1`, and the final drafted instruction keeps `FB2`, DOCX comment id `1`, the normalized feedback plan path, and the revision plan path recoverable without changing downstream schemas.

## Out Of Scope

This architecture does not implement:

- PDF annotation extraction
- tracked changes
- direct DOCX, PDF, TeX, Markdown, or form rewriting
- source-document patch application
- plugin sync
- downstream contextualization or drafting from feedback targets

Those belong to later bounded implementation passes after this contract is stable.
