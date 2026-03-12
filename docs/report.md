# DesignJanus: Report (Template)

*Fill in after completing analysis.*

---

## 1. Problem

2D→3D generation methods produce outputs that can look inconsistent across views. Current evaluation does not tell us which inconsistencies matter most to humans or to design usefulness.

## 2. Why Existing Evaluation Is Incomplete

[Brief: model-side metrics vs. perceptual/design-oriented evaluation.]

## 3. Taxonomy of Inconsistency

We define 5 categories: identity, geometry, semantic-part, material, silhouette. See [rubric.md](rubric.md).

## 4. Benchmark Setup

- 20 prompts across 4 object groups
- 3 methods
- 6 views per sample
- [N] raters

## 5. Human Study

- Interface: Streamlit app
- Dimensions: overall, identity, geometry, parts, material, silhouette, usefulness
- Failure tags: part duplication, disappearing part, asymmetry drift, texture drift, shape collapse, front-back mismatch

## 6. Automatic Metrics

- CLIP adjacent-view similarity
- Silhouette overlap
- Color variance
- (Optional) DINO similarity

## 7. Results

[Add 4–6 plots and tables.]

## 8. Key Insight

> Semantic-part inconsistency and silhouette drift mattered more to perceived design usefulness than mild material or lighting inconsistency.

*(Or your actual finding.)*

## 9. Limitations

- Small scale
- Limited methods
- [Other]

## 10. Future Work

- Larger benchmark
- More methods
- Calibrated PMCS metric
