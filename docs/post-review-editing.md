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

The planned editing flow has four core phases, followed by an optional post-draft review iteration loop when the drafted instructions need quality checking before human application.

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

### 5. Post-Draft Edit Review Iteration

Evaluate the candidate revised document state implied by `drafted-edit-instructions.json` before treating the edit pass as ready for human application.

This loop is part of the editing subsystem. It is not a SUPLEX governance loop, and it does not make reviewer-agent output authoritative by itself. The authoritative next planning artifact, when another iteration is warranted, is a versioned contextualized edit plan such as `contextualized-edit-plan-v2.json`.

The loop sequence is:

```text
drafted-edit-instructions.json
-> projected-revision-state.json
-> edit-review-panel-report.json
-> contextualized-edit-plan-v2.json
-> drafted-edit-instructions-v2.json
-> drafted-edit-recommendations-v2.md
```

Later iterations use the same pattern with `-v3`, `-v4`, and so on. The loop stops when the projected state passes local and global checks, when remaining issues require human verification rather than another automated edit pass, or when further iteration would overfit reviewer preferences at the expense of the document's overall purpose.

### Object-Family Support Matrix

Support status is tracked separately for review, shared editing stages, object-specific contextualization and drafting, the post-draft edit-review loop, representative validation artifacts, and plugin exposure. This prevents user-facing docs and plugin metadata from implying that one validated family means all families are implemented.

| Object family | Review support | Shared editing-stage support | Contextualize/draft support | Post-draft edit-review loop support | Representative validation artifacts | Plugin exposure status | Deferred or unsupported boundaries |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Grants | Implemented through `review-grant`, with grant-context and review-plan support. | Implemented for `plan-revisions`, `load-writing-constraints`, DOCX-comment feedback planning, and feedback-plan conversion. | Implemented through `contextualize-revisions-grant` and `draft-edits-grant`. | Implemented as a canonical `review-drafted-edits` loop for validated grant editing chains. | Representative Google.org grant loop artifacts exist under `artifacts/grants/google-impact-challenge-ai-for-science-application/editing/`; feedback-derived Benrimoh downstream artifacts exist under `artifacts/grants/benrimoh-research-vision/editing/`. | Existing plugin exposes review, planning, contextualization, drafting, and `review-drafted-edits` loop skills for validated grant chains. | No source-document rewrite, tracked changes, live-form patching, or unsupported new sponsor/budget/partner facts. |
| Papers | Implemented through `review-paper` and `review-paper-light`. | Implemented for `plan-revisions` and `load-writing-constraints`. | Implemented through `contextualize-revisions-paper` and `draft-edits-paper`. | Implemented as a canonical `review-drafted-edits` loop for validated paper editing chains. | Representative Communications Psychology paper loop artifacts exist under `artifacts/papers/s44271-024-00170-w/editing/`. | Existing plugin exposes review, planning, contextualization, drafting, and `review-drafted-edits` loop skills for validated paper chains. | No source-manuscript rewrite, tracked changes, TeX/Markdown/PDF patching, or unsupported new analyses, citations, results, or journal claims. |
| PAPs | Implemented for review through `review-pap`. | Shared `plan-revisions` and `load-writing-constraints` contracts allow `document_type = pap`, but no representative PAP editing chain has been validated. | Deferred; no canonical PAP contextualizer or PAP drafter exists. | Deferred; `review-drafted-edits` must stop rather than run on PAP artifacts. | None for PAP edit-review loops. | Review skill may be plugin-exposed; editing-loop support is not plugin-exposed. | Do not claim PAP edit-review loop support until PAP contextualization, drafting, loop artifacts, and validation exist. |
| Paper-code | Implemented for review through `review-paper-code`. | Shared `plan-revisions` and `load-writing-constraints` contracts allow `document_type = paper-code`, but no representative paper-code editing chain has been validated. | Deferred; no canonical paper-code contextualizer or paper-code drafter exists. | Deferred; `review-drafted-edits` must stop rather than run on paper-code artifacts. | None for paper-code edit-review loops. | Review skill may be plugin-exposed; editing-loop support is not plugin-exposed. | Do not claim paper-code edit-review loop support until manuscript-code alignment contextualization, drafting, loop artifacts, and validation exist. |

### Canonical Loop Skill Surface

The canonical user-invoked surface for the post-draft loop is:

- `Skills/review-drafted-edits.md`

This is a single generic loop skill with an explicit family gate. It supports grants and papers because those families have contextualization, drafting, projected-state, panel-report, versioned-plan, versioned-drafting, and focused validation evidence. It refuses PAP and paper-code loop execution until those families have their own representative contextualization, drafting, loop artifacts, and validation.

The skill consumes a saved `drafted-edit-instructions.json` or versioned drafted artifact, resolves the prior contextualized plan and upstream artifacts, emits `projected-revision-state.json` and `edit-review-panel-report.json`, and emits versioned `contextualized-edit-plan-vN.json` plus `drafted-edit-instructions-vN.json` and `drafted-edit-recommendations-vN.md` when another automated iteration is warranted. It does not replace `plan-revisions`, `load-writing-constraints`, `contextualize-revisions-<object>`, or `draft-edits-<object>`; it starts only after a first drafted-instructions artifact exists.

The plugin bundle now includes this canonical skill through the derivation allowlist. Plugin docs and metadata should describe `review-drafted-edits` as plugin-exposed for validated grant and paper drafted edit instructions only, with PAP and paper-code loop paths still deferred.

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
- a human-readable drafted edit recommendations artifact

Canonical schemas for these artifacts now live under `templates/editing/`:

- `templates/editing/normalized-feedback-plan.schema.json`
- `templates/editing/revision-plan.schema.json`
- `templates/editing/writing-constraints.schema.json`
- `templates/editing/contextualized-edit-plan.schema.json`
- `templates/editing/drafted-edit-instructions.schema.json`
- `templates/editing/projected-revision-state.schema.json`
- `templates/editing/edit-review-panel-report.schema.json`

The two post-draft loop schemas are formal contracts for the shared iteration artifacts. `projected-revision-state.schema.json` validates the projected state as review evidence and requires explicit no-source-rewrite and no-tracked-changes boundary fields. `edit-review-panel-report.schema.json` validates advisory panel output and requires source, drafted-instruction, projected-state, assessment, recommendation, and advisory-only provenance.

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

Each `drafted-edit-instructions*.json` artifact must have a same-version `drafted-edit-recommendations*.md` companion. The JSON remains the machine-validated contract; the Markdown companion is the durable human-facing replacement manual. A workflow that reports completion without this readable recommendations document is incomplete, even if the JSON validates.

### Projected Revision State Artifact

This is the first artifact in the post-draft edit review loop.

The artifact represents the document state implied by applying `drafted-edit-instructions.json`; it does not directly rewrite a source PDF, DOCX, TeX file, Markdown manuscript, live grant form, or other canonical source document. For form-style grants, PDF sources, and other hard-to-patch formats, the projection may be a structured field-by-field or section-by-section representation rather than literal rebuilt source text.

Minimum contract:

- `artifact_version`
- `document_type`
- `source_document_path`
- `drafted_edit_instructions_path`
- `contextualized_edit_plan_path`
- `generated_at`
- `projection_mode`: `structured-field`, `structured-section`, `text-excerpt`, or another documented mode
- `baseline_references`: source paths, field labels, section names, or excerpts used to identify the baseline state
- `applied_instruction_map`: one entry per drafted instruction, including instruction id, target id, action type, projected local result, and whether application was complete, partial, rejected, or verification-blocked
- `unresolved_items`: instructions that could not be safely projected, with the reason and needed human check
- `source_local_uncertainties`: anchoring, extraction, live-form, or formatting uncertainties that affect review confidence
- `projection_notes`: concise notes on what the projection can and cannot support

The projected state is review evidence, not a patched source document. It must preserve provenance to the drafted instructions and prior contextualized plan so later iterations can explain which projected changes are being accepted, revised, or rolled back.

### Edit Review Panel Report Artifact

This is the advisory review artifact produced from the projected state.

The panel should reuse the standards, lenses, and review behavior of the existing grant and paper review workflows where appropriate. Grant edit review should borrow sponsor fit, feasibility, public impact, compliance, team, budget, internal consistency, and adversarial-panel concerns from `review-grant`. Paper edit review should borrow contribution, claim discipline, methods credibility, internal consistency, tables/figures, style, and target-journal fit concerns from `review-paper`.

The edit-review panel adds delta analysis: it compares the baseline source evidence, the drafted edit instructions, and the projected revised state. Its job is to judge whether the edit pass improved the document, introduced new risks, or left the highest-priority concerns unresolved.

Minimum contract:

- `artifact_version`
- `document_type`
- `source_document_path`
- `projected_revision_state_path`
- `drafted_edit_instructions_path`
- `baseline_reference_paths`
- `review_standard`: grant sponsor archetype, saved grant profile/review plan, target journal, or general paper standard used for the review
- `panel_lenses`: reviewer lenses run, including any omitted lenses and why
- `local_assessments`: target-level checks tied to drafted instruction ids and contextualized target ids
- `global_assessment`: document-level judgment of the projected revised state
- `recommended_dispositions`: accept, revise, reject, verify, or stop for each material issue
- `evidence_for_next_plan`: reviewer evidence that should feed the next contextualized edit plan if another iteration is needed
- `stop_condition_recommendation`: accept current drafted instructions, loop to a new contextualized plan, or escalate to human verification

Reviewer output is advisory evidence. It should not become a separate authoritative decision plan and should not override source evidence, writing constraints, or editorial judgment without being folded into the next contextualized edit plan.

### Local And Global Optimization

The loop evaluates edit quality at two levels.

Local optimization checks each drafted target:

- whether the proposed action addresses the specific review or feedback concern it claims to address
- whether the target location is still the smallest credible location after projection
- whether replacement or insertion text fits local wording, section purpose, field limits, and known constraints
- whether the edit preserves target id continuity, feedback provenance, review evidence, and source anchors
- whether the edit introduces unsupported facts, analyses, methods, partners, budgets, citations, outcomes, or claims
- whether dependencies and propagation targets were handled rather than left inconsistent
- whether uncertain source placement or live-form behavior should be marked `verify`

Global optimization checks the projected document as a whole:

- for grants: fundability, sponsor fit, public-benefit legibility, feasibility, operational credibility, budget/team coherence, compliance signals, and strategic clarity
- for papers: publishability, contribution framing, claim discipline, methods credibility, journal fit, abstract/body alignment, results/discussion consistency, and table/figure support
- for all document types: narrative coherence, cross-section consistency, truthfulness, constraint compliance, reviewer confidence, and the risk that item-by-item edits have weakened the overall document

The global assessment can reject or narrow a locally plausible edit when it damages the document's overall strategy, overfits one reviewer preference, duplicates higher-priority material, or crowds out required content.

### Contextualized Plan Iteration

When the edit-review panel recommends another pass, its evidence is folded into `contextualized-edit-plan-v2.json`.

The versioned contextualized plan remains the authoritative next planning artifact. It should preserve the existing contextualized-plan contract and add schema-adjacent iteration fields in a future specification or schema pass as needed, including:

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

The current validation decision is schema-compatible and backward-compatible: `templates/editing/contextualized-edit-plan.schema.json` allows these iteration fields as optional top-level properties, so first-version contextualized plans remain valid while `contextualized-edit-plan-v2.json` can carry review-loop provenance. `templates/editing/drafted-edit-instructions.schema.json` does not need new top-level iteration fields because `drafted-edit-instructions-v2.json` records the versioned contextualized plan path at the top level and keeps prior-plan, projected-state, and panel-report provenance inside each instruction's existing `provenance` object. The focused runtime validation suite checks both decisions against the Google.org grant loop artifacts.

Target ids should remain stable when the same underlying concern continues across iterations. New ids should be introduced only for genuinely new concerns discovered by the edit review. The next drafted artifact should point to the versioned contextualized plan that produced it, for example:

```text
contextualized-edit-plan-v2.json -> drafted-edit-instructions-v2.json
contextualized-edit-plan-v3.json -> drafted-edit-instructions-v3.json
```

### Stop Conditions

The post-draft loop should stop with `accept current drafted instructions` when:

- all critical local checks pass or are explicitly marked for human verification
- no global assessment identifies a material loss in fundability, publishability, coherence, fit, or truthfulness
- remaining issues are minor polishing issues that do not justify another full iteration
- the drafted instructions remain human-applied and do not imply direct source rewriting

The loop should continue to `contextualized-edit-plan-vN.json` when:

- a drafted edit only partially addresses a high-priority concern
- projection reveals a conflict with constraints, section purpose, or source-local evidence
- multiple locally reasonable edits create a global coherence, fit, or consistency problem
- reviewer evidence identifies a better target location or narrower action
- a rejected or narrowed reviewer suggestion needs an explicit traceable rationale in the next plan

The loop should escalate to human verification when:

- the projected state depends on inaccessible live-form behavior, unrecoverable PDF/DOCX anchors, missing source text, or unavailable factual confirmation
- the edit would require new empirical analyses, partner commitments, budget facts, citations, or administrative details
- reviewer standards conflict in a way that cannot be resolved from source evidence and writing constraints alone
- further automated iteration would likely overfit reviewer preferences or obscure the human editor's responsibility for final source changes

## Deterministic Output Locations

Shared editing artifacts should save under `artifacts/<object-folder>/<source-slug>/editing/` rather than next to the canonical skill or schema files.

The deterministic layout is:

- `artifacts/grants/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/grants/<source-slug>/editing/revision-plan.json`
- `artifacts/grants/<source-slug>/editing/writing-constraints.json`
- `artifacts/grants/<source-slug>/editing/contextualized-edit-plan.json`
- `artifacts/grants/<source-slug>/editing/drafted-edit-instructions.json`
- `artifacts/grants/<source-slug>/editing/drafted-edit-recommendations.md`
- `artifacts/grants/<source-slug>/editing/projected-revision-state.json`
- `artifacts/grants/<source-slug>/editing/edit-review-panel-report.json`
- `artifacts/grants/<source-slug>/editing/contextualized-edit-plan-v2.json`
- `artifacts/grants/<source-slug>/editing/drafted-edit-instructions-v2.json`
- `artifacts/grants/<source-slug>/editing/drafted-edit-recommendations-v2.md`
- `artifacts/papers/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/papers/<source-slug>/editing/revision-plan.json`
- `artifacts/papers/<source-slug>/editing/writing-constraints.json`
- `artifacts/papers/<source-slug>/editing/contextualized-edit-plan.json`
- `artifacts/papers/<source-slug>/editing/drafted-edit-instructions.json`
- `artifacts/papers/<source-slug>/editing/drafted-edit-recommendations.md`
- `artifacts/papers/<source-slug>/editing/projected-revision-state.json`
- `artifacts/papers/<source-slug>/editing/edit-review-panel-report.json`
- `artifacts/papers/<source-slug>/editing/contextualized-edit-plan-v2.json`
- `artifacts/papers/<source-slug>/editing/drafted-edit-instructions-v2.json`
- `artifacts/papers/<source-slug>/editing/drafted-edit-recommendations-v2.md`
- `artifacts/paps/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/paps/<source-slug>/editing/revision-plan.json`
- `artifacts/paps/<source-slug>/editing/writing-constraints.json`
- `artifacts/paps/<source-slug>/editing/contextualized-edit-plan.json`
- `artifacts/paps/<source-slug>/editing/drafted-edit-instructions.json`
- `artifacts/paps/<source-slug>/editing/drafted-edit-recommendations.md`
- `artifacts/paps/<source-slug>/editing/projected-revision-state.json`
- `artifacts/paps/<source-slug>/editing/edit-review-panel-report.json`
- `artifacts/paps/<source-slug>/editing/contextualized-edit-plan-v2.json`
- `artifacts/paps/<source-slug>/editing/drafted-edit-instructions-v2.json`
- `artifacts/paps/<source-slug>/editing/drafted-edit-recommendations-v2.md`
- `artifacts/paper-code/<source-slug>/editing/normalized-feedback-plan.json`
- `artifacts/paper-code/<source-slug>/editing/revision-plan.json`
- `artifacts/paper-code/<source-slug>/editing/writing-constraints.json`
- `artifacts/paper-code/<source-slug>/editing/contextualized-edit-plan.json`
- `artifacts/paper-code/<source-slug>/editing/drafted-edit-instructions.json`
- `artifacts/paper-code/<source-slug>/editing/drafted-edit-recommendations.md`
- `artifacts/paper-code/<source-slug>/editing/projected-revision-state.json`
- `artifacts/paper-code/<source-slug>/editing/edit-review-panel-report.json`
- `artifacts/paper-code/<source-slug>/editing/contextualized-edit-plan-v2.json`
- `artifacts/paper-code/<source-slug>/editing/drafted-edit-instructions-v2.json`
- `artifacts/paper-code/<source-slug>/editing/drafted-edit-recommendations-v2.md`

Naming rules:

- `<source-slug>` is derived from the source document being revised, not from the review report filename
- the object folder must match the normalized `document_type`
- if an artifact for the same source already exists and should be preserved, append `-v2`, `-v3`, and so on to the artifact filename
- post-draft loop artifacts should use the same version number as the contextualized plan and drafted instructions for that iteration when preservation is required
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
- `Skills/review-drafted-edits.md`

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

They do not claim that PAP editing or paper-code editing paths are already implemented.

## First Grant Contextualization Path

The first object-specific contextualization workflow now lives in:

- `Skills/contextualize-revisions-grant.md`

It consumes saved `revision-plan.json` and `writing-constraints.json` artifacts for one grant source document and emits:

- `artifacts/grants/<source-slug>/editing/contextualized-edit-plan.json`

The grant contextualizer localizes revision targets to grant-facing sections, records constraint checks, and preserves review evidence. It intentionally stops before drafting replacement text. PAP and paper-code contextualizers are not yet implemented.

## First Grant Drafting Path

The first object-specific drafting workflow now lives in:

- `Skills/draft-edits-grant.md`

It consumes a saved grant `contextualized-edit-plan.json` and emits:

- `artifacts/grants/<source-slug>/editing/drafted-edit-instructions.json`
- `artifacts/grants/<source-slug>/editing/drafted-edit-recommendations.md`

The grant drafter turns contextualized targets into human-applied edit instructions, with bounded proposed text where the existing artifact evidence supports wording. It does not rewrite the source grant file directly. PAP and paper-code drafting skills are not yet implemented.

For grant applications, the expected user-facing output is not a parallel rewritten proposal. It is a replacement manual: for each grant prompt or paragraph, the editor should state what review suggestion it is acting on, whether that suggestion is accepted or rejected, what exact current text is being replaced when recoverable, what exact replacement should be pasted, and whether the replacement stays inside the known word or character limit.

## First Paper Contextualization Path

The first paper-specific contextualization workflow now lives in:

- `Skills/contextualize-revisions-paper.md`

It consumes saved paper `revision-plan.json` and `writing-constraints.json` artifacts for one source manuscript and emits:

- `artifacts/papers/<source-slug>/editing/contextualized-edit-plan.json`

The paper contextualizer localizes revision targets to manuscript-facing sections, records constraint checks, and preserves review evidence. It intentionally stops before drafting replacement text. The representative validation path uses the local Communications Psychology fixture under:

- `artifacts/papers/s44271-024-00170-w/editing/`

Paper drafting is handled by a separate downstream workflow. PAP and paper-code contextualizers are not yet implemented.

## First Paper Drafting Path

The first paper-specific drafting workflow now lives in:

- `Skills/draft-edits-paper.md`

It consumes a saved paper `contextualized-edit-plan.json` and emits:

- `artifacts/papers/<source-slug>/editing/drafted-edit-instructions.json`
- `artifacts/papers/<source-slug>/editing/drafted-edit-recommendations.md`

The paper drafter turns contextualized manuscript targets into human-applied edit instructions for claim qualification, methods clarity, results/discussion alignment, and venue-facing framing. It does not rewrite the source manuscript directly. The representative validation path uses:

- `artifacts/papers/s44271-024-00170-w/editing/drafted-edit-instructions.json`
- `artifacts/papers/s44271-024-00170-w/editing/drafted-edit-recommendations.md`

PAP drafting and paper-code drafting are not yet implemented.

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
- canonical post-draft edit-review loop support now exists for validated grant and paper editing chains through:
  - `review-drafted-edits`
- representative shared-stage runtime artifacts now exist for one grant validation path under `artifacts/grants/google-impact-challenge-ai-for-science-application/editing/`
- representative DOCX-comment normalized feedback artifacts now exist under `artifacts/grants/benrimoh-research-vision/editing/`
- representative DOCX-comment compatibility revision-plan artifacts now exist under `artifacts/grants/benrimoh-research-vision/editing/`
- representative feedback-derived downstream validation artifacts for the Benrimoh single-comment `FB2` path now exist under `artifacts/grants/benrimoh-research-vision/editing/`
- representative grant contextualization runtime evidence now exists for that same validation path
- representative grant drafting runtime evidence now exists for that same validation path
- representative paper contextualization runtime evidence now exists under `artifacts/papers/s44271-024-00170-w/editing/`
- representative paper drafting runtime evidence now exists under `artifacts/papers/s44271-024-00170-w/editing/`
- representative grant and paper post-draft loop artifacts now exist for the Google.org grant fixture and Communications Psychology paper fixture
- PAP editing and paper-code editing skills are not yet implemented
- PAP and paper-code edit-review loops are deferred and must not be claimed as implemented or plugin-exposed
