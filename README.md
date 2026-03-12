# DesignJanus

*A human-centered benchmark for perceptual multi-view consistency in 2D→3D generation.*

---

## Why This Exists

When we generate 3D objects from text or images, the results often look wrong when we rotate them. A chair might have four legs from the front and three from the back. A mug handle might appear on both sides. These "Janus" failures—named after the two-faced Roman god—are well known in the field, and recent methods like Consistent Flow Distillation and RecDreamer explicitly aim to reduce them.

But the field still asks: *how do we measure consistency?* Most evaluation relies on model-side metrics or image similarity scores. We rarely ask: *which kinds of inconsistency actually matter to people?* And to designers, who might use these outputs as references?

DesignJanus is a small, human-centered benchmark that fills that gap. Instead of building a new 3D generator, we ask: when multi-view outputs are inconsistent, which failures most reduce perceived coherence and design usefulness? The answer shapes how we should evaluate—and optimize—future methods.

---

## Research Questions

1. **Which inconsistency types are most noticeable to humans?**
2. **Which ones most reduce design usefulness?**
3. **Which simple automatic metrics best track human judgment?**

---

## What We Built

- **Taxonomy** — Five inconsistency categories (identity, geometry, semantic parts, material, silhouette) with clear definitions and rater instructions
- **Prompt set** — 20 prompts across furniture, accessories, household objects, and animals/characters
- **Benchmark data** — Multi-view outputs from SDXL + Zero123++ (Replicate), with 6 views per sample
- **Annotation interface** — Streamlit app for human ratings with 1–5 scales and failure tags
- **Analysis pipeline** — Scripts for automatic metrics (CLIP, silhouette, color) and merge with human ratings

---

## Project Structure

```
BeyondJanus/
├── data/
│   ├── prompts.csv              # 20 prompts by category
│   ├── processed_views/         # Multi-view images (method/prompt_id/)
│   ├── annotations/             # Human ratings (CSV per participant)
│   └── metrics/                # Automatic proxy metrics
├── app/
│   └── streamlit_app.py        # Annotation interface
├── scripts/
│   ├── collect_real_data.py    # Replicate / iso3d / dxgl data collection
│   ├── preprocess_views.py     # Resize, grid, metadata
│   ├── run_metrics.py         # CLIP, silhouette, color
│   └── merge_results.py        # Join annotations + metrics
├── notebooks/
│   ├── pilot_analysis.ipynb    # Inter-rater agreement, rubric refinement
│   └── final_analysis.ipynb   # Failure importance, metric correlation
└── docs/
    ├── project_brief.md        # Scope and deliverables
    ├── rubric.md              # Annotation taxonomy
    └── pilot_instructions.md   # Pilot study checklist
```

---

## Current Status

| Milestone | Status |
|-----------|--------|
| Taxonomy & rubric | ✅ |
| Prompt set (20) | ✅ |
| Data collection (Replicate) | ✅ 20 samples |
| Preprocessing & grids | ✅ |
| Annotation app | ✅ Ready |
| Pilot study (5–8 raters) | 🔲 Next |
| Automatic metrics | 🔲 Optional |
| Analysis & report | 🔲 After pilot |

---

## Quick Start

```bash
pip install -r requirements.txt

# If you need to collect data:
python scripts/collect_real_data.py --source replicate   # Replicate API
python scripts/collect_real_data.py --source iso3d_views # Free, from Hugging Face

python scripts/preprocess_views.py

# Run the annotation app
streamlit run app/streamlit_app.py
```

---

## Next Steps

1. **Run a pilot study** — Recruit 5–8 raters. Have them annotate 10–15 samples each. Use [docs/pilot_instructions.md](docs/pilot_instructions.md). Look for confusing labels, redundant categories, and prompts that are hard to interpret.

2. **Refine the rubric** — After the pilot, merge categories if needed, rewrite instructions, and remove ambiguous prompts. This step is where the benchmark becomes credible.

3. **Full annotation** — Scale to 20–30 raters. Aim for overlap on a subset to compute inter-rater agreement.

4. **Compute automatic metrics** — Run `python scripts/run_metrics.py` (requires PyTorch, CLIP). Merge with `python scripts/merge_results.py`.

5. **Analyze** — Use `notebooks/final_analysis.ipynb` to answer: which failure types hurt overall consistency most? Which hurt design usefulness? Which automatic metric best predicts human judgment?

6. **Package** — Write up findings in [docs/report.md](docs/report.md). A strong closing line: *Semantic-part and silhouette inconsistency mattered more to perceived design usefulness than mild material or lighting inconsistency.*

---

## Key Documents

- [Project Brief](docs/project_brief.md)
- [Annotation Rubric](docs/rubric.md)
- [Pilot Instructions](docs/pilot_instructions.md)

---

## Citation

If you use this benchmark or build on it:

```bibtex
@misc{designjanus,
  title = {DesignJanus: A Human-Centered Benchmark for Perceptual Multi-View Consistency in 2D→3D Generation},
  year = {2025},
  url = {https://github.com/j-jw-yim/BeyondJanus}
}
```
