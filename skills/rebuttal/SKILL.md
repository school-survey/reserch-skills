---
name: rebuttal
description: >
  Rebuttal pipeline for conference paper reviews. Parses reviewer feedback,
  classifies concerns by severity/type, builds a per-reviewer response
  strategy, and drafts a venue-compliant rebuttal with placeholders for
  pending experiments. Supports follow-up rounds. Use when user says
  "rebuttal", "reply to reviewers", "respond to reviews", "rebuttal draft",
  or wants to answer reviewer comments for a conference submission.
user-invocable: true
argument-hint: "<paper-path> <reviews-path> [--venue NeurIPS|ICML|CVPR|ACL|AAAI|ICCV|ICLR] [--char-limit 5000] [--plan-only] [--followup]"
---

## Overview

Prepare a grounded, venue-compliant rebuttal for conference paper reviewer feedback. The skill follows a 3-phase pipeline:

1. **Review Analysis** — Parse reviews, atomize concerns, classify severity/type, identify shared themes
2. **Strategy Plan** — Per-reviewer response strategy with attitude, angle, evidence mapping, and experiment gap report
3. **Draft & Validate** — Write rebuttal with placeholders for pending experiments, run lints and stress test, produce paste-ready output

The skill writes all rebuttal prose except experiment results. For issues requiring new experiments, it writes the surrounding context and inserts `[INSERT: ...]` placeholders where results should go.

## Arguments

### `<paper-path>` (required)
Path to the submitted paper. Can be:
- A PDF file (absolute or relative path)
- A LaTeX project directory (will look for `main.tex` or first `.tex` file)

### `<reviews-path>` (required)
Path to a markdown file containing reviews copied from OpenReview/CMT/HotCRP. Reviewer IDs should be preserved (e.g., `## Reviewer 1`, `## Reviewer #2`, `## R3`).

### `--venue` (optional)
Target conference. Options: `NeurIPS`, `ICML`, `CVPR`, `ACL`, `AAAI`, `ICCV`, `ICLR`.
- Default: auto-detect from review format and scoring scale
- Fallback: generic format
- Determines character limits, response structure, and review parsing heuristics

### `--char-limit` (optional, default: venue-specific or 5000)
Character limit for the rebuttal. Overrides venue default. This is the total limit across all reviewer responses.

### `--plan-only` (optional)
Stop after Phase 2. Outputs ISSUE_BOARD.md + STRATEGY_PLAN.md + EXPERIMENT_GAPS.md without drafting the rebuttal. Useful for reviewing the strategy before committing to a draft.

### `--followup` (optional)
Follow-up round mode. Expects an existing output directory from a prior run. Parses new reviewer comments and generates delta replies only.

## Setup

Install dependencies:
```bash
python -m pip install -r "BASE_DIR/scripts/requirements.txt"
```

## Workflow

### Phase 1: Review Analysis

#### Step 1.0: Detect Paper Source

If paper-path is a PDF: read directly with the Read tool (paginate for PDFs over 20 pages).

If paper-path is a directory:
1. Check if the directory contains a compiled PDF — if so, prefer the PDF
2. Otherwise, look for `main.tex` or the first `.tex` file found
3. Resolve `\input{}` and `\include{}` by recursively reading referenced files
4. Parse concatenated `.tex` content as the paper text (equations remain as LaTeX source)

#### Step 1.1: Read and Understand the Paper

Read the entire paper. While reading, compile notes on:
- **Title, authors, affiliation**
- **Core claims and contributions** (from abstract + introduction)
- **Methodology** — key techniques, algorithms, theoretical results
- **Experimental setup** — datasets, baselines, metrics, ablations
- **Results** — key numbers, tables, figures
- **Limitations** — author-acknowledged weaknesses
- **Specific sections/tables/equations** — note identifiers (e.g., "Table 3", "Eq. 5", "Section 4.2") for citation in rebuttal

#### Step 1.2: Parse and Normalize Reviews

1. Read the reviews markdown file
2. Split by reviewer ID. Supported patterns: `Reviewer 1`, `Reviewer #1`, `R1`, `Reviewer A`, or markdown headings (`## Reviewer 1`). If the format is non-standard, ask the user to clarify reviewer boundaries.
3. For each reviewer, extract:
   - **Scores** (if present): overall score, confidence, sub-scores
   - **Strengths section**
   - **Weaknesses section**
   - **Questions section**
   - **Minor issues**
4. Save verbatim copy to `REVIEWS_RAW.md` in the output directory

#### Step 1.3: Atomize and Classify Concerns

For each reviewer, break down their feedback into discrete atomic concerns. Each concern gets:

| Field | Description |
|-------|-------------|
| `issue_id` | Unique ID: `R{reviewer}-C{number}` (e.g., R1-C1, R2-C3) |
| `raw_quote` | Verbatim excerpt from the review |
| `issue_type` | One of: `novelty`, `empirical_support`, `baseline_comparison`, `theorem_rigor`, `assumptions`, `complexity`, `clarity`, `reproducibility`, `practical_significance`, `other` |
| `severity` | `critical` (blocks acceptance), `major` (significant concern), `minor` (nice-to-fix) |
| `reviewer_stance` | Inferred from scores + tone using the lookup table in `references/rebuttal_guidelines.md` |
| `needs_experiment` | `true` if addressing this concern requires new experimental results |
| `status` | Initially `open` for all concerns |

#### Step 1.4: Identify Shared Themes

Scan across all reviewers for overlapping concerns:
- Group issues by `issue_type` and semantic similarity
- Flag themes raised by 2+ reviewers (these go in the global opener)
- Note contradictions between reviewers (one praises what another criticizes)

#### Step 1.5: Situation Assessment

Compute and write a summary:
- Scores per reviewer (raw and normalized stance)
- Champions vs swing voters vs detractors
- Shared themes with reviewer overlap
- **Path to acceptance**: which reviewers to convert and what it takes

#### Output: `ISSUE_BOARD.md`

```markdown
# Situation Assessment

- Scores: R1 (6/10, lean_accept), R2 (4/10, lean_reject), R3 (5/10, neutral)
- Champions: R1 | Swing voters: R3 | Detractors: R2
- Shared themes: [scalability concerns (R2, R3), missing ablation (R1, R2)]
- Path to acceptance: Convert R3 by addressing scalability + ablation

# Issue Board

| ID | Reviewer | Type | Severity | Quote | Needs Experiment | Status |
|----|----------|------|----------|-------|-----------------|--------|
| R1-C1 | R1 | clarity | minor | "Section 3.2 is hard to follow" | false | open |
| R1-C2 | R1 | empirical_support | major | "Ablation missing for component X" | true | open |
| R2-C1 | R2 | empirical_support | critical | "No comparison with Method Y" | true | open |
| R2-C2 | R2 | novelty | major | "Similar to Z (2024)" | false | open |
| R3-C1 | R3 | complexity | major | "Scalability not demonstrated" | true | open |
```

---

### Phase 2: Strategy Plan

#### Step 2.1: Assign Response Modes

For each issue in ISSUE_BOARD.md, assign a response mode using this decision tree (in priority order — prefer the first applicable mode):

1. **Does the reviewer factually misread the paper or miss existing content?**
   → `direct_clarification` — Point to specific section/table/equation they missed

2. **Is there existing evidence in the paper that answers the concern?**
   → `grounded_evidence` — Cite specific numbers, theorems, or results already present

3. **Is this a novelty dispute?**
   → `nearest_work_delta` — Name the closest prior work + exact technical difference

4. **Does the concern require new experimental results to address?**
   → `additional_experiment` — Placeholder in draft, added to EXPERIMENT_GAPS.md

5. **Is the reviewer correct about a limitation?**
   → `narrow_concession` — Acknowledge honestly, then scope the impact narrowly

6. **Is the concern valid but out of scope for this paper?**
   → `future_work` — Commit to future investigation, explain current scope boundary

If multiple modes apply, prefer the one higher in the list (stronger evidence first).

#### Step 2.2: Define Response Angles

For each issue, write 1-2 sentences describing:
- **What to say** — the core argument or evidence to present
- **Tone** — e.g., "Politely clarify that Table 3 already shows this", "Acknowledge the gap and present the planned ablation"

#### Step 2.3: Build Experiment Gap Report

Create `EXPERIMENT_GAPS.md` listing all `needs_experiment: true` issues:

```markdown
# Experiment Gaps

| ID | Issue | Experiment Needed | Metric | Satisfies | Priority |
|----|-------|-------------------|--------|-----------|----------|
| R2-C1 | No comparison with Method Y | Run Method Y on datasets A, B | Accuracy, FLOPs | R2-C1, R3-C1 | P0 (blocks acceptance) |
| R1-C2 | Missing ablation for X | Ablate component X | Accuracy delta | R1-C2 | P1 (strengthens case) |
```

#### Step 2.4: Build Character Budget

Calculate character allocation based on `--char-limit`:
- **10-15%** — Global opener (thank reviewers + shared theme resolutions)
- **75-80%** — Per-reviewer responses (proportional to issue count × severity weight: critical=3, major=2, minor=1)
- **5-10%** — Closing (resolved summary + acceptance case)

Order reviewers by priority: detractors first (most to gain), then swing voters, then champions.

#### Step 2.5: Present Strategy for Confirmation

Write `STRATEGY_PLAN.md`:

```markdown
# Response Strategy

## Global Themes (for opener)
1. Scalability: addressed by [approach]
2. Missing ablation: [approach]

## Per-Reviewer Strategy

### R2 (lean_reject → target: neutral+)
| ID | Mode | Angle | Priority |
|----|------|-------|----------|
| R2-C1 | additional_experiment | Run comparison with Y on benchmarks A, B; placeholder until results ready | P0 |
| R2-C2 | nearest_work_delta | Clarify 3 key differences from Z (2024): [diff1], [diff2], [diff3] | P1 |

### R3 (neutral → target: lean_accept)
| ID | Mode | Angle | Priority |
|----|------|-------|----------|
| R3-C1 | additional_experiment | Scale-up experiment on dataset C; shares evidence with R2-C1 | P0 |

### R1 (lean_accept → target: champion)
| ID | Mode | Angle | Priority |
|----|------|-------|----------|
| R1-C1 | direct_clarification | Rewrite Section 3.2 intro paragraph for clarity | P2 |
| R1-C2 | additional_experiment | Ablation study for component X | P1 |

## Character Budget
- Opener: ~600 / 5000 chars
- R2: ~1800 chars (2 issues, 1 critical + 1 major)
- R3: ~1200 chars (1 issue, 1 major)
- R1: ~900 chars (2 issues, 0 critical)
- Closing: ~500 chars
- Total: ~5000 / 5000 limit
```

**`--plan-only` exit point**: If set, present ISSUE_BOARD.md + STRATEGY_PLAN.md + EXPERIMENT_GAPS.md to the user and stop.

**Otherwise**: Present the strategy plan to the user. Ask: "Does this strategy look right? Adjust any response modes, angles, or priorities before I draft the rebuttal." Wait for confirmation before proceeding to Phase 3.

---

### Phase 3: Draft, Validate & Finalize

#### Step 3a: Draft Rebuttal

Write `REBUTTAL_DRAFT.md` following the confirmed strategy plan.

**Structure:**

1. **Global opener** (10-15% of budget)
   - Thank all reviewers for their thorough feedback
   - Address 2-4 shared themes with concise resolutions
   - Set the narrative: what the rebuttal will demonstrate

2. **Per-reviewer responses** (75-80% of budget, in priority order)
   For each issue, follow this pattern:
   - **Sentence 1**: Direct answer to the concern
   - **Sentences 2-4**: Grounded evidence (cite specific paper sections, tables, equations, or numbers)
   - **Last sentence**: Implication — why this strengthens the paper or resolves the concern
   - For `additional_experiment` issues: write full surrounding prose but replace results with `[INSERT: description of what goes here, e.g., "accuracy comparison between our method and Method Y on datasets A, B (Table format: Method | Dataset A | Dataset B)"]`

3. **Closing** (5-10% of budget)
   - Summary of what is resolved
   - Remaining items (with `[INSERT: ...]` marked)
   - Case for acceptance directed at meta-reviewer

**Drafting heuristics:**
- Evidence > assertion — always cite specific numbers, tables, sections
- Global narrative before per-reviewer detail
- Name closest prior work + exact delta for novelty disputes
- Concede narrowly when reviewer is correct — honest narrow concession > broad denial
- Answer champion reviewers too — reinforce their positive framing
- Don't argue unwinnable points more than once
- For theory: separate core contribution from technical assumptions
- Concrete numbers for counter-intuitive claims

**Hard rules:**
- NEVER invent experiments, numbers, derivations, or citations
- NEVER promise experiments the user hasn't confirmed
- Every claim must trace to: paper content, reviewer's own statement, or `[INSERT: ...]` placeholder
- If no strong evidence exists for a point, say less not more

#### Step 3b: Automated Lints

Run 5 checks on the draft and write results to `LINT_REPORT.md`:

1. **Coverage check** — For every issue in ISSUE_BOARD.md, verify there is a corresponding response in the draft. Flag any missing issues.

2. **Provenance check** — For every factual claim in the draft:
   - Claims citing paper sections/tables/equations: verify the referenced section/table exists in the paper
   - Claims citing reviewer statements: verify the quote appears in REVIEWS_RAW.md
   - `[INSERT: ...]` placeholders: verify correct formatting
   - Other factual claims with no clear source: flag as "needs manual verification"

3. **Tone check** — Flag these problematic patterns:
   - Aggressive: "the reviewer is wrong", "this is clearly stated", "obviously"
   - Submissive: "we apologize", "we are sorry", excessive hedging
   - Evasive: changing the subject, answering a different question
   - Replace with neutral-professional alternatives

4. **Consistency check** — Verify no contradictions across reviewer replies (e.g., telling R1 "we do X" and R2 "we don't do X")

5. **Character count check** — Count exact characters in the draft. If over the limit, compress using this priority:
   1. Identify and merge duplicate arguments across reviewer responses
   2. Remove filler phrases and tighten wording throughout
   3. Trim responses to minor issues from champion reviewers
   4. Shorten closing section
   5. Compress opener to bare essentials
   6. NEVER drop responses to critical/major issues
   7. If still over after all compression, flag to user: "Cannot fit within limit — need manual cuts"

#### Step 3c: Stress Test (Adversarial Self-Review)

Re-read the entire draft from the perspective of an adversarial meta-reviewer. Systematically check:

1. **Unanswered concerns** — Any issue from ISSUE_BOARD.md that the draft fails to address convincingly?
2. **Unsupported claims** — Any factual statement not traceable to paper, review, or `[INSERT: ...]`?
3. **Risky promises** — Any commitment to work the user hasn't confirmed?
4. **Tone problems** — Aggressive, defensive, evasive, or submissive passages?
5. **Backfire risk** — Which paragraph is most likely to annoy the meta-reviewer? Why?

Write findings to `STRESS_TEST.md` with a verdict: `safe_to_submit` | `needs_revision`.

If `needs_revision`: apply minimal grounded fixes (no invented evidence), re-run the lint checks, and produce the final version. Maximum 1 revision round. If still problematic after revision, flag remaining issues to user for manual intervention.

#### Step 3d: Finalize — Two Outputs

Produce two versions:

1. **`PASTE_READY.txt`** — Strict venue-compliant version
   - Plain text only (no markdown formatting)
   - Exact character count within venue limit
   - Ready to paste directly into OpenReview/CMT/HotCRP
   - `[INSERT: ...]` placeholders preserved for user to fill

2. **`REBUTTAL_DRAFT_rich.md`** — Extended version
   - Same structure with more detail: fuller explanations, additional evidence, optional paragraphs
   - Sections marked `[OPTIONAL — cut if over limit]` for easy trimming
   - Pre-written material for potential follow-up rounds
   - Authors read this version, then decide what to keep/cut/rewrite

Present to user with:
- Character count of PASTE_READY.txt vs venue limit
- Number and list of `[INSERT: ...]` placeholders that need filling
- Any remaining risks from STRESS_TEST.md
- Suggested next steps (fill placeholders, run experiments, review rich version)

---

### Follow-up Rounds (`--followup`)

When re-invoked with `--followup`:

1. **Load state**: Read existing output directory (requires ISSUE_BOARD.md, STRATEGY_PLAN.md, REBUTTAL_DRAFT.md at minimum). If directory is missing or incomplete, ask user for the correct path.

2. **Parse new comments**: Read the updated reviews file. Identify new reviewer comments that weren't in the original REVIEWS_RAW.md.

3. **Link or create issues**: For each new comment:
   - If it relates to an existing issue in ISSUE_BOARD.md, link it and update the issue status
   - If it's a new concern, create a new issue entry
   - If the new comment contradicts a prior rebuttal claim, flag as conflict and ask user for resolution

4. **Draft delta reply**: Write responses to new comments only — not a full rewrite. Reference prior rebuttal responses where relevant.

5. **Validate**: Re-run lint checks and stress test on the delta reply.

6. **Save**: Append to `FOLLOWUP_LOG.md` with round number and timestamp.

**Follow-up rules:**
- Escalate technically, not rhetorically
- Concede if reviewer is right and no new evidence exists
- Stop arguing immovable points — answer once and move on
- If same issue is re-raised, reference prior response and only add new content if prior response was insufficient

---

## Output Directory

All outputs are saved to: `./output/rebuttal/YYYY-MM-DD-HHMMSS/`

```
./output/rebuttal/YYYY-MM-DD-HHMMSS/
├── REVIEWS_RAW.md           # Verbatim copy of input reviews
├── ISSUE_BOARD.md           # Phase 1: classified concerns + situation assessment
├── STRATEGY_PLAN.md         # Phase 2: per-reviewer response strategy + character budget
├── EXPERIMENT_GAPS.md       # Phase 2: experiments needed with priorities
├── REBUTTAL_DRAFT.md        # Phase 3: working draft
├── REBUTTAL_DRAFT_rich.md   # Phase 3: extended version with optional sections
├── PASTE_READY.txt          # Phase 3: venue-compliant plain text for submission
├── LINT_REPORT.md           # Phase 3: automated lint check results
├── STRESS_TEST.md           # Phase 3: adversarial self-review findings
└── FOLLOWUP_LOG.md          # Follow-up round responses (if --followup)
```

## Best Practices

1. **Provide complete reviews**: Copy the full review text from OpenReview including scores and confidence — more context leads to better analysis
2. **Include reviewer IDs**: Preserve reviewer numbering from the venue system
3. **Specify the venue**: While auto-detection works, explicit `--venue` ensures correct character limits and format
4. **Use `--plan-only` first**: Review the strategy before committing to a full draft, especially for contentious reviews
5. **Fill placeholders promptly**: After running experiments, replace `[INSERT: ...]` markers with actual results
6. **Review the rich version**: REBUTTAL_DRAFT_rich.md contains extra material useful for follow-up rounds
7. **Check character count**: Always verify PASTE_READY.txt fits within the venue limit before submitting
8. **Don't over-argue**: If the strategy marks something as `narrow_concession`, trust that framing — conceding gracefully is stronger than arguing weakly

## Limitations

- Does NOT run experiments — produces placeholders where experimental results are needed
- Does NOT edit or upload revised PDFs
- Does NOT submit to OpenReview/CMT/HotCRP
- Cannot verify claims about unpublished or in-progress work
- Novelty assessment for `nearest_work_delta` depends on knowledge of the field
- Character count is approximate until PASTE_READY.txt is generated

## Related Skills

- `paper-reviewing` — Generate conference-style reviews (useful for self-review before submission)
- `paper-polishing` — Get ICML meta-review style feedback on drafts
- `citation-assistant` — Find and insert missing citations
- `literature-survey` — Survey related work for novelty defense
