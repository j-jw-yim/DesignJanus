"""
DesignJanus Annotation Interface

Each page shows one sample (6-view grid), rating sliders, failure checkboxes.
Saves to CSV with participant ID and randomized order.
"""

import csv
import random
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed_views"
ANNOTATIONS_DIR = REPO_ROOT / "data" / "annotations"
PROMPTS_CSV = REPO_ROOT / "data" / "prompts.csv"

ANNOTATIONS_DIR.mkdir(parents=True, exist_ok=True)

# Rating dimensions
DIMENSIONS = [
    ("overall", "Overall consistency", "Does this look like the same object from all views?"),
    ("identity", "Identity consistency", "Do front and back look like the same object?"),
    ("geometry", "Geometry consistency", "Do parts stay coherent? No vanishing/duplicating?"),
    ("parts", "Semantic parts consistency", "Do handles, straps, limbs stay in place?"),
    ("material", "Material consistency", "Does texture/color stay consistent?"),
    ("silhouette", "Silhouette consistency", "Does the outline change plausibly?"),
    ("usefulness", "Design usefulness", "Would you use this as a design reference?"),
]

FAILURE_TAGS = [
    "part_duplication",
    "disappearing_part",
    "asymmetry_drift",
    "texture_drift",
    "shape_collapse",
    "front_back_mismatch",
]


def load_prompts() -> list[dict]:
    rows = []
    with open(PROMPTS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def discover_samples() -> list[tuple[str, str]]:
    samples = []
    for method_dir in PROCESSED_DIR.iterdir():
        if not method_dir.is_dir():
            continue
        method = method_dir.name
        for prompt_dir in method_dir.iterdir():
            if not prompt_dir.is_dir():
                continue
            grid_path = prompt_dir / "grid.png"
            if grid_path.exists():
                samples.append((method, prompt_dir.name))
    return samples


def save_response(participant_id: str, sample_id: str, method: str, prompt_id: str, ratings: dict, failure_tags: list[str]):
    path = ANNOTATIONS_DIR / f"annotations_{participant_id}.csv"
    row = {
        "participant_id": participant_id,
        "sample_id": sample_id,
        "method": method,
        "prompt_id": prompt_id,
        **ratings,
        "failure_tags": "|".join(failure_tags) if failure_tags else "",
    }
    file_exists = path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main():
    st.set_page_config(page_title="DesignJanus Annotation", layout="wide")
    st.title("DesignJanus: Multi-View Consistency Annotation")

    samples = discover_samples()
    if not samples:
        st.error(
            "No samples found. Place processed views in "
            "data/processed_views/{method}/{prompt_id}/ with grid.png"
        )
        st.info("Run preprocess_views.py after collecting outputs.")
        return

    # Session state
    if "participant_id" not in st.session_state:
        st.session_state.participant_id = ""
    if "sample_order" not in st.session_state:
        st.session_state.sample_order = random.sample(samples, len(samples))
    if "current_idx" not in st.session_state:
        st.session_state.current_idx = 0
    if "started" not in st.session_state:
        st.session_state.started = False

    # Participant ID
    if not st.session_state.started:
        pid = st.text_input("Enter your participant ID", placeholder="e.g., p01")
        if st.button("Start"):
            if pid.strip():
                st.session_state.participant_id = pid.strip()
                st.session_state.started = True
                st.rerun()
            else:
                st.warning("Please enter a participant ID.")
        return

    idx = st.session_state.current_idx
    order = st.session_state.sample_order
    if idx >= len(order):
        st.success("You have completed all samples. Thank you!")
        return

    method, prompt_id = order[idx]
    sample_dir = PROCESSED_DIR / method / prompt_id
    grid_path = sample_dir / "grid.png"

    # Load prompt text from prompts.csv or meta.json
    prompts = {r["prompt_id"]: r for r in load_prompts()}
    prompt_text = prompts.get(prompt_id, {}).get("prompt_text", prompt_id)
    category = prompts.get(prompt_id, {}).get("category", "")
    meta_path = sample_dir / "meta.json"
    if meta_path.exists():
        import json
        meta = json.loads(meta_path.read_text())
        prompt_text = meta.get("prompt_text", prompt_text)

    st.caption(f"Participant: {st.session_state.participant_id} | Sample {idx + 1} of {len(order)}")
    st.subheader(f"Prompt: {prompt_text}")
    if category:
        st.caption(f"Category: {category}")

    # Grid
    if grid_path.exists():
        st.image(str(grid_path), use_container_width=True)
    else:
        # Fallback: show individual views
        cols = st.columns(3)
        for i in range(6):
            vp = sample_dir / f"view_{i}.png"
            if vp.exists():
                cols[i % 3].image(str(vp), caption=f"View {i}")

    # Ratings
    st.divider()
    ratings = {}
    for key, label, help_text in DIMENSIONS:
        ratings[key] = st.slider(label, 1, 5, 3, help=help_text)

    # Failure tags
    st.write("**Failure tags (check all that apply):**")
    failure_tags = []
    cols = st.columns(3)
    for i, tag in enumerate(FAILURE_TAGS):
        label = tag.replace("_", " ").title()
        if st.checkbox(label, key=f"tag_{idx}_{tag}"):
            failure_tags.append(tag)

    # Submit and next
    st.divider()
    if st.button("Next"):
        sample_id = f"{method}_{prompt_id}"
        save_response(
            st.session_state.participant_id,
            sample_id,
            method,
            prompt_id,
            ratings,
            failure_tags,
        )
        st.session_state.current_idx += 1
        st.rerun()


if __name__ == "__main__":
    main()
