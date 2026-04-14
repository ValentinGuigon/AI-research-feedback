# Quick Pre-Submission Check

**Paper**: Metacognition biases information seeking in assessing ambiguous news
**Authors**: Valentin Guigon, Marie Claire Villeval, Jean-Claude Dreher
**Date**: 2026-04-13

---

## Overall Assessment

This paper studies whether confidence in ambiguous-news veracity judgments predicts willingness to seek more information, using an incentivized within-subject experiment on headline evaluation. The contribution is significant rather than transformative: the paper tackles a timely problem with a careful behavioral design, but the strongest claims lean beyond what the confidence measure can support causally. The single most pressing issue is claim discipline around statements that confidence "drives" or "mediates" information seeking when confidence was measured, not experimentally manipulated.

**Preliminary Recommendation**: Revise before sending to referees

---

## 1. Contribution & Identification

## Agent A: Contribution & Identification

### Part 1 - Central Contribution
The paper claims to show that, under ambiguous-news evaluation, confidence is poorly calibrated to accuracy yet strongly predicts whether people seek more information.

This is genuinely useful and timely, but not fully transformative. The closest prior work is the confidence-based information-sampling literature in perceptual decision-making that the paper itself cites as the benchmark it extends to real-news judgments. What this paper adds is a non-partisan, incentivized ambiguous-news task plus an attempt to connect ambiguity, confidence, and information-seeking in the same design.

**Contribution rating**: Significant

The paper has a credible behavioral design, a reasonably large sample, and a clear bridge from controlled metacognition tasks to misinformation-relevant judgments. The main limitation is that the strongest mechanistic language overreaches relative to what the design can establish, which lowers confidence in the headline claim even if the empirical pattern is interesting.

### Part 2 - Identification and Credibility
The design is an incentivized within-subject online behavioral experiment. That is appropriate for the central descriptive question, and partly appropriate for the ambiguity manipulation because headline ambiguity was designed and pretested. It is less appropriate for any causal claim that confidence itself drives information-seeking, because confidence is an observed internal state rather than a randomized intervention.

Main threats to internal validity:
- Confidence is treated as a driver and mediator, but it is measured concurrently with judgments and may proxy for latent factors such as task ease, response style, or unmodeled stimulus properties.
- The study was not preregistered, which matters because the paper uses many linked analyses, including Bayesian models, mixed models, and moderated mediation.
- The key ambiguity ratings come from a separate small rater sample and the paper itself notes only moderate reliability for content imprecision.
- External validity is narrow: French student participants, brief headline stimuli, and non-partisan content only.

The main finding is strongest as descriptive/predictive: lower confidence is associated with more information-seeking, while confidence is weakly calibrated to accuracy. A skeptical methods reviewer would likely say the paper is interesting and likely publishable after revision, but the mechanistic interpretation of confidence as a causal driver is not yet earned.

### Part 3 - Required Analyses
1. [CRITICAL] Sensitivity analysis that downgrades mechanistic interpretation of the mediation model | The paper currently leans on moderated mediation to imply process, but mediation with measured confidence does not identify causal mechanism by itself | A positive result showing the core association survives under a more explicitly predictive framing would preserve the paper's contribution while reducing overclaiming.
2. [CRITICAL] Stronger robustness analysis around stimulus-level heterogeneity and ambiguity measurement reliability | Confidence and information-seeking may partly reflect item-specific structure beyond the reported imprecision/polarization measures, especially given moderate reliability for one ambiguity dimension | A positive result would show the main pattern is not an artifact of a subset of headlines or noisy ambiguity coding.
3. [CRITICAL] Clearer analysis or framing separating response bias from discrimination performance in the central takeaways | The paper notes a true-news bias and chance-level overall performance, but the headline interpretation still risks conflating calibration, bias, and discrimination | A positive result would clarify exactly what participants are bad at and strengthen the paper's theoretical contribution.
4. [CRITICAL] Robustness check for the claim that confidence predicts information-seeking independently of performance accuracy and plausible covariates | The central contribution depends on this independence claim, and the design leaves room for residual confounding by difficulty or individual strategy | A positive result would materially strengthen the paper's credibility.

### Part 4 - Questions to the Authors
1. What justifies describing confidence as a driver or mediator of information-seeking rather than a correlated summary of perceived difficulty or item-level uncertainty?
2. How stable are the main confidence and reception effects after richer stimulus-level random effects or alternative operationalizations of ambiguity reliability?
3. Why should readers treat the moderated mediation analysis as evidence about mechanism rather than a compact way to summarize associations among measured variables?
4. Can you make the distinction between discrimination ability, response bias, and calibration more central in the framing so the contribution is not overstated?
5. Which claims, if any, would you remove or soften because the study was not preregistered and the analysis stack is relatively large?

---

## 2. Causal Overclaiming & Unsupported Claims

## Agent B: Causal Overclaiming & Unsupported Claims

### Causal Overclaiming
1. [CRITICAL] Abstract / Conclusion | "confidence in one's judgment was the primary driver of the demand for additional information about the news." | The study shows a strong association between confidence and information-seeking, but confidence was not randomized or manipulated, so "driver" implies causal leverage not established by the design. | Replace with "was the strongest predictor of" or "was strongly associated with."
2. [CRITICAL] Abstract | "Structural equation modeling revealed that the demand for disambiguating information, driven by uncalibrated metacognition, became increasingly ineffective as individuals are drawn in by the ambiguity of the news." | Structural equation modeling on observed variables does not by itself show that uncalibrated metacognition drives the process; this is mechanistic language beyond the design. | Reframe as an associative mediation pattern and explicitly avoid causal verbs.
3. [MAJOR] Conclusions and limitations | "confidence in one's judgment drives the willingness to seek additional information to better assess news veracity." | Same issue: "drives" overstates a measured predictor in a non-preregistered behavioral study. | Use "predicts" or "is inversely associated with."

### Mechanism Claims Stated as Facts
1. [MAJOR] Discussion | "Our novel findings underscore the prime role of metacognitive abilities in mediating the relationship between ambiguous information assessment and the demand or avoidance of extra information." | This treats mediation as an established mechanism rather than a model-based interpretation of associations. | State that the data are consistent with a mediating account rather than proving one.
2. [MAJOR] Discussion | "Individuals misjudge what they know but they also seek to receive information according to what they know. As a consequence, they misidentify shortfalls in their knowledge, preventing them from filling the gaps." | The last clause asserts a downstream mechanism and consequence not directly tested in this design. | Limit to observed task behavior and frame broader implications as hypotheses.

### Missing Caveats
1. [MAJOR] Methods / framing | The study is explicitly "not preregistered," yet the main text relies on a broad analytical stack including mixed models, Bayesian models, and moderated mediation. | Add a sharper caveat in the abstract or discussion that the mechanistic interpretation is exploratory rather than confirmatory.
2. [MAJOR] Discussion / generalization | The task uses French student participants rating brief, non-partisan headlines only. | Add a more prominent caveat against generalizing to broader populations, partisan misinformation, or real-world full-article consumption.
3. [MAJOR] Ambiguity measurement | The paper notes only moderate inter-rater reliability for content imprecision. | Acknowledge more explicitly that one core stimulus-level construct is somewhat noisy and that this limits precision of the ambiguity interpretation.

### Other Issues
1. [MINOR] Priority claim | The paper makes a novelty claim via "Our novel findings" without directly verifying the relevant priority boundary. | Soften the claim unless the authors have checked adjacent work on confidence-guided information search in misinformation contexts.
2. [MINOR] Practical significance | The paper reports many statistically strong effects, but the practical implications for interventions are discussed more aggressively than the current single-task evidence supports. | Keep intervention implications explicitly provisional.

---

## Priority Action Items

**CRITICAL** (could cause desk rejection or major objections):
1. Replace causal and mechanistic wording that says confidence "drives" information-seeking with predictive language that matches the design.
2. Reframe the moderated mediation and SEM results as model-based associative evidence, not direct evidence of psychological mechanism.
3. Strengthen robustness around stimulus heterogeneity, ambiguity measurement reliability, and the claim that the confidence effect survives plausible alternative explanations.
4. Clarify the distinction between response bias, discrimination performance, and calibration in the paper's central takeaway.

**MAJOR** (will likely be raised by referees):
5. Add a stronger caveat that the study was not preregistered and that the mechanism-oriented interpretation is exploratory.
6. Narrow the generalization claims to the observed setting: French student participants, brief non-partisan headlines, and this specific incentive structure.
7. Tone down intervention implications and broader claims about misinformation behavior outside the task.
8. Soften unverified novelty phrasing unless adjacent literature has been checked carefully.

**MINOR** (polish):
9. Make practical significance more explicit alongside the statistically strong results.
