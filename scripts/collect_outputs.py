#!/usr/bin/env python3
"""
Collect multi-view outputs from 2D→3D generation methods.

Target: 20 prompts × 3 methods × 6 views = 360 images

Usage:
  1. Run 2-3 public methods (CFD, RecDreamer, etc.) or use demo outputs
  2. Place raw outputs in data/raw_outputs/{method}/{prompt_id}/
  3. Run this script to copy/organize into processed_views/
  4. Or run preprocess_views.py directly if raw format matches

Expected raw layout (adapt to your source):
  data/raw_outputs/{method}/{prompt_id}/view_0.png ... view_5.png

Output layout:
  data/processed_views/{method}/{prompt_id}/view_0.png ... view_5.png
  data/processed_views/{method}/{prompt_id}/meta.json
"""

import json
import shutil
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw_outputs"
PROCESSED_DIR = REPO_ROOT / "data" / "processed_views"
PROMPTS_CSV = REPO_ROOT / "data" / "prompts.csv"

# Config
NUM_VIEWS = 6
METHODS = ["method_a", "method_b", "method_c"]  # Replace with actual method names


def load_prompt_ids() -> list[str]:
    """Load prompt IDs from prompts.csv."""
    import csv
    ids = []
    with open(PROMPTS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.append(row["prompt_id"])
    return ids


def collect_from_raw(method: str, prompt_id: str) -> bool:
    """
    Copy raw outputs to processed_views with standard naming.
    Returns True if successful.
    """
    src = RAW_DIR / method / prompt_id
    dst = PROCESSED_DIR / method / prompt_id
    dst.mkdir(parents=True, exist_ok=True)

    # Try common naming patterns
    patterns = [
        [f"view_{i}.png" for i in range(NUM_VIEWS)],
        [f"{i:02d}.png" for i in range(NUM_VIEWS)],
        [f"angle_{i}.png" for i in range(NUM_VIEWS)],
    ]

    found = False
    for names in patterns:
        if all((src / n).exists() for n in names):
            for i, n in enumerate(names):
                shutil.copy2(src / n, dst / f"view_{i}.png")
            found = True
            break

    if not found:
        # List what's there for debugging
        files = list(src.glob("*.png")) if src.exists() else []
        if len(files) >= NUM_VIEWS:
            for i, f in enumerate(sorted(files)[:NUM_VIEWS]):
                shutil.copy2(f, dst / f"view_{i}.png")
            found = True

    if found:
        meta = {
            "method": method,
            "prompt_id": prompt_id,
            "num_views": NUM_VIEWS,
        }
        with open(dst / "meta.json", "w") as f:
            json.dump(meta, f, indent=2)

    return found


def main():
    prompt_ids = load_prompt_ids()
    print(f"Loaded {len(prompt_ids)} prompts: {prompt_ids[:5]}...")

    for method in METHODS:
        for pid in prompt_ids:
            ok = collect_from_raw(method, pid)
            status = "✓" if ok else "✗"
            print(f"  {status} {method}/{pid}")

    print("\nDone. Run preprocess_views.py next to generate grids and standardize.")


if __name__ == "__main__":
    main()
