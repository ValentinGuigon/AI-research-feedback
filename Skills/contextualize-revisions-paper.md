---
description: Contextualize paper revision targets against a source manuscript and saved writing constraints
---

You are coordinating the paper-specific contextualization stage of the post-review editing pipeline.

Your job is to turn a saved `revision-plan.json` and a saved `writing-constraints.json` for one paper into a deterministic `contextualized-edit-plan.json` that downstream drafting can consume.

## Goal

Produce a schema-conformant contextualized edit plan that:

- consumes saved shared-stage artifacts rather than re-parsing review state ad hoc
- maps each abstract revision target to manuscript sections or paper-local dependencies
- checks the proposed localization against journal, reporting, and truth constraints
- preserves provenance back to the review evidence already recorded in the revision plan
- stops before drafting replacement text

This skill is paper-specific. It does not implement grant, PAP, paper-code, or drafting workflows.

## Runtime Rules

- Work from local repository files only.
- Produce exactly one contextualized edit plan for one paper source document per run.
- Require saved `revision-plan.json` and `writing-constraints.json` inputs.
- Keep all source evidence grounded in the saved revision plan and local source document.
- Prefer exact manuscript headings and nearby text when recoverable.
- Use bounded fallback localization only when source extraction is unavailable.
- Do not draft replacement prose, rewrite the source document, or emit patch-like edits.

## Phase 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- Required or inferable revision-plan argument:
  - `revision_plan=<path>`
  - `plan=<path>`
- Required or inferable writing-constraints argument:
  - `writing_constraints=<path>`
  - `constraints=<path>`
- Optional source argument:
  - `source=<path>`
- Optional text extraction argument:
  - `source_text=<path>`
- Remaining unresolved path-like token may be treated as the source document path when `source=` is absent.

Resolution rules:

1. Resolve all supplied paths to absolute local paths.
2. If `revision_plan=` is absent, search the resolved source's deterministic paper editing directory for `revision-plan.json`.
3. If `writing_constraints=` is absent, search the resolved source's deterministic paper editing directory for `writing-constraints.json`.
4. If `source=` is absent, use `source_document_path` from the revision plan.
5. Stop if the revision plan, writing constraints artifact, or source document cannot be resolved.

Store:

- `REVISION_PLAN_PATH`
- `WRITING_CONSTRAINTS_PATH`
- `SOURCE_DOCUMENT_PATH`
- `SOURCE_TEXT_PATH` when supplied or generated locally

## Phase 2: Validate Inputs And Contract

1. Confirm that `REVISION_PLAN_PATH`, `WRITING_CONSTRAINTS_PATH`, and `SOURCE_DOCUMENT_PATH` exist locally.
2. Read `templates/editing/contextualized-edit-plan.schema.json` when it exists and treat it as the controlling artifact contract.
3. Parse both saved shared-stage artifacts as JSON.
4. Confirm both artifacts have `document_type = paper`.
5. Confirm both artifacts name the same `source_document_path`.
6. Confirm the revision plan has a non-empty `revision_targets` array.
7. Confirm the writing constraints artifact has `constraints` and `constraint_sources`.

Stop rather than coercing incompatible artifacts.

## Phase 3: Read Paper Source Structure

Read enough source-document structure to localize each revision target.

Prefer these source cues:

- title, abstract, introduction, methods, results, discussion, references, and supplementary-information pointers
- journal-required order when stated in review or constraints
- headings around experiment design, participants, stimuli, statistical analyses, measures, and limitations
- figure, table, appendix, or supplement references when a target must propagate outside the main text
- nearby text surrounding likely target claims

If the source document is a PDF and direct extraction is available, extract or read text before localizing. If extraction is unavailable:

- continue with the source filename, saved revision-plan `candidate_locations`, writing constraints, and review evidence
- set unrecoverable `heading_match`, `paragraph_hint`, or `text_quote` fields to `null`
- add a `context_notes` entry explaining that final paragraph-level placement should be checked against the manuscript

## Phase 4: Build Paper Context Model

For papers, map each target to one or more of these location families:

- title, abstract, and contribution framing
- introduction and literature-positioning logic
- methods, participants, stimuli, measures, incentives, exclusions, and statistical analysis
- results, robustness analyses, and supplementary analyses
- discussion, limitations, overclaiming, and future work
- references, reporting statements, and supplementary materials
- claim propagation across abstract, introduction, results, discussion, figures, tables, and supplement

Use the smallest credible final location, but add `propagation_targets` when the same change must be checked across multiple paper sections.

## Phase 5: Contextualize Each Revision Target

For every revision target in the saved plan, create one contextualized target with:

- `id`
- `priority`
- `issue`
- `location`
- `suggestion`
- `motivation`
- `dependencies` when the revision has linked effects
- `propagation_targets` when paper consistency needs cross-section checks
- `constraint_checks`
- `source_evidence`

### Location Rules

Populate `location.section` with a paper-facing section or section family. Use `heading_match`, `paragraph_hint`, `text_quote`, and `source_path` when recoverable.

### Suggestion Rules

Write an executable edit instruction, not replacement prose.

Good:

- "Revise the discussion limitations paragraph so stimulus-selection ambiguity is treated as a boundary condition on the confidence-accuracy conclusion."

Not allowed:

- drafted replacement paragraphs
- invented empirical results, analyses, citations, samples, or journal requirements
- new claims not present in the source artifacts

### Constraint-Check Rules

Each contextualized target must include at least one constraint check. Prefer checks from:

- `constraints.hard_constraints`
- required manuscript sections
- journal or reviewer reporting requests
- style requirements
- truth constraints against unsupported new analyses or claims
- cross-section consistency requirements

## Phase 6: Resolve Deterministic Output Path

Save under the same deterministic paper editing directory as the shared-stage artifacts:

- `review/editing/papers/<source-slug>/contextualized-edit-plan.json`

Derive `<source-slug>` from the source document filename:

- lowercase
- remove extension
- replace every run of non-alphanumeric characters with one hyphen
- trim leading and trailing hyphens

If an artifact for the same source already exists and should be preserved, append `-v2`, `-v3`, and so on:

- `contextualized-edit-plan.json`
- `contextualized-edit-plan-v2.json`
- `contextualized-edit-plan-v3.json`

Store the final absolute path as `CONTEXTUALIZED_EDIT_PLAN_OUTPUT_PATH`.

## Phase 7: Write The Artifact

Write one JSON artifact at `CONTEXTUALIZED_EDIT_PLAN_OUTPUT_PATH` with at minimum:

- `artifact_version`: `1.0`
- `document_type`: `paper`
- `source_document_path`
- `revision_plan_path`
- `writing_constraints_path`
- `generated_at`: today's date in `YYYY-MM-DD`
- `revision_targets`

Include `context_notes` when there is meaningful source-extraction or localization uncertainty.

Use absolute paths internally.

## Phase 8: Validate Before Stopping

Before reporting success:

1. Re-open the saved file and verify it parses as JSON.
2. Manually confirm that all top-level required fields from `templates/editing/contextualized-edit-plan.schema.json` are present.
3. Confirm `document_type` is `paper`.
4. Confirm `revision_plan_path` and `writing_constraints_path` point to the saved shared-stage artifacts used for this run.
5. Confirm the output path follows `review/editing/papers/<source-slug>/contextualized-edit-plan.json` or the documented `-vN` rule.
6. Confirm `revision_targets` is non-empty.
7. Confirm every target contains location data, a suggestion, motivation, non-empty `constraint_checks`, and non-empty `source_evidence`.
8. Confirm no target drafts replacement text or rewrites the source document directly.
9. Fix the artifact before stopping if any required field is missing or malformed.

## Phase 9: Report Back

After saving and validating, report:

1. the saved contextualized-edit-plan path
2. the source document path
3. the revision-plan path used
4. the writing-constraints path used
5. how many targets were contextualized
6. the strongest source-local section anchors recovered
7. any uncertainty left for the later `draft-edits-paper` stage

## Non-Scope And Guardrails

This skill must not:

- emit a revision plan
- emit writing constraints
- draft replacement text
- rewrite the paper directly
- implement `draft-edits-paper`
- support grants, PAPs, or paper-code packages
- change shared schemas to make the paper path easier
