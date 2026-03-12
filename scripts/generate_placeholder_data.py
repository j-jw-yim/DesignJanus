#!/usr/bin/env python3
"""
Generate placeholder view images for testing the pipeline.

Creates simple colored squares so you can run the app and scripts
without real 3D outputs. Replace with real data when available.
"""

from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise ImportError("pip install Pillow")

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed_views"
PROMPTS_CSV = REPO_ROOT / "data" / "prompts.csv"

METHODS = ["method_a", "method_b", "method_c"]
SIZE = 256


def load_prompt_ids():
    import csv
    ids = []
    with open(PROMPTS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ids.append(row["prompt_id"])
    return ids


def make_placeholder_view(index: int, method_idx: int, prompt_idx: int) -> Image.Image:
    """Simple gradient/color per view for visual variety."""
    r = (50 + index * 30 + method_idx * 20) % 256
    g = (100 + prompt_idx * 10) % 256
    b = (150 + index * 25) % 256
    img = Image.new("RGB", (SIZE, SIZE), (r, g, b))
    return img


def main():
    prompt_ids = load_prompt_ids()
    print(f"Creating placeholders for {len(METHODS)} methods × {len(prompt_ids)} prompts")

    for mi, method in enumerate(METHODS):
        for pi, prompt_id in enumerate(prompt_ids):
            out_dir = PROCESSED_DIR / method / prompt_id
            out_dir.mkdir(parents=True, exist_ok=True)
            for vi in range(6):
                img = make_placeholder_view(vi, mi, pi)
                img.save(out_dir / f"view_{vi}.png")

    print("Done. Run: python scripts/preprocess_views.py")
    print("Then: streamlit run app/streamlit_app.py")
