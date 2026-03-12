# Milestone 1: Locked Scope and Research Questions

**Status:** Draft — ready for review and lock-in

---

## One-Sentence Project Thesis

**DesignJanus studies which kinds of multi-view inconsistency in 2D→3D outputs most reduce perceived coherence and design usefulness.**

---

## Research Questions

1. **Which inconsistency types are most noticeable to humans?**  
   Do raters reliably identify the same failure modes, and which categories get flagged most often?

2. **Which inconsistency types most reduce design usefulness?**  
   Does semantic-part or silhouette inconsistency hurt perceived usability more than mild lighting drift?

3. **Do automated metrics correlate with human judgments?**  
   Which proxy signals (CLIP, DINO, silhouette, color) best predict overall consistency and design usefulness?

4. **Are some object categories more sensitive than others?**  
   Do chairs, shoes, or characters show more or different failure patterns than mugs or lamps?

---

## Inconsistency Categories (5–6)

| # | Category | Definition | Example |
|---|----------|------------|---------|
| 1 | **Identity inconsistency** | Front view and side/back view look like different objects | Chair from front vs. chair from back has different legs, backrest |
| 2 | **Geometry inconsistency** | Parts appear/disappear, symmetry breaks, weird concavities | Handle appears in one view, vanishes in another; asymmetric legs |
| 3 | **Material inconsistency** | Texture or reflectance changes across views | Wood grain shifts; metal becomes matte |
| 4 | **Semantic part inconsistency** | Handles, ears, wheels, straps, limbs shift or duplicate | Two handles on one side; ear moves when rotating |
| 5 | **Silhouette inconsistency** | Outline changes implausibly across adjacent views | Contour jumps or collapses between nearby viewpoints |
| 6 | **Lighting/view entanglement** | Shading changes look like object changes rather than illumination | Shadow read as geometry; highlight mistaken for part |

**Hypothesis:** Humans will care most about semantic-part, silhouette, and identity inconsistency, and less about mild lighting inconsistency.

---

## Success Criteria for "Done"

### Minimal viable benchmark

- [ ] **20 prompts** across 6–8 object categories (chairs, shoes, mugs, lamps, bags, toys, animals)
- [ ] **3 methods** with standardized multi-view outputs
- [ ] **6 views per sample** in a fixed format
- [ ] **20–30 raters** complete the rating interface
- [ ] **5 main failure categories** with clear definitions and examples

### Deliverables

- [ ] **Working rating interface** — local app, CSV export, randomized order
- [ ] **Final rubric** — annotation instructions, examples per failure mode
- [ ] **Human ratings dataset** — merged with sample metadata
- [ ] **4–6 analysis plots** — failure-type importance, method comparison, metric correlation
- [ ] **Takeaway bullets** — which failures matter most for design usefulness
- [ ] **README** — problem, method, findings, visual examples

### Smallest possible final demo

A visitor can:

1. Read a 1-page summary of the problem and findings
2. See 2–3 example pairs (high vs. low consistency)
3. Understand the ranked failure-type importance
4. Optionally run the rating interface on a small subset

---

## What Counts as a Failure

A **failure** is any multi-view inconsistency where:

- The same 3D object, when viewed from different angles, appears to change in a way that violates physical plausibility or design coherence
- A human rater would say "this does not look like the same object" or "this would not be usable as a design reference"

**Not a failure:** Mild lighting variation, expected perspective foreshortening, or subtle texture sampling differences that do not affect perceived identity or usability.

---

## What We Are Measuring

| Construct | Operationalization |
|-----------|--------------------|
| **Overall consistency** | 1–5 scale: "Does this look like the same object from all views?" |
| **Design usefulness** | 1–5 scale: "Would this be usable as a design reference?" |
| **Per-category consistency** | 1–5 for identity, geometry, material, semantic parts, silhouette |
| **Failure presence** | Multi-select tags: part duplication, disappearing part, asymmetry drift, texture drift, shape collapse, front-back mismatch |

---

## Next Steps

1. Review and lock this scope (edit if needed)
2. Proceed to **Milestone 2**: Read core papers, refine taxonomy, list methods and repos
