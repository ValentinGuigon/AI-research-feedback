---
description: Route natural-language editing requests to the existing staged post-review editing workflows
---

# Run Editing

You are the top-level editing orchestrator for this repository. Your job is to understand a user's editing request, discover the most relevant local editing artifacts, ask only the short question that blocks safe routing, and then delegate to an existing editing-stage skill.

This skill does not generate revision plans, writing constraints, contextualized plans, drafted instructions, human-readable recommendations, projected states, or edit-review reports directly. It does not rewrite source documents, create tracked changes, patch live forms, or overwrite artifacts. It routes to existing stage skills and preserves their contracts.

## Supported Editing Families

Supported routes:

- DOCX-comment or feedback-bearing source normalization: `plan-feedback-revisions`
- Normalized feedback conversion into a revision plan: `convert-feedback-plan-to-revision-plan`
- Review-report revision planning: `plan-revisions`
- Writing-constraint extraction: `load-writing-constraints`
- Grant contextualization: `contextualize-revisions-grant`
- Paper contextualization: `contextualize-revisions-paper`
- Grant drafting: `draft-edits-grant`
- Paper drafting: `draft-edits-paper`
- Post-draft edit-review loop for validated grant and paper chains: `review-drafted-edits`

Grant and paper editing chains are supported through the staged skills above. PAP and paper-code shared planning contracts may be routed only when the user explicitly asks for those shared artifacts. PAP and paper-code contextualization, drafting, and edit-review loop execution are unsupported and must stop.

## Operating Rules

1. Inspect explicit user inputs before searching broadly.
2. Treat explicit paths as primary evidence.
3. Discover local matching candidates and existing artifacts before asking avoidable questions.
4. Search the most advanced editing artifact first, then decide whether the user wants to continue, reuse, review, version, or stop.
5. Ask the smallest number of concise guided questions needed to route safely.
6. Preserve object-family boundaries and name the stage skill that should run next.
7. Preserve feedback selection mode; never expand a `single` or `subset` request into `all`.
8. Do not create artifacts directly, overwrite existing artifacts, rewrite sources, create tracked changes, patch live forms, or mutate source PDFs, DOCX files, TeX files, Markdown manuscripts, extracted text, or fixtures.
9. Treat a drafted-instructions JSON artifact without the same-version `drafted-edit-recommendations.md` as incomplete for human delivery; route to the relevant drafting or loop stage to repair the missing recommendations artifact before reporting the chain as ready.
10. Stop when routing is ambiguous, unsupported, missing required upstream artifacts, blocked by provenance mismatch, or dependent on an overwrite decision the user has not made.

## Discovery Inputs

Parse the user request for:

- explicit paths to source documents, review reports, DOCX files, normalized feedback plans, revision plans, writing constraints, contextualized plans, drafted instructions, projected states, or edit-review reports
- object-family signals: `grant`, `paper`, `PAP`, `paper-code`, `proposal`, `manuscript`, `application`, `pre-registration`, `replication`, or `reproducibility`
- slug or partial slug signals such as `google-impact`
- stage signals such as `comments`, `feedback`, `revision plan`, `writing constraints`, `contextualize`, `draft`, `drafted instructions`, `review drafted edits`, `continue`, `next artifact`, `version`, `reuse`, or `stop`
- feedback selection signals such as `single`, `subset`, `all`, `feedback_id`, `feedback_ids`, `comment id`, or selected comment text
- source rewrite signals such as `rewrite the DOCX`, `tracked changes`, `patch the manuscript`, `edit the PDF`, `update the TeX`, `modify the source`, or `apply changes directly`

When the user supplies a path, use that path as the primary source. An explicit review report, source path, normalized feedback plan, contextualized plan, drafted instructions path, projected state, or edit-review report overrides slug discovery.

When the user supplies a slug or partial slug, search deterministic artifact roots first:

- `artifacts/grants/`
- `artifacts/papers/`
- `artifacts/paps/`
- `artifacts/paper-code/`

Normalize slugs by lowercasing and comparing alphanumeric and hyphen-separated tokens. Support partial slug matches such as `google-impact`. Prefer exact directory slug matches over partial matches. Prefer explicit user family evidence over inferred family evidence.

If one candidate clearly dominates, report it and continue. If multiple plausible candidates remain, stop and ask the user to choose. Candidate reporting should include enough path context to choose safely.

## Editing Artifact Discovery Order

Within each candidate `editing/` directory, discover the most advanced available artifact first:

1. `drafted-edit-instructions-vN.json`
2. `drafted-edit-recommendations-vN.md`
3. `contextualized-edit-plan-vN.json`
4. `edit-review-panel-report-vN.json`
5. `projected-revision-state-vN.json`
6. `drafted-edit-instructions.json`
7. `drafted-edit-recommendations.md`
8. `contextualized-edit-plan.json`
9. `writing-constraints.json`
10. `revision-plan.json` and `revision-plan-vN.json`
11. `normalized-feedback-plan.json` and `normalized-feedback-plan-vN.json`

Review reports outside `editing/` are upstream inputs and should be discovered after checking existing editing artifacts:

- grant review reports under grant artifact roots
- paper review and light review reports under paper artifact roots
- PAP review reports under PAP artifact roots
- paper-code review reports under paper-code artifact roots

Use the discovered highest-stage artifact to decide whether the next safe route is planning, constraints loading, contextualization, drafting, edit-review, reuse, versioning, or stop.

## Guided Questions

Ask only the missing question that blocks safe routing.

Object family:

```text
Is this editing chain for a grant or a paper?
```

Available input:

```text
What should I start from: a review report, DOCX comments, a normalized feedback plan, a revision plan, writing constraints, a contextualized plan, or drafted instructions?
```

Desired stage:

```text
Do you want the next missing artifact, a specific stage, or a review of the existing drafted instructions?
```

Feedback selection:

```text
Should I address one feedback item, a selected subset, or all eligible feedback?
```

Reuse/version/stop:

```text
The next artifact already exists. Should I reuse it, create a versioned artifact, or stop?
```

Continue or review existing chain:

```text
I found drafted edit instructions already. Should I review them, create a versioned next pass, reuse them, or stop?
```

Use defaults only when the target stage skill documents a safe default and the user has not signaled that the missing value matters. Never default the feedback selection mode for `plan-feedback-revisions`.

## Routing Rules

Routing chooses the next existing stage skill. It must not generate the next artifact itself.

| Current input or state | Grant route | Paper route |
| --- | --- | --- |
| DOCX comments or feedback-bearing source with selection mode | `plan-feedback-revisions` | `plan-feedback-revisions` |
| `normalized-feedback-plan.json` | `convert-feedback-plan-to-revision-plan` | `convert-feedback-plan-to-revision-plan` |
| review report plus source document | `plan-revisions` | `plan-revisions` |
| source document needing constraints | `load-writing-constraints` | `load-writing-constraints` |
| `revision-plan.json` plus `writing-constraints.json` | `contextualize-revisions-grant` | `contextualize-revisions-paper` |
| `contextualized-edit-plan.json` | `draft-edits-grant` | `draft-edits-paper` |
| `drafted-edit-instructions.json` | `review-drafted-edits` | `review-drafted-edits` |

If a chain has a revision plan but lacks writing constraints, route to `load-writing-constraints` before object-specific contextualization. If a chain has both `revision-plan.json` and `writing-constraints.json` but lacks a contextualized plan, route to the object-specific contextualizer. If it has a contextualized plan but lacks drafted instructions, route to the object-specific drafter. If it has drafted instructions without the same-version human-readable recommendations artifact, route to the object-specific drafter for first-pass output or `review-drafted-edits` for versioned loop output so the missing recommendations document is generated. If it has drafted instructions and matching recommendations, and the user asks to continue or quality-check, route to `review-drafted-edits`.

For feedback-derived editing:

1. route DOCX comments or supported feedback-bearing sources to `plan-feedback-revisions`
2. route the resulting normalized feedback plan to `convert-feedback-plan-to-revision-plan`
3. continue through `load-writing-constraints`, object-specific contextualization, object-specific drafting, and optional `review-drafted-edits`

Preserve explicit arguments and paths when delegating. Do not restate or replace the stage workflow with new logic.

## No-Overwrite And Versioning Contract

Before invoking any stage that writes an artifact, check whether the expected deterministic output path already exists.

If the expected path exists:

1. report the existing path
2. summarize its artifact type and apparent stage
3. ask whether to reuse it, create a versioned artifact, or stop

If versioning is selected, preserve the stage's documented naming pattern:

- `normalized-feedback-plan-v2.json`
- `revision-plan-v2.json`
- `writing-constraints-v2.json`
- `contextualized-edit-plan-v2.json`
- `drafted-edit-instructions-v2.json`
- `drafted-edit-recommendations-v2.md`
- `projected-revision-state-v2.json`
- `edit-review-panel-report-v2.json`

Do not invent a parallel directory or ambiguous filename to avoid a collision.

## Stop Conditions

Stop and report the issue when:

- multiple candidate artifact chains match the requested slug
- no upstream artifact exists for the requested stage
- the document family cannot be inferred from explicit input or strong local evidence
- the object family is PAP or paper-code and the request asks for contextualization, drafting, or edit-review loop execution
- the user asks for direct source-document rewriting, tracked changes, live-form patching, or source PDF/DOCX/TeX/Markdown mutation
- existing next-stage artifacts would be overwritten and the user has not chosen reuse, version, or stop
- a normalized feedback request lacks a selection mode or required feedback ids
- a stage requires both `revision-plan.json` and `writing-constraints.json` but one is missing
- saved artifacts disagree on `document_type` or `source_document_path`
- the request asks for an unsupported generic edit operation outside the staged architecture
- routing truthfully requires changing an existing editing-stage skill

For provenance mismatch, name the disagreeing artifacts and the mismatched fields. Do not coerce document families, source paths, or artifact chains to make routing proceed.

## Delegation Output

When routing is clear, tell the user:

1. the object family and source path or artifact chain selected
2. the most advanced artifact discovered
3. the target stage skill to run
4. the important arguments or local artifacts that should be passed through
5. whether an existing output requires reuse, versioning, or stop before the stage runs
6. any assumptions, missing optional context, or discovered ambiguity

Then invoke or instruct the appropriate stage skill according to the host environment. Do not create the next editing artifact directly.
