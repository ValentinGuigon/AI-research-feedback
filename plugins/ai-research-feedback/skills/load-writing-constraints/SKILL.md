---
description: Load explicit and inferred post-review writing constraints for one source document and save a deterministic writing-constraints artifact
---

You are coordinating the shared writing-constraints stage that sits between completed review and any object-specific contextualization or drafting work.

Your job is to gather the governing writing rules for one source document, normalize them into a deterministic `writing-constraints.json` artifact, and preserve provenance so later stages can distinguish explicit requirements from carefully bounded inference.

## Goal

Produce a schema-conformant writing-constraints artifact that:

- captures explicit writing requirements from the source materials and nearby context
- records high-confidence inferred constraints when the format or package implies them
- separates hard constraints from soft preferences
- remains generic across grants, papers, PAPs, and paper-code workflows

This skill defines the shared constraints-loading contract only. It does not contextualize revisions and it does not draft edits.

## Runtime Rules

- Work from local repository files only.
- Produce exactly one writing-constraints artifact for one source document per run.
- Treat explicit evidence as higher priority than inference.
- Record provenance for every material constraint decision.
- Keep object-specific interpretation shallow here; deep localization belongs to later stages.
- Do not invent sponsor, journal, registry, or user rules that are not evidenced or clearly inferred.

## Phase 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- Optional document-type arguments:
  - `type=grant`
  - `type=paper`
  - `type=pap`
  - `type=paper-code`
- Optional source argument:
  - `source=<path>`
- Optional review arguments:
  - `review=<path>`
  - `reviews=<path1,path2,...>`
- Optional context arguments:
  - `profile=<path>`
  - `guidelines=<path1,path2,...>`
  - `instructions=<path>`
- Remaining unresolved path-like token should be treated as the source document path when `source=` is absent

Resolution rules:

1. Resolve all supplied paths to absolute local paths.
2. If `source=` is absent, infer the source path from the remaining path-like token or stop and report that a source document is required.
3. If `type=` is supplied, use it as `DOCUMENT_TYPE`.
4. If `type=` is absent, infer `DOCUMENT_TYPE` from the source path, nearby review folders, and any supplied profile path using only:
   - `grant`
   - `paper`
   - `pap`
   - `paper-code`
5. If the document type cannot be resolved confidently, stop and report the ambiguity instead of guessing.
6. Treat `REVIEW_PATHS`, `GUIDELINE_PATHS`, `PROFILE_PATH`, and `INSTRUCTIONS_PATH` as optional supporting inputs rather than required inputs.

Store:

- `DOCUMENT_TYPE`
- `SOURCE_DOCUMENT_PATH`
- `REVIEW_PATHS`
- `GUIDELINE_PATHS`
- `PROFILE_PATH`
- `INSTRUCTIONS_PATH`

## Phase 2: Validate Inputs And Contract

1. Confirm that `SOURCE_DOCUMENT_PATH` exists and is a local file.
2. Confirm that every optional supporting path that was supplied exists before using it.
3. Sort all multi-path inputs lexicographically after absolute-path resolution for deterministic output.
4. Read `templates/editing/writing-constraints.schema.json` when it exists and treat it as the controlling artifact contract.
5. Validate that the schema requires at minimum:
   - `artifact_version`
   - `document_type`
   - `source_document_path`
   - `generated_at`
   - `constraints`
   - `constraint_sources`

If the schema file is missing, still produce the artifact using the contract described in this skill.

## Phase 3: Read Constraint Sources

Collect writing constraints from the strongest available local materials in this order:

1. the source document itself
2. explicit user instructions supplied as a file
3. call, journal, registry, or package guideline files supplied locally
4. grant profile files when present
5. review artifacts only when they contain clear constraint statements rather than general criticism
6. tightly bounded inference from document type, visible structure, and directly evidenced workflow context

Read enough to recover:

- length or format caps
- required sections or required component mentions
- ordering rules
- audience expectations
- style or tone expectations
- non-negotiable truth constraints
- any explicit prohibition against unsupported additions or structural drift

If the source document is not directly readable in the current local environment:

- continue with the strongest explicit local materials that are available
- prefer supplied instructions, guidelines, grant profiles, and clear review-stated rules over inference
- use bounded inference only when concrete local evidence supports it
- record that source-document extraction was unavailable in `constraint_sources` if that materially shaped the result

This fallback is allowed so the shared constraints stage can still produce a deterministic artifact without pretending to have exact source-local formatting evidence it could not read.

## Phase 4: Normalize The Constraint Buckets

Populate `constraints` with all required buckets:

- `length_limits`
- `required_sections`
- `ordering_rules`
- `style_requirements`
- `audience`
- `hard_constraints`
- `soft_preferences`

Normalization rules for each bucket:

### `length_limits`

Use objects with:

- `scope`
- `unit`
- `value`
- `strict`

Include `notes` when needed.

Use this bucket only for concrete limits such as:

- total word count
- page cap
- abstract length
- figure or table caps

Do not encode vague brevity advice here.

### `required_sections`

Use objects with:

- `name`
- `required`

Include `notes` when needed.

Use this bucket for sections or components that must appear or must be preserved.

### `ordering_rules`

Use concise strings for sequence constraints such as:

- required section order
- mandatory placement of summaries or broader impacts
- package ordering constraints across manuscript and supplement materials

### `style_requirements`

Use concise strings for format and style expectations such as:

- sponsor-language mirroring
- journal-style terseness
- plain-language accessibility for mixed review panels
- registration-style commitment clarity

### `audience`

Populate:

- `primary`
- `secondary`

Use the strongest directly supported audience framing available from the local materials.

### `hard_constraints`

Use strings for non-negotiable rules such as:

- do not add unsupported empirical claims
- preserve required headings
- stay within page cap
- avoid introducing methods not actually used

### `soft_preferences`

Use strings for meaningful but non-binding preferences such as:

- emphasize public benefit earlier
- keep prose accessible to non-specialists
- foreground novelty in the introduction

## Phase 5: Record Provenance

Every material constraint decision must be represented in `constraint_sources`.

Each source object must include:

- `source_type`
- `source_ref`
- `evidence`
- `explicit`

Allowed `source_type` values:

- `source-document`
- `review-report`
- `grant-profile`
- `call-material`
- `journal-guidelines`
- `registry-guidelines`
- `user-instruction`
- `inference`

Provenance rules:

- use `explicit = true` when the rule is stated directly in the source
- use `explicit = false` only for bounded inference
- every inference entry must explain what concrete evidence licensed the inference
- do not rely on undocumented background knowledge alone

At least one `constraint_sources` entry is required.

## Phase 6: Resolve Deterministic Output Path

Save under `review/editing/` using the normalized object folder for `DOCUMENT_TYPE`:

- `grant` -> `review/editing/grants/`
- `paper` -> `review/editing/papers/`
- `pap` -> `review/editing/paps/`
- `paper-code` -> `review/editing/paper-code/`

Derive `<source-slug>` from the source document filename:

- lowercase
- remove extension
- replace every run of non-alphanumeric characters with one hyphen
- trim leading and trailing hyphens

Default output path:

- `review/editing/<object-folder>/<source-slug>/writing-constraints.json`

If that file already exists and should be preserved, append `-v2`, `-v3`, and so on to the filename.

Versioning rule:

- first artifact: `writing-constraints.json`
- next preserved artifact: `writing-constraints-v2.json`
- then `writing-constraints-v3.json`

Store the final absolute path as `WRITING_CONSTRAINTS_OUTPUT_PATH`.

## Phase 7: Write The Artifact

Write one JSON artifact at `WRITING_CONSTRAINTS_OUTPUT_PATH` with at minimum:

- `artifact_version`: `1.0`
- `document_type`
- `source_document_path`
- `generated_at`: today's date in `YYYY-MM-DD`
- `constraints`
- `constraint_sources`

Include `review_paths` only when review artifacts were actually used as supporting sources.

Use absolute paths internally.

## Phase 8: Validate Before Stopping

Before reporting success:

1. Re-open the saved file and verify it parses as JSON.
2. Manually confirm that all top-level required fields from `templates/editing/writing-constraints.schema.json` are present.
3. Confirm `document_type` is one of:
   - `grant`
   - `paper`
   - `pap`
   - `paper-code`
4. Confirm `constraints` contains all required buckets.
5. Confirm `constraints.audience.primary` is populated.
6. Confirm `constraint_sources` is non-empty.
7. Confirm every `length_limits` entry contains:
   - `scope`
   - `unit`
   - `value`
   - `strict`
8. Confirm every `required_sections` entry contains:
   - `name`
   - `required`
9. Confirm every `constraint_sources` entry contains:
   - `source_type`
   - `source_ref`
   - `evidence`
   - `explicit`
10. Fix the artifact before stopping if any required field is missing or malformed.

## Phase 9: Report Back

After saving and validating, report:

1. the saved writing-constraints path
2. the resolved document type
3. the source document path
4. which supporting inputs were used
5. the strongest hard constraints recovered
6. any soft preferences that are likely to shape downstream drafting
7. which constraints were explicit versus inferred

## Non-Scope And Guardrails

This skill must not:

- emit a revision plan
- emit a contextualized edit plan
- draft replacement text
- rewrite the source document directly
- decide final local edit placement
- smuggle object-specific drafting logic into the shared constraints layer
- treat vague review preferences as hard constraints without evidence
