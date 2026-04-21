---
description: Plan normalized post-review revisions for one source document and save a deterministic revision-plan artifact
---

You are coordinating the shared revision-planning stage that sits between completed review and any object-specific contextualization or drafting work.

Your job is to turn one source document plus one or more review artifacts into a deterministic `revision-plan.json` that downstream editing stages can consume without re-parsing the original review from scratch.

## Goal

Produce a schema-conformant revision plan that:

- normalizes review findings into bounded revision targets
- preserves provenance back to the exact review artifact(s)
- proposes candidate edit locations without pretending to know final local placement
- stays generic across grants, papers, PAPs, and paper-code workflows

This skill defines the shared planning contract only. It does not draft replacement text and it does not perform object-specific contextualization.

## Runtime Rules

- Work from local repository files only.
- Produce exactly one revision-plan artifact for one source document per run.
- Prefer deterministic normalization over exhaustive interpretation.
- Preserve provenance for every revision target.
- Do not invent unsupported reviewer findings or new source facts.
- Do not collapse planning into contextualization or drafting.

## Phase 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- Optional document-type arguments:
  - `type=grant`
  - `type=paper`
  - `type=pap`
  - `type=paper-code`
- Optional source argument:
  - `source=<path>`
- Optional review arguments:
  - `review=<path>`
  - `reviews=<path1,path2,...>`
- Optional shorthand review paths:
  - any token ending in `.md`, `.txt`, or `.json` may be a review artifact if it is not the source path
- Remaining unresolved path-like token should be treated as the source document path when `source=` is absent

Resolution rules:

1. Resolve all supplied paths to absolute local paths.
2. If `source=` is absent, infer the source path from the remaining path-like token or stop and report that a source document is required.
3. If no review path is supplied, search under `artifacts/` for likely review artifacts tied to the source slug and stop if none are found.
4. If `type=` is supplied, use it as `DOCUMENT_TYPE`.
5. If `type=` is absent, infer `DOCUMENT_TYPE` from the source path and neighboring review directory names using only:
   - `grant`
   - `paper`
   - `pap`
   - `paper-code`
6. If the document type cannot be resolved confidently, stop and report the ambiguity instead of guessing.

Store:

- `DOCUMENT_TYPE`
- `SOURCE_DOCUMENT_PATH`
- `REVIEW_PATHS`

## Phase 2: Validate Inputs

1. Confirm that `SOURCE_DOCUMENT_PATH` exists and is a local file.
2. Confirm that every path in `REVIEW_PATHS` exists and is a local file.
3. Sort `REVIEW_PATHS` lexicographically after absolute-path resolution for deterministic output.
4. Read `templates/editing/revision-plan.schema.json` when it exists and use it as the controlling artifact contract.
5. Validate that the schema requires at minimum:
   - `artifact_version`
   - `document_type`
   - `source_document_path`
   - `review_paths`
   - `generated_at`
   - `revision_targets`

If the schema file is missing, still produce the artifact using the contract described in this skill.

## Phase 3: Read Source Context

Read enough of the source document to support location hints and issue normalization.

At minimum record:

- source filename
- top-level headings or visible section structure when recoverable
- obvious title if recoverable
- any repeated structural anchors that later stages can use for placement

The purpose of this phase is not to rewrite the source or infer missing facts. It is only to gather enough structure to create plausible candidate locations.

If the source document cannot be extracted cleanly because the local format reader is unavailable or extraction fails:

- do not invent local structure
- fall back to the strongest available structural cues from:
  - visible filename terms
  - nearby saved review artifacts
  - nearby profile or package metadata already supplied for this run
- set unresolved `section_hint`, `heading_hint`, or `paragraph_hint` fields to `null`
- record the uncertainty in `plan_notes`

This fallback keeps the stage runnable for bounded validation while preserving the boundary that exact placement belongs to later object-specific contextualization.

## Phase 4: Read Review Artifacts

Read every review artifact in `REVIEW_PATHS`.

For each review artifact, extract when available:

- overall recommendation or decision framing
- critical, major, and minor issue groupings
- required revisions
- numbered concerns
- explicit questions for the author or PI
- any section-specific references

Normalization rules:

- prefer explicit required revisions and major concerns over softer commentary
- merge duplicate findings across review artifacts when they clearly point to the same underlying revision need
- preserve multiple evidence entries when more than one review artifact supports the same target
- split compound findings into separate revision targets when they would require materially different edits

## Phase 5: Build Normalized Revision Targets

Create `revision_targets` as a non-empty ordered list.

Each target must include:

- `id`
- `priority`
- `issue`
- `edit_intent`
- `motivation`
- `source_evidence`
- `candidate_locations`

Populate fields as follows.

### `id`

- Use deterministic identifiers in source order:
  - `R1`
  - `R2`
  - `R3`

### `priority`

Map review language into:

- `critical`
- `high`
- `medium`
- `low`

Priority guidance:

- `critical`: likely submission blocker, fundability threat, or validity threat
- `high`: materially weakens the document and should be fixed before submission
- `medium`: meaningful but not central
- `low`: polish or local cleanup

### `edit_intent`

Normalize into one of:

- `add`
- `clarify`
- `qualify`
- `restructure`
- `compress`
- `remove`
- `align`
- `verify`

Use the smallest intent that captures the action required.

### `motivation`

Write one concise sentence explaining why the revision matters to reviewer confidence, compliance, validity, clarity, or fit.

### `source_evidence`

Every target must carry at least one evidence object with:

- `review_path`
- `quote_or_summary`

Include when recoverable:

- `review_section`
- `finding_id`

Evidence rules:

- use short summaries rather than long quotations
- preserve the original review path exactly
- include multiple evidence entries when a target is corroborated by multiple reviews

### `candidate_locations`

Every target must carry at least one candidate location object with:

- `reason`

Include when recoverable:

- `section_hint`
- `heading_hint`
- `paragraph_hint`

Location rules:

- propose likely edit zones, not final placements
- prefer source-document section names over generic labels when available
- when no credible local hint is available, set the hints to `null` and explain the best available rationale in `reason`

Optional fields:

- `dependencies`
- `notes`

Use `dependencies` for linked edits that later stages should cross-check.
Use `notes` sparingly for unresolved interpretation caveats that do not belong in the core issue statement.

## Phase 6: Add Plan Notes

Populate `plan_notes` only when needed to preserve high-value execution context such as:

- merged duplicate findings across multiple reviews
- uncertainty about exact section naming in the source
- known gaps that require later object-specific contextualization

Do not use `plan_notes` as a dumping ground for full review summaries.

## Phase 7: Resolve Deterministic Output Path

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

If that file already exists and should be preserved, append `-v2`, `-v3`, and so on to the filename.

Versioning rule:

- first artifact: `revision-plan.json`
- next preserved artifact: `revision-plan-v2.json`
- then `revision-plan-v3.json`

Store the final absolute path as `REVISION_PLAN_OUTPUT_PATH`.

## Phase 8: Write The Artifact

Write one JSON artifact at `REVISION_PLAN_OUTPUT_PATH` with at minimum:

- `artifact_version`: `1.0`
- `document_type`
- `source_document_path`
- `review_paths`
- `generated_at`: today's date in `YYYY-MM-DD`
- `revision_targets`

Include `plan_notes` only when non-empty.

Use absolute paths internally.

## Phase 9: Validate Before Stopping

Before reporting success:

1. Re-open the saved file and verify it parses as JSON.
2. Manually confirm that all top-level required fields from `templates/editing/revision-plan.schema.json` are present.
3. Confirm `document_type` is one of:
   - `grant`
   - `paper`
   - `pap`
   - `paper-code`
4. Confirm `review_paths` is non-empty.
5. Confirm `revision_targets` is non-empty.
6. Confirm every revision target contains:
   - `id`
   - `priority`
   - `issue`
   - `edit_intent`
   - `motivation`
   - `source_evidence`
   - `candidate_locations`
7. Confirm every `source_evidence` array is non-empty.
8. Confirm every `candidate_locations` array is non-empty.
9. Fix the artifact before stopping if any required field is missing or malformed.

## Phase 10: Report Back

After saving and validating, report:

1. the saved revision-plan path
2. the resolved document type
3. the source document path
4. the review paths used
5. how many revision targets were created
6. the highest-priority issues represented in the plan
7. any important uncertainty left for later object-specific contextualization

## Non-Scope And Guardrails

This skill must not:

- draft replacement text
- emit a contextualized edit plan
- emit writing constraints
- rewrite the source document directly
- add unsupported claims not grounded in the review artifacts or source materials
- encode object-specific logic that belongs in `contextualize-revisions-<object>` or `draft-edits-<object>`
