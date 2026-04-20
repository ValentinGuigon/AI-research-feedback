# Paper Review

## Workflows

### `review-paper`

Full referee-style paper review with journal-aware critique.

Examples:

```text
/review-paper
/review-paper PsychSci
/review-paper NatureNeuro path/to/paper.docx
```

Supported journal personas:

- `NatureNeuro`
- `Neuron`
- `eLife`
- `CurrBiol`
- `NatureHB`
- `PNAS`
- `PsychSci`
- `JNeurosci`
- `NeuroImage`
- `CerebCortex`
- `PLoSCB`
- `PLoSOne`
- `CommsPsych`

Output:

- `review/papers/paper-review--<paper-slug>--YYYY-MM-DD.md`

### `review-paper-light`

Fast paper check for quick iteration.

Examples:

```text
/review-paper-light
/review-paper-light path/to/paper
```

Output:

- `review/papers/paper-light-review--<paper-slug>--YYYY-MM-DD.md`

### `review-paper-code`

Paper-code reproducibility and alignment review.

Examples:

```text
/review-paper-code
/review-paper-code path/to/paper
/review-paper-code path/to/paper path/to/code_dir
/review-paper-code path/to/paper path/to/code_dir full
```

Output:

- `review/code/paper-code-review--<subject-slug>--YYYY-MM-DD.md`

## Output Rule

Paper review outputs are deterministic:

- `review-paper` -> `review/papers/paper-review--<paper-slug>--YYYY-MM-DD.md`
- `review-paper-light` -> `review/papers/paper-light-review--<paper-slug>--YYYY-MM-DD.md`
- `review-paper-code` -> `review/code/paper-code-review--<subject-slug>--YYYY-MM-DD.md`

If a filename already exists, the workflow appends `-v2`, `-v3`, and so on.

## File Types

Supported paper inputs:

- `.tex`
- `.md`
- `.pdf`
- `.docx`

For `.pdf`, install `pdftotext` or `pypdf`. For `.docx`, install `pandoc`.
