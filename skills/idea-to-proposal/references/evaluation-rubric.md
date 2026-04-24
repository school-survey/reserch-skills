# Evaluation Rubric: 8-Dimension Research Idea Scoring

This rubric provides detailed criteria for scoring a research idea on each of the 8 evaluation dimensions. Each dimension is scored 1-10 with specific anchors.

---

## 1. Novelty (1-10)

**Question:** Does prior work already solve this? How differentiated is this idea?

| Score | Criteria |
|-------|----------|
| 1-2 | Idea is essentially a re-implementation of existing work with no meaningful difference |
| 3-4 | Minor variation on existing work; incremental improvement without new insight |
| 5-6 | Combines existing ideas in a new way, or applies known technique to new domain; moderate novelty |
| 7-8 | Introduces a new perspective, formulation, or component not seen in prior work; clear differentiation from closest related work |
| 9-10 | Fundamentally new approach or paradigm; opens a new research direction |

**Evidence required:** Must cite 3-5 closest prior works and articulate specific differences.

---

## 2. Technical Soundness (1-10)

**Question:** Is the proposed method theoretically grounded? Any logical gaps?

| Score | Criteria |
|-------|----------|
| 1-2 | Approach has fundamental logical flaws or contradictions |
| 3-4 | Core idea is plausible but key steps are hand-wavy or unjustified |
| 5-6 | Generally sound but some assumptions are unstated or some derivations are incomplete |
| 7-8 | Well-grounded with clear theoretical basis; assumptions stated and reasonable |
| 9-10 | Rigorous theoretical foundation with formal guarantees or proofs; all assumptions justified |

**Check for:** Logical consistency, mathematical correctness, valid assumptions, completeness of reasoning.

---

## 3. Feasibility (1-10)

**Question:** Can this be implemented with available data, compute, and time?

| Score | Criteria |
|-------|----------|
| 1-2 | Requires unavailable data, impossible compute, or years of development |
| 3-4 | Theoretically possible but requires significant resources beyond typical lab |
| 5-6 | Feasible with moderate effort; some data/compute challenges but solvable |
| 7-8 | Clearly implementable with standard resources; datasets exist, compute is reasonable |
| 9-10 | Can be prototyped quickly; all resources readily available |

**For agent-based proposals, include token cost estimation:**

| Component | Model | Calls/Run | Avg Input Tokens | Avg Output Tokens | Est. Cost/Run |
|-----------|-------|-----------|-----------------|-------------------|---------------|

**Sensitivity note:** Costs may be 2-3x higher if error handling requires retries.

---

## 4. Significance / Impact (1-10)

**Question:** How important is the problem? How large is the potential contribution?

| Score | Criteria |
|-------|----------|
| 1-2 | Problem is trivial or already solved; no one would benefit from this |
| 3-4 | Niche problem affecting a small community; limited practical value |
| 5-6 | Moderately important problem; would interest a subset of the target venue's audience |
| 7-8 | Important problem with broad relevance; would attract significant attention |
| 9-10 | Critical problem with wide-reaching implications; potential to change how the field operates |

**Evidence required:** Quantify the scope of the problem (number of affected users, systems, or applications).

---

## 5. Clarity (1-10)

**Question:** Is the idea unambiguous? Could someone implement it from this description?

| Score | Criteria |
|-------|----------|
| 1-2 | Vague and poorly defined; multiple conflicting interpretations possible |
| 3-4 | General direction is clear but key details are missing or ambiguous |
| 5-6 | Main approach is understandable but some components need further specification |
| 7-8 | Well-defined with clear components, inputs/outputs, and workflow |
| 9-10 | Precisely specified; someone could implement a prototype from the description alone |

**Check for:** Unambiguous terminology, well-defined inputs/outputs, clear algorithmic steps, no hand-waving.

---

## 6. Experimental Validity (1-10)

**Question:** Can the claims be tested? Is the proposed evaluation plan convincing?

| Score | Criteria |
|-------|----------|
| 1-2 | No evaluation plan; claims are untestable |
| 3-4 | Vague evaluation plan; metrics or datasets not specified |
| 5-6 | Basic evaluation plan with some metrics and datasets, but missing ablations or baselines |
| 7-8 | Comprehensive evaluation with clear metrics, appropriate baselines, ablation studies, and statistical rigor |
| 9-10 | Exceptional evaluation plan with multiple axes of analysis (quantitative, qualitative, ablation, robustness, scaling, human evaluation) |

**Must include:** At least 2 established benchmarks, 3+ baselines, and ablation plan.

---

## 7. Scalability (1-10)

**Question:** Does the approach generalize beyond the specific experimental setup?

| Score | Criteria |
|-------|----------|
| 1-2 | Approach is highly specific to one dataset/task/setting; no generalization path |
| 3-4 | Works for specific case but unclear how to extend; strong domain-specific assumptions |
| 5-6 | Could generalize with modifications; some domain-specific components are replaceable |
| 7-8 | Designed with generalization in mind; core idea applies across related tasks/domains |
| 9-10 | Highly general framework; demonstrated or demonstrable applicability across multiple domains |

**Check for:** Domain-specific vs. general components, transferability of core mechanism, scaling behavior.

---

## 8. Positioning (1-10)

**Question:** Does this idea fit the target venue? Is the timing right for the community?

| Score | Criteria |
|-------|----------|
| 1-2 | Completely misaligned with venue scope or community interests |
| 3-4 | Tangentially related to venue; community may not see the relevance |
| 5-6 | Fits venue scope but doesn't address a hot topic or emerging trend |
| 7-8 | Well-aligned with venue's recent interests; builds on trending topics |
| 9-10 | Perfect timing; addresses a problem the community is actively discussing; fills a recognized gap |

**If no target venue:** Score based on general AI research community interest.

**Evidence required:** Reference 2-3 recent papers from the target venue on related topics.

---

## Scoring Guidelines

### Overall Score
- **Mean** of all 8 dimensions (arithmetic average)
- Report both individual scores and overall

### Threshold
- Default: ALL dimensions must score ≥ 7/10
- Configurable via `--threshold` parameter

### Refinement Priority
When multiple dimensions are below threshold, prioritize refinement by:
1. **Largest gap** from threshold (biggest deficit first)
2. **Technical dimensions** (Novelty, Technical Soundness, Experimental Validity) over presentation dimensions (Clarity, Positioning) when gaps are equal
3. **Feasibility** is a hard constraint — if fundamentally infeasible, flag as structural limitation early

### Structural Limitation Flag
If a dimension cannot reach threshold after 2 rounds of targeted refinement, flag it:
```
⚠️ Structural Limitation: [Dimension] capped at [X]/10
Reason: [Why this cannot be improved without fundamentally changing the idea]
Recommendation: [Accept limitation / Pivot idea / Reduce scope]
```
