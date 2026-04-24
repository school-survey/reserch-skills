---
name: idea-to-proposal
description: >
  Multi-dimensional research idea evaluation with iterative refinement and publication-quality
  proposal generation. Takes any research idea (free text, structured brief, paper extension,
  or file path), scores it across 8 dimensions (novelty, technical soundness, feasibility,
  significance, clarity, experimental validity, scalability, positioning), refines autonomously
  for 2-3 rounds, then generates a detailed proposal with method design (architecture diagrams,
  equations, pseudocode), experiment plan (benchmarks, baselines, ablations, supplementary
  experiments), and qualitative/quantitative analysis plans. Use when the user wants to
  "evaluate my idea", "research proposal", "refine this idea", "idea to proposal",
  "score my research idea", or "turn this idea into a paper plan".
user-invocable: true
argument-hint: "<idea-text | file-path | arxiv-url> [--target-venue NeurIPS] [--threshold 7] [--max-rounds 3]"
---

# Idea-to-Proposal Skill

## Overview

This skill takes a raw research idea through a rigorous multi-phase pipeline:

1. **Idea Structuring** — Parse any input format into a structured research brief
2. **Literature Search + 8-Dimension Evaluation** — Parallel agents search literature and score the idea
3. **Autonomous Refinement Loop** — Iteratively improve weak dimensions until all meet threshold
4. **Human Review Gate** — Present scores and refined idea for user approval
5. **Proposal Generation** — Parallel agents write method design and experiment plan

The output is a publication-quality research proposal suitable for a top-tier AI conference, saved to the user's Obsidian vault.

## Setup

Before running the skill, install dependencies:

```bash
pip install -r "BASE_DIR/scripts/requirements.txt"
```

Required packages:
- `arxiv` — arXiv API access
- `requests` — HTTP requests for paper fetching
- `bibtexparser` — BibTeX parsing and generation
- `semanticscholar` — Semantic Scholar API integration

## Parameters

Parse the following from `$ARGUMENTS`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--target-venue` | none (general) | Conference/journal: NeurIPS, ICML, CVPR, ACL, AAAI, ICCV, ICLR |
| `--threshold` | 7 | Minimum score (1-10) across all 8 dimensions to pass |
| `--max-rounds` | 3 | Maximum autonomous refinement rounds before human gate |
| `--domain` | auto-detect | Research domain for literature search focus |

Everything else in `$ARGUMENTS` is the idea input (text, file path, or URL).

## Output Directory

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/My_note/10_Projects/Idea-Proposals/YYYY-MM-DD-<topic>/
├── idea-evolution.md          # Version history through refinement rounds
├── evaluation-report.md       # Final scores + per-dimension analysis
├── proposal.md                # The full research proposal
├── references.bib             # All collected BibTeX citations
├── experiment-benchmarks.md   # Detailed benchmark/baseline survey
└── figures/                   # Mermaid diagrams
```

**Collision handling:** If directory exists, create versioned copy (`-v2`, `-v3`, etc.).

## Output Quality Targets

- **Proposal length:** 10-15 pages (Markdown), approximately 5000-8000 words
- **Target format:** Conference pre-proposal or detailed concept paper
- **Assumed reader:** Program committee member from neighboring subfield
- **Math depth:** Key equations with intuition; full proofs only if central to contribution
- **Citation style:** `[Author et al., Year]` with corresponding `references.bib`

---

## Phase 1: Idea Structuring

**Purpose:** Parse any input format into a structured research brief.

### Input Detection

Detect input type from `$ARGUMENTS`:

- **File path** — Ends in `.md`, `.txt`, or is an absolute/relative path to a file
  - Read file content, extract the idea description
- **arXiv URL** — Contains `arxiv.org/abs/`
  - Extract paper ID, fetch metadata via `paper_search.py --arxiv-id <ID>`
  - Treat as paper-extension input: user wants to extend/improve this paper
- **PDF path** — Ends in `.pdf`
  - Read with pagination (pages 1-20); extract core concepts
  - Treat as paper-extension input
- **Free text** — Any other format
  - Parse directly as idea description

### Structured Brief Schema

Normalize all inputs into this schema:

```markdown
## Research Idea Brief
- **Problem Statement**: What gap/limitation exists?
- **Proposed Approach**: Core technical idea (1-3 sentences)
- **Key Innovation**: What's novel vs. prior work?
- **Target Domain**: e.g., multi-agent systems, NLP, CV, RL
- **Target Venue**: (from --target-venue or "General")
- **Input Type**: free-text | structured | paper-extension
- **Reference Papers**: (if provided, extracted metadata)
```

### Completeness Rules
- **Required:** Problem Statement, Proposed Approach, Target Domain
- **Optional:** Target Venue, Reference Papers, Key Innovation
- If Key Innovation missing: infer from Proposed Approach
- If Target Venue missing: prompt user; if skipped, set to "General (all venues)"
- If Reference Papers missing: leave blank; populated from Phase 2

### Workflow
1. Detect input type
2. If paper-extension: read paper, extract core concepts (following `paper-triggered-survey` patterns)
3. Normalize into structured brief schema
4. If any required field is unclear, ask user for clarification
5. Present brief to user for confirmation
6. Create output directory; save brief as Version 0 in `idea-evolution.md`

**Wait for user confirmation before proceeding to Phase 2.**

---

## Phase 2: Literature Search + Multi-Dimensional Evaluation

Launch **two parallel agents** via the Agent tool.

### Agent A: Literature Search

**Agent prompt must include:**
- The structured brief from Phase 1
- Instructions to use `paper_search.py`

**Agent A workflow:**
1. Generate 5-8 search queries from the brief:
   - Method-focused queries (technique + domain)
   - Problem-focused queries (problem statement keywords)
   - Cross-domain queries (technique applied in other domains)
2. For each query, run:
   ```bash
   python "BASE_DIR/scripts/paper_search.py" \
     --query "<query>" \
     --max-results 20 \
     --output json \
     --sort relevance
   ```
3. Deduplicate results across queries
4. Identify seminal works (5-year window) vs. recent advances (1-2 years)
5. Classify papers into 3-6 thematic clusters
6. Extract SOTA baselines and benchmark datasets for the target task
7. For each key paper, fetch BibTeX:
   ```bash
   python "BASE_DIR/scripts/bibtex_utils.py" \
     fetch \
     --title "<paper-title>"
   ```
8. Return structured results: paper list with themes, benchmarks, baselines, gaps

**Graceful degradation:**
- 0-2 papers found: Flag as "Highly Novel / Unexplored Area"
- 3-10 papers: Proceed with reduced context
- For niche ideas: identify related task benchmarks from adjacent domains

### Agent B: 8-Dimension Evaluation

**Agent B runs AFTER Agent A completes** (needs literature context for accurate Novelty and Positioning scores).

Score the idea 1-10 on each dimension using the evaluation rubric (see `references/evaluation-rubric.md`):

| Dimension | Key Question |
|-----------|-------------|
| **Novelty** | Does prior work already solve this? How differentiated from closest work? |
| **Technical Soundness** | Is the method theoretically grounded? Any logical gaps? |
| **Feasibility** | Data/compute/time realistic? For agent-based proposals: estimate token cost (model, calls/run, input/output tokens, $/run) |
| **Significance** | How important is the problem? Size of potential impact? |
| **Clarity** | Is the idea unambiguous? Could someone implement from this description? |
| **Experimental Validity** | Can claims be tested? Are metrics well-defined? |
| **Scalability** | Does approach generalize beyond the specific setup? |
| **Positioning** | Fits target venue? Right timing for the community? |

**Output format:**
```markdown
## Evaluation Round 1
| Dimension | Score | Justification |
|-----------|-------|---------------|
| Novelty | X/10 | [2-3 sentence justification citing specific papers] |
| Technical Soundness | X/10 | [justification] |
| Feasibility | X/10 | [justification; token cost if agent-based] |
| Significance | X/10 | [justification] |
| Clarity | X/10 | [justification] |
| Experimental Validity | X/10 | [justification] |
| Scalability | X/10 | [justification] |
| Positioning | X/10 | [justification] |

**Overall: X.X/10**
**Weakest dimensions:** [list dimensions below threshold]
**Refinement targets:**
- [Dimension]: [specific suggestion for improvement]
- [Dimension]: [specific suggestion for improvement]
```

Save evaluation to `evaluation-report.md`.

---

## Phase 3: Autonomous Refinement Loop

**Goal:** Improve the idea until ALL dimensions score ≥ threshold (default 7/10).

### Loop Logic

```
for round in 1..max_rounds:
    1. Identify dimensions scoring < threshold
    2. For each weak dimension, generate specific refinement actions:
       - Novelty low       → Differentiate from closest prior work, add unique component
       - Tech Soundness low → Add theoretical justification, fix logical gaps
       - Feasibility low    → Simplify architecture, reduce data/compute needs
       - Significance low   → Strengthen problem motivation, broaden impact scope
       - Clarity low        → Rewrite ambiguous parts, add concrete examples
       - Exp Validity low   → Add metrics, design stronger evaluation plan
       - Scalability low    → Generalize approach, remove domain-specific assumptions
       - Positioning low    → Adjust framing for target venue, cite venue-relevant papers
    3. Apply refinements to structured brief → produce updated version
    4. Re-evaluate all 8 dimensions on updated version
    5. Append to idea-evolution.md:
       - Round number
       - Before/after scores for each dimension
       - Changes made with reasoning
    6. If ALL dimensions ≥ threshold → break loop
```

### Refinement Rules
- **Conflict resolution:** If refinements for different dimensions conflict, prioritize the dimension with the largest gap from threshold
- **Additive only:** Never contradict a refinement the user previously approved
- **Structural limitations:** If a dimension is stubbornly low after 2 rounds, flag it as a structural limitation rather than over-engineering a fix

### Literature Context Update Policy
- If refinement modifies < 30% of technical approach: reuse Phase 2 literature context
- If refinement substantially pivots (≥ 30% change): trigger 1-2 supplementary search queries on new components only
- Log which policy was applied each round

---

## Phase 4: Human Review Gate

Present the following to the user and **wait for their response:**

```markdown
## Idea Refinement Complete — Review Required

### Final Scores (Round N)
| Dimension | Score | Status |
|-----------|-------|--------|
| Novelty | X/10 | ✓/✗ |
| Technical Soundness | X/10 | ✓/✗ |
| Feasibility | X/10 | ✓/✗ |
| Significance | X/10 | ✓/✗ |
| Clarity | X/10 | ✓/✗ |
| Experimental Validity | X/10 | ✓/✗ |
| Scalability | X/10 | ✓/✗ |
| Positioning | X/10 | ✓/✗ |
| **Overall** | **X.X/10** | **Ready / Not Ready** |

### Evolution Summary
- Round 0 → 1: [changes and score deltas]
- Round 1 → 2: [changes and score deltas]
- Round 2 → 3: [changes and score deltas]

### Structural Limitations (if any)
- [Dimension]: Capped at X/10 because [reason]

### Current Idea (Refined Version)
[Full structured brief — latest version]

### Options
- **proceed** — Generate full proposal
- **refine [dimension]** — Further refine specific dimension(s)
- **modify** — Manually edit the idea, then re-evaluate
- **pivot** — Substantially change direction, restart from Phase 1
- **abort** — Stop here, keep all artifacts
```

### Status Determination
- **Ready:** ALL dimensions ≥ threshold
- **Not Ready:** Any dimension < threshold after max rounds

### Response Handling
- `proceed` → Phase 5 (works even if "Not Ready" — user's choice)
- `refine X` → Additional targeted refinement round on dimension X, then re-present
- `modify` → User provides edited brief, run 1 round of full re-evaluation
- `pivot` → Return to Phase 1 with new/revised idea
- `abort` → Save all artifacts, end skill

---

## Phase 5: Proposal Generation

Launch **two parallel agents** via Agent tool. Both receive:
- Refined idea (structured brief, latest version)
- Literature context (all papers from Phase 2 + any Phase 3 supplements)
- Evaluation history (all rounds, scores, refinements, structural limitations)

### Agent C: Method Design Writer

Agent C generates the following sections for `proposal.md`:

#### 1. Title & Abstract
- Concise, venue-appropriate title
- 150-250 word abstract covering problem, approach, key innovation, expected results

#### 2. Motivation & Problem Statement
- Gap identification with real-world relevance
- Formal problem definition (mathematical where appropriate)
- Why existing approaches are insufficient (cite Phase 2 literature)

#### 3. Related Work
- Organized by themes from Phase 2 literature search
- 3-6 thematic subsections
- Positioning statements: "Unlike [X] which..., our approach..."
- Citations as `[Author et al., Year]`

#### 4. Method Design
- **Architecture overview:** Mermaid diagram showing system components and data flow
  ```mermaid
  graph TD
      A[Input] --> B[Component 1]
      B --> C[Component 2]
      C --> D[Output]
  ```
- **Component descriptions:** Each component with:
  - Purpose and intuition
  - Mathematical formulation (LaTeX equations: `$\mathcal{L} = ...$`)
  - Input/output specification
- **Algorithm pseudocode:**
  ```
  Algorithm 1: [Name]
  Input: ...
  Output: ...
  1: for each ... do
  2:   compute ...
  3: end for
  4: return ...
  ```
- **Complexity analysis:** Time and space complexity
- **Token cost estimation** (for agent-based proposals):
  | Component | Model | Calls/Run | Input Tokens | Output Tokens | Cost/Run |
  |-----------|-------|-----------|--------------|---------------|----------|
  Mark as [ESTIMATED]. Include sensitivity note: "Cost is 2-3x if errors require re-runs."

#### 5. Limitations & Risks
- Reference structural limitations from evaluation
- Acknowledge known weaknesses transparently
- Discuss failure modes and mitigation strategies

### Agent D: Experiment Design Writer

Agent D generates the experiment sections for `proposal.md` and a separate `experiment-benchmarks.md`:

#### 6. Task Definition
- Formal problem setup
- Input/output specification
- Evaluation criteria

#### 7. Benchmark Survey
Search literature for benchmarks on this task:
- Temporal scope: last 5 years for recent, 10-year window for foundational
- Venues: top-tier (NeurIPS, ICML, CVPR, ACL) + domain-specific
- If niche: identify related task benchmarks; note "proposed new benchmark" as contribution

```bash
python "BASE_DIR/scripts/paper_search.py" \
  --query "<task> benchmark dataset" \
  --max-results 15 \
  --sort citations
```

Output table in `experiment-benchmarks.md`:
| Benchmark | Size | Task | Metrics | Used By (Papers) |
|-----------|------|------|---------|-------------------|

#### 8. Baseline Survey
Identify SOTA methods:
| Method | Year | Venue | Key Result | Code Available? |
|--------|------|-------|------------|-----------------|

#### 9. Main Experiment Settings
- Datasets chosen with justification (reference benchmark survey)
- Evaluation metrics (primary + secondary)
- Hyperparameter ranges
- Hardware requirements (GPU type, training time estimate)
- Number of runs / random seeds for statistical validity

#### 10. Ablation Studies
One per key design choice:

| Ablation | Component Removed/Replaced | Hypothesis | Metric |
|----------|---------------------------|------------|--------|
| w/o Component A | Remove A, keep rest | Performance drops by ~X% | Main metric |
| Replace B with baseline | Swap B for standard approach | Our B adds ~Y% improvement | Main metric |

#### 11. Supplementary Experiments
- **Efficiency analysis:** Latency, memory, token cost vs. baselines
- **Scaling behavior:** Vary data size / model size / agent count
- **Robustness tests:** Noisy input, distribution shift, adversarial examples

#### 12. Qualitative Analysis Plan
- Case studies: 2-3 success cases + 1-2 failure cases with analysis
- Visualization plan: attention maps, agent traces, t-SNE embeddings, decision trees (as appropriate)

#### 13. Quantitative Bonus Analysis
- Statistical significance: paired t-test or bootstrap confidence intervals
- Cross-domain transfer evaluation (if applicable)
- Error analysis: categorize failure types, quantify each category

### Assembly

After both agents complete:
1. Merge Agent C and Agent D outputs into single `proposal.md`
2. Ensure consistent notation (variable names, acronyms) across all sections
3. Add cross-references between method and experiment sections
4. Compile all citations into `references.bib`:
   ```bash
   python "BASE_DIR/scripts/bibtex_utils.py" \
     merge \
     --output "<output-dir>/references.bib"
   ```
5. Verify every `[Author et al., Year]` in proposal has a matching BibTeX entry
6. For non-academic sources (blog posts, preprints): auto-generate minimal BibTeX
7. Save all files to output directory

---

## Error Handling

### Agent Failures
- **Agent A (Literature) fails:** Retry with 3 queries. If still fails, proceed with empty context; flag evaluation as "Preliminary (Literature Search Failed)"
- **Agent B (Evaluation) fails:** Halt and inform user; suggest re-invocation
- **Agent C (Method Writer) fails:** Fill available sections, mark missing as [TODO]
- **Agent D (Experiment Writer) fails:** Same — partial output with [TODO] markers
- On partial failure: flag proposal as "Incomplete — manual review required"

### Checkpointing
- Each phase saves outputs to disk immediately upon completion
- If session is interrupted, user can re-invoke and reference existing output directory
- `idea-evolution.md` serves as the checkpoint log

### Multi-Idea Input
If Phase 1 detects multiple distinct ideas:
- Present options: evaluate all (parallel), select one, or merge
- Default: prompt user for clarification

---

## Usage Examples

**Free text idea:**
```
/idea-to-proposal Use graph attention networks to model inter-agent communication in cooperative MARL, where attention weights represent communication bandwidth allocation --target-venue NeurIPS
```

**Paper extension:**
```
/idea-to-proposal https://arxiv.org/abs/2305.12345 --target-venue ICML
```
(User describes extension in follow-up message after Phase 1 structuring)

**From Obsidian note:**
```
/idea-to-proposal ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/My_note/00_Inbox/my-research-idea.md
```

**With custom threshold:**
```
/idea-to-proposal "Diffusion-based program synthesis with formal verification feedback" --threshold 8 --max-rounds 5
```

---

## Dependencies

- `paper_search.py` — Unified academic paper search (arXiv + Semantic Scholar + DBLP)
- `bibtex_utils.py` — BibTeX reference management (fetch, merge, validate)
- Claude Agent tool — For launching parallel sub-agents in Phases 2 and 5
- Claude Read tool — PDF/file extraction
- Claude WebFetch tool — URL content extraction

---

**Version:** 1.0
**Last Updated:** 2026-03-23
