# AI Research Feedback

Research-review workflows for papers, pre-analysis plans, and grant proposals.

Most users should start with the guided orchestrators:

- `run-review`: review a grant, paper, PAP, or paper-code package; asks short routing questions when needed
- `run-editing`: continue a post-review editing chain; discovers existing artifacts and avoids silent overwrites

This repo supports two surfaces:

- Claude Code commands authored from `Skills/*.md`
- a Codex plugin packaged under `plugins/ai-research-feedback/`

The canonical authored workflows live in `Skills/`. The Codex plugin bundles derived copies under `plugins/ai-research-feedback/skills/`.

## Quick Start

### Claude Code

Copy one or more workflows into `.claude/commands/`, then run them as slash commands. For guided use, install the orchestrators first.

Example:

```powershell
New-Item -ItemType Directory -Force .claude\commands | Out-Null
Copy-Item Skills\run-review.md .claude\commands\run-review.md
Copy-Item Skills\run-editing.md .claude\commands\run-editing.md
```

Then in Claude Code:

```text
/run-review path/to/document.pdf
/run-editing erc-starting-grant
```

If the document depends on nearby context, include the context path in the request:

```text
/run-review path/to/document.pdf context=./context/
```

### Codex

Install the repo-local plugin, then invoke a workflow in normal chat by naming the skill explicitly. Start with `run-review` or `run-editing` unless you already know the exact stage skill to use.

When relevant material lives outside the main document, point the orchestrator to the folder or files that contain it. This is useful for grant calls, sponsor guidelines, reviewer comments, response letters, supplements, figures, tables, code, budgets, and prior review or editing artifacts.

Guided review examples:

```text
Use the AI Research Feedback plugin skill `run-review` to review this document and ask only the missing routing question. The context is available in ./context/.
```

```text
Use the AI Research Feedback plugin skill `run-review` to review this grant proposal. The call context, budget notes, and supporting files are available in ./context/.
```

```text
Use the AI Research Feedback plugin skill `run-review` to run a full paper review for ./paper/my-paper-to-review.pdf with target journal PNAS.
```

```text
Use the AI Research Feedback plugin skill `run-review` to review the NIH grant application and reuse any matching profile or review plan.
```

Guided editing examples:

```text
Use the AI Research Feedback plugin skill `run-editing` to continue the editing chain for ERC-starting-grant without overwriting existing artifacts.
```

```text
Use the AI Research Feedback plugin skill `run-editing` to run the editing phase for this proposal. The source document, reviewer comments, call materials, and prior review artifacts are in ./context/.
```

```text
Use the AI Research Feedback plugin skill `run-editing` to turn selected DOCX comments into revision guidance; ask me for the feedback selection mode if needed.
```

Direct stage examples, when you already know the exact step:

```text
Use the AI Research Feedback plugin skill `review-paper` on ./paper/my-paper-to-review.pdf with journal=PNAS.
```

```text
Use the AI Research Feedback plugin skill `plan-feedback-revisions` with type=grant source=./proposal-with-comments.docx source_type=docx-comment mode=single feedback_id=1.
```

## Workflows

- `run-review`: plugin-exposed review orchestrator that routes natural review requests to the existing review workflows
- `run-editing`: plugin-exposed editing orchestrator that routes natural editing requests to the existing staged editing workflows
- `review-paper`: full referee-style paper review
- `review-paper-light`: quick paper check
- `review-paper-code`: paper-code reproducibility review
- `review-pap`: pre-analysis plan review
- `fetch-grant-context`: grant call intake and normalization
- `plan-grant-review`: reviewer-panel planning and confirmation before grant review
- `review-grant`: proposal review against a sponsor archetype and optional cached grant profile
- `plan-feedback-revisions`: shared feedback-addressed planning from DOCX comments into normalized feedback targets
- `convert-feedback-plan-to-revision-plan`: compatibility bridge from normalized feedback targets into revision-plan artifacts
- `plan-revisions`: shared post-review revision planning from saved review reports
- `load-writing-constraints`: shared writing-constraint extraction for revision passes
- `contextualize-revisions-grant`: grant-specific post-review contextualization from saved editing artifacts
- `draft-edits-grant`: grant-specific drafted edit instructions from a saved contextualized edit plan
- `contextualize-revisions-paper`: paper-specific post-review contextualization from saved editing artifacts
- `draft-edits-paper`: paper-specific drafted edit instructions from a saved contextualized edit plan
- `review-drafted-edits`: post-draft edit-review loop for validated grant and paper drafted edit instructions

## Choosing A Workflow

The canonical `run-review` and `run-editing` orchestrators are specified in `docs/interactive-orchestrators.md`, implemented in `Skills/run-review.md` and `Skills/run-editing.md`, and exposed through the Codex plugin. Use them when you want guided discovery, short routing questions, and safe delegation to the explicit stage skills. You can still name a specific stage skill directly when the route is already clear.

Use `run-review` when you can describe the review goal in ordinary language:

- "Review this paper."
- "Run a quick check on this manuscript."
- "Review this grant against the ERC Starting Grant call."
- "Review this PAP for OSF."
- "Review this paper and code for reproducibility."

Use `run-editing` when you want to continue from review feedback, comments, or existing editing artifacts:

- "Run the editing phase for erc-starting-grant."
- "Continue the editing chain for this paper."
- "Turn these DOCX comments into revision guidance."
- "Review the drafted edit instructions."
- "Tell me what editing artifacts already exist and what the next safe step is."

Both orchestrators detect existing artifacts first and ask only the missing routing question. They do not rewrite source documents, create tracked changes, patch live forms, or silently overwrite existing artifacts.

When using the skills in your own project folder, point the orchestrator to the relevant context if it is not already captured in `artifacts/`. Useful context includes call documents, grant profiles, review plans, reviewer comments, response letters, source manuscripts, supplements, figures, tables, code folders, budgets, and prior review or editing artifacts. For example:

```text
Use the AI Research Feedback plugin skill `run-review` to review this document and ask only the missing routing question. The context is available in ./context/.
```

```text
Use the AI Research Feedback plugin skill `run-editing` to continue the editing chain for this proposal. Relevant source files, comments, and grant-call context are in ./proposal-context/.
```

Use the review workflows when you want a fresh assessment of a document:

- Use `review-grant` for a grant proposal review. Add `fetch-grant-context` and `plan-grant-review` first when the grant call matters and you want the reviewer panel to reflect the sponsor, call profile, and selected review lenses.
- Use `review-paper` for a full paper referee-style review.
- Use `review-paper-light` for a faster paper check when you do not need the full six-agent referee report.
- Use `review-pap` for pre-analysis plans.
- Use `review-paper-code` for paper-plus-code reproducibility review.

Use the editing workflows when you already have review feedback or comments and want revision guidance:

1. `plan-revisions` or `plan-feedback-revisions`
2. `convert-feedback-plan-to-revision-plan` when starting from normalized feedback
3. `revision-recommendations*.md` as the specified human-readable advisory companion to `revision-plan*.json`
4. `load-writing-constraints`
5. `contextualize-revisions-grant` or `contextualize-revisions-paper`
6. `draft-edits-grant` or `draft-edits-paper`
7. `review-drafted-edits` when you want the post-draft loop to evaluate the projected revised state before human application

### Mode Guidelines

For grant call intake and grant review:

- `foundation`: use for philanthropic, public-good, impact-challenge, nonprofit, or open-science calls.
- `major-funder`: use when the sponsor is not one of the built-in funder archetypes or when you want a broad competitive-grant review.
- `NSF`, `NIH`, `ERC`, and `HorizonEurope`: use when the proposal should be judged against those funder norms.
- A saved `profile.json` can override the default funder context through its call-specific priorities, constraints, and reviewer brief. A saved `review-plan.json` should be used when you want the panel composition to follow a planned lens set rather than the fallback standing panel.

For feedback-addressed editing:

- `single`: revise one selected feedback item. Use this for focused comment response or when you want to avoid touching unrelated feedback.
- `subset`: revise a selected group of feedback items. Use this when several comments belong to the same revision theme.
- `all`: normalize all eligible feedback items from the source. Use this for comprehensive comment processing, then rely on guideline appraisal to accept, narrow, reject, or verify each item.

For post-draft edit review:

- `review-drafted-edits` supports validated grant and paper drafted edit instructions.
- It produces review evidence and versioned editing artifacts; it does not rewrite source documents, create tracked changes, or patch live forms.
- It must stop for PAP or paper-code drafted artifacts until those editing-loop paths are implemented and validated.

Planned next layer:

- post-review editing as a staged architecture, documented in `docs/post-review-editing.md`
- feedback-addressed editing as a generalized upstream layer for DOCX comments, PDF annotations, review reports, inline notes, and direct user instructions, documented in `docs/feedback-addressed-editing.md`; the first DOCX-comment adapter path is represented by `plan-feedback-revisions`
- shared editing schemas under `templates/editing/`
- PAP or paper-code editing workflow specs and representative edit-review loop validation

## Output Locations

Review reports save to deterministic locations:

- `review-paper` -> `artifacts/papers/<paper-slug>/review/paper-review--YYYY-MM-DD.md`
- `review-paper-light` -> `artifacts/papers/<paper-slug>/review/paper-light-review--YYYY-MM-DD.md`
- `review-paper-code` -> `artifacts/paper-code/<subject-slug>/review/paper-code-review--YYYY-MM-DD.md`
- `review-pap` -> `artifacts/paps/<source-slug>/review/pap-review--<pap-slug>--YYYY-MM-DD.md`
- `plan-grant-review` with profile -> next to the profile as `review-plan.json`
- `review-grant` with profile -> next to the profile as `grant-review--<proposal-slug>--YYYY-MM-DD.md`
- `review-grant` without profile -> `artifacts/grants/<proposal-slug>/review/grant-review--YYYY-MM-DD.md`

If a filename already exists, the workflow appends `-v2`, `-v3`, and so on.

Planned post-review editing artifacts save under deterministic per-source folders:

- `normalized-feedback-plan` -> `artifacts/<object-folder>/<source-slug>/editing/normalized-feedback-plan.json`
- `revision-plan` -> `artifacts/<object-folder>/<source-slug>/editing/revision-plan.json`
- `revision-recommendations` -> `artifacts/<object-folder>/<source-slug>/editing/revision-recommendations.md`
- `writing-constraints` -> `artifacts/<object-folder>/<source-slug>/editing/writing-constraints.json`
- `contextualized-edit-plan` -> `artifacts/<object-folder>/<source-slug>/editing/contextualized-edit-plan.json`
- `drafted-edit-instructions` -> `artifacts/<object-folder>/<source-slug>/editing/drafted-edit-instructions.json`
- `projected-revision-state` -> `artifacts/<object-folder>/<source-slug>/editing/projected-revision-state.json`
- `edit-review-panel-report` -> `artifacts/<object-folder>/<source-slug>/editing/edit-review-panel-report.json`
- versioned loop outputs -> `artifacts/<object-folder>/<source-slug>/editing/contextualized-edit-plan-vN.json` and `drafted-edit-instructions-vN.json`

Current object folders are:

- `grants`
- `papers`
- `paps`
- `paper-code`

Shared post-review editing stages now specified:

- `plan-feedback-revisions` -> `artifacts/<object-folder>/<source-slug>/editing/normalized-feedback-plan.json`
- `convert-feedback-plan-to-revision-plan` -> `artifacts/<object-folder>/<source-slug>/editing/revision-plan.json`
- `revision-recommendations*.md` -> `artifacts/<object-folder>/<source-slug>/editing/revision-recommendations.md` and versioned companions such as `revision-recommendations-v2.md`
- `plan-revisions` -> `artifacts/<object-folder>/<source-slug>/editing/revision-plan.json`
- `load-writing-constraints` -> `artifacts/<object-folder>/<source-slug>/editing/writing-constraints.json`
- `contextualize-revisions-grant` -> `artifacts/grants/<source-slug>/editing/contextualized-edit-plan.json`
- `draft-edits-grant` -> `artifacts/grants/<source-slug>/editing/drafted-edit-instructions.json`
- `contextualize-revisions-paper` -> `artifacts/papers/<source-slug>/editing/contextualized-edit-plan.json`
- `draft-edits-paper` -> `artifacts/papers/<source-slug>/editing/drafted-edit-instructions.json`
- `review-drafted-edits` -> grant or paper `projected-revision-state.json`, `edit-review-panel-report.json`, and, when another iteration is warranted, versioned contextualized and drafted artifacts

Formal shared editing schemas live under `templates/editing/`, including the post-draft loop contracts for `projected-revision-state.json` and `edit-review-panel-report.json`.

Current post-review editing support by object family:

| Object family | Review support                       | Editing support                                                                          | Post-draft loop support                  | Representative validation                                                       | Plugin exposure                                                               |
| ------------- | ------------------------------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Grants        | `review-grant`                       | shared planning/constraints plus `contextualize-revisions-grant` and `draft-edits-grant` | canonical `review-drafted-edits` support | representative grant loop artifacts; Benrimoh feedback-derived downstream artifacts | current plugin exposes first-pass editing and the `review-drafted-edits` loop |
| Papers        | `review-paper`, `review-paper-light` | shared planning/constraints plus `contextualize-revisions-paper` and `draft-edits-paper` | canonical `review-drafted-edits` support | Communications Psychology paper loop artifacts                                  | current plugin exposes first-pass editing and the `review-drafted-edits` loop |
| PAPs          | `review-pap`                         | shared contracts only; no PAP contextualizer or drafter                                  | deferred                                 | none                                                                            | review only; no editing-loop exposure                                         |
| Paper-code    | `review-paper-code`                  | shared contracts only; no paper-code contextualizer or drafter                           | deferred                                 | none                                                                            | review only; no editing-loop exposure                                         |

Editing artifacts are human-applied instructions and review evidence. They do not rewrite source documents, create tracked changes, patch live forms, or add unsupported empirical, sponsor, budget, partner, citation, or analysis claims.

The newly specified `revision-recommendations*.md` stage is a human-readable advisory memo derived from `revision-plan*.json`. It is optional but strongly recommended so existing chains remain valid while later implementation work adds the readable companion stage.

Representative runtime validation artifacts now exist for a grant fixture under:

- `artifacts/grants/example-erc-starting-grant-application/editing/`

Representative DOCX-comment feedback normalization artifacts now exist for the Benrimoh Research Vision fixture under:

- `artifacts/grants/benrimoh-research-vision/editing/`

That same Benrimoh path also contains representative compatibility revision-plan artifacts converted from the single-comment and all-comment normalized feedback plans. The selected single-comment `FB2` path additionally has downstream validation artifacts for writing constraints, grant contextualization, and drafted edit instructions.

Representative paper contextualization validation artifacts now exist for the Communications Psychology paper fixture under:

- `artifacts/papers/s44271-024-00170-w/editing/`

Representative paper drafting validation artifacts now exist for the same fixture under:

- `artifacts/papers/s44271-024-00170-w/editing/`

## Grant Review In One Glance

Grant review is a 3-step flow:

1. Fetch the grant call into `artifacts/grants/<slug>/profile.json`
2. Plan the review panel in `artifacts/grants/<slug>/review-plan.json`
3. Review the proposal using that saved profile and review plan

When you use `review-grant` with a profile, the review report is saved next to that profile using:

- `grant-review--<proposal-slug>--YYYY-MM-DD.md`

Claude Code example:

```text
/fetch-grant-context "ERC Starting Grant" slug=erc-starting-grant mode=ERC
/plan-grant-review ERC profile=artifacts/grants/erc-starting-grant/profile.json ./path/to/erc-starting-grant-application.pdf
/review-grant ERC profile=artifacts/grants/erc-starting-grant/profile.json plan=artifacts/grants/erc-starting-grant/review-plan.json ./path/to/erc-starting-grant-application.pdf
```

Codex example:

```text
Use the AI Research Feedback plugin skill `fetch-grant-context` on "ERC Starting Grant" with slug=erc-starting-grant and mode=ERC.
Use the AI Research Feedback plugin skill `plan-grant-review` on ./path/to/erc-starting-grant-application.pdf with mode=ERC and context from artifacts/grants/erc-starting-grant/profile.json.
Use the AI Research Feedback plugin skill `review-grant` on ./path/to/erc-starting-grant-application.pdf with mode=ERC, context from artifacts/grants/erc-starting-grant/profile.json, and plan from artifacts/grants/erc-starting-grant/review-plan.json.
```

## Repo Structure

- `Skills/`: canonical workflow definitions
- `plugins/ai-research-feedback/`: Codex plugin package
- `.agents/plugins/marketplace.json`: repo-local Codex marketplace entry
- `scripts/derive_codex_plugin_skills.py`: syncs canonical workflows into the plugin bundle
- `artifacts/grants/`: run-specific grant profiles and review plans
- `templates/grants/`: reusable grant schemas and expert-registry templates
- `templates/editing/`: shared post-review editing artifact schemas

## Docs

- [docs/claude-code.md](docs/claude-code.md)
- [docs/codex.md](docs/codex.md)
- [docs/paper-review.md](docs/paper-review.md)
- [docs/pap-review.md](docs/pap-review.md)
- [docs/grant-review.md](docs/grant-review.md)
- [docs/grant-review-planning.md](docs/grant-review-planning.md)
- [docs/post-review-editing.md](docs/post-review-editing.md)
- [docs/feedback-addressed-editing.md](docs/feedback-addressed-editing.md)
- [docs/interactive-orchestrators.md](docs/interactive-orchestrators.md)
