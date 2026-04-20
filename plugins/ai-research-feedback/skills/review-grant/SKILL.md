---
description: Run a grant proposal review using a sponsor archetype, optional call-specific grant profile, and optional saved review plan
---

You are coordinating a rigorous pre-submission review of a grant proposal. You will use a saved review plan when available so the reviewer panel matches the grant's likely evaluator mix instead of assuming one fixed panel.

## Goal

Review the proposal against:

- a base sponsor archetype
- plus, when available, a call-specific grant profile cached locally
- plus, when available, a saved review plan that specifies the expert lenses to run

The sponsor archetype provides the stable reviewer persona. The call-specific profile provides the exact priorities, constraints, review criteria, and required components for one grant opportunity.
The review plan provides the grant-specific reviewer panel and any organization-specific overlays.

## Phase 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- Recognized built-in sponsor archetypes:
  - `NSF`
  - `NIH`
  - `ERC`
  - `HorizonEurope`
  - `major-funder`
  - `foundation`
- Optional review-plan arguments:
  - `plan=<path>`
  - `review-plan=<path>`
- Optional grant-profile arguments:
  - `profile=<path>`
  - `grant-profile=<path>`
- Optional shorthand grant-profile path:
  - if a token ends in `profile.json`, treat it as a profile path
- Optional shorthand review-plan path:
  - if a token ends in `review-plan.json`, treat it as a review-plan path
- Remaining text is the proposal path

Resolution rules:

1. If the first token matches a built-in sponsor archetype, treat it as the requested base review mode.
2. If a profile path is provided, read it and treat it as the source of call-specific context.
3. If the profile contains `base_funder_mode`, use that as the effective reviewer persona unless the user explicitly provided a built-in sponsor archetype; if both are present and they differ, prefer the explicit user argument but record the mismatch in the final report assumptions.
4. If neither a built-in sponsor archetype nor a profile path is provided, default to `major-funder`.
5. If no proposal path is provided, auto-detect it.

Store:

- `REQUESTED_TARGET_PROGRAM`
- `GRANT_PROFILE_PATH`
- `REVIEW_PLAN_PATH`
- `EFFECTIVE_TARGET_PROGRAM`

## Phase 2: Load Call-Specific Grant Profile When Present

If `GRANT_PROFILE_PATH` is set:

1. Read the JSON file.
2. Validate that it appears to match the schema at `templates/grants/profile.schema.json` when that file exists; otherwise validate the profile by checking for the required fields listed below.
3. Record at minimum:
   - `grant_name`
   - `sponsor`
   - `program_name`
   - `base_funder_mode`
   - `deadline`
   - `required_documents`
   - `budget_rules`
   - `review_criteria`
   - `program_priorities`
   - `language_to_mirror`
   - `risks_and_ambiguities`
   - `reviewer_brief`
   - `manual_review_required`
4. If `sources.md` exists next to the profile, read it as supporting provenance.
5. Build a concise `CALL_PROFILE_CONTEXT` block that summarizes the profile for downstream reviewers.

If no profile is provided:

- set `CALL_PROFILE_CONTEXT` to a short note saying that no call-specific profile was supplied and the review should rely on the built-in sponsor archetype plus the proposal materials alone

## Phase 2.5: Load Review Plan When Present

If `REVIEW_PLAN_PATH` is set:

1. Read the JSON file.
2. Validate it against `templates/grants/review-plan.schema.json` when that file exists. At minimum verify:
   - all top-level required fields are present
   - `panel_selection` is a non-empty array
   - every `panel_selection` entry contains:
     - `lens_id`
     - `label`
     - `status`
     - `rationale`
     - `priority`
     - `core_questions`
3. Record:
   - `planning_mode`
   - `panel_selection`
   - `uncertainties`
   - `confirmation`
   - `proposal_path`
   - `grant_profile_path`
   - `expert_registry_path`
4. Build `SELECTED_PLAN_LENSES` by keeping only `panel_selection` entries whose `status` is `selected`.
5. Keep the selected lenses in plan order. Do not silently re-expand the panel to a historical default count.
6. If `SELECTED_PLAN_LENSES` is empty, stop and report that the supplied plan selected no executable review lenses.
7. If `expert_registry_path` exists, read it and collect overlay adaptation notes for any selected `organization_overlay_ids`. If it is missing or cannot be parsed, continue with the saved overlay ids alone rather than guessing new overlays.
8. Build a concise `REVIEW_PLAN_CONTEXT` block summarizing:
   - planning mode
   - selected primary lenses
   - selected secondary lenses
   - optional or excluded lenses that were not launched
   - any organization-specific overlays attached to selected lenses
   - whether confirmation had been required

If no review plan is provided:

- set `REVIEW_PLAN_CONTEXT` to a short note saying that no saved plan was supplied and the workflow should fall back to a default standing panel
- set `SELECTED_PLAN_LENSES` to an empty list

## Phase 3: Discover the Proposal

If a file path was provided, use it as the main proposal file. Otherwise, auto-detect:

1. Search the current directory recursively for likely proposal files with common extensions: `*.md`, `*.txt`, `*.tex`, `*.docx`, `*.pdf` (exclude hidden folders, `.git`, build output, and dependency directories).
2. Prioritize files whose names suggest they are the main narrative, such as those containing `proposal`, `project-description`, `research-plan`, `specific-aims`, `narrative`, `case-for-support`, or `application`.
3. Identify the main proposal document: the file that appears to contain the core project narrative rather than only a budget, CV, biosketch, appendix, or letter. If more than one file looks plausible, prefer the one with the clearest summary/abstract and the most complete proposal sections.
4. Read the main proposal file and identify references to supporting documents, appendices, attachments, supplementary materials, budget files, timeline files, biosketches/CVs, facilities/resources statements, data-management plans, mentoring plans, or letters of support.
5. Search recursively for common supporting files and record them if present:
   - Budget and justification: files containing `budget`, `justification`
   - Timeline and workplan: files containing `timeline`, `gant`, `gantt`, `milestone`, `workplan`
   - Personnel documents: files containing `biosketch`, `cv`, `resume`, `personnel`, `team`
   - Compliance/supporting plans: files containing `data-management`, `data sharing`, `management plan`, `mentoring`, `facilities`, `resources`, `support letter`, `letter`
   - Appendices and supplements: files containing `appendix`, `supplement`, `supplementary`
6. Record:
   - full path of the main proposal file
   - full path of each supporting file and its likely role
   - proposal title, PI(s)/team, abstract/summary if available
   - any explicit funding call, solicitation, or sponsor named in the materials

Set `CREATED_REVIEW_INPUT = false`.

If the resolved file is `.tex`, `.txt`, or `.md`:

- set `INPUT_MODE = "plain-direct"`
- read directly
- do not create `_review_input.txt`

If the resolved file is `.pdf`:

- set `INPUT_MODE = "plain"`
- run: `pdftotext -layout "<path>" _review_input.txt`
- fallback: `python3 -c "import pypdf; r=pypdf.PdfReader('<path>'); open('_review_input.txt','w').write('\n'.join(p.extract_text() for p in r.pages))"`
- if both fail, halt with install instructions for pdftotext (poppler-utils) or pypdf
- set `CREATED_REVIEW_INPUT = true`

If the resolved file is `.docx`:

- set `INPUT_MODE = "plain"`
- run: `pandoc "<path>" -t plain -o _review_input.txt`
- if pandoc unavailable, halt with install instructions
- set `CREATED_REVIEW_INPUT = true`

## Phase 4: Build Shared Review Context

Construct a shared review context block for all agents containing:

- `EFFECTIVE_TARGET_PROGRAM`
- whether a call-specific profile was provided
- `GRANT_PROFILE_PATH` if present
- proposal title
- PI(s)/team
- explicit funding call or sponsor named in the proposal materials
- `CALL_PROFILE_CONTEXT`
- `REVIEW_PLAN_CONTEXT`
- any profile freshness or ambiguity warnings

When passing the proposal file path to agents:

- if `INPUT_MODE = "plain"`, substitute `_review_input.txt` for the main proposal file path
- otherwise use the original proposal file path

Pass the complete list of proposal and supporting file paths to every agent.

## Phase 4.5: Resolve Report Output Path

Before launching agents, resolve a deterministic output directory and filename.

Directory rules:

- If `GRANT_PROFILE_PATH` is present, save the report in the same directory as that `profile.json`.
- Otherwise, save the report under `review/`.

Filename rules:

- Derive `PROPOSAL_SLUG` from the main proposal filename:
  - lowercase
  - letters, numbers, and hyphens only
  - remove the original extension
- Base filename:
  - `grant-review--<PROPOSAL_SLUG>--[YYYY-MM-DD].md`
- If that filename already exists in the target directory, append `-v2`, `-v3`, and so on.

Store the final absolute report path as `REPORT_OUTPUT_PATH`.

## Phase 5: Resolve The Executed Review Panel

Build `EXECUTED_PANEL` as follows:

If `REVIEW_PLAN_PATH` is present:

1. Set `REVIEW_EXECUTION_MODE = "plan-driven"`.
2. Use `SELECTED_PLAN_LENSES` as the controlling list of reviewer lenses.
3. Launch only the selected lenses from the saved plan.
4. Do not add fallback standing-panel reviewers on top of the saved plan.

If `REVIEW_PLAN_PATH` is absent:

1. Set `REVIEW_EXECUTION_MODE = "fallback-standing-panel"`.
2. Build the default standing panel in this order:
   - `clarity-compliance`
   - `significance-fit`
   - `methods-feasibility`
   - `budget-team-operations`
   - `internal-consistency`
   - `adversarial-panel`
3. For each fallback reviewer, create a runtime entry with:
   - `status = selected`
   - `priority = primary`
   - `rationale = "No saved review plan was supplied, so the default standing panel was used."`
   - concise default `core_questions` appropriate to that reviewer
   - empty `organization_overlay_ids`

Every runtime reviewer entry must carry:

- `lens_id`
- `label`
- `priority`
- `rationale`
- `core_questions`
- `organization_overlay_ids`

## Phase 5.5: Map Runtime Lenses To Reviewer Briefs

For each entry in `EXECUTED_PANEL`, map `lens_id` to the corresponding reviewer brief below.

Supported plan-driven and fallback lens ids:

- `clarity-compliance`
- `significance-fit`
- `methods-feasibility`
- `budget-team-operations`
- `philanthropy-public-impact`
- `ethics-philosophy`
- `internal-consistency`
- `adversarial-panel`

If a supplied saved plan selects any other `lens_id`, stop and report that the plan contains an unsupported executable lens rather than inventing a new reviewer role.

Use these reviewer briefs:

- `clarity-compliance`
  - Review for readability, proposal structure, sponsor-language mirroring, required-component visibility, and compliance signals.
- `significance-fit`
  - Review for problem importance, novelty discipline, sponsor fit, competitive positioning, and whether the value proposition is strong enough for this call.
- `methods-feasibility`
  - Review for methodological adequacy, feasibility, dependencies, execution risk, risk mitigation, and outcome measurement.
- `budget-team-operations`
  - Review for budget credibility, staffing adequacy, timeline realism, coordination clarity, and missing operational support.
- `philanthropy-public-impact`
  - Review for theory of change, public-benefit plausibility, openness, non-technical legibility, scalability, sustainability, and implementation-facing impact claims.
- `ethics-philosophy`
  - Review for responsible-AI expectations, fairness or legitimacy claims, hidden normative assumptions, downstream harms, and governance adequacy.
- `internal-consistency`
  - Review for consistency across aims, methods, deliverables, staffing, budget story, terminology, and referenced attachments.
- `adversarial-panel`
  - Review as a demanding final panelist who gives an overall rating, major strengths, major weaknesses, required revisions, strategic fit assessment, and pointed panel questions.

## Phase 5.6: Launch Review Agents In Parallel

Launch one review agent per entry in `EXECUTED_PANEL`, preserving order.

Every launched agent must receive:

- the shared review context block
- the proposal/supporting file list
- the instruction to use the call-specific profile when present and to fall back to the built-in sponsor archetype when it is not
- the selected lens metadata:
  - `lens_id`
  - `label`
  - `priority`
  - `rationale`
  - `core_questions`
  - `organization_overlay_ids`
- any overlay adaptation notes recovered from the expert registry

Use this runtime prompt template for each launched reviewer:

```text
You are the reviewer for lens `[label]` (`[lens_id]`).

Adopt the reviewer brief mapped to this lens. Use the shared review context, the proposal files, the saved plan rationale, and the core questions below as controlling instructions for what to emphasize.

Saved plan rationale:
[rationale]

Priority:
[priority]

Core questions:
[bulleted core_questions]

Organization-specific overlays to honor:
[overlay ids or "none"]

Overlay adaptation notes:
[notes from registry if available, otherwise "none recovered"]

Additional reviewer brief for this lens:
[mapped reviewer brief text from Phase 5.5]

Output format:
## Lens Review: [label] (`[lens_id]`)

### Selection Rationale
[1 short paragraph tying the saved plan rationale to the actual proposal]

### Major Strengths
[numbered list]

### Major Concerns
[numbered list]

### Required Revisions
[numbered list]

### Questions For The PI
[numbered list]

### Bottom Line
[2-3 sentences on how this lens affects fundability]
```

In plan-driven mode, the saved plan is the controlling panel definition. In fallback mode, the standing panel definitions above are the controlling panel definition.

## Phase 6: Consolidate and Save

After all reviewers return, consolidate them into a single structured report and save it to `REPORT_OUTPUT_PATH`.

The coordinator must produce the final synthesis even if `adversarial-panel` was not launched. In plan-driven mode, derive the overall recommendation from the full set of selected lens outputs rather than inventing a missing standing-panel voice.

Report structure:

```markdown
# Grant Proposal Review

**Proposal**: [Title]
**PI(s)/Team**: [PI(s) or team]
**Date**: [Today's date]
**Review Standard**: [EFFECTIVE_TARGET_PROGRAM - if `major-funder`, write "Competitive Major Funder"; if `foundation`, write "Foundation"; otherwise write the specific program/funder name]
**Grant Profile**: [Path to profile if provided, otherwise "None supplied"]
**Saved Review Plan**: [Path to plan if provided, otherwise "None supplied"]

---

## Context and Assumptions

- Requested target program: [...]
- Effective target program: [...]
- Call-specific profile used: [yes/no]
- Saved review plan used: [yes/no]
- Review execution mode: [`plan-driven` or `fallback-standing-panel`]
- Profile freshness warning: [...]
- Profile ambiguity warning: [...]
- Proposal-indicated sponsor/call: [...]

---

## Panel Configuration

- Planning status: [saved plan used / planning skipped]
- Planning mode from saved plan: [...]
- Launched lenses: [ordered list of `label` (`lens_id`)]
- Selected but not launched from plan: [optional/excluded entries, if any]
- Organization-specific overlays honored: [...]
- Confirmation requirement from plan: [...]

---

## Overall Assessment

[3-4 sentences: What the proposal aims to do, its principal strength, and the single most critical issue that must be resolved before submission.]

**Preliminary Recommendation**: [Submit as-is | Revise before submitting | Substantial revision required | Do not submit in current form]

---
## Priority Action Items

Order the final action list by this hierarchy:

1. `adversarial-panel` or `significance-fit`
2. `methods-feasibility`
3. `internal-consistency`
4. `budget-team-operations`
5. `philanthropy-public-impact`
6. `ethics-philosophy`
7. `clarity-compliance`

If a lens was not launched, skip that tier rather than fabricating it.

**CRITICAL** (must fix - these could sink the proposal in panel review):
1. ...
2. ...
3. ...

**MAJOR** (should fix - these are likely to weaken scores materially):
4. ...
5. ...
6. ...
7. ...

**MINOR** (polish - improves reviewer confidence and readability):
8. ...
9. ...
10. ...

---

## Call Profile Summary

[If a profile was provided, summarize the most important call-specific criteria, constraints, and priorities that shaped the review. If no profile was provided, say so explicitly.]

---

## Lens Reviews

[Include each launched reviewer output in execution order, preserving the per-lens headings.]

---
```

After saving, report to the user:

1. the full path to the saved report
2. the preliminary recommendation from the consolidated review
3. the launched lenses
4. the top 5 priority action items
5. how many issues were flagged in each category
6. whether the review used a call-specific profile or only the generic sponsor archetype
7. whether the review used a saved review plan or the fallback standing panel

If `CREATED_REVIEW_INPUT = true` for this run, delete `_review_input.txt`.
