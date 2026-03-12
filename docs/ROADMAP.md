# DesignJanus: Project Roadmap

A human-centered benchmark for perceptual multi-view consistency in 2D→3D generation.

---

## Milestone 1: Lock the scope and research question

**Goal:** Define exactly what you are studying.

**Deliverables:**
- One-sentence project thesis
- 3–4 research questions
- 5–6 inconsistency categories
- Success criteria for "done"

**Outcome:** You know what counts as a failure, what you are measuring, and what your smallest possible final demo looks like.

---

## Milestone 2: Read and reverse-engineer the core papers

**Goal:** Understand how current methods frame Janus / multi-view inconsistency.

**Deliverables:**
- 1-page notes doc
- Short taxonomy draft
- List of methods you might compare
- List of reusable repos / demo outputs

**Outcome:** Be able to explain, in plain English, what "multi-view consistency" means technically and perceptually.

---

## Milestone 3: Define the benchmark categories and prompt set

**Goal:** Create a small but intentional dataset of test cases.

**Object classes:** chairs, shoes, mugs, lamps, bags, toy characters, animals

**Deliverables:**
- 20–40 prompts total, organized by object category
- Spreadsheet with columns: `prompt_id`, `category`, `object_complexity`, `symmetry`, `expected_important_parts`

**Prompt design principles:**
- Parts are semantically meaningful
- View changes reveal new geometry
- "Same object" is easy to judge

---

## Milestone 4: Build the data generation pipeline

**Goal:** Collect outputs from public repos, demos, or local runs.

**Deliverables:**
- Standardized folder of outputs
- Fixed number of views per object (6 or 8)
- Same render format for every sample
- Metadata JSON for each example

**Example structure:**
```
data/
  method_a/
    prompt_001/
      view_0.png
      view_1.png
      ...
      meta.json
  method_b/
  baseline/
```

---

## Milestone 5: Create the failure annotation schema

**Goal:** Turn intuition into a reproducible rubric.

**Labels per sample:**
- Overall consistency: 1–5
- Identity consistency: 1–5
- Geometry consistency: 1–5
- Material consistency: 1–5
- Semantic parts consistency: 1–5
- Silhouette consistency: 1–5
- Design usefulness: 1–5

**Multi-select failure tags:**
- Part duplication
- Disappearing part
- Asymmetry drift
- Texture drift
- Shape collapse
- Front-back mismatch

**Deliverables:**
- Final rubric doc
- Examples of each failure mode
- Annotation instructions for raters

---

## Milestone 6: Build the rating interface

**Goal:** Simple interface in Gradio, Streamlit, or lightweight React.

**Per task:**
- Rotating GIF or 6-view grid
- Rating sliders
- Failure checkboxes
- Optional free-response box

**Deliverables:**
- Working local app
- CSV export of ratings
- Randomized presentation order
- Participant ID tracking

**MVP:** One page per sample, next button, results saved to CSV or SQLite.

---

## Milestone 7: Run a pilot study and refine the rubric

**Goal:** Test with 5–10 people before full data collection.

**Look for:**
- Confusing questions
- Categories people interpret inconsistently
- Tasks that take too long
- Prompts that are too ambiguous

**Deliverables:**
- Pilot results
- Revised instructions
- Revised label set
- Estimate of annotation time per sample

---

## Milestone 8: Add automatic proxy metrics

**Goal:** Compute simple automatic metrics for comparison.

**Possible proxies:**
- CLIP similarity across adjacent views
- DINO feature similarity across views
- Silhouette overlap / contour stability
- Color histogram variance
- Segmentation-based part consistency (if feasible)

**Deliverables:**
- Script to compute metrics for every sample
- Merged table of human ratings + automated metrics
- Basic plots and correlations

**Research question:** Which automated signals best predict what humans care about?

---

## Milestone 9: Analyze results and surface insights

**Goal:** Turn raw ratings into findings.

**Questions to answer:**
- Which failure type most hurts overall consistency?
- Which failure type most hurts design usefulness?
- Do certain object categories break more often?
- Which method performs best under human judgment?
- Do existing automatic metrics align with human perception?

**Deliverables:**
- 4–6 clean plots
- Ranked failure-type importance
- Short takeaway bullets
- Examples of high-scoring vs low-scoring samples

---

## Milestone 10: Package it into a polished artifact

**Goal:** Final presentation.

**Possible outputs:**
- GitHub repo
- Short paper or technical report
- Project website
- Interactive demo
- Portfolio case study

**Deliverables:**
- README with problem, method, and findings
- Visual examples of failure modes
- Benchmark description
- Final summary figure
- Future work section

**Final framing:** *We built a small human-centered benchmark showing that semantic-part and silhouette inconsistencies matter more to perceived design usefulness than mild lighting inconsistency.*

---

## Recommended final scope

| Dimension | Target |
|-----------|--------|
| Prompts | 20 |
| Methods | 3 |
| Views per sample | 6 |
| Raters | 20–30 |
| Failure categories | 5 main |

Enough to be meaningful without exploding scope.
