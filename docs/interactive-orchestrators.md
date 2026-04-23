# Interactive Review And Editing Orchestrators

## Status

This document specifies the intended behavior for two top-level orchestrators:

- `run-review`, implemented as a canonical skill in `Skills/run-review.md`
- `run-editing`, implemented as a canonical skill in `Skills/run-editing.md`

`run-review` and `run-editing` are canonical and plugin-exposed. Claude Code users can install them manually as slash commands from `Skills/`, and Codex plugin users can name them directly for guided routing. Existing stage workflows remain available for explicit invocation when the route is already clear.

The orchestrators must route to existing skills instead of reimplementing review, planning, contextualization, drafting, or edit-review logic.

## Design Goals

The orchestrators should let a user start from natural requests such as:

- "Review this document."
- "Run a full review of this paper."
- "Review this PAP for OSF."
- "Review this paper and code."
- "Run the editing phase for google-impact."
- "Continue the post-review editing chain for this proposal."
- "Turn these DOCX comments into revision guidance."

They should discover available repo context first, ask only short targeted questions when discovery is insufficient, and stop rather than guessing across unsupported or ambiguous boundaries.

## Shared Operating Rules

Both orchestrators must:

- inspect explicit user inputs before searching broadly
- discover existing artifacts before proposing new generation
- report the artifact or source candidates they found when a choice is needed
- ask the smallest number of simple questions needed to route safely
- preserve existing stage boundaries and call stage skills by name
- avoid direct source-document rewriting, tracked changes, live-form patching, or source PDF/DOCX/TeX/Markdown mutation
- avoid overwriting existing artifacts by default
- stop on unsupported families, missing required targets, or ambiguous candidates

When a deterministic output already exists, the orchestrator must not overwrite it silently. It should report the existing path and ask whether to:

- reuse the existing artifact
- create a versioned artifact such as `-v2` or `-v3`
- stop

## Slug And Candidate Discovery

When the user supplies a path, use that path as the primary source.

When the user supplies a slug or partial slug, search deterministic artifact roots first:

- `artifacts/grants/`
- `artifacts/papers/`
- `artifacts/paps/`
- `artifacts/paper-code/`

Matching rules:

- normalize slugs by lowercasing and comparing alphanumeric and hyphen-separated tokens
- support partial slug matches such as `google-impact`
- prefer exact directory slug matches over partial matches
- prefer object-family evidence supplied by the user over inferred family evidence
- if one candidate clearly dominates, report it and continue
- if multiple plausible candidates remain, stop and ask the user to choose

Candidate reporting should include enough path context to make the choice easy, for example:

```text
I found two grant editing chains matching "google-impact":
1. artifacts/grants/google-impact-challenge-ai-for-science-application/editing/
2. artifacts/grants/google-impact-challenge-ai-for-science/editing/
Which one should I use?
```

## `run-review`

### Supported Intents

`run-review` handles requests for fresh assessment of a document or paper-code package.

Supported review families:

- grant proposal review through `fetch-grant-context`, `plan-grant-review`, and `review-grant`
- full paper review through `review-paper`
- light paper review through `review-paper-light`
- PAP review through `review-pap`
- paper-code reproducibility and alignment review through `review-paper-code`

Example prompts:

- "Review this grant proposal against the Google.org call."
- "Run a grant review for this application; use the saved profile if available."
- "Review this paper for PNAS."
- "Do a quick paper check."
- "Review this PAP for OSF."
- "Review this paper and its code for reproducibility."

### Review Discovery Inputs

`run-review` should inspect:

- explicit source paths in the user prompt
- explicit target names such as journal, registry, sponsor archetype, or grant call
- explicit mode words such as `light`, `quick`, `full`, `main`, or `paper-code`
- nearby or matching grant `profile.json` and `review-plan.json`
- obvious source-document candidates only when the user did not supply a path

The orchestrator should not perform a broad repo audit by default. It should use the discovery behavior already defined by the target review skill after routing is selected.

### Review Guided Questions

Ask only the missing question that blocks safe routing.

Document family:

```text
What kind of review should I run: grant, paper, PAP, or paper-code?
```

Paper light/full ambiguity:

```text
Do you want a quick paper check or the full referee-style review?
```

Paper-code involvement:

```text
Should I review only the paper, or the paper together with the code?
```

Grant-call context:

```text
Should I use an existing grant profile, fetch a new call profile, or run with a generic sponsor archetype?
```

PAP target:

```text
What registration or journal target should the PAP review use?
```

Use defaults only when the target skill already defines a safe default and the user has not signaled that the missing value matters. For example, `review-paper` can default to a general top-field standard, but `run-review` should still ask about light versus full when the prompt makes speed or depth ambiguous.

### Review Routing

Routing is stage delegation, not stage implementation.

| User intent | Route |
| --- | --- |
| Grant call intake only | `fetch-grant-context` |
| Grant panel planning only | `plan-grant-review` |
| Grant proposal review with existing profile or plan | `review-grant` |
| Grant proposal review without profile | ask whether to fetch/profile first or use sponsor archetype, then route |
| Full paper review | `review-paper` |
| Quick paper check | `review-paper-light` |
| PAP review | `review-pap` |
| Paper plus code review | `review-paper-code` |

For grants, when a matching profile and review plan are discoverable, `run-review` should offer to reuse them. If no profile exists but a grant call is named, it should ask whether to run `fetch-grant-context` first or proceed with a generic sponsor archetype.

For papers, if the user says "quick", "light", "fast", or "sanity check", route to `review-paper-light`. If the user says "full", "referee", "six-agent", or names a journal review target without speed constraints, route to `review-paper` after confirming any missing path.

For paper-code, explicit code involvement such as "code", "reproducibility", "replication package", "pipeline", "scripts", or a provided code directory routes to `review-paper-code`.

### Review Stop Conditions

`run-review` must stop when:

- no source document or code package can be found for the requested review
- more than one source candidate is plausible and the user did not choose one
- the document family cannot be inferred from explicit input or strong local evidence
- PAP review is requested without a target and the user declines to provide one
- a grant review needs call-specific context but no profile, call source, or sponsor archetype is available
- the request asks for a review family not supported by existing review skills
- the request asks the orchestrator to rewrite or edit the source document as part of review

## `run-editing`

### Supported Intents

`run-editing` handles requests to continue or inspect staged editing artifacts after review feedback, DOCX comments, or drafted edit instructions exist.

Supported editing families:

- grant editing through shared planning, writing constraints, grant contextualization, grant drafting, and validated grant edit-review loop
- paper editing through shared planning, writing constraints, paper contextualization, paper drafting, and validated paper edit-review loop
- shared normalized feedback planning through DOCX comments
- normalized feedback to revision-plan conversion

PAP and paper-code editing loops are not supported yet. The orchestrator may route PAP or paper-code sources only through shared planning contracts when a user explicitly asks for those shared artifacts, but it must stop before contextualization, drafting, or edit-review loop execution for those families.

Example prompts:

- "Run the editing phase for google-impact."
- "Continue editing from this grant review report."
- "Make the next artifact in the paper editing chain."
- "Turn the selected DOCX comment into a revision plan."
- "Review the drafted edit instructions for this paper."
- "Do not overwrite existing artifacts; just tell me where the chain is."

### Editing Artifact Discovery Order

`run-editing` should discover the most advanced available artifact first, then decide whether the user wants to continue, reuse, review, or version the chain.

Discovery order within a candidate `editing/` directory:

1. `drafted-edit-instructions-vN.json`
2. `drafted-edit-recommendations-vN.md`
3. `contextualized-edit-plan-vN.json`
4. `edit-review-panel-report-vN.json`
5. `projected-revision-state-vN.json`
6. `drafted-edit-instructions.json`
7. `drafted-edit-recommendations.md`
8. `contextualized-edit-plan.json`
9. `writing-constraints.json`
10. `revision-recommendations.md` and `revision-recommendations-vN.md`
11. `revision-plan.json` and `revision-plan-vN.json`
12. `normalized-feedback-plan.json` and `normalized-feedback-plan-vN.json`

Review reports outside `editing/` are upstream inputs and should be discovered after checking existing editing artifacts:

- grant review reports under grant artifact roots
- paper review and light review reports under paper artifact roots
- PAP review reports under PAP artifact roots
- paper-code review reports under paper-code artifact roots

If the user provides a review report path, source path, normalized feedback plan, contextualized plan, or drafted instructions path, that explicit input overrides slug discovery.

### Editing Guided Questions

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

Continue or review existing chain:

```text
I found drafted edit instructions already. Should I review them, create a versioned next pass, reuse them, or stop?
```

Overwrite/versioning:

```text
The next artifact already exists. Should I reuse it, create a versioned artifact, or stop?
```

### Editing Routing

Routing should choose the next existing stage skill, not generate artifacts itself.

| Current input or state | Grant route | Paper route |
| --- | --- | --- |
| DOCX comments and selection mode | `plan-feedback-revisions` | `plan-feedback-revisions` |
| `normalized-feedback-plan.json` | `convert-feedback-plan-to-revision-plan` | `convert-feedback-plan-to-revision-plan` |
| review report and source document | `plan-revisions` | `plan-revisions` |
| `revision-plan.json` with user request for human-readable guidance | route to the new `revision-recommendations*.md` stage when implemented; until then, stop or report that the stage is specified but not implemented | route to the new `revision-recommendations*.md` stage when implemented; until then, stop or report that the stage is specified but not implemented |
| source document needing constraints | `load-writing-constraints` | `load-writing-constraints` |
| `revision-plan.json` plus `writing-constraints.json` | `contextualize-revisions-grant` | `contextualize-revisions-paper` |
| `contextualized-edit-plan.json` | `draft-edits-grant` | `draft-edits-paper` |
| `drafted-edit-instructions.json` with matching `drafted-edit-recommendations.md` | `review-drafted-edits` | `review-drafted-edits` |

If a chain has `revision-plan*.json` but no `revision-recommendations*.md`, `run-editing` should treat the Markdown companion as the preferred next human-readable stage when the user asks for readable revision guidance. Because this pass is specification only, the orchestrator must not claim that the new stage already exists or is already implemented. If a chain has both `revision-plan.json` and `writing-constraints.json` but lacks a contextualized plan, route to the object-specific contextualizer. If it has a contextualized plan but no drafted instructions, route to the object-specific drafter. If it has drafted instructions without the same-version human-readable recommendations artifact, route to the relevant drafting or loop stage to repair the missing recommendations artifact before reporting the chain as ready. If it has drafted instructions and matching recommendations, and the user asks to continue or quality-check, route to `review-drafted-edits`.

For feedback-derived editing:

1. route DOCX comments to `plan-feedback-revisions`
2. route the resulting normalized feedback plan to `convert-feedback-plan-to-revision-plan`
3. continue with `load-writing-constraints`, object-specific contextualization, object-specific drafting, and optional `review-drafted-edits`

The orchestrator must preserve selection mode. A `single` or `subset` feedback request must not silently become an `all` request.

### Editing Stop Conditions

`run-editing` must stop when:

- multiple candidate artifact chains match the requested slug
- no upstream artifact exists for the requested stage
- the object family is PAP or paper-code and the request asks for contextualization, drafting, or edit-review loop execution
- the user requests direct source-document rewriting, tracked changes, live-form patching, or source PDF/DOCX/TeX/Markdown mutation
- existing next-stage artifacts would be overwritten and the user has not chosen reuse, version, or stop
- a normalized feedback request lacks a selection mode or required feedback ids
- a stage requires both `revision-plan.json` and `writing-constraints.json` but one is missing
- saved artifacts disagree on `document_type` or `source_document_path`
- the user asks for an unsupported generic edit operation outside the staged architecture

## No-Overwrite And Versioning Contract

Before invoking any stage that writes an artifact, an orchestrator must check whether the expected output path already exists.

If the expected path exists:

1. report the existing path
2. summarize its artifact type and apparent stage
3. ask whether to reuse, write a versioned artifact, or stop

If versioning is selected, preserve the stage's documented naming pattern:

- `revision-plan-v2.json`
- `revision-recommendations-v2.md`
- `writing-constraints-v2.json`
- `contextualized-edit-plan-v2.json`
- `drafted-edit-instructions-v2.json`
- `drafted-edit-recommendations-v2.md`
- `projected-revision-state-v2.json`
- `edit-review-panel-report-v2.json`

The orchestrator must not invent a parallel directory or ambiguous filename to avoid a collision.

## Validation Matrix For Future Implementation

Later implementation and validation passes should cover at least these cases.

| Case | Prompt shape | Expected behavior |
| --- | --- | --- |
| Grant review with known source | "Review the Google.org proposal using google-impact" | Discover or ask for the proposal, offer matching profile/review plan if present, route to `review-grant`. |
| Paper review with light/full ambiguity | "Review this paper" | Ask whether the user wants quick/light or full referee-style review unless other prompt signals decide it. |
| Paper-code explicit involvement | "Review this paper and code for reproducibility" | Route to `review-paper-code`, preserving any explicit paper path, code dir, and depth. |
| PAP missing target | "Review this PAP" | Ask for registration or journal target, or use only a documented safe default if the user accepts it. |
| Editing for `google-impact` with discoverable artifacts | "Run editing for google-impact" | Match the artifact chain under `artifacts/grants/.../editing/`, report current highest-stage artifact, and ask whether to continue, reuse, review, or version if needed. |
| Multiple editing candidates | "Run editing for grant application" | Stop and present candidate paths rather than choosing silently. |
| Feedback selection ambiguity | "Address comments in this DOCX" | Ask whether to use `single`, `subset`, or `all`, and require ids for `single` or `subset`. |
| Unsupported PAP edit-review loop | "Review drafted edits for this PAP" | Stop with a deferred-support message; do not call `review-drafted-edits`. |
| Unsupported paper-code edit-review loop | "Continue the paper-code editing loop" | Stop with a deferred-support message; do not contextualize, draft, or review drafted edits. |
| Existing complete chain | "Continue editing this paper" when drafted instructions and loop artifacts exist | Report the complete chain and ask whether to reuse, review, version another pass, or stop. |
| Existing next artifact | Any next-stage request where output already exists | Ask reuse/version/stop before invoking a writing stage. |
| Saved artifact mismatch | `revision-plan.json` and `writing-constraints.json` point to different sources | Stop and report the mismatch rather than coercing paths. |

These cases are sufficient specification evidence for `run-review` and `run-editing` validation, guided-question validation, discovery validation, and no-overwrite validation.

## Future Implementation Notes

Plugin sync has exposed the accepted canonical orchestrators:

- `Skills/run-review.md` is implemented as the canonical review orchestrator.
- `Skills/run-editing.md` is implemented as the canonical editing orchestrator.

The plugin-bundled copies are derived from the canonical files. The orchestrators remain routing contracts: they delegate to existing review and editing stage skills, avoid source-document rewrites and tracked changes, require reuse/version/stop decisions before overwrites, and stop for unsupported PAP or paper-code editing-loop requests.
