# Rebuttal Guidelines by Venue

## Venue-Specific Rebuttal Limits

| Venue | Format | Default Limit | Scope | Appendix Allowed | Notes |
|-------|--------|---------------|-------|-----------------|-------|
| NeurIPS | Markdown (OpenReview) | 5000 chars | Per reviewer | No | Separate response box per reviewer |
| ICML | Markdown (OpenReview) | 5000 chars | Total | No | Single response covering all reviewers |
| CVPR | Plain text (CMT) | 4000 chars | Total | No | Combined response to all reviewers |
| ACL | Markdown (OpenReview) | 5000 chars | Total | Yes (1 page PDF) | Response + optional appendix |
| AAAI | Plain text (OpenReview) | 4000 chars | Total | No | Combined response |
| ICCV | Plain text (CMT) | 4000 chars | Total | No | Combined response to all reviewers |
| ICLR | Markdown (OpenReview) | Unlimited | Per reviewer | No | Separate response per reviewer; no hard limit but brevity valued |

**Important**: Venue limits change year-to-year. Always verify the current year's guidelines. When `--char-limit` is provided, it overrides these defaults.

## Reviewer Stance Inference

### By Normalized Score

Map each venue's scoring scale to a 0-1 range, then classify:

| Venue | Scale | Normalization Formula |
|-------|-------|----------------------|
| NeurIPS | 1-10 | (score - 1) / 9 |
| ICML | 1-10 | (score - 1) / 9 |
| CVPR | 1-6 | (score - 1) / 5 |
| ACL | 1-5 | (score - 1) / 4 |
| AAAI | 1-10 | (score - 1) / 9 |
| ICCV | 1-6 | (score - 1) / 5 |
| ICLR | 1-10 | (score - 1) / 9 |

| Normalized Score | Stance | Description |
|-----------------|--------|-------------|
| 0.75 - 1.0 | champion | Strong supporter, likely to advocate for the paper |
| 0.55 - 0.74 | lean_accept | Positive but with reservations, convertible to champion |
| 0.45 - 0.54 | neutral | On the fence, could go either way |
| 0.25 - 0.44 | lean_reject | Skeptical, needs significant convincing |
| 0.0 - 0.24 | reject | Strongly opposed, focus on damage control |

### By Tone (when score is unavailable)

| Stance | Keywords / Phrases |
|--------|-------------------|
| champion | "excellent", "strong contribution", "significant advance", "clearly accept", "well above threshold" |
| lean_accept | "interesting", "solid work", "good contribution", "promising", "above average" |
| neutral | "borderline", "mixed feelings", "some merit but", "on the fence", "could go either way" |
| lean_reject | "unconvincing", "insufficient", "limited contribution", "below threshold", "needs major revision" |
| reject | "fundamentally flawed", "strongly reject", "not ready for publication", "serious concerns", "major issues" |

### Confidence Weighting

Higher reviewer confidence means their stance carries more weight with the meta-reviewer. When allocating effort:
- High confidence detractor: highest priority (they're sure and negative)
- Low confidence detractor: moderate priority (easier to convert)
- High confidence champion: low effort needed (reinforce their view)

## Response Mode Reference

### direct_clarification
**When**: Reviewer missed or misread existing paper content.
**Pattern**: "We thank the reviewer for this point. As shown in [Section X / Table Y / Eq. Z], [specific content they missed]. We will improve the clarity of this section in the revision."
**Tone**: Polite, not condescending. Never say "the reviewer failed to notice."

### grounded_evidence
**When**: Paper already contains evidence that addresses the concern.
**Pattern**: "Our results in [Table X] demonstrate that [specific evidence]. Specifically, [cite exact numbers]. This shows [implication]."
**Tone**: Confident but not defensive. Let the evidence speak.

### nearest_work_delta
**When**: Novelty dispute — reviewer claims work is similar to prior art.
**Pattern**: "While [prior work] addresses [shared aspect], our approach differs in [N] key ways: (1) [technical diff 1], (2) [technical diff 2], (3) [technical diff 3]. These differences lead to [concrete improvement]."
**Tone**: Respectful of prior work while clearly articulating the delta.

### additional_experiment
**When**: Reviewer requests new evidence not in the paper.
**Pattern**: "[Prose explaining what the experiment tests and why it matters]. [INSERT: results of experiment X, showing metric Y on dataset Z]. [Prose interpreting the expected implications]."
**Tone**: Proactive — show you take the concern seriously.

### narrow_concession
**When**: Reviewer is correct about a limitation.
**Pattern**: "The reviewer raises a valid point about [limitation]. We acknowledge that [specific concession]. However, we note that [scoping statement limiting the impact]: (1) [reason 1], (2) [reason 2]. We will add this discussion to the paper."
**Tone**: Honest and measured. Concede the specific point, then scope.

### future_work
**When**: Valid concern but genuinely out of scope.
**Pattern**: "This is an important direction that we plan to explore in future work. The current paper focuses on [scope], and extending to [reviewer's suggestion] would require [what's needed]. We will add this to the future work section."
**Tone**: Appreciative of the suggestion, clear about scope boundaries.

## Issue Type Classification Guide

| Type | Description | Common Keywords in Reviews |
|------|-------------|---------------------------|
| novelty | Originality and differentiation from prior work | "incremental", "similar to", "not novel", "already proposed" |
| empirical_support | Missing or insufficient experimental evidence | "no experiments", "ablation missing", "not enough datasets" |
| baseline_comparison | Missing or unfair comparisons | "no comparison with", "should compare", "unfair comparison" |
| theorem_rigor | Mathematical correctness or proof issues | "proof is wrong", "assumption unjustified", "gap in theorem" |
| assumptions | Unrealistic or unstated assumptions | "assumes", "unrealistic", "what if", "doesn't hold when" |
| complexity | Scalability or computational concerns | "doesn't scale", "too expensive", "complexity analysis" |
| clarity | Writing, organization, presentation quality | "hard to follow", "unclear", "poorly written", "confusing" |
| reproducibility | Missing details for reproduction | "no code", "hyperparameters missing", "can't reproduce" |
| practical_significance | Real-world applicability concerns | "toy problem", "not practical", "limited applicability" |
| other | Doesn't fit above categories | Miscellaneous concerns |

## Tone Guidelines

### Words/Phrases to AVOID
- "The reviewer is wrong/mistaken" → "We respectfully clarify that..."
- "Obviously" / "Clearly" → Remove or replace with evidence
- "We apologize" → "We appreciate this feedback"
- "We will try" → "We will" (commitment) or "We plan to explore" (future work)
- "As we already stated" → "As shown in Section X"
- "The reviewer should note" → "We would like to highlight"
- "We disagree" → "We offer an alternative perspective supported by..."

### Words/Phrases to USE
- "We thank the reviewer for this insightful comment"
- "To address this concern, we provide the following evidence"
- "As demonstrated in Table X / Figure Y / Equation Z"
- "We agree that [specific point] and have [action taken]"
- "We will clarify this in the revised manuscript"
- "This is an excellent suggestion that we will incorporate"
