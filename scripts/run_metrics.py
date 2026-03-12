#!/usr/bin/env python3
"""
Compute automatic proxy metrics for each sample.

Metrics:
  - CLIP similarity across adjacent views
  - DINO feature similarity (if available)
  - Silhouette overlap between neighboring views
  - Color histogram variance across views

Output: data/metrics/{method}_{prompt_id}.json
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed_views"
METRICS_DIR = REPO_ROOT / "data" / "metrics"
METRICS_DIR.mkdir(parents=True, exist_ok=True)


def compute_clip_similarity(view_paths: list[Path]) -> float:
    """Average pairwise CLIP similarity across adjacent views."""
    try:
        import torch
        import clip
        from PIL import Image
    except ImportError:
        return float("nan")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    images = [preprocess(Image.open(p).convert("RGB")) for p in view_paths]
    images = torch.stack(images).to(device)
    with torch.no_grad():
        features = model.encode_image(images)
        features = features / features.norm(dim=-1, keepdim=True)

    sims = []
    n = len(view_paths)
    for i in range(n):
        j = (i + 1) % n
        sim = (features[i] @ features[j]).item()
        sims.append(sim)
    return sum(sims) / len(sims) if sims else float("nan")


def compute_silhouette_overlap(view_paths: list[Path]) -> float:
    """Average IoU of binary silhouettes between adjacent views."""
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return float("nan")

    def to_silhouette(path: Path) -> np.ndarray:
        img = np.array(Image.open(path).convert("L"))
        return (img < 240).astype(np.float32)  # Simple threshold

    silhouettes = [to_silhouette(p) for p in view_paths]
    overlaps = []
    n = len(silhouettes)
    for i in range(n):
        j = (i + 1) % n
        a, b = silhouettes[i], silhouettes[j]
        intersection = (a * b).sum()
        union = ((a + b) > 0).sum()
        iou = intersection / union if union > 0 else 0
        overlaps.append(iou)
    return sum(overlaps) / len(overlaps) if overlaps else float("nan")


def compute_color_variance(view_paths: list[Path]) -> float:
    """Variance of mean RGB across views (lower = more consistent)."""
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return float("nan")

    means = []
    for p in view_paths:
        img = np.array(Image.open(p).convert("RGB"))
        means.append(img.mean(axis=(0, 1)))
    arr = np.array(means)
    return float(np.var(arr))


def compute_dino_similarity(view_paths: list[Path]) -> float | None:
    """DINO feature similarity across adjacent views. Returns None if unavailable."""
    try:
        import torch
        import torchvision.transforms as T
        from PIL import Image
        dinov2 = torch.hub.load("facebookresearch/dinov2", "dinov2_vits14")
        dinov2.eval()
        transform = T.Compose([
            T.Resize(224),
            T.CenterCrop(224),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])
        imgs = torch.stack([transform(Image.open(p).convert("RGB")) for p in view_paths])
        with torch.no_grad():
            feats = dinov2(imgs)
            feats = feats / feats.norm(dim=-1, keepdim=True)
        sims = [(feats[i] @ feats[(i + 1) % 6]).item() for i in range(6)]
        return sum(sims) / 6
    except Exception:
        return None


def compute_metrics_for_sample(method: str, prompt_id: str, dino_fn=None) -> dict:
    """Compute all metrics for one sample."""
    sample_dir = PROCESSED_DIR / method / prompt_id
    view_paths = [sample_dir / f"view_{i}.png" for i in range(6)]
    if not all(p.exists() for p in view_paths):
        return {}

    metrics = {
        "method": method,
        "prompt_id": prompt_id,
        "clip_adjacent_sim": compute_clip_similarity(view_paths),
        "silhouette_overlap": compute_silhouette_overlap(view_paths),
        "color_variance": compute_color_variance(view_paths),
    }
    if dino_fn is not None:
        metrics["dino_adjacent_sim"] = dino_fn(view_paths)
    else:
        metrics["dino_adjacent_sim"] = None

    return metrics


def discover_samples() -> list[tuple[str, str]]:
    samples = []
    for method_dir in PROCESSED_DIR.iterdir():
        if not method_dir.is_dir():
            continue
        method = method_dir.name
        for prompt_dir in method_dir.iterdir():
            if not prompt_dir.is_dir():
                continue
            prompt_id = prompt_dir.name
            if (prompt_dir / "view_0.png").exists():
                samples.append((method, prompt_id))
    return samples


def main():
    samples = discover_samples()
    if not samples:
        print("No samples found. Run preprocess_views.py first.")
        return

    # Try loading DINO once; use for all samples if available
    dino_fn = None
    method, prompt_id = samples[0]
    view_paths = [PROCESSED_DIR / method / prompt_id / f"view_{i}.png" for i in range(6)]
    if all(p.exists() for p in view_paths):
        try:
            compute_dino_similarity(view_paths)
            dino_fn = compute_dino_similarity
            print("DINO available.")
        except Exception:
            print("DINO not available; skipping.")

    print(f"Computing metrics for {len(samples)} samples...")
    for method, prompt_id in samples:
        metrics = compute_metrics_for_sample(method, prompt_id, dino_fn)
        out_path = METRICS_DIR / f"{method}_{prompt_id}.json"
        with open(out_path, "w") as f:
            json.dump(metrics, f, indent=2)
        print(f"  ✓ {method}/{prompt_id}")

    print("\nDone. Metrics saved to data/metrics/")


if __name__ == "__main__":
    main()
