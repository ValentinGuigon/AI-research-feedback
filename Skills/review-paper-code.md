---
name: review-paper-code
description: Review research code for reproducibility and quality, extract the paper's main empirical claims, compare paper to code, and write a constructive markdown report. Designed for psychology and neuroscience projects with papers in any supported format and Python, R, MATLAB, or BIDS pipeline code.
user-invocable: true
argument-hint: [optional: path/to/paper] [optional: path/to/code_dir] [optional: main|full]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Review Paper Code

Review a research project's paper and code for reproducibility, code quality, and paper-code alignment. Be constructive, concrete, and calibrated. Treat gaps as items to verify, not accusations.

## Scope

This skill supports:
- Papers in supported formats: LaTeX (`.tex`), Markdown (`.md`), PDF (`.pdf`), and Word (`.docx`)
- Python (`.py`), R (`.R`, `.r`), MATLAB (`.m`), notebook (`.ipynb`), shell (`.sh`), and BIDS pipeline code

Default review depth:
- `main`: prioritize the main paper, main scripts, and core outputs
- `full`: inspect all detected code files in scope

If no depth is provided, default to `main`.

## Phase 1: Discover the Project

First parse `$ARGUMENTS`:
- If one argument looks like a `.tex`, `.md`, `.pdf`, or `.docx` path, use it as `PAPER_FILE`.
- If one argument looks like a directory path, use it as `CODE_DIR`.
- If one argument is `main` or `full`, use it as `REVIEW_DEPTH`.

If any of the above are missing, auto-detect them.

### 1. Find the paper

After parsing the file path, detect the paper format and set `INPUT_MODE` plus a cleanup flag `CREATED_REVIEW_INPUT = false`.

If a file path was provided:

1. Detect the extension: `.tex`, `.md`, `.pdf`, or `.docx`.
2. If the extension is unrecognized, halt and tell the user: "Unsupported file format. Supported formats: .tex, .md, .pdf, .docx."

If no file path was provided, auto-detect in this priority order:

1. First, look for a `.tex` file containing `\documentclass`.
2. Then look for root-level `.md` files, preferring `main.md`, then `paper.md`, then the alphabetically first `.md` file in the root.
3. Then look for a single `.pdf` in the root directory.
4. Then look for a single `.docx` in the root directory.
5. If nothing is found, halt and tell the user that you searched for: a `.tex` main document in the current directory tree (excluding `_minted-*` and build output folders), root-level `.md` files (preferring `main.md` or `paper.md`), a single root-level `.pdf`, and a single root-level `.docx`.

If the resolved input is `.tex`, set `INPUT_MODE = "latex"` and keep the existing logic exactly:

1. Use Glob to search for `**/*.tex`, excluding obvious build folders such as `_minted-*`, `build/`, `output/`, `.git/`, `node_modules/`.
2. Identify the main paper file as the best candidate containing `\documentclass` or `\begin{document}`.
3. If multiple candidates exist, prefer:
   1. A path explicitly provided in `$ARGUMENTS`
   2. A file in `Writing/`, `writing/`, `Paper/`, `paper/`, `Draft/`, or the repo root
   3. The file that appears to include the most component files via `\input{}` / `\include{}`

If the resolved input is `.md`, set `INPUT_MODE = "plain"` and:

1. Read the Markdown file directly.
2. Write its contents unchanged to `_review_input.txt`.
3. Set `CREATED_REVIEW_INPUT = true`.

If the resolved input is `.pdf`, set `INPUT_MODE = "plain"` and:

1. Run: `pdftotext -layout "<path>" _review_input.txt`
2. If `pdftotext` is not available, run: `python3 -c "import pypdf; r=pypdf.PdfReader('<path>'); open('_review_input.txt','w').write('\n'.join(p.extract_text() for p in r.pages))"`
3. If both fail, halt and tell the user to install `pdftotext` (`poppler-utils`) or `pypdf`.
4. Set `CREATED_REVIEW_INPUT = true`.

If the resolved input is `.docx`, set `INPUT_MODE = "plain"` and:

1. Run: `pandoc "<path>" -t plain -o _review_input.txt`
2. If `pandoc` is not available, halt and tell the user to install pandoc.
3. Set `CREATED_REVIEW_INPUT = true`.

Record the result as `PAPER_FILE`.

### 2. Find the code

If `CODE_DIR` was not provided, look for likely code roots in this order:
- `Code/`
- `Analysis/`
- `code/`
- `analysis/`
- `scripts/`
- `src/`
- `programs/`
- `replication/`

If no single directory is clearly best, use the repo root and limit later discovery to likely code files.

Record the result as `CODE_DIR`.

### 3. Find code files

Within `CODE_DIR` and subdirectories, find:
- `**/*.py`
- `**/*.R`
- `**/*.r`
- `**/*.m`
- `**/*.ipynb`
- `**/*.sh`

Then search separately for BIDS and pipeline files:
- `dataset_description.json` (BIDS root marker)
- `participants.tsv`
- `**/*model*.json` and `**/*statsmodel*.json` (BIDS stats model files)
- `**/*_events.tsv` (up to 10; record count if more)
- Any files named `fmriprep*`, `fitlins*`, or located under `derivatives/fmriprep/` or `derivatives/fitlins/` (record presence, do not attempt to read all)

Record these as `BIDS_FILES` (present/absent for each category).

Exclude obvious caches, environments, and generated folders where appropriate.

If `REVIEW_DEPTH = main`, prioritize:
- Master scripts such as `main.py`, `run.py`, `run_all.py`, `run_analysis.py`, `main.R`, `run_all.R`, `main.m`, `run.sh`
- Files referenced by those scripts
- Files that generate tables, figures, or final datasets
- If no master script exists, select the most central files and cap the initial review set at a reasonable number

If `REVIEW_DEPTH = full`, include all detected code files.

Record:
- `CODE_FILES_ALL`
- `CODE_FILES_REVIEWED`
- `BIDS_FILES`
- languages present

### 4. Find supporting documentation

Look for:
- `README.md`, `README.txt`, `readme.md`
- `requirements.txt`, `environment.yml`, `pyproject.toml`
- `renv.lock`, `DESCRIPTION`

Record relevant files as available.

### 5. Handle ambiguity gracefully

If you find a paper and at least some code, continue even if discovery is imperfect.

Only stop if you cannot find either:
- a main paper file, or
- any relevant Python, R, MATLAB, notebook, shell, or BIDS pipeline code files

If you stop, tell the user briefly what was missing and what paths they can pass explicitly.

Before proceeding, tell the user:
- the paper file chosen
- the code directory chosen
- the number of code files detected and the number selected for review
- the review depth
- any ambiguity worth noting

## Phase 2: Read the Paper

If `INPUT_MODE = "latex"`, read `PAPER_FILE`.

Recursively read files referenced by:
- `\input{}`
- `\include{}`
- `\subfile{}`

If `INPUT_MODE = "plain"`, read `_review_input.txt` as the full paper content.

Extract a compact working summary for later cross-checking:
- Paper title
- Main research question
- Main sample description
- Main data sources
- Main dependent variables
- Main explanatory variables or treatments
- Study design type (experimental, observational, computational modeling, neuroimaging, or combination)
- Main task(s) or paradigm(s)
- If neuroimaging: acquisition type, key preprocessing choices stated in paper
- If computational modeling: model name/family, key parameters reported
- Statistical approach and any correction for multiple comparisons stated
- Main sample restrictions
- Main tables and figures only
- Headline quantitative claims only

Do not try to extract every statistic in the paper. Prioritize the main empirical design and the outputs most likely to map to code.

Store this as `PAPER_SUMMARY`.

## Phase 3: Launch 2 Agents in Parallel

In a single message, launch both agents using the Agent tool with `subagent_type: "general-purpose"`.

Each agent must produce a compact, high-signal output. Do not ask for exhaustive per-file prose on every file unless the project is very small.

---

### AGENT A: Code Reproducibility and Quality

Store as `CODE_REVIEW_SUMMARY`.

Prompt:

> You are reviewing research code for reproducibility and code quality in a psychology or neuroscience project.
>
> Files in scope:
> - Reviewed code files: [insert `CODE_FILES_REVIEWED`]
> - README / documentation files: [insert discovered supporting files or "none found"]
> - BIDS files: [insert `BIDS_FILES`]
>
> Review the files and produce a compact report focused on the most decision-relevant findings.
>
> Check:
> 1. Hardcoded absolute paths or machine-specific assumptions
> 2. Randomized procedures without an obvious seed in local or upstream execution context
> 3. Outputs that appear to be consumed but not obviously generated in the reviewed pipeline
> 4. Data inputs and whether path conventions are consistent
> 5. Dependency management and software requirements
> 6. Run order and presence of a master script or documented pipeline
> 7. Large commented-out blocks, weak script structure, or hard-to-follow long files
> 8. Opaque transformations, unexplained filters, recodes, merges, or thresholds that are important for interpretation
> 9. **BIDS compliance** (if `BIDS_FILES` indicates a neuroimaging project): Is a `dataset_description.json` present at the root? Are event files (`*_events.tsv`) present for task-based fMRI? Is the BIDS stats model JSON (`*model*.json`) present and does it specify contrasts? Flag absent required files as MISSING.
> 10. **Computational model code** (if Python or MATLAB files implement a behavioral or neural model): Are fitting functions and model comparison scripts present? Is there a parameter recovery script (simulation from known parameters to verify identifiability)? Are priors stated for Bayesian models? Flag absent components as MISSING or VERIFY as appropriate.
>
> Use these labels:
> - PASS: looks solid
> - NOTE: minor improvement opportunity
> - VERIFY: worth human confirmation before treating as a problem
> - MISSING: expected project support file or documentation is absent
>
> Output exactly these sections:
>
> ## Overall
> 3-6 bullets on the overall state of the codebase.
>
> ## Top Findings
> Up to 10 items total, ordered by importance.
> Format each item as:
> - [LABEL] Short finding title — file(s): line reference(s) if available — why it matters — what to check next
>
> ## Strengths
> 3-8 bullets with genuine positives.
>
> ## Reproducibility Checklist
> One line each for:
> - Relative paths
> - Random seed practice
> - Outputs generated by pipeline
> - Dependency management
> - Run order
> - README / documentation
>
> Use this format:
> - Check name: PASS / NOTE / VERIFY / MISSING — brief note
>
> ## File Notes
> Include brief notes only for files that have a VERIFY, NOTE, or especially strong positive signal.
> Use at most 1-3 bullets per file.
>
> Be calibrated. If something might be handled in an upstream script, say so.

---

### AGENT B: Paper-to-Code Mapping

Store as `MAPPING_SUMMARY`.

Prompt:

> You are mapping a research paper's main empirical claims to its code implementation.
>
> Inputs:
> - Paper summary: [insert `PAPER_SUMMARY`]
> - Reviewed code files: [insert `CODE_FILES_REVIEWED`]
> - Code directory: [insert `CODE_DIR`]
>
> Read the code files as needed and identify whether the paper's core empirical design appears in the code.
>
> Focus on the main paper elements only:
> 1. Main tables and figures
> 2. Main variables and treatments
> 3. Main sample restrictions and time period
> 4. Main estimation methods
> 5. Contrasts or conditions of interest as stated in the paper
> 6. Main datasets, intermediate analysis files, or BIDS derivatives
> 7. **BIDS stats model alignment** (if applicable): Do the contrasts defined in the BIDS stats model JSON match the contrasts reported in the paper? Flag any contrast in the paper with no corresponding entry in the model file, and any model contrast not mentioned in the paper.
> 8. **Computational model alignment** (if applicable): Does the model implemented in code match the model described in the paper? Check: number of free parameters, parameter names, likelihood function or loss, fitting algorithm, and any model comparison procedure.
>
> Use these confidence labels:
> - HIGH: clear and specific match
> - MEDIUM: plausible match but not airtight
> - LOW: weak or indirect match
> - NOT FOUND: no plausible match found in reviewed files
>
> Output exactly these sections:
>
> ## Verified Matches
> Up to 10 bullets.
> Format:
> - Paper element -> Code evidence -> HIGH / MEDIUM -> brief note
>
> ## Items To Verify
> Up to 12 bullets.
> Format:
> - Paper element -> Code evidence or absence -> LOW / NOT FOUND / MEDIUM -> why this deserves a check
>
> ## Likely Discrepancies
> Only include items where paper and code appear to point in different directions.
> Use up to 8 bullets.
>
> ## Coverage Notes
> 3-6 bullets on what was easy to match, what was ambiguous, and what may sit outside the reviewed files.
>
> Be conservative. Do not mark a match HIGH unless the specification, output, or variable mapping is genuinely clear.

## Phase 4: Synthesize

After both agents return, synthesize the results yourself.

Do not launch another critic agent by default. Instead:
- compare the two outputs for agreement and tension
- downgrade any overconfident claims
- note where limited file coverage or naming ambiguity weakens confidence

If the repo is unusually complex and a second-pass critic is truly necessary, you may launch one additional agent. Otherwise, keep the workflow lean.

Create:
- `OVERALL_ASSESSMENT`: 2-4 sentences leading with what works
- `TOP_ACTIONS`: 3-8 concrete next steps, ordered by importance
- `MATCHED_ITEMS`: high-confidence paper-code matches
- `VERIFY_ITEMS`: gaps or ambiguous matches worth checking
- `NOT_FOUND_ITEMS`: important paper elements with no plausible code match in reviewed files

## Phase 5: Write the Report

Write the final report to the current working directory as:
- `code_review_report.md`

Use this structure:

```markdown
# Code Review Report: [Paper Title]

*Reviewed: [today's date] | Languages: [languages found] | Depth: [REVIEW_DEPTH] | Paper: [PAPER_FILE filename]*

## Overall Assessment

[2-4 sentences. Lead with strengths. Then summarize the main reproducibility or alignment issues worth checking.]

## What's Working Well

- [Specific positive]
- [Specific positive]
- [Specific positive]

## Reproducibility Checklist

| Check | Status | Details |
|---|---|---|
| Relative file paths | [PASS / NOTE / VERIFY / MISSING] | [...] |
| Random seed practice | [PASS / NOTE / VERIFY / MISSING] | [...] |
| Outputs generated by pipeline | [PASS / NOTE / VERIFY / MISSING] | [...] |
| Dependency management | [PASS / NOTE / VERIFY / MISSING] | [...] |
| Run order documented | [PASS / NOTE / VERIFY / MISSING] | [...] |
| README / documentation | [PASS / NOTE / VERIFY / MISSING] | [...] |

## Code Quality Summary

[Short prose summary grouped by module, pipeline stage, or only the files with notable findings. Do not force one paragraph per file if the project is large.]

## Paper-Code Consistency

### Matched
- [High-confidence match]

### Items To Verify
- [Paper element] — [what the paper says] — [what the code appears to do] — [why it is worth checking] — [specific suggested next step]

### Not Found In Reviewed Files
- [Important paper element] — [brief note]

## Suggested Next Steps

1. ...
2. ...
3. ...

## Appendix: Compact Evidence

### Code Review Summary
[Paste `CODE_REVIEW_SUMMARY`]

### Paper Summary
[Paste the compact `PAPER_SUMMARY`]

### Mapping Summary
[Paste `MAPPING_SUMMARY`]
```

Keep the final report readable. Prefer concise, high-signal summaries over exhaustive dumps.

## Final User Message

After writing the report, tell the user:
- that the code review is complete
- that the report was written to `code_review_report.md`
- the `Overall Assessment`
- 3-5 bullets from `What's Working Well`
- the top 3 suggested next steps

If `CREATED_REVIEW_INPUT = true` for this run, delete `_review_input.txt`.
