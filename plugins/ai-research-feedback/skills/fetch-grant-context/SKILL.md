---
description: Fetch, normalize, and cache the requirements for a specific grant call into a reusable local profile
---

You are building a reusable local grant-context profile for one specific funding opportunity. Your job is to fetch the relevant source materials, extract the real requirements and review criteria, infer the best sponsor archetype, and save a normalized profile that downstream grant-review agents can consume.

## Goal

Produce a local sidecar cache for one exact grant call so proposal reviews can use:

- a stable sponsor archetype
- plus call-specific instructions and evidence

This workflow writes the profile that `review-grant` should consume later.

## Phase 1: Parse Arguments and Resolve Output Location

Parse `$ARGUMENTS` as follows:

- Accept one required grant identifier:
  - a URL
  - a local PDF path
  - a local folder path containing call materials
  - or a free-text grant/program name to search for online
- Accept an optional output override in either of these forms:
  - `slug=<slug>`
  - `out=<path>`
- Accept an optional sponsor override:
  - `mode=NSF`
  - `mode=NIH`
  - `mode=ERC`
  - `mode=HorizonEurope`
  - `mode=major-funder`
  - `mode=foundation`

Resolution rules:

1. If `out=<path>` is provided, use that exact directory.
2. Otherwise, create the profile under:
   - `review/grants/<slug>/`
3. If `slug=<slug>` is not provided, derive a slug from the grant/program name or source title:
   - lowercase
   - letters, numbers, and hyphens only
   - concise but recognizable

Always plan to write:

- `profile.json`
- `sources.md`

Optionally write:

- `raw/` for raw extracts or downloaded source files

If a target directory already exists, update its contents rather than creating a parallel duplicate.

## Phase 2: Gather Source Materials

Retrieve the most authoritative materials you can access. Prioritize primary sources over summaries.

Target sources include:

1. Main call page or program page
2. Official solicitation or guidelines PDF
3. FAQ or sponsor help page
4. Eligibility page
5. Budget rules or allowable-cost guidance
6. Submission instructions and required attachments
7. Deadline page or schedule page

When the input is a free-text program name:

- search for official sources first
- prefer sponsor-owned domains
- avoid third-party summaries unless no primary source is available

When the input is a local PDF or folder:

- treat those local files as primary sources
- still search for companion official web pages if clearly needed for missing pieces such as FAQs or deadlines

## Phase 3: Extract and Normalize Grant Context

From the gathered materials, extract the following:

- grant name
- sponsor
- program name
- cycle/year if stated
- deadlines
- eligibility constraints
- required application documents
- budget caps, budget logic, or budget restrictions
- explicit review criteria
- stated reviewer groups, partner reviewers, or external-review organizations
- program priorities and mission language
- deliverable or reporting expectations
- theory of change / public value / broader impacts expectations if present
- governance, ethics, openness, or responsible-innovation expectations if present
- unclear, missing, or conflicting requirements

Classify the call into one `base_funder_mode`:

- `NSF`
- `NIH`
- `ERC`
- `HorizonEurope`
- `major-funder`
- `foundation`

Use the explicit sponsor identity where possible. Use `major-funder` or `foundation` only when a more specific built-in archetype does not apply. If `mode=...` was provided in the arguments, treat that as an override and record the override in the profile notes.

## Phase 4: Preserve Provenance

For each important fact you store, keep enough provenance that a later reviewer can verify where it came from.

Distinguish:

- explicit requirements stated in the source materials
- reasonable inferences needed to make the profile usable

If something is inferred rather than stated directly, say so explicitly in:

- `risks_and_ambiguities`
- `source_evidence`

## Phase 5: Write `profile.json`

Write `profile.json` using the schema at:

- `templates/grants/profile.schema.json` when that file exists in the current workspace

If the schema file is not present, still write `profile.json` using the required field contract described in this skill.

Populate all required fields. If a field is unknown:

- use `null` only where the schema permits it
- otherwise write an empty array or a short explanatory note

Required guidance for key fields:

- `profile_version`: set to `1.0`
- `source_urls`: include local file paths as strings when local files are primary sources
- `fetched_at`: use today's date
- `expires_after_days`: use a conservative default such as `14` unless the source suggests a better refresh interval
- `manual_review_required`: set `true` when important details are missing, conflicting, or inferred
- `reviewer_brief`: write a concise, high-signal summary that downstream review agents can consume directly
- `reviewer_ecosystem`: record declared reviewer groups, inferred reviewer groups, recommended expert lenses, and any organization-specific overlays
- `theory_of_change_expectations`: capture public-value, impact-pathway, or philanthropy-facing expectations when present
- `governance_and_ethics_expectations`: capture responsible-AI, governance, legitimacy, fairness, or openness expectations when present
- `source_evidence`: include short evidence entries for major facts such as criteria, deadlines, budget rules, and required components

## Phase 6: Write `sources.md`

Write a human-readable provenance file at `sources.md`.

Include:

- grant name
- output directory
- fetch date
- inferred `base_funder_mode`
- all source URLs or local files consulted
- what each source contributed
- any important missing information
- any places where the profile contains inference rather than explicit source language

## Phase 7: Final Validation

Before finishing:

1. Re-open `profile.json`
2. Check it against `templates/grants/profile.schema.json` when available; otherwise validate required fields manually
3. Verify that the most important reviewer inputs are present:
   - `base_funder_mode`
   - `review_criteria`
   - `required_documents`
   - `budget_rules`
   - `program_priorities`
   - `reviewer_ecosystem` when reviewer groups are discoverable
   - `reviewer_brief`
4. If any are weak or missing, improve the profile before stopping

## Output to the User

Report:

1. The path to the saved profile
2. The inferred `base_funder_mode`
3. The most important review criteria captured
4. Any important ambiguities or missing information
5. Whether manual review is recommended before using the profile

## Quality Rules

- Prefer official sponsor materials over summaries
- Prefer one normalized cached profile over repeated browsing by downstream review agents
- Be explicit about uncertainty
- Do not invent review criteria that are not supported by the source materials
- Keep the profile reusable across multiple revisions of the same proposal
