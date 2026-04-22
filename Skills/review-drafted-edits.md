---
description: Run the post-draft edit-review loop for validated grant or paper drafted edit instructions
---

You are coordinating the post-draft edit-review iteration loop for one saved grant or paper editing chain.

Your job is to evaluate the candidate revised document state implied by `drafted-edit-instructions.json`, produce advisory edit-review evidence, and, when another automated iteration is warranted, emit the next versioned contextualized plan and drafted edit instructions.

## Goal

Produce a bounded edit-review loop artifact set that:

- consumes saved staged editing artifacts rather than re-reading review state ad hoc
- projects the document state implied by human-applied drafted edit instructions without rewriting the source document
- runs an advisory edit-review panel using the appropriate grant or paper standards
- folds reviewer evidence into a versioned `contextualized-edit-plan-vN.json` when another iteration is needed
- regenerates versioned `drafted-edit-instructions-vN.json` from that versioned contextualized plan
- writes the matching versioned `drafted-edit-recommendations-vN.md` so the latest loop output is human-readable without parsing JSON
- preserves provenance across the original plan, drafted instructions, projected state, panel report, and versioned outputs

This skill currently supports validated grant and paper editing chains only. It does not implement PAP or paper-code edit-review loops.

## Runtime Rules

- Work from local repository files only.
- Produce one loop pass for one source document per run.
- Require a saved `drafted-edit-instructions.json` or versioned drafted instructions artifact.
- Resolve the matching `contextualized-edit-plan.json`, `revision-plan.json`, and `writing-constraints.json` from artifact paths rather than from chat state.
- Use `document_type` to select grant or paper review standards.
- Preserve no-source-rewrite, no-tracked-changes, and advisory-only boundaries in every loop artifact.
- Do not edit source PDF, DOCX, TeX, Markdown, live form, extracted text, or manuscript files directly.
- Stop if `document_type` is `pap` or `paper-code`; those object-family loop paths are deferred until representative artifacts and validation exist.

## Phase 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- Required or inferable drafted-instructions argument:
  - `drafted_instructions=<path>`
  - `instructions=<path>`
  - `draft=<path>`
- Optional document-type argument:
  - `type=grant`
  - `type=paper`
- Optional source argument:
  - `source=<path>`
- Optional iteration argument:
  - `iteration=<integer>`
- Remaining unresolved path-like token may be treated as the drafted-instructions path when an explicit argument is absent.

Resolution rules:

1. Resolve all supplied paths to absolute local paths.
2. If `drafted_instructions=` is absent, search the resolved source's deterministic editing directory for `drafted-edit-instructions.json`.
3. Parse the drafted instructions artifact and use its `document_type` unless `type=` is supplied and matches it.
4. If `source=` is absent, use `source_document_path` from the drafted instructions artifact.
5. Use `contextualized_edit_plan_path` from the drafted instructions artifact to resolve the prior contextualized plan.
6. Use `revision_plan_path` and `writing_constraints_path` from the contextualized plan or instruction provenance when present.
7. Stop if any required artifact cannot be resolved.

Store:

- `DOCUMENT_TYPE`
- `SOURCE_DOCUMENT_PATH`
- `DRAFTED_EDIT_INSTRUCTIONS_PATH`
- `PRIOR_CONTEXTUALIZED_EDIT_PLAN_PATH`
- `REVISION_PLAN_PATH`
- `WRITING_CONSTRAINTS_PATH`
- `ITERATION_NUMBER`

## Phase 2: Validate Inputs And Contract

1. Confirm that `DOCUMENT_TYPE` is `grant` or `paper`.
2. Stop with a clear deferred-status message for `pap` or `paper-code`.
3. Confirm that every resolved path exists locally.
4. Read `templates/editing/projected-revision-state.schema.json`, `templates/editing/edit-review-panel-report.schema.json`, `templates/editing/contextualized-edit-plan.schema.json`, and `templates/editing/drafted-edit-instructions.schema.json` when they exist.
5. Parse the drafted instructions, prior contextualized plan, revision plan, and writing constraints as JSON.
6. Confirm all parsed artifacts use the same `document_type` and `source_document_path`.
7. Confirm the drafted instructions have a non-empty `edit_instructions` array.
8. Confirm every drafted instruction has provenance that points back to the contextualized target it implements.

Stop rather than coercing incompatible artifacts.

## Phase 3: Build Projected Revision State

Create `projected-revision-state.json` for the implied revised state.

The projection must:

- point to `DRAFTED_EDIT_INSTRUCTIONS_PATH`
- point to `PRIOR_CONTEXTUALIZED_EDIT_PLAN_PATH`
- include `projection_boundary.source_rewrite_performed = false`
- include `projection_boundary.tracked_changes_created = false`
- include `projection_boundary.review_evidence_only = true`
- map every drafted instruction into `applied_instruction_map`
- record whether each projection is complete, partial, rejected, or verification-blocked
- preserve source-local uncertainties and unresolved items
- describe whether the projection is structured by field, section, or text excerpt

For grants, use form fields, prompt labels, narrative sections, sponsor constraints, and public-impact logic as the projection frame.

For papers, use manuscript sections, claim propagation paths, methods/results/discussion dependencies, and journal-facing fit as the projection frame.

## Phase 4: Run Advisory Edit Review

Create `edit-review-panel-report.json` from the projected state.

For grants, borrow standards from grant review:

- sponsor fit
- fundability
- feasibility
- public impact
- compliance signals
- team, budget, and operational coherence
- internal consistency
- adversarial panel concerns

For papers, borrow standards from paper review:

- contribution and journal fit
- claim discipline
- methods credibility
- internal consistency
- results/discussion alignment
- tables, figures, references, and supplement support

The panel report must:

- point to the projected revision state
- point to the drafted instructions it reviewed
- include local assessments tied to instruction ids and contextualized target ids
- include a global assessment of the projected revised state
- recommend accept, revise, reject, verify, or stop dispositions
- state whether to accept current drafted instructions, loop to a new contextualized plan, or escalate to human verification
- record `advisory_boundary.reviewer_output_authoritative = false`
- name the next authoritative artifact when another iteration is recommended

Reviewer output is evidence for the next plan, not the next plan itself.

## Phase 5: Decide Stop Or Iterate

Stop after the panel report when:

- the recommendation is `accept current drafted instructions`
- all remaining material issues require human verification
- further iteration would overfit reviewer preferences or exceed local evidence

When the recommendation is `loop to a new contextualized plan`, create the next versioned artifacts:

- `contextualized-edit-plan-vN.json`
- `drafted-edit-instructions-vN.json`
- `drafted-edit-recommendations-vN.md`

The version number should be one greater than the drafted/contextualized plan being reviewed, unless the user supplied an explicit `iteration=` value that does not conflict with existing files.

## Phase 6: Write Versioned Contextualized Plan

The versioned contextualized plan must preserve the standard contextualized-plan contract and add iteration provenance:

- `previous_contextualized_edit_plan_path`
- `previous_drafted_edit_instructions_path`
- `projected_revision_state_path`
- `edit_review_panel_report_path`
- `iteration_reason`
- `local_assessment_summary`
- `global_assessment_summary`
- `accepted_prior_targets`
- `revised_prior_targets`
- `rejected_or_rolled_back_targets`
- `verification_required`
- `tradeoff_notes`

Target ids should remain stable when the underlying concern continues across iterations. New ids are allowed only for genuinely new concerns discovered by the review loop.

## Phase 7: Write Versioned Drafted Instructions

The versioned drafted instructions must:

- point to the versioned contextualized plan
- preserve standard drafted-instruction fields
- preserve prior-plan, projected-state, and panel-report provenance inside each instruction's `provenance`
- use human-applied instructions only
- keep `replacement_text` bounded to evidence-supported wording, or `null` for delete, reject, verify, or source-local verification actions
- include word-count or length-limit checks when known

Also write the matching versioned Markdown recommendations manual from the same drafted instruction model. It must include the same minimum human-readable sections required by `draft-edits-grant` and `draft-edits-paper`, including paste-ready edits, verification-required items, rejected or no-replacement items not already listed as verification-required, every instruction id, every non-null replacement text, and provenance summaries. The Markdown file is the durable human-facing output of the loop; the chat response is not a substitute.

## Phase 8: Resolve Deterministic Output Paths

Use the same deterministic editing directory as the input drafted instructions:

- `artifacts/grants/<source-slug>/editing/`
- `artifacts/papers/<source-slug>/editing/`

Default loop outputs:

- `projected-revision-state.json`
- `edit-review-panel-report.json`
- `contextualized-edit-plan-v2.json`
- `drafted-edit-instructions-v2.json`
- `drafted-edit-recommendations-v2.md`

When preserving an existing loop, append or increment the same version number:

- `projected-revision-state-v3.json`
- `edit-review-panel-report-v3.json`
- `contextualized-edit-plan-v3.json`
- `drafted-edit-instructions-v3.json`
- `drafted-edit-recommendations-v3.md`

Do not write PAP or paper-code loop artifacts.

## Phase 9: Validate Before Stopping

Before reporting success:

1. Re-open every saved artifact and verify it parses as JSON.
2. Confirm every saved artifact uses the same `document_type` and `source_document_path`.
3. Confirm projected state and panel report contain all top-level fields required by their schemas.
4. Confirm no artifact claims source rewriting, tracked changes, or source-document patching.
5. Confirm the panel report is advisory and points to the next authoritative contextualized plan when another iteration is recommended.
6. If versioned artifacts are produced, confirm the contextualized plan contains iteration fields and the drafted instructions point to that contextualized plan.
7. If versioned drafted instructions are produced, confirm the matching `drafted-edit-recommendations-vN.md` exists, names every instruction id, and contains every non-null `replacement_text`.
8. Confirm artifact paths remain inside the deterministic grant or paper editing directory.
9. Confirm no source documents were modified.
10. Fix malformed artifacts before stopping.

## Phase 10: Report Back

After saving and validating, report:

1. the projected revision state path
2. the edit-review panel report path
3. any versioned contextualized plan path
4. any versioned drafted instructions path
5. any versioned human-readable recommendations path
6. the source document path
7. the document family
8. how many drafted instructions were reviewed
9. the panel recommendation
10. which issues were accepted, revised, rejected, or left for human verification
11. any remaining uncertainty for final human source editing

## Non-Scope And Guardrails

This skill must not:

- produce the first-pass `revision-plan.json`
- produce `writing-constraints.json`
- produce a first-pass contextualized plan or first-pass drafted instructions
- rewrite source documents directly
- create tracked changes
- support PAP or paper-code loops before representative artifacts and validation exist
- sync plugin-bundled skill copies unless a separate handoff authorizes plugin sync
- change schemas to make one loop run easier
