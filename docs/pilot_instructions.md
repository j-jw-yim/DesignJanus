# Pilot Study Instructions

**Goal:** Test the annotation interface with 5–8 people before full data collection.

---

## What to Look For

| Issue | How to detect |
|-------|---------------|
| **Confusing labels** | Raters ask "what does X mean?" or interpret differently |
| **Redundant categories** | Two dimensions always rated the same; consider merging |
| **Inconsistent answers** | Same sample gets very different scores from different raters |
| **Ambiguous prompts** | Raters unsure what the object "should" look like |
| **Low-quality samples** | Outputs too blurry or broken to judge fairly |
| **Too long** | Annotation takes >5 min per sample; people fatigue |

---

## Pilot Checklist

- [ ] Recruit 5–8 raters (can be friends, lab mates, or yourself multiple times)
- [ ] Give them the rubric (docs/rubric.md) to read first
- [ ] Have them annotate 5–10 samples each
- [ ] Debrief: ask what was confusing
- [ ] Compute inter-rater agreement (e.g., Krippendorff's alpha) if possible
- [ ] Note which categories correlate highly (candidates for merging)
- [ ] Estimate time per sample

---

## Post-Pilot Refinement

After the pilot:

1. **Merge categories** if two are always rated similarly (e.g., identity + geometry)
2. **Rewrite instructions** for any label that caused confusion
3. **Remove bad prompts** that are too ambiguous
4. **Shorten the task** if needed (fewer dimensions or fewer samples per rater)
5. **Add examples** to the rubric for the trickiest categories

---

## Debrief Questions (Ask Raters)

1. Which rating was hardest to use?
2. Did any two categories feel like the same thing?
3. Were any prompts unclear?
4. How long did each sample take?
5. Would you change anything about the interface?
