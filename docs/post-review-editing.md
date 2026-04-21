# Post-Review Editing Architecture

## Purpose

This document defines the planned post-review editing pipeline for this repo.

The core design goal is to turn review output into actionable revision guidance without collapsing diagnosis, constraint handling, document-context reasoning, and drafting into one opaque step.

This architecture is intended to work across:

- grant proposals
- papers
- pre-analysis plans
- paper-plus-code review packages

## Design Principle

Post-review editing should be a staged workflow.

One generic editor is too blunt because the repo reviews several different objects with different structural rules, constraints, and context needs. At the same time, the pipeline should not duplicate the same normalization logic separately for grants, papers, PAPs, and code-linked papers.

The intended architecture is:

- one shared revision-planning core
- one shared constraints contract
- one object-specific contextualization layer
- one object-specific drafting layer

## Pipeline Overview

The planned editing flow has four phases.

### 1. `plan-revisions`

Translate one or more review reports into normalized revision targets.

This phase is cross-cutting. It should work after any review type and should not require full local rewriting yet.

Its output is a structured artifact that answers:

- what the issue is
- how severe it is
- which review finding triggered it
- what type of revision is needed
- where the likely edit belongs
- why the change matters

### 2. `load-writing-constraints`

Load the writing rules that govern the next edit pass.

This phase is also cross-cutting, but its extraction logic depends on object type and available materials. It should capture both explicit constraints and high-confidence inferred constraints when the source format does not declare them cleanly.

Examples:

- page or word limits
- required sections
- ordering rules
- audience and tone
- citation or formatting conventions
- call-specific sponsor language
- journal or registry expectations
- non-negotiable truth constraints

### 3. `contextualize-revisions-<object>`

Map abstract revision targets onto the actual source document and its local dependencies.

This phase is object-specific because location models differ:

- a grant may care about named sections, page limits, and sponsor-facing framing
- a paper may care about title, abstract, introduction, methods, results, discussion, appendices, and claim propagation
- a PAP may care about hypotheses, outcomes, estimands, identification, power, and decision rules
- a paper-code package may care about alignment between manuscript claims, appendices, figures, and code or reproducibility assets

This phase determines:

- exact target location
- nearby text or section context
- whether the edit is local or must propagate elsewhere
- whether the proposed revision conflicts with constraints
- whether the edit is feasible without unsupported new claims

### 4. `draft-edits-<object>`

Produce executable edit suggestions.

This phase should draft concrete actions only after revision planning, constraints loading, and contextualization are complete.

Depending on workflow maturity, it may output:

- edit instructions only
- insertion text
- replacement text
- deletion or compression proposals
- patch-like suggestions for local files

## Why The Pipeline Is Split

The split is deliberate.

`plan-revisions` works on review findings.
`contextualize-revisions-<object>` works on source text and structural dependencies.
`draft-edits-<object>` works on wording and local fit.

If these are merged too early, the system becomes harder to validate because it is no longer clear whether a bad edit came from:

- a poor review diagnosis
- a missed constraint
- bad location mapping
- weak drafting

The staged design keeps each failure mode inspectable.

## Shared Artifact Contract

The editing pipeline should be driven by explicit artifacts, not only transient chat state.

The minimum planned artifacts are:

- a normalized feedback plan artifact for feedback-addressed workflows
- a revision plan artifact
- a writing constraints artifact
- a contextualized edit plan artifact
- a drafted edit instructions artifact

Canonical schemas for these artifacts now live under `templates/editing/`:

- `templates/editing/normalized-feedback-plan.schema.json`
- `templates/editing/revision-plan.schema.json`
- `templates/editing/writing-constraints.schema.json`
- `templates/editing/contextualized-edit-plan.schema.json`
- `templates/editing/drafted-edit-instructions.schema.json`

### Feedback-Addressed Editing Entry Layer

Generalized feedback-addressed editing is specified separately in `docs/feedback-addressed-editing.md`.

That architecture treats DOCX comments, PDF annotations, review reports, inline notes, and direct user instructions as adapter inputs into a shared `normalized-feedback-plan.json` contract. The normalized feedback layer supports single, subset, and all-feedback selection modes, records guideline appraisal states, and then maps selected feedback into revision-plan-compatible targets.

The downstream post-review editing stages remain unchanged: writing constraints are still loaded explicitly, object-specific contextualizers still decide source-local placement, and drafting stages still emit human-applied edit instructions rather than rewriting source documents directly.

The first implemented feedback-addressed planning path is:

- `Skills/plan-feedback-revisions.md`
- `Skills/convert-feedback-plan-to-revision-plan.md`

`plan-feedback-revisions` defines the DOCX-comment adapter path into `normalized-feedback-plan.json`, with representative validation artifacts for `single` and `all` comment selection under `artifacts/grants/benrimoh-research-vision/editing/`. `convert-feedback-plan-to-revision-plan` bridges those normalized feedback artifacts into schema-compatible `revision-plan.json` and `revision-plan-v2.json` artifacts for the same fixture. Both stages stop before writing constraints, contextualization, drafting, tracked changes, or source-document rewriting. A separate bounded validation chain now demonstrates that the selected single-comment `FB2` revision plan can be consumed by the existing downstream grant editing stages while preserving `FB2`, DOCX comment id `1`, and `F1 -> R1` target continuity.

### Revision Plan Artifact

This is the output of `plan-revisions`.

Suggested shape:

```json
{
  "artifact_version": "1.0",
  "document_type": "grant|paper|pap|paper-code",
  "source_document_path": "path/to/source",
  "review_paths": [
    "path/to/review-1.md"
  ],
  "revision_targets": [
    {
      "id": "R1",
      "priority": "critical",
      "issue": "The identification strategy is underspecified.",
      "edit_intent": "clarify",
      "motivation": "This weakens reviewer confidence in causal credibility.",
      "source_evidence": [
        {
          "review_path": "path/to/review-1.md",
          "section": "Required Revisions",
          "quote_or_summary": "Specify assumptions and robustness checks."
        }
      ],
      "candidate_locations": [
        {
          "section_hint": "Methods",
          "reason": "This is where identification is introduced."
        }
      ]
    }
  ]
}
```

Contract notes:

- `document_type` must be one of `grant`, `paper`, `pap`, or `paper-code`
- `review_paths` must enumerate the exact review artifacts used to build the plan
- `revision_targets` is required and each target must carry explicit `source_evidence` plus at least one `candidate_location`
- `edit_intent` is normalized into a finite set so downstream contextualizers can branch deterministically

### Writing Constraints Artifact

This is the output of `load-writing-constraints`.

Suggested shape:

```json
{
  "artifact_version": "1.0",
  "document_type": "grant|paper|pap|paper-code",
  "source_document_path": "path/to/source",
  "constraints": {
    "length_limits": [],
    "required_sections": [],
    "ordering_rules": [],
    "style_requirements": [],
    "audience": "",
    "hard_constraints": [],
    "soft_preferences": []
  },
  "constraint_sources": []
}
```

Contract notes:

- constraints are split into explicit buckets rather than a single free-text block
- `constraint_sources` is required and records provenance for each explicit or inferred rule
- the schema treats `hard_constraints` and `soft_preferences` separately so later drafting stages can distinguish must-follow rules from style preferences

### Contextualized Edit Plan Artifact

This is the output of `contextualize-revisions-<object>`.

Suggested shape:

```json
{
  "artifact_version": "1.0",
  "document_type": "grant|paper|pap|paper-code",
  "source_document_path": "path/to/source",
  "revision_targets": [
    {
      "id": "R1",
      "priority": "critical",
      "issue": "The identification strategy is underspecified.",
      "location": {
        "section": "Methods",
        "heading_match": "Identification Strategy",
        "paragraph_hint": "opening paragraph"
      },
      "suggestion": "Add 3 to 5 sentences naming assumptions, threats, and planned robustness checks.",
      "motivation": "This directly addresses the methods-credibility concern raised by the review.",
      "dependencies": [
        "Check consistency with abstract and limitations section."
      ],
      "constraint_checks": [
        "No new empirical result should be introduced."
      ],
      "source_evidence": []
    }
  ]
}
```

Contract notes:

- every contextualized target must point back to both the saved revision plan and the saved writing constraints artifact
- `location.section` is required even when finer-grained location hints are unavailable
- `constraint_checks` is required so the drafting layer can see what was already verified before wording is proposed

### Drafted Edit Instructions Artifact

This is the output of `draft-edits-<object>`.

Suggested shape:

```json
{
  "artifact_version": "1.0",
  "document_type": "grant|paper|pap|paper-code",
  "source_document_path": "path/to/source",
  "contextualized_edit_plan_path": "path/to/contextualized-edit-plan.json",
  "edit_instructions": [
    {
      "id": "R1",
      "priority": "critical",
      "location": {
        "section": "Expected Outcomes"
      },
      "editorial_judgment": {
        "status": "accept|partial|reject|verify",
        "rationale": "Why this review suggestion should be implemented, narrowed, rejected, or verified.",
        "review_suggestion_addressed": "Concise summary of the review suggestion.",
        "human_decision_needed": false
      },
      "action_type": "insert",
      "edit_instruction": "In Q19a, replace the existing answer with the replacement text below.",
      "source_text": "The current field text or enough exact source text to identify the field.",
      "replacement_text": "Paste-ready replacement text, or null only for deletion, rejection, or verification actions.",
      "word_count_check": {
        "limit": 100,
        "unit": "words",
        "replacement_count": 74,
        "within_limit": true,
        "notes": "Recheck in the live form if its counter handles punctuation differently."
      },
      "constraint_checks": [],
      "provenance": {}
    }
  ]
}
```

Contract notes:

- every drafted instruction must point back to the saved contextualized edit plan
- `edit_instruction` is required even when `replacement_text` is `null`
- `editorial_judgment` is required so the editor records which review suggestions were accepted, narrowed, rejected, or left for factual verification
- `source_text` should quote the exact current field text when available, or a uniquely identifying excerpt when the full field is long
- `replacement_text` must be paste-ready for accepted or partially accepted text edits, except deletion-only edits
- `word_count_check` is required for every instruction and must report the known field limit when available
- `replacement_text` must not introduce unsupported new facts, methods, partners, budgets, outcomes, or claims
- drafting artifacts propose human-applied edits and do not modify source documents directly

## Deterministic Output Locations

Shared editing artifacts should save under `artifacts/<object-folder>/<source-slug>/editing/` rather than next to the canonical skill or schema files.

The deterministic layout is:

- `artifacts/grants/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/grants/<source-slug>/editing/revision-plan.json`
- `artifacts/grants/<source-slug>/editing/writing-constraints.json`
- `artifacts/grants/<source-slug>/editing/contextualized-edit-plan.json`
- `artifacts/grants/<source-slug>/editing/drafted-edit-instructions.json`
- `artifacts/papers/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/papers/<source-slug>/editing/revision-plan.json`
- `artifacts/papers/<source-slug>/editing/writing-constraints.json`
- `artifacts/papers/<source-slug>/editing/contextualized-edit-plan.json`
- `artifacts/papers/<source-slug>/editing/drafted-edit-instructions.json`
- `artifacts/paps/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/paps/<source-slug>/editing/revision-plan.json`
- `artifacts/paps/<source-slug>/editing/writing-constraints.json`
- `artifacts/paps/<source-slug>/editing/contextualized-edit-plan.json`
- `artifacts/paps/<source-slug>/editing/drafted-edit-instructions.json`
- `artifacts/paper-code/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/paper-code/<source-slug>/editing/revision-plan.json`
- `artifacts/paper-code/<source-slug>/editing/writing-constraints.json`
- `artifacts/paper-code/<source-slug>/editing/contextualized-edit-plan.json`
- `artifacts/paper-code/<source-slug>/editing/drafted-edit-instructions.json`

Naming rules:

- `<source-slug>` is derived from the source document being revised, not from the review report filename
- the object folder must match the normalized `document_type`
- if an artifact for the same source already exists and should be preserved, append `-v2`, `-v3`, and so on to the artifact filename
- downstream stages should consume the latest explicit artifact path rather than infer state from chat context alone

This keeps the staged pipeline inspectable because all intermediate artifacts for one source live in one stable directory.

## Object-Specific Adapters

The shared phases should not erase domain differences.

### Grants

Grant-specific contextualization should be sensitive to:

- sponsor language mirroring
- page or section caps
- required call components
- theory-of-change or public-impact framing
- consistency across narrative, workplan, budget, and team story

Likely object-specific edit intents:

- align with sponsor priorities
- surface required component earlier
- tighten feasibility story
- reduce scope inflation
- improve public-benefit legibility

### Papers

Paper-specific contextualization should be sensitive to:

- venue norms
- title and abstract compression
- introduction and literature-positioning logic
- alignment between claims, methods, results, and discussion
- where a change implies updates in multiple sections

Likely object-specific edit intents:

- qualify claims
- sharpen contribution statement
- add missing methodological justification
- reframe novelty relative to prior work
- reduce overclaiming

### PAPs

PAP-specific contextualization should be sensitive to:

- estimands and hypotheses
- outcome definitions
- identification and robustness plans
- sample, power, and exclusion rules
- registration compliance and non-analytic flexibility

Likely object-specific edit intents:

- specify decision rules
- operationalize outcomes
- tighten estimand language
- resolve ambiguity in robustness commitments

### Paper-Code Packages

Paper-code contextualization should be sensitive to:

- manuscript-to-code consistency
- experiment traceability
- figure or table provenance
- reproducibility promises
- missing documentation or run instructions

Likely object-specific edit intents:

- narrow unsupported reproducibility claims
- add missing implementation details
- connect manuscript claims to released assets
- correct mismatch between reported and runnable pipeline

## Constraints Are First-Class

The editing pipeline should never assume that the review alone is sufficient to guide rewriting.

Many edit failures happen because the system ignores constraints such as:

- strict page or word limits
- forbidden structural changes
- call-mandated headings
- journal abstract limits
- registry-required fields
- truth constraints such as "do not add unsupported empirical claims"

For this reason, `load-writing-constraints` is not optional architecture. It is a required phase.

## Shared Stage Specifications

The canonical shared-stage workflow specifications now live in:

- `Skills/plan-feedback-revisions.md`
- `Skills/convert-feedback-plan-to-revision-plan.md`
- `Skills/plan-revisions.md`
- `Skills/load-writing-constraints.md`
- `Skills/contextualize-revisions-grant.md`
- `Skills/draft-edits-grant.md`
- `Skills/contextualize-revisions-paper.md`
- `Skills/draft-edits-paper.md`

These are specification-layer contracts for:

- required inputs
- deterministic output paths under `artifacts/<object-folder>/<source-slug>/editing/`
- schema conformance requirements
- provenance and normalization rules
- explicit non-scope boundaries that keep shared stages separate from object-specific contextualization and drafting

They now also encode the shared runtime fallback behavior needed for bounded execution:

- deterministic slugification from the source-document filename
- deterministic `-vN` versioning when an artifact must be preserved
- explicit fallback behavior when direct source extraction is unavailable locally

They do not claim that plugin sync, PAP editing, or paper-code editing paths are already implemented.

## First Grant Contextualization Path

The first object-specific contextualization workflow now lives in:

- `Skills/contextualize-revisions-grant.md`

It consumes saved `revision-plan.json` and `writing-constraints.json` artifacts for one grant source document and emits:

- `artifacts/grants/<source-slug>/editing/contextualized-edit-plan.json`

The grant contextualizer localizes revision targets to grant-facing sections, records constraint checks, and preserves review evidence. It intentionally stops before drafting replacement text. Plugin-bundled copies for the paper contextualizer and PAP or paper-code contextualizers are not yet implemented.

## First Grant Drafting Path

The first object-specific drafting workflow now lives in:

- `Skills/draft-edits-grant.md`

It consumes a saved grant `contextualized-edit-plan.json` and emits:

- `artifacts/grants/<source-slug>/editing/drafted-edit-instructions.json`

The grant drafter turns contextualized targets into human-applied edit instructions, with bounded proposed text where the existing artifact evidence supports wording. It does not rewrite the source grant file directly. Plugin-bundled copies and non-grant drafting skills are not yet implemented.

For grant applications, the expected user-facing output is not a parallel rewritten proposal. It is a replacement manual: for each grant prompt or paragraph, the editor should state what review suggestion it is acting on, whether that suggestion is accepted or rejected, what exact current text is being replaced when recoverable, what exact replacement should be pasted, and whether the replacement stays inside the known word or character limit.

## First Paper Contextualization Path

The first paper-specific contextualization workflow now lives in:

- `Skills/contextualize-revisions-paper.md`

It consumes saved paper `revision-plan.json` and `writing-constraints.json` artifacts for one source manuscript and emits:

- `artifacts/papers/<source-slug>/editing/contextualized-edit-plan.json`

The paper contextualizer localizes revision targets to manuscript-facing sections, records constraint checks, and preserves review evidence. It intentionally stops before drafting replacement text. The representative validation path uses the local Communications Psychology fixture under:

- `artifacts/papers/s44271-024-00170-w/editing/`

Paper drafting is handled by a separate downstream workflow. Plugin-bundled copies, PAP contextualizers, and paper-code contextualizers are not yet implemented.

## First Paper Drafting Path

The first paper-specific drafting workflow now lives in:

- `Skills/draft-edits-paper.md`

It consumes a saved paper `contextualized-edit-plan.json` and emits:

- `artifacts/papers/<source-slug>/editing/drafted-edit-instructions.json`

The paper drafter turns contextualized manuscript targets into human-applied edit instructions for claim qualification, methods clarity, results/discussion alignment, and venue-facing framing. It does not rewrite the source manuscript directly. The representative validation path uses:

- `artifacts/papers/s44271-024-00170-w/editing/drafted-edit-instructions.json`

Plugin-bundled copies, PAP drafting, and paper-code drafting are not yet implemented.

## Recommended User-Facing Shape

The internal pipeline should stay modular even if the user-facing surface is simpler.

A reasonable future surface is:

- `plan-revisions`
- `load-writing-constraints`
- `contextualize-revisions-grant`
- `contextualize-revisions-paper`
- `contextualize-revisions-pap`
- `contextualize-revisions-paper-code`
- `draft-edits-grant`
- `draft-edits-paper`
- `draft-edits-pap`
- `draft-edits-paper-code`

The repo may later expose higher-level composite workflows per object type, but those workflows should call the same underlying staged logic rather than reimplement it.

## Recommended Implementation Order

The intended order is:

1. define the shared revision-plan artifact
2. define the shared writing-constraints artifact
3. implement `plan-revisions`
4. implement `load-writing-constraints`
5. implement grant and paper contextualizers
6. implement grant and paper drafting skills
7. extend to PAP and paper-code contextualizers
8. add validation fixtures and deterministic output rules

This order minimizes premature complexity while preserving the right abstraction boundary.

## Current Status

This document is an architecture target, not a claim that the full editing pipeline is already implemented.

At the current phase state:

- review workflows already exist
- grant review planning already exists
- canonical shared-stage specs now exist for:
  - `plan-feedback-revisions`
  - `plan-revisions`
  - `load-writing-constraints`
- canonical grant contextualization now exists for:
  - `contextualize-revisions-grant`
- canonical grant drafting now exists for:
  - `draft-edits-grant`
- canonical paper contextualization now exists for:
  - `contextualize-revisions-paper`
- canonical paper drafting now exists for:
  - `draft-edits-paper`
- representative shared-stage runtime artifacts now exist for one grant validation path under `artifacts/grants/google-impact-challenge-ai-for-science-application/editing/`
- representative DOCX-comment normalized feedback artifacts now exist under `artifacts/grants/benrimoh-research-vision/editing/`
- representative DOCX-comment compatibility revision-plan artifacts now exist under `artifacts/grants/benrimoh-research-vision/editing/`
- representative feedback-derived downstream validation artifacts for the Benrimoh single-comment `FB2` path now exist under `artifacts/grants/benrimoh-research-vision/editing/`
- representative grant contextualization runtime evidence now exists for that same validation path
- representative grant drafting runtime evidence now exists for that same validation path
- representative paper contextualization runtime evidence now exists under `artifacts/papers/s44271-024-00170-w/editing/`
- representative paper drafting runtime evidence now exists under `artifacts/papers/s44271-024-00170-w/editing/`
- PAP editing and paper-code editing skills are not yet implemented
