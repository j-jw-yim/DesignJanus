# DesignJanus: Annotation Rubric

**Purpose:** Make labels tight enough that two different raters would mostly agree.

---

## 1. Identity Inconsistency

**Definition:** Front view and side/back view look like different objects—the object seems to change identity across viewpoints.

**What to look for:** Does the object from one angle look like it could be the same physical object from another angle? Or does it feel like a different design entirely?

| Counts | Does not count |
|--------|-----------------|
| Chair from front has 4 legs, from back has 3 legs | Chair has 4 legs; one is occluded from front view |
| Bag has one strap from left, two straps from right | Strap is hidden behind the bag in one view |
| Mug handle is on the right in one view, left in another | Handle position is consistent; only perspective changes |

---

## 2. Geometry Inconsistency

**Definition:** Parts appear or disappear across views, symmetry breaks, or implausible concavities/convexities emerge.

**What to look for:** Does the 3D shape stay coherent? Do parts vanish or materialize? Is symmetry violated in a way that cannot be explained by occlusion?

| Counts | Does not count |
|--------|-----------------|
| Handle visible in view 1, completely absent in view 2 | Handle is occluded by the mug body in one view |
| One leg shorter than the other when viewed from front | Legs are symmetric; foreshortening makes one look shorter |
| Extra bulge or hole appears in one view only | Normal surface curvature; no new topology |

---

## 3. Semantic-Part Inconsistency

**Definition:** Recognizable parts (handles, ears, wheels, straps, limbs) shift position, duplicate, or behave implausibly across views.

**What to look for:** Do named parts stay in the right place? Do they multiply? Do they move when they shouldn’t?

| Counts | Does not count |
|--------|-----------------|
| Two handles on one side of a mug | Single handle; consistent across views |
| Ear of a character moves when rotating | Ear stays fixed; only lighting changes |
| Strap of a bag appears on both left and right | Single strap; visible from both sides when rotated |

---

## 4. Material Inconsistency

**Definition:** Texture, color, or reflectance changes across views in a way that suggests different materials rather than lighting.

**What to look for:** Does the surface look like the same material from all angles? Or does wood become plastic, metal become matte?

| Counts | Does not count |
|--------|-----------------|
| Wood grain shifts to a different pattern in another view | Same grain; different lighting makes it look darker |
| Metal surface becomes matte in one view | Specular highlight moves with viewpoint |
| Color changes from red to orange across views | Slight color variation from lighting; same base color |

---

## 5. Silhouette Inconsistency

**Definition:** The outline or contour of the object changes implausibly across adjacent views—jumps, collapses, or expands in ways that violate smooth rotation.

**What to look for:** If you imagine smoothly rotating the object, would the silhouette change gradually? Or does it jump or collapse between nearby viewpoints?

| Counts | Does not count |
|--------|-----------------|
| Contour collapses between view 2 and 3 | Silhouette changes smoothly as object rotates |
| Outline jumps or doubles between adjacent views | Normal occlusion; part goes behind another |
| Back view has completely different shape than side | Gradual transition; back is consistent with sides |

---

## Rating Scales (1–5)

For each dimension, use:

| Score | Meaning |
|-------|---------|
| 1 | Severe inconsistency; clearly different object or broken |
| 2 | Noticeable inconsistency; distracting |
| 3 | Mild inconsistency; some doubt |
| 4 | Mostly consistent; minor issues |
| 5 | Fully consistent; same object from all views |

**Design usefulness (1–5):** Would you use this as a design reference?

| Score | Meaning |
|-------|---------|
| 1 | No; too broken to be useful |
| 2 | Probably not; major issues |
| 3 | Maybe; with caveats |
| 4 | Yes; minor issues only |
| 5 | Yes; fully usable |

---

## Failure Tags (Multi-Select)

Check all that apply:

- **Part duplication** — A part appears twice (e.g., two handles)
- **Disappearing part** — A part vanishes across views
- **Asymmetry drift** — Left/right symmetry breaks
- **Texture drift** — Material/texture changes across views
- **Shape collapse** — Silhouette or volume collapses
- **Front-back mismatch** — Front and back look like different objects

---

## Rater Instructions (Summary)

1. Look at all 6 views before rating.
2. Rate each dimension independently; use the full 1–5 scale.
3. Check failure tags only when you observe that specific problem.
4. When in doubt, favor the lower score for consistency and the higher score for usefulness only if you would actually use it.
