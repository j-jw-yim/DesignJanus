#!/usr/bin/env python3
"""
Preprocess multi-view outputs: resize, standardize, generate grids and optional GIFs.

Outputs:
  processed_views/{method}/{prompt_id}/view_0.png ... view_5.png  (standardized)
  processed_views/{method}/{prompt_id}/grid.png                   (6-view grid)
  processed_views/{method}/{prompt_id}/meta.json                   (metadata)
"""

import json
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise ImportError("pip install Pillow")

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed_views"
TARGET_SIZE = (256, 256)  # Standard size per view
GRID_COLS = 3
GRID_ROWS = 2


def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def resize_and_save(img: Image.Image, path: Path) -> None:
    img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
    img.save(path)


def make_grid(view_paths: list[Path]) -> Image.Image:
    """Create a 3x2 grid of view images."""
    images = [load_image(p) for p in view_paths]
    w, h = TARGET_SIZE
    grid_w = w * GRID_COLS
    grid_h = h * GRID_ROWS
    grid = Image.new("RGB", (grid_w, grid_h))

    for i, img in enumerate(images):
        img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        row, col = divmod(i, GRID_COLS)
        grid.paste(img, (col * w, row * h))

    return grid


def process_sample(method: str, prompt_id: str) -> bool:
    """Process one sample: resize views, create grid, update meta."""
    sample_dir = PROCESSED_DIR / method / prompt_id
    if not sample_dir.exists():
        return False

    view_paths = [sample_dir / f"view_{i}.png" for i in range(6)]
    if not all(p.exists() for p in view_paths):
        return False

    # Resize and overwrite
    for p in view_paths:
        img = load_image(p)
        resize_and_save(img, p)

    # Create grid
    grid = make_grid(view_paths)
    grid.save(sample_dir / "grid.png")

    # Update meta
    meta_path = sample_dir / "meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    meta.update({
        "method": method,
        "prompt_id": prompt_id,
        "num_views": 6,
        "target_size": list(TARGET_SIZE),
    })
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    return True


def discover_samples() -> list[tuple[str, str]]:
    """Find all method/prompt_id pairs with view_0..5."""
    samples = []
    for method_dir in PROCESSED_DIR.iterdir():
        if not method_dir.is_dir():
            continue
        method = method_dir.name
        for prompt_dir in method_dir.iterdir():
            if not prompt_dir.is_dir():
                continue
            prompt_id = prompt_dir.name
            views = [prompt_dir / f"view_{i}.png" for i in range(6)]
            if all(v.exists() for v in views):
                samples.append((method, prompt_id))
    return samples


def main():
    samples = discover_samples()
    if not samples:
        print("No samples found. Ensure processed_views/{method}/{prompt_id}/view_0..5.png exist.")
        print("")
        print("For testing:  python scripts/generate_placeholder_data.py")
        print("For real data: put outputs in raw_outputs/{method}/{prompt_id}/ then run collect_outputs.py")
        return

    print(f"Processing {len(samples)} samples...")
    for method, prompt_id in samples:
        ok = process_sample(method, prompt_id)
        status = "✓" if ok else "✗"
        print(f"  {status} {method}/{prompt_id}")

    print("\nDone. Grids saved as grid.png in each sample folder.")


if __name__ == "__main__":
    main()
