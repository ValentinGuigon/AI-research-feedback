---
description: Run a fast 2-agent pre-submission check for a psychology or neuroscience paper — focuses on contribution, design credibility, and causal overclaiming. Completes in ~1 minute.
---

You are coordinating a fast pre-submission check of an academic paper in psychology or neuroscience. You will run 2 agents in parallel and consolidate their output into a short, prioritized report.

## Phase 1: Discover the Paper

Parse `$ARGUMENTS` for a file path. Detect the paper format and set `INPUT_MODE`
plus a cleanup flag `CREATED_REVIEW_INPUT = false`.

If a file path was provided:

1. Detect the extension: `.tex`, `.md`, `.pdf`, or `.docx`.
2. If the extension is unrecognized, halt and tell the user: "Unsupported file
   format. Supported formats: .tex, .md, .pdf, .docx."

If no file path was provided, auto-detect in this priority order:

1. First, look for a `.tex` file containing `\documentclass`.
2. Then look for root-level `.md` files, preferring `main.md`, then `paper.md`,
   then the alphabetically first `.md` file in the root.
3. Then look for a single `.pdf` in the root directory.
4. Then look for a single `.docx` in the root directory.
5. If nothing is found, halt and tell the user that you searched for: a `.tex`
   main document in the current directory tree (excluding `_minted-*` and build
   output folders), root-level `.md` files, a single root-level `.pdf`, and a
   single root-level `.docx`.

If the resolved input is `.tex`, set `INPUT_MODE = "latex"` and keep the
existing logic exactly:

1. Use Glob with pattern `**/*.tex` to list all .tex files (exclude `_minted-*`,
   `build/`, `output/`).
2. Identify the main document: the .tex file containing `\documentclass` or
   `\begin{document}`.
3. Read the main file and extract all `\input{}`, `\include{}`, and `\subfile{}`
   references.
4. Read all component .tex files.
5. Use Glob to find table files: `**/Tables/**/*.tex`, `**/tables/**/*.tex`,
   root-level `*table*.tex`.

If the resolved input is `.md`, set `INPUT_MODE = "plain"` and:

1. Read the Markdown file directly. No component resolution is needed.
2. Write its contents unchanged to `_review_input.txt`.
3. Set `CREATED_REVIEW_INPUT = true`.

If the resolved input is `.pdf`, set `INPUT_MODE = "plain"` and:

1. Run: `pdftotext -layout "<path>" _review_input.txt`
2. If `pdftotext` is not available, run:
   `python3 -c "import pypdf; r=pypdf.PdfReader('<path>'); open('_review_input.txt','w').write('\n'.join(p.extract_text() for p in r.pages))"`
3. If both fail, halt and tell the user to install `pdftotext` (`poppler-utils`)
   or `pypdf`.
4. Set `CREATED_REVIEW_INPUT = true`.

If the resolved input is `.docx`, set `INPUT_MODE = "plain"` and:

1. Run: `pandoc "<path>" -t plain -o _review_input.txt`
2. If `pandoc` is not available, halt and tell the user to install pandoc.
3. Set `CREATED_REVIEW_INPUT = true`.

Record:
- If `INPUT_MODE = "latex"`: full path of each `.tex` file and its role in the
  paper
- If `INPUT_MODE = "plain"`: the path `_review_input.txt`
- Paper title, authors, and abstract (from `.tex` for LaTeX inputs, or
  best-effort from the extracted text for non-LaTeX inputs)

## Phase 2: Launch 2 Agents in Parallel

In a **single message**, launch both agents using the Agent tool with
`subagent_type: "general-purpose"`. If `INPUT_MODE = "latex"`, pass the list of
`.tex` file paths as currently specified in each agent prompt. If
`INPUT_MODE = "plain"`, pass `_review_input.txt` as the single content file;
where any agent prompt says `[LIST ALL TEX FILE PATHS HERE]`, replace that
instruction with: "The paper has been extracted to `_review_input.txt`. Read
that file as the full paper content. There are no separate component files."

---

### AGENT A — Contribution, Identification & Required Analyses

You are a demanding associate editor at a top psychology or neuroscience journal. Read all content files completely. Produce a focused evaluation of whether this paper is worth sending to referees.

**Part 1 — The Central Contribution**

- State in one sentence what the paper claims to contribute.
- Is this finding genuinely new, or is it a replication of known results in a
  new setting or population?
- What is the closest prior paper? What does this paper add beyond it?
- Does this finding change how researchers in the field think about the topic,
  or does it add a data point to an already-settled question?
- Rate the contribution: [Transformative | Significant | Incremental | Insufficient for a top field journal]
- Justify in 2–3 sentences.

**Part 2 — Design and Credibility**

- What is the design (experimental, quasi-experimental, observational,
  computational modeling, neuroimaging)? Is it appropriate for the central
  claim?
- What are the main threats to internal validity? Are confounds controlled,
  randomized, or left unaddressed?
- If the paper uses computational modeling: are the model assumptions stated,
  is parameter recovery demonstrated, and are alternative models compared?
- If the paper uses fMRI or other neuroimaging: are preprocessing choices
  justified, is the multiple comparisons correction appropriate, and are ROI
  definitions pre-specified or exploratory?
- Is the main finding causal, correlational, or descriptive? Does the paper
  claim the right thing?
- What would a skeptical reviewer with deep methods expertise in this area say
  at a conference?

**Part 3 — Required Analyses**

List up to 5 analyses whose absence is a blocker for acceptance. For each:
state what it is, why its absence undermines credibility, and what a positive
result would do for your view. If nothing is missing, write "None — the paper
adequately addresses the main design and evidentiary concerns."

Tag each required analysis `[CRITICAL]`.

**Part 4 — Pointed Questions to the Authors**

Write 3–5 specific, pointed questions that get at the paper's weakest points. Frame them as a referee would.

**Output format:**

```
## Agent A: Contribution & Identification

### Part 1 — Central Contribution
[assessment + rating]

### Part 2 — Identification and Credibility
[assessment]

### Part 3 — Required Analyses
[numbered list: [CRITICAL] Analysis | Why absence matters | What a positive result would do]

### Part 4 — Questions to the Authors
[numbered list of 3–5 questions]
```

The .tex files to review are: [LIST ALL TEX FILE PATHS HERE]

---

### AGENT B — Causal Overclaiming & Unsupported Claims

You are a skeptical methodologist enforcing "claim discipline." Read all content
files and flag every place where the paper overstates its evidence.

**What to check:**

1. **Causal language without causal warrant**: Flag every specific sentence
   where causal language ("causes", "leads to", "drives", "determines", "because
   of", "due to", "results in") is applied to findings from correlational,
   observational, or cross-sectional designs. Also flag: (a) claims that neural
   activation "reflects", "underlies", or "drives" a cognitive process when only
   a correlation is shown; (b) between-group comparisons framed causally when
   participants were not randomly assigned; (c) claims that a computational model
   "reveals" a mechanism rather than fits a behavioral pattern. Quote the exact
   sentence and explain why the language exceeds what the design supports.

2. **Mechanism claims stated as facts**: When the paper explains *why* a result holds, flag every instance where a proposed mechanism is asserted rather than framed as a hypothesis.

3. **Generalization beyond the sample**: Claims that extend findings beyond the
   data's scope without adequate caveats. Flag: (a) WEIRD population concerns
   when the sample is narrow and claims are broad; (b) generalization from
   patient populations to healthy individuals or vice versa without explicit
   justification; (c) extrapolation from a single lab task to naturalistic
   behavior or real-world outcomes; (d) claims about stable individual traits
   based on single-session measurements.

4. **Missing caveats and design confounds**: Places where a reader would
   naturally ask "but what about...?" and the paper doesn't address it. Focus on
   the most obvious threats for the specific design: demand characteristics; order
   and practice effects in within-subject designs; absence of manipulation checks;
   underpowered sample; multiple comparisons without correction or
   pre-registration; consequential but undisclosed preprocessing choices in
   neuroimaging; model identifiability concerns for computational models.

5. **Statistical vs. practical significance**: Flag: (a) key comparisons where
   effect size estimates (Cohen's d, partial eta-squared, Bayes factors, or
   equivalent) are absent; (b) null results presented as evidence of absence
   without power analysis or equivalence testing; (c) "statistically significant"
   used as if it means "large" or "clinically meaningful."

6. **Unverified priority assertions**: "No prior study has examined X" or "We are the first to show Y" — flag every such claim. Authors must verify before submission.

Tag every issue `[CRITICAL]`, `[MAJOR]`, or `[MINOR]`.

**Output format:**

```
## Agent B: Causal Overclaiming & Unsupported Claims

### Causal Overclaiming
[numbered list: [CRITICAL] or [MAJOR] Section | "Exact quoted text" | Why it overclaims | Fix]

### Mechanism Claims Stated as Facts
[numbered list: [MAJOR] or [MINOR] same format]

### Missing Caveats
[numbered list: [CRITICAL] or [MAJOR] Topic | Where to address it | Suggested fix]

### Other Issues
[numbered list: [MAJOR] or [MINOR] same format]
```

The .tex files to review are: [LIST ALL TEX FILE PATHS HERE]

---

## Phase 3: Consolidate and Save

After both agents return, consolidate into a single report.

Check whether `QUICK_REVIEW_[YYYY-MM-DD].md` already exists. If so, append `-v2` (or `-v3`, etc.).

Save to: `QUICK_REVIEW_[YYYY-MM-DD].md`

**Report structure:**

```markdown
# Quick Pre-Submission Check

**Paper**: [Title]
**Authors**: [Authors]
**Date**: [Today's date]

---

## Overall Assessment

[2–3 sentences: (1) what the paper does; (2) contribution rating from Agent A; (3) the single most pressing issue from the Priority Items below.]

**Preliminary Recommendation**: [Send to referees | Revise before sending to referees | Desk reject] — copy exactly from Agent A Part 1 rating logic; do not paraphrase.

---

## 1. Contribution & Identification

[Agent A output]

---

## 2. Causal Overclaiming & Unsupported Claims

[Agent B output]

---

## Priority Action Items

Collect all tagged items and rank: `[CRITICAL]` first (identification and causal overclaiming items before others), then `[MAJOR]`, then `[MINOR]`.

**CRITICAL** (could cause desk rejection or major objections):
1. ...

**MAJOR** (will likely be raised by referees):
4. ...

**MINOR** (polish):
8. ...
```

After saving, report to the user:
1. Path to the saved report
2. Preliminary recommendation
3. Top 3 priority action items
4. Issue counts by severity

If `CREATED_REVIEW_INPUT = true` for this run, delete `_review_input.txt` after saving the report.
