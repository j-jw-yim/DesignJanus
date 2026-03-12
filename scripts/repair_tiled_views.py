#!/usr/bin/env python3
"""
Repair samples where Zero123++ saved a single tiled image as view_0.png.
Splits the tiled 2x3 grid into view_0 through view_5.
"""

from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise ImportError("pip install Pillow")

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed_views"


def repair_sample(sample_dir: Path) -> bool:
    """If view_0 exists but view_5 doesn't, split view_0 (2x3 grid) into 6 views."""
    view0 = sample_dir / "view_0.png"
    view5 = sample_dir / "view_5.png"
    if not view0.exists() or view5.exists():
        return False

    img = Image.open(view0).convert("RGB")
    w, h = img.size
    tw, th = w // 3, h // 2
    for vi in range(6):
        row, col = vi // 3, vi % 3
        tile = img.crop((col * tw, row * th, (col + 1) * tw, (row + 1) * th))
        tile.save(sample_dir / f"view_{vi}.png")
    return True


def main():
    count = 0
    for method_dir in PROCESSED_DIR.iterdir():
        if not method_dir.is_dir():
            continue
        for prompt_dir in method_dir.iterdir():
            if not prompt_dir.is_dir():
                continue
            if repair_sample(prompt_dir):
                print(f"  ✓ {method_dir.name}/{prompt_dir.name}")
                count += 1
    print(f"\nRepaired {count} samples. Run: python scripts/preprocess_views.py")


if __name__ == "__main__":
    main()
