# PAP Review

## Workflow

### `review-pap`

Pre-analysis plan review for registry or journal-facing submissions.

Examples:

```text
/review-pap
/review-pap OSF
/review-pap PsychSci path/to/pap.docx
```

Supported targets:

- `OSF`
- `AsPredicted`
- `ClinicalTrials`
- `ISRCTN`
- `PsychSci`
- `JNeurosci`
- `NatureNeuro`
- `eLife`
- `NatureHB`
- `PNAS`
- `NeuroImage`
- `CommsPsych`
- `PLoSCB`
- `top-journal`
- `working-paper`

Supporting files it can inspect:

- power calculations
- survey instruments
- randomization protocols
- code skeletons
- mock tables
- data dictionaries
- ethics materials

Output:

- `review/paps/pap-review--<pap-slug>--YYYY-MM-DD.md`

If that filename already exists, the workflow appends `-v2`, `-v3`, and so on.

Supported PAP inputs:

- `.md`
- `.txt`
- `.tex`
- `.pdf`
- `.docx`
