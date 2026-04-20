---
description: Plan a grant-specific review panel before proposal review and save the result as a reusable review plan
---

You are coordinating the planning step that sits between grant-context intake and full proposal review. Your job is to propose the right reviewer panel for this specific grant, record why each lens is included, and save a structured review plan that downstream review agents can execute.

## Goal

Produce a deterministic `review-plan.json` that translates:

- a base sponsor archetype
- a call-specific grant profile when available
- the actual proposal package

into:

- a selected set of expert lenses
- any organization-specific overlays
- a confirmation requirement

The planning step should be lightweight but explicit. It exists to avoid silently reviewing a grant with the wrong panel.

## Runtime Rules

- Work from local repository files only.
- Prefer deterministic behavior over speculative breadth.
- Keep the panel compact by default:
  - normally 4 to 6 `primary` lenses
  - use `secondary` only when a lens materially changes review coverage
- Reuse base lenses plus overlays instead of inventing new reviewer roles.
- Save exactly one JSON artifact for the run and validate it before stopping.

## Phase 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- Recognized built-in sponsor archetypes:
  - `NSF`
  - `NIH`
  - `ERC`
  - `HorizonEurope`
  - `major-funder`
  - `foundation`
- Optional profile arguments:
  - `profile=<path>`
  - `grant-profile=<path>`
- Optional plan mode:
  - `mode=standard`
  - `mode=fast`
  - `mode=high-stakes`
- Optional shorthand profile path:
  - if a token ends in `profile.json`, treat it as a profile path
- Remaining text is the proposal path

Resolution rules:

1. If the first token matches a built-in sponsor archetype, treat it as the requested sponsor archetype.
2. If a profile path is supplied, resolve it first and read it before finalizing defaults.
3. If no sponsor archetype is supplied, use `base_funder_mode` from the profile when available.
4. If neither arguments nor profile provide a sponsor archetype, default to `major-funder`.
5. If no planning mode is supplied, default to `standard`.
6. If no proposal path is supplied, auto-detect it using the proposal-discovery rules below.

Store:

- `REQUESTED_TARGET_PROGRAM`
- `EFFECTIVE_TARGET_PROGRAM`
- `PLANNING_MODE`
- `GRANT_PROFILE_PATH`
- `PROPOSAL_PATH`

## Phase 2: Load Registry And Optional Grant Profile

1. Read `templates/grants/expert-registry.json`.
2. Read `templates/grants/expert-registry.schema.json` when it exists.
3. Validate the registry before using it:
   - it must parse as JSON
   - it must contain `registry_version`, `updated_at`, and `expert_lenses`
   - every lens must contain:
     - `id`
     - `label`
     - `category`
     - `default_inclusion`
     - `selection_signals`
     - `core_questions`
     - `output_focus`
4. If `GRANT_PROFILE_PATH` is set:
   - read it as JSON
   - extract when present:
     - `grant_name`
     - `sponsor`
     - `program_name`
     - `base_funder_mode`
     - `manual_review_required`
     - `review_criteria`
     - `program_priorities`
     - `reviewer_brief`
     - `reviewer_ecosystem`
     - `theory_of_change_expectations`
     - `governance_and_ethics_expectations`
     - `risks_and_ambiguities`
5. If the profile path does not exist or the JSON cannot be parsed, stop and report the error instead of guessing.

## Phase 3: Resolve The Proposal And Supporting Files

Use the same minimal discovery contract documented for `review-grant`.

If a proposal path was supplied:

- resolve it to an existing local file
- use it as the main proposal

If no proposal path was supplied, auto-detect:

1. Search recursively for likely proposal files with common extensions:
   - `*.md`
   - `*.txt`
   - `*.tex`
   - `*.docx`
   - `*.pdf`
2. Exclude hidden folders, `.git`, dependency folders, build outputs, and cached review output folders.
3. Prefer filenames containing:
   - `proposal`
   - `project-description`
   - `research-plan`
   - `specific-aims`
   - `narrative`
   - `case-for-support`
   - `application`
4. If multiple candidates remain, prefer the document that appears to be the main narrative rather than only a budget, CV, appendix, or letter.

Then discover supporting files recursively near the proposal path and record files whose names suggest:

- budget or justification
- timeline, gantt, milestone, or workplan
- biosketch, CV, resume, personnel, or team
- data-management, facilities, resources, mentoring, support letter, or letter
- appendix, supplement, or supplementary

Save supporting files as objects with:

- `path`
- `role`

Sort supporting files by `role`, then by path, for deterministic output.

## Phase 4: Read Proposal Content

You need enough proposal text to infer the likely reviewer mix and summarize the project.

If the proposal is `.md`, `.txt`, or `.tex`:

- read it directly
- do not create a temp extraction file

If the proposal is `.pdf`:

- first try `pdftotext -layout "<path>" _review_input.txt`
- if that fails, use Python with `pypdf` to extract text into `_review_input.txt`
- if both fail, stop and report that proposal text extraction failed

If the proposal is `.docx`:

- try `pandoc "<path>" -t plain -o _review_input.txt`
- if that fails, stop and report that `pandoc` is required for `.docx` input

After extraction:

- read the extracted plain text
- keep `_review_input.txt` only as a temporary local artifact for this run
- delete `_review_input.txt` before finishing if you created it

From the proposal text, record:

- proposal title if obvious from the first page or heading
- a 2 to 4 sentence `proposal_summary`
- any named sponsor or program
- strong topic signals relevant to lens selection
- explicit mentions of:
  - AI
  - public benefit
  - open science
  - responsible AI
  - ethics, fairness, legitimacy, justice, or governance
  - partnerships, implementation, public sector, or systems change

## Phase 5: Build Deterministic Selection Signals

Create one normalized bag of lowercase text signals from:

- proposal summary and proposal text
- proposal filename
- supporting file names and roles
- `grant_name`
- `sponsor`
- `program_name`
- `reviewer_brief`
- `review_criteria`
- `program_priorities`
- `reviewer_ecosystem`
- `theory_of_change_expectations`
- `governance_and_ethics_expectations`

Then apply these rules in order:

1. Include all lenses whose `default_inclusion` is `always`.
2. For each conditional lens in registry order, mark it `selected` when any of these are true:
   - one of its `selection_signals` appears in the normalized signals
   - the profile's `reviewer_ecosystem.recommended_lenses` includes the lens id
   - its category is directly implicated by proposal/profile language even if the exact phrase differs
3. Mark a conditional lens `optional` instead of `selected` when:
   - it is plausible but weakly supported
   - omitting it would not materially reduce coverage
4. Do not emit `excluded` entries unless the user explicitly asked for a full registry audit.

Priority rules:

- `always` lenses are normally `primary`
- selected conditional lenses are `primary` only when they materially change review coverage
- otherwise selected conditional lenses are `secondary`

Rationale rules:

- every `panel_selection` entry must explain why the lens was chosen using proposal/profile evidence
- cite the strongest proposal or profile signals in prose, not raw keyword lists

Core-question rules:

- start from the registry's `core_questions`
- keep them unless a proposal/profile-specific adaptation is needed
- if adapting them, preserve the lens intent and keep the list concise

## Phase 6: Activate Organization-Specific Overlays

Organization overlays should extend a base lens, not replace it.

For every selected or optional lens that defines `organization_overlays`:

1. Check overlay `activation_signals` against the normalized signals.
2. Also activate overlays explicitly named in `reviewer_ecosystem.organization_overlays` when present.
3. Attach matching overlay ids to `organization_overlay_ids`.
4. Keep overlay ids sorted.

Special handling:

- If the profile sponsor is `Google.org`, expect `google-org-public-benefit` and `google-org-responsible-ai` to activate when the supporting signals are present.
- If `Centre for Public Impact` appears in the profile or reviewer ecosystem, activate `centre-for-public-impact` on the relevant public-impact lens when signals support it.

## Phase 7: Set Confirmation Requirement

Set `confirmation.required = true` when any of the following apply:

- `PLANNING_MODE` is `high-stakes`
- the profile says `manual_review_required = true`
- the reviewer ecosystem is inferred rather than clearly stated
- more than one organization-specific overlay is activated across the plan
- the proposal appears to target a mixed technical and public-impact panel

Set `confirmation.required = false` only when all of the following apply:

- `PLANNING_MODE` is `fast`
- confidence is high
- no major reviewer-ecosystem ambiguity remains
- the plan does not depend on unresolved sponsor-specific overlays

Set `confirmation.reason` to one concise sentence that explains the highest-salience trigger.

## Phase 8: Resolve Output Path

If `GRANT_PROFILE_PATH` is present:

- save next to it as `review-plan.json`

Otherwise:

1. Derive `PROPOSAL_SLUG` from the proposal filename:
   - lowercase
   - remove extension
   - letters, numbers, and hyphens only
2. Save under `review/` as:
   - `review-plan--<proposal-slug>--YYYY-MM-DD.json`

Use absolute paths internally. Save the artifact at the deterministic path required by the applicable rule above.

## Phase 9: Write `review-plan.json`

Write the plan using `templates/grants/review-plan.schema.json`.

Populate at minimum:

- `plan_version`: `1.0`
- `created_at`: today's date in `YYYY-MM-DD`
- `planning_mode`
- `proposal_path`
- `supporting_files`
- `effective_target_program`
- `grant_profile_path`
- `expert_registry_path`
- `proposal_summary`
- `panel_selection`
- `uncertainties`
- `confirmation`

`uncertainties` should include:

- any proposal ambiguities that affected lens selection
- any reviewer-ecosystem ambiguity
- any profile ambiguity that could change overlays or confirmation

Keep `panel_selection` compact. The normal target is:

- 4 always-on `primary` lenses
- plus 0 to 2 additional conditional lenses

## Phase 10: Validate Before Stopping

Before reporting success:

1. Re-open the saved file and verify it parses as JSON.
2. Manually validate that all top-level required fields from `templates/grants/review-plan.schema.json` are present.
3. Validate every `supporting_files` entry contains:
   - `path`
   - `role`
4. Validate every `panel_selection` entry contains:
   - `lens_id`
   - `label`
   - `status`
   - `rationale`
   - `priority`
   - `core_questions`
5. Validate:
   - `planning_mode` is one of `standard`, `fast`, `high-stakes`
   - `status` is one of `selected`, `optional`, `excluded`
   - `priority` is one of `primary`, `secondary`
   - `confirmation.required` is boolean
6. If any required field is missing or malformed, fix the JSON before reporting completion.

## Phase 11: Report Back

After saving and validating, report:

1. the saved plan path
2. the selected primary lenses
3. any organization-specific overlays
4. the main uncertainties
5. whether confirmation is required before running `review-grant`
6. which proposal path and profile path were used for the plan
