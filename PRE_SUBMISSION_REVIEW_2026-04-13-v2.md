# Pre-Submission Referee Report

**Paper**: Metacognition biases information seeking in assessing ambiguous news
**Authors**: Valentin Guigon, Marie Claire Villeval, Jean-Claude Dreher
**Date**: 2026-04-13
**Review Standard**: Leading Field Journal

---

## Reviewed Materials

- Main paper: `tests/fixtures/s44271-024-00170-w.pdf`
- Direct review inputs: `_review_input.txt`; `tests/fixtures/_supmat.txt`
- Calibration/context only: `tests/fixtures/_peer_review.txt`; `tests/fixtures/_s44271.txt`
- Supplementary files discovered: `tests/fixtures/_supmat.txt`; `tests/fixtures/44271_2024_170_MOESM1_ESM.pdf`; `tests/fixtures/44271_2024_170_MOESM2_ESM.pdf`
- Reviewer-comment files discovered: `tests/fixtures/_peer_review.txt`
- Note: the supplement was used as part of the evidence base. Reviewer comments were used only to calibrate the review and to check whether major concerns were independently supported, contradicted, or resolved by the manuscript and supplement. The extracted main-text companion `_s44271.txt` was used only as a cross-check against PDF extraction, not as an independent evidence source.

---

## Overall Assessment

This paper studies whether confidence in veracity judgments predicts information seeking when people evaluate ambiguous news headlines. Its main strength is the attempt to separate confidence from accuracy while linking both to downstream information-demand behavior, and the supplement materially strengthens the evidentiary picture by exposing the underlying reliability estimates, wave comparisons, and robustness models. The most important issue remains construct validity: the paper's central information-seeking outcome is partly inferred from willingness to pay over a later email-based delivery that participants could ignore, and that limitation still constrains how strongly the headline claims can be framed. A leading field journal would likely view the project as interesting and potentially publishable, but still in need of tighter claim discipline, clearer surfacing of supplement-dependent robustness evidence, and a more explicit treatment of ambiguity-measure reliability.

**Preliminary Recommendation**: Revise before sending to referees

---

## 1. Contribution & Referee Assessment

## Agent 6: Contribution Evaluation

### Part 1 - Central Contribution
The paper argues that, when people assess ambiguous news, subjective confidence is weakly calibrated to actual accuracy but still strongly predicts whether they seek or avoid additional information.

This is a timely and nontrivial contribution because it connects misinformation-relevant judgment, metacognition, and information demand within one controlled design. The main manuscript becomes more credible once read alongside the supplement, which documents the stimulus pretest, wave comparisons, and robustness models that the main text relies on. The contribution is best described as **Significant** rather than transformative: it opens an interesting line of work, but the core behavioral outcome and some of the strongest mechanistic language still outrun what the design cleanly identifies.

### Part 2 - Design and Credibility
The design is an incentivized within-subject online experiment with ambiguous headlines, confidence reports, and willingness-to-pay choices over whether to receive more information later by email. That is appropriate for studying associations among ambiguity, confidence, and information demand, but the direct review of the supplement makes clear that several key interpretive safeguards live outside the main text.

1. [CRITICAL] Outcome-validity threat | The main behavioral interpretation still depends on an email-based information outcome that participants could later ignore. The manuscript acknowledges this in the Discussion, and the reviewer file shows this was already a major external concern; the concern remains independently supported by the task structure itself.
2. [CRITICAL] Design-to-claim gap | Confidence is measured rather than manipulated. The paper therefore supports a strong association between confidence and information demand, not a clean causal claim that confidence drives later choices.
3. [MAJOR] Ambiguity-measure reliability | The supplement reports ICC(2k) around 0.54 for content imprecision and 0.59 for desirability, which falls in the moderate range by the supplement's own rule-of-thumb summary. Because imprecision is central to the paper's story, that caveat should be elevated in the main narrative rather than left mostly in the supplement.
4. [MAJOR] Supplement dependence for key robustness claims | Several important credibility claims sit mainly in the supplement: wave comparisons in Supplementary Methods V.4, prior-belief nulls in Supplementary Table 11, response-time controls in Supplementary Table 12, and confidence robustness for information-demand outcomes in Supplementary Tables 15-16. The paper is stronger with those materials, but it should not require a supplement-only reading to understand what is doing the evidentiary work.

A skeptical methods reviewer would likely say the paper is promising, but the manuscript still blurs the difference between a carefully designed ambiguity task and a definitive account of epistemic information seeking in the wild. To make the paper convincing for a leading journal, the authors need more restrained associational framing, earlier acknowledgment of the outcome-validity limitation, and tighter integration of the supplement's key robustness evidence into the main argument.

### Part 3 - Analyses: Required and Suggested
**Required:**
1. [CRITICAL] Main-text integration of supplement-dependent robustness evidence | Bring the most decision-relevant supplement results into the main Results or Discussion, especially the wave comparisons and the control-inclusive confidence models in Supplementary Tables 15-16 | A positive result would make the main claims easier to verify without forcing readers to reconstruct the argument from supplementary materials.
2. [CRITICAL] Stronger validation of the information-seeking outcome | Clarify, and where possible further validate, why willingness to pay to avoid or receive a later email should be interpreted as epistemic avoidance or demand rather than as pricing around future nuisance | A positive result would materially strengthen the paper's central behavioral interpretation.
3. [CRITICAL] Sharper treatment of ambiguity-measure reliability | The main text should explicitly acknowledge that content-imprecision ratings rest on moderate inter-rater reliability and explain how that constrains the downstream interpretation of imprecision-based claims | A positive result would narrow the gap between what the analyses show and what the paper says those predictors mean.

**Suggested:**
1. [MAJOR] Trial-level robustness summary in the main text | Readers would benefit from a compact summary of how the confidence effect behaves once response times, socio-demographics, and theme/veracity controls are added | Feasible given Supplementary Tables 12, 15, and 16.
2. [MAJOR] Heterogeneity analysis by topic, distrust, or baseline beliefs | This matters because the theory implies stable differences in how people use confidence when deciding to seek more information | Feasible from the reported measures.
3. [MAJOR] Explicit justification for leaving desirability outside the main paper's core story | The supplement and reviewer file both suggest desirability had some predictive role; the manuscript should explain more directly why imprecision and polarization are privileged | Feasible with the existing analyses or a short explanatory note.

### Part 4 - Literature Positioning
The manuscript cites the right broad literatures on misinformation, confidence, and information acquisition. Its framing is strongest when it emphasizes ambiguous news as a setting where calibration can fail while still shaping behavior. It is weaker when it drifts toward broad societal implications without carrying the task-specific caveats forward. The reviewer file also points to relevant truth-bias and fake-news metacognition references that would likely improve the introduction's positioning.

### Part 5 - Journal Fit and Recommendation
For a generic leading field journal, the paper is plausible but not yet ready for immediate referral. The topic is timely and the supplement shows that the authors did substantial robustness work, but the central construct-validity limitation and the dependence on supplement-only verification remain meaningful barriers.

**Preliminary recommendation**: Revise before sending to referees

Concretely, the manuscript would need tighter associational wording, earlier and more explicit discussion of the email-ignore limitation, clearer treatment of moderate ambiguity-measure reliability, and better surfacing of supplement-based robustness results. Best realistic outlets, if it does not clear a top-field generalist bar, would be journals at the intersection of misinformation, judgment and decision-making, and metacognition.

### Part 6 - Questions to the Authors
1. Why should readers interpret willingness to pay around a later email as a valid measure of epistemic information seeking or avoidance rather than as a choice about future nuisance or attention costs?
2. Which claims in the abstract and conclusions are intended to be causal, and which should be read as strictly associational?
3. Why is the moderate ICC for content imprecision not surfaced more prominently in the main manuscript, given how central imprecision is to the argument?
4. Can you move the wave-comparison and control-inclusive robustness evidence most essential to the paper's claims out of the supplement and into the main text?
5. Why does the prior-beliefs discussion point readers to Supplementary Table 11 while the response-time evidence appears in Supplementary Table 12?
6. What is the principled reason for treating desirability as secondary when the supplement and reviewer correspondence indicate it also predicted information demand?

### Reviewer Calibration
- Independently corroborated concerns: the reviewer file's worries about the email-based outcome measure, low-to-moderate reliability of some pretest ratings, and dependence on supplementary controls are all supported by the manuscript plus supplement.
- Resolved or weakened reviewer concerns: the absence of a supplement index appears resolved because `_supmat.txt` contains an explicit index, and the previously missing Table S11 is now present in the supplement.
- Reviewer-specific unresolved concerns: the response-time / prior-beliefs / Table S11 issue is only partly resolved, because the supplement now contains Table 11 for prior beliefs and Table 12 for response times, but the main-text traceability remains easy to misread.

---

## 2. Unsupported Claims & Experimental Design Integrity

## Agent 3: Unsupported Claims & Experimental Design Integrity

### Causal Overclaiming (must address)
1. [CRITICAL] Abstract and conclusions | "confidence in one's judgment was the primary driver of the demand for additional information" | The design shows a strong association, not a randomized or otherwise identified causal effect of confidence | Fix: recast as "the strongest observed predictor" or equivalent.
2. [CRITICAL] Abstract | "the demand for disambiguating information, driven by uncalibrated metacognition, became increasingly ineffective" | The moderated mediation model does not identify uncalibrated metacognition as a demonstrated mechanism | Fix: frame this as a pattern consistent with that interpretation rather than a demonstrated mechanism.
3. [MAJOR] Discussion | claims that confidence "guided" or played a "prime role" in information-seeking behavior | These formulations remain too strong once the outcome-validity limitation and nonmanipulated confidence measure are taken seriously | Fix: use associational wording.

### Generalization Issues
1. [MAJOR] Discussion and conclusion | broad claims about how individuals or societies respond to misinformation and deepfakes | The data come from a French student sample evaluating short ambiguous headlines under controlled incentives | Fix: tether claims to the specific task and sample.
2. [MINOR] Discussion | suggestions that the observed metacognitive pattern characterizes stable traits | The design is single-session and does not identify stable individual traits | Fix: frame these as task-bound tendencies.

### Missing Caveats & Design Confounds
1. [CRITICAL] Outcome validity | Participants could choose to ignore the later email, which directly weakens interpretation of the "avoid information" choice | Where it should be addressed: Methods, Results framing, and Limitations | Suggested text: clarify that the observed outcome is willingness to pay around later information delivery, not verified later consumption.
2. [MAJOR] Ambiguity-measure reliability | Supplementary Methods I report only moderate ICC for content-imprecision ratings | Where it should be addressed: Results and Discussion | Suggested text: qualify imprecision-based interpretations and distinguish stronger from weaker ambiguity measures.
3. [MAJOR] Supplement dependence | Core robustness claims rely on Supplementary Tables 11, 12, 15, and 16 and on wave comparisons in Supplementary Methods V.4 | Where it should be addressed: Results lead-ins and table/figure references | Suggested text: name the exact supplementary analyses in the same sentence as the claim they support.
4. [MAJOR] Alternative explanation | The reviewer file is right that confidence may partly proxy interest, ambiguity, or fluency rather than a distinct metacognitive mechanism | Where it should be addressed: Discussion | Suggested text: acknowledge that information demand may reflect curiosity or nuisance-avoidance as well as epistemic regulation.

### Minor Language Issues
1. [MINOR] Abstract and Discussion | "underscore the importance," "prime role," and related emphasis terms | The rhetoric overcommits relative to the design | Fix: switch to more neutral language.

---

## 3. Internal Consistency & Cross-Reference Verification

## Agent 2: Internal Consistency & Cross-Reference Verification

### Critical Inconsistencies
No clear numerical contradictions were identified between the main manuscript text and the supplement passages reviewed.

### Terminology Drift
1. [MAJOR] Outcome variable | The paper alternates among "demand for extra information," "reception choices," "willingness to receive extra information," and WTP-based wording | Recommended standardization: define one label for the binary outcome and one for the WTP outcome, then use them consistently.
2. [MAJOR] Ambiguity construct | "content imprecision," "ambiguity," and nearby descriptors sometimes blur a rated stimulus property with the broader theoretical construct | Recommended standardization: keep the rated measure and the broader theory term clearly separate.

### Minor Inconsistencies
1. [MAJOR] Main-text to supplement traceability | The manuscript states that alignment of beliefs showed no significant effects while response times were highly significant, but the reviewer-calibration check shows those claims split across Supplementary Tables 11 and 12 rather than living in one place | Recommended fix: cite both tables explicitly and separate the two claims.
2. [MINOR] Robustness referencing | Several main-text robustness claims are made before the exact supplementary table is named | Recommended fix: pair each robustness statement with its supporting supplementary table in the same sentence.
3. [MINOR] Limitation placement | The email-ignore limitation appears late relative to its importance for interpreting the central outcome | Recommended fix: signal the limitation earlier when the outcome is first defined.

---

## 4. Mathematics, Equations & Notation

## Agent 4: Mathematics, Equations & Notation

### Mathematical Errors
No obvious algebraic or statistical formula errors were visible in the extracted manuscript and supplement text reviewed here.

### Notation Inconsistencies
1. [MINOR] Coefficient scales | The manuscript moves among standardized coefficients, odds ratios, and WTP deltas with limited repeated reminders of scale | Resolution: add scale reminders in captions and transition sentences.

### Undefined Notation
1. [MINOR] Moderated mediation outputs | Table 2 is interpretable, but the path labels and reporting scale would be easier to follow with a slightly more explicit caption-note bridge | Where to add definition: Table 2 caption or first note line.

### Model Specification Issues
1. [MAJOR] Robustness traceability | The main moderated-mediation story is easier to overread because the most relevant control-inclusive confidence models live in Supplementary Tables 15 and 16 rather than near Table 2 | Resolution: explicitly tie the main model to those supplementary robustness checks.
2. [MINOR] Prior-beliefs versus response-time controls | The split between Supplementary Tables 11 and 12 is substantively fine, but the manuscript should reference them more cleanly so readers can follow which control belongs to which model claim | Resolution: separate the citations in the Results text.

### LaTeX Math Formatting
No formatting problems can be reliably assessed from the PDF and extracted supplement text alone.

---

## 5. Tables, Figures & Documentation

## Agent 5: Tables, Figures & Documentation

### Tables with Missing or Incomplete Notes
1. [MAJOR] Table 1 | The main text leans on this table for the ambiguity story, but readers also need a clearer bridge to the supplement's reliability and stimulus-selection details | Suggested addition: point explicitly to Supplementary Methods I and Table 7 when interpreting imprecision and polarization.
2. [MAJOR] Table 2 | The table summarizes the mediation story, but it is not sufficiently self-contained about how the direct claim depends on supplementary robustness analyses | Suggested addition: add a note directing readers to Supplementary Tables 15 and 16 for control-inclusive models.
3. [MINOR] Supplementary Tables 11 and 12 | The two tables are individually interpretable, but the manuscript citation pattern makes them feel interchangeable | Suggested addition: cite them separately with their distinct inferential roles.

### Figures with Missing or Incomplete Notes
1. [MAJOR] Figure 4 | The figure is central to the confidence-accuracy and WTP interpretation, yet the main manuscript still relies on supplementary material for several robustness details needed to contextualize it | Suggested addition: make the caption or surrounding text point readers to the specific supplement analyses that establish robustness.
2. [MINOR] Figure 5 | The moderated mediation figure would benefit from a more explicit reminder that the mechanism language remains inferentially limited | Suggested addition: clarify in the caption that the model captures conditional association structure rather than identified mechanism.

### Cross-Reference Issues
1. [MAJOR] Supplement dependence | Key robustness claims about waves, prior beliefs, response times, and control-inclusive information-demand models are recoverable only by consulting Supplementary Methods V.4 and Supplementary Tables 11, 12, 15, and 16 | Issue: the paper should name those supplement locations at the point of claim.
2. [MAJOR] Table S11 traceability | The reviewer-calibration file identified a real traceability problem: prior-beliefs and response-time claims are easy to conflate because the text does not cleanly distinguish Supplementary Tables 11 and 12 | Issue: split the references and rewrite the sentence.
3. [MINOR] Figure inspectability in plain-mode review | Because the present review relied on extracted text plus captions rather than directly parsed figure source, the manuscript benefits especially from self-contained captions and explicit supplementary references | Recommendation: strengthen caption self-sufficiency.

### Formatting Inconsistencies
1. [MINOR] Outcome labels | "Receive extra information," "demand for further information," and "reception choice" vary across prose and tables | Standardization recommendation: harmonize the outcome labels throughout.

---

## 6. Spelling, Grammar & Style

## Agent 1: Spelling, Grammar & Style

### Critical Issues (must fix before submission)
No clear sentence-level grammar or spelling errors require emergency correction.

### Minor Issues
1. [MINOR] Multiple locations | evaluative signposts such as "Importantly" and "Crucially" | These words often do argumentative work that the evidence should carry instead | Remove or reduce them.
2. [MINOR] Conclusion | "prime role" | Stylistically stronger than the design warrants | Replace with more neutral phrasing.

### Style Patterns to Fix Throughout
1. [MAJOR] Causal wording pattern | Example: confidence "drives" information seeking | Global fix instruction: reserve causal verbs for manipulated or otherwise identified effects.
2. [MAJOR] Supplement-opacity pattern | Example: robustness claims stated in the main text without naming the exact supplementary table carrying them | Global fix instruction: cite the supplement at the sentence level whenever it bears core evidentiary weight.
3. [MINOR] Scope inflation pattern | Example: movement from this task to broad societal misinformation claims | Global fix instruction: keep extrapolations explicitly bounded.

---

## Priority Action Items

Each agent has tagged its findings as `[CRITICAL]`, `[MAJOR]`, or `[MINOR]`. Collect all tagged items across agents and rank them here using the following triage hierarchy: `[CRITICAL]` items from Agent 3 and Agent 6 Part 2 first, then `[CRITICAL]` from Agent 6 Part 3, then remaining `[CRITICAL]` items by agent order, then all `[MAJOR]` items, then `[MINOR]` items.

**CRITICAL** (must fix - these could cause desk rejection or major referee objections):
1. [CRITICAL] Reframe the headline claim that confidence "drives" information seeking as associational unless the paper can supply stronger identification.
2. [CRITICAL] Elevate and sharpen the outcome-validity threat that participants could simply ignore the later email, weakening the interpretation of information avoidance or demand.
3. [CRITICAL] Bring the key supplement-based robustness evidence into the main text, especially the wave comparisons and the control-inclusive confidence models in Supplementary Tables 15-16.
4. [CRITICAL] Explicitly acknowledge that content-imprecision ratings rest on only moderate inter-rater reliability and explain how that constrains the interpretation of imprecision-based claims.
5. [CRITICAL] Recast the moderated-mediation result as consistent with a mechanism rather than as proof that uncalibrated metacognition caused ineffective information seeking.

**MAJOR** (should fix - will likely be raised by referees):
6. [MAJOR] Separate the prior-beliefs and response-time citations so readers can tell that Supplementary Table 11 and Supplementary Table 12 support different claims.
7. [MAJOR] Make the dependence on supplementary analyses explicit wherever the main text claims robustness to controls, waves, or alternative explanations.
8. [MAJOR] Tighten the manuscript's population and task-bound generalizations beyond French students evaluating short ambiguous headlines.
9. [MAJOR] Explain more directly why desirability is secondary if it also predicted information demand in the supplementary material and reviewer correspondence.
10. [MAJOR] Standardize the terminology for the binary information-demand outcome and the WTP outcome.

**MINOR** (polish - improves paper quality):
11. [MINOR] Remove evaluative filler such as "Importantly," "Crucially," and "prime role."
12. [MINOR] Add repeated scale cues when switching among standardized coefficients, odds ratios, and WTP deltas.
13. [MINOR] Strengthen self-contained table and figure references for plain-text readability and supplement traceability.
