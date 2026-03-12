#!/usr/bin/env python3
"""
Collect real multi-view outputs.

Sources:
  1. iso3d_views: FREE - Use iso3d images as 6 identical views (perfect consistency baseline)
  2. dxgl: FREE - Download from DX.GL (10 objects). May get 403 from their server.
  3. replicate: SDXL + Zero123++ (requires REPLICATE_API_TOKEN + billing)
  4. iso3d: iso3d + Zero123++ via Replicate (requires REPLICATE_API_TOKEN)

Usage:
  python scripts/collect_real_data.py --source iso3d_views --limit 10   # Free, always works
  python scripts/collect_real_data.py --source dxgl --limit 3
  python scripts/collect_real_data.py --source replicate --limit 5
"""

import argparse
import json
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed_views"
PROMPTS_CSV = REPO_ROOT / "data" / "prompts.csv"


def load_prompts(limit: int | None = None) -> list[dict]:
    import csv
    rows = []
    with open(PROMPTS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
            if limit and len(rows) >= limit:
                break
    return rows


# DX.GL free multi-view dataset (10 objects, 196 views each, CC0)
DXGL_OBJECTS = [
    ("apple", "Apple", "https://dx.gl/api/v/EJbs8npt2RVM/vCHDLxjWG65d/dataset"),
    ("cash_register", "Cash Register", "https://dx.gl/api/v/EJbs8npt2RVM/JfjLRexr6J7z/dataset"),
    ("drill", "Drill", "https://dx.gl/api/v/EJbs8npt2RVM/A0dcsk7HHgAg/dataset"),
    ("fire_extinguisher", "Fire Extinguisher", "https://dx.gl/api/v/EJbs8npt2RVM/cLgyqM5mhQoq/dataset"),
    ("led_lightbulb", "LED Lightbulb", "https://dx.gl/api/v/EJbs8npt2RVM/ZuYmv3K9xN7u/dataset"),
    ("measuring_tape", "Measuring Tape", "https://dx.gl/api/v/EJbs8npt2RVM/qqvDYx7RtHZd/dataset"),
    ("modern_arm_chair", "Modern Arm Chair", "https://dx.gl/api/v/EJbs8npt2RVM/KLBJAuie9JaB/dataset"),
    ("multi_cleaner", "Multi Cleaner 5L", "https://dx.gl/api/v/EJbs8npt2RVM/79gDW15Gw9Ft/dataset"),
    ("potted_plant", "Potted Plant", "https://dx.gl/api/v/EJbs8npt2RVM/o4c5zRyGuT7W/dataset"),
    ("wet_floor_sign", "Wet Floor Sign", "https://dx.gl/api/v/EJbs8npt2RVM/tHdRul1GzzoU/dataset"),
]


def collect_via_iso3d_views(limit: int | None = 20) -> None:
    """Use iso3d images as 6 identical views. Free, no API. Perfect consistency baseline."""
    try:
        from datasets import load_dataset
    except ImportError:
        raise ImportError("pip install datasets")

    ds = load_dataset("dylanebert/iso3d", split="train", trust_remote_code=True)
    rows = list(ds)[: limit or 20]

    method_name = "iso3d_views"
    out_dir = PROCESSED_DIR / method_name
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, row in enumerate(rows):
        prompt_id = f"iso3d_{i:03d}"
        sample_dir = out_dir / prompt_id
        if (sample_dir / "view_5.png").exists():
            print(f"  Skip {prompt_id}")
            continue

        img = row.get("image")
        if img is None or not hasattr(img, "save"):
            continue

        print(f"  [{i+1}/{len(rows)}] {prompt_id}")
        sample_dir.mkdir(parents=True, exist_ok=True)
        for vi in range(6):
            img.save(sample_dir / f"view_{vi}.png")

        prompt_text = row.get("prompt", row.get("text", str(prompt_id)))
        meta = {"method": method_name, "prompt_id": prompt_id, "prompt_text": prompt_text,
                "source": "iso3d_views", "num_views": 6}
        (sample_dir / "meta.json").write_text(json.dumps(meta, indent=2))
        print(f"    ✓ Saved 6 views (identical, perfect consistency)")


def collect_via_dxgl(limit: int | None = None) -> None:
    """Download free multi-view data from DX.GL. No API key required."""
    try:
        import zipfile
        import requests
    except ImportError:
        raise ImportError("pip install requests")

    method_name = "dxgl_multiview"
    out_dir = PROCESSED_DIR / method_name
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = REPO_ROOT / "data" / ".cache_dxgl"
    cache_dir.mkdir(parents=True, exist_ok=True)

    # DX.GL may block requests without a browser-like User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/zip,*/*",
    }

    objects = DXGL_OBJECTS[:limit] if limit else DXGL_OBJECTS

    for obj_id, obj_name, url in objects:
        sample_dir = out_dir / obj_id
        if (sample_dir / "view_5.png").exists():
            print(f"  Skip {obj_id} (already exists)")
            continue

        print(f"  Downloading {obj_name}...")
        zip_path = cache_dir / f"{obj_id}.zip"

        try:
            if not zip_path.exists():
                r = requests.get(url, headers=headers, timeout=120, stream=True)
                r.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            with zipfile.ZipFile(zip_path, "r") as zf:
                # List images: images/frame_00000.png, frame_00001.png, ...
                names = sorted(n for n in zf.namelist() if n.startswith("images/") and n.endswith(".png"))
                if len(names) < 6:
                    print(f"    ✗ Not enough views")
                    continue
                # Pick 6 evenly spaced
                step = max(1, len(names) // 6)
                indices = [i * step for i in range(6)][:6]
                selected = [names[i] for i in indices]

            sample_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                for vi, name in enumerate(selected):
                    data = zf.read(name)
                    (sample_dir / f"view_{vi}.png").write_bytes(data)

            meta = {
                "method": method_name,
                "prompt_id": obj_id,
                "prompt_text": obj_name,
                "source": "dxgl",
                "num_views": 6,
            }
            (sample_dir / "meta.json").write_text(json.dumps(meta, indent=2))
            print(f"    ✓ Saved 6 views")
        except Exception as e:
            print(f"    ✗ Error: {e}")


def collect_via_replicate(prompts: list[dict], method_name: str = "replicate_sdxl_zero123", delay: int = 12) -> None:
    """Use Replicate: SDXL (text→image) then Zero123++ (image→6 views)."""
    try:
        import replicate
        import requests
    except ImportError:
        raise ImportError("pip install replicate requests")

    token = __import__("os").environ.get("REPLICATE_API_TOKEN")
    if not token:
        raise RuntimeError("Set REPLICATE_API_TOKEN. Get one at https://replicate.com/account/api-tokens")

    SDXL_MODEL = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
    ZERO123_MODEL = "jd7h/zero123plusplus:c69c6559a29011b576f1ff0371b3bc1add2856480c60520c7e9ce0b40a6e9052"

    # With <$5 credit: 6 req/min, burst 1. Need ~10s between each API call.
    DELAY_BETWEEN_CALLS = delay
    RETRY_WAIT = 65  # Wait for rate limit reset

    out_dir = PROCESSED_DIR / method_name
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, row in enumerate(prompts):
        prompt_id = row["prompt_id"]
        prompt_text = row["prompt_text"]
        sample_dir = out_dir / prompt_id
        sample_dir.mkdir(parents=True, exist_ok=True)

        if (sample_dir / "view_5.png").exists():
            print(f"  Skip {prompt_id} (already exists)")
            continue

        print(f"  [{i+1}/{len(prompts)}] {prompt_id}: {prompt_text[:50]}...")

        for attempt in range(4):  # Up to 4 attempts (1 initial + 3 retries)
            try:
                # Step 1: Text → Image (SDXL)
                sdxl_out = replicate.run(
                    SDXL_MODEL,
                    input={
                        "prompt": prompt_text + ", isolated object on white background, product photo",
                        "width": 512,
                        "height": 512,
                    },
                )
                img_url = sdxl_out[0] if isinstance(sdxl_out, (list, tuple)) else sdxl_out
                if hasattr(img_url, "url"):
                    img_url = img_url.url
                img_url = str(img_url)

                time.sleep(DELAY_BETWEEN_CALLS)

                # Step 2: Image → 6 views (Zero123++)
                zero_out = replicate.run(
                    ZERO123_MODEL,
                    input={"image": img_url},
                )
                view_urls = [item.url if hasattr(item, "url") else str(item) for item in zero_out]

                # Zero123++ may return 1 tiled image (2x3 grid) or 6 separate URLs
                if len(view_urls) == 1:
                    r = requests.get(view_urls[0], timeout=60)
                    r.raise_for_status()
                    from PIL import Image
                    import io
                    img = Image.open(io.BytesIO(r.content)).convert("RGB")
                    w, h = img.size
                    # Assume 2 rows x 3 cols
                    tw, th = w // 3, h // 2
                    for vi in range(6):
                        row, col = vi // 3, vi % 3
                        tile = img.crop((col * tw, row * th, (col + 1) * tw, (row + 1) * th))
                        tile.save(sample_dir / f"view_{vi}.png")
                else:
                    for vi, url in enumerate(view_urls[:6]):
                        r = requests.get(url, timeout=60)
                        r.raise_for_status()
                        (sample_dir / f"view_{vi}.png").write_bytes(r.content)

                meta = {
                    "method": method_name,
                    "prompt_id": prompt_id,
                    "prompt_text": prompt_text,
                    "source": "replicate",
                    "num_views": 6,
                }
                (sample_dir / "meta.json").write_text(json.dumps(meta, indent=2))
                print(f"    ✓ Saved 6 views")
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "throttled" in err_str.lower():
                    if attempt < 3:
                        print(f"    Rate limited, waiting {RETRY_WAIT}s...")
                        time.sleep(RETRY_WAIT)
                    else:
                        print(f"    ✗ Error after retries: {e}")
                else:
                    print(f"    ✗ Error: {e}")
                    break

        time.sleep(DELAY_BETWEEN_CALLS)


def collect_via_iso3d(limit: int | None = 5) -> None:
    """Download iso3d images, run Zero123++ on each via Replicate."""
    try:
        from datasets import load_dataset
        import replicate
        import requests
    except ImportError:
        raise ImportError("pip install datasets replicate requests")

    ds = load_dataset("dylanebert/iso3d", split="train", trust_remote_code=True)
    rows = list(ds)
    if limit:
        rows = rows[:limit]

    method_name = "iso3d_zero123"
    out_dir = PROCESSED_DIR / method_name
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, row in enumerate(rows):
        prompt_id = f"iso3d_{i:03d}"
        sample_dir = out_dir / prompt_id
        sample_dir.mkdir(parents=True, exist_ok=True)

        if (sample_dir / "view_5.png").exists():
            print(f"  Skip {prompt_id}")
            continue

        img = row.get("image")
        if img is None:
            continue

        # Save PIL image to temp file; Replicate accepts file objects
        tmp_path = sample_dir / "_input.png"
        if hasattr(img, "save"):
            img.save(tmp_path)
        else:
            continue

        print(f"  [{i+1}/{len(rows)}] {prompt_id}")

        try:
            with open(tmp_path, "rb") as f:
                zero_out = replicate.run(
                    "jd7h/zero123plusplus:c69c6559a29011b576f1ff0371b3bc1add2856480c60520c7e9ce0b40a6e9052",
                    input={"image": f},
                )
            view_urls = [item.url if hasattr(item, "url") else str(item) for item in zero_out]
            for vi, url in enumerate(view_urls[:6]):
                r = requests.get(url, timeout=60)
                r.raise_for_status()
                (sample_dir / f"view_{vi}.png").write_bytes(r.content)

            prompt_text = row.get("prompt", row.get("text", ""))
            meta = {"method": method_name, "prompt_id": prompt_id, "prompt_text": prompt_text,
                    "source": "iso3d", "num_views": 6}
            (sample_dir / "meta.json").write_text(json.dumps(meta, indent=2))
            print(f"    ✓ Saved 6 views")
        except Exception as e:
            print(f"    ✗ Error: {e}")
        finally:
            tmp_path.unlink(missing_ok=True)

        time.sleep(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["iso3d_views", "dxgl", "replicate", "iso3d"], default="iso3d_views",
                    help="iso3d_views=free+reliable, dxgl=free(may 403), replicate/iso3d=need API+billing")
    ap.add_argument("--limit", type=int, default=None, help="Limit samples (for testing)")
    ap.add_argument("--delay", type=int, default=12,
                    help="Seconds between Replicate API calls (default 12 for <$5 credit)")
    ap.add_argument("--dry-run", action="store_true", help="Print plan without API/download")
    args = ap.parse_args()

    if args.source == "iso3d_views":
        print("Collecting from iso3d (6 identical views per image, free)")
        if args.dry_run:
            print("  Would load iso3d and save each image as 6 views")
            return
        collect_via_iso3d_views(limit=args.limit)
    elif args.source == "dxgl":
        print("Collecting from DX.GL (free, no API key)")
        if args.dry_run:
            for obj_id, obj_name, _ in DXGL_OBJECTS[: args.limit or 10]:
                print(f"  Would download: {obj_id} - {obj_name}")
            return
        collect_via_dxgl(limit=args.limit)
    elif args.source == "replicate":
        prompts = load_prompts(args.limit)
        print(f"Collecting {len(prompts)} samples via Replicate (SDXL + Zero123++)")
        if args.dry_run:
            for r in prompts:
                print(f"  Would process: {r['prompt_id']} - {r['prompt_text'][:50]}...")
            return
        collect_via_replicate(prompts, delay=args.delay)
    else:
        print("Collecting iso3d samples via Zero123++")
        if args.dry_run:
            print("  Would download iso3d and run Zero123++ on each image")
            return
        collect_via_iso3d(limit=args.limit or 5)

    print("\nDone. Run: python scripts/preprocess_views.py")


if __name__ == "__main__":
    main()
