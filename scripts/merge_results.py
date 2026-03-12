#!/usr/bin/env python3
"""
Merge human annotations with prompt metadata and automatic metrics into one analysis table.

Output: data/annotations/merged_results.csv

Columns:
  participant_id, sample_id, method, prompt_id, category, prompt_text,
  overall, identity, geometry, parts, material, silhouette, usefulness,
  failure_tags, clip_adjacent_sim, silhouette_overlap, color_variance, ...
"""

import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ANNOTATIONS_DIR = REPO_ROOT / "data" / "annotations"
METRICS_DIR = REPO_ROOT / "data" / "metrics"
PROMPTS_CSV = REPO_ROOT / "data" / "prompts.csv"
OUTPUT_CSV = ANNOTATIONS_DIR / "merged_results.csv"


def load_prompts() -> dict[str, dict]:
    """prompt_id -> {category, prompt_text, ...}"""
    prompts = {}
    with open(PROMPTS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            prompts[row["prompt_id"]] = row
    return prompts


def load_metrics() -> dict[tuple[str, str], dict]:
    """(method, prompt_id) -> metrics dict"""
    metrics = {}
    for p in METRICS_DIR.glob("*.json"):
        try:
            import json
            data = json.loads(p.read_text())
            key = (data["method"], data["prompt_id"])
            metrics[key] = data
        except Exception:
            pass
    return metrics


def load_annotations() -> list[dict]:
    """Load all annotation CSVs."""
    rows = []
    for csv_path in ANNOTATIONS_DIR.glob("*.csv"):
        if csv_path.name == "merged_results.csv":
            continue
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    return rows


def main():
    prompts = load_prompts()
    metrics = load_metrics()
    annotations = load_annotations()

    if not annotations:
        print("No annotation CSVs found in data/annotations/")
        print("Run the Streamlit app and collect some ratings first.")
        return

    # Build merged rows
    merged = []
    for ann in annotations:
        method = ann.get("method", "")
        prompt_id = ann.get("prompt_id", "")
        prompt_info = prompts.get(prompt_id, {})
        metric_info = metrics.get((method, prompt_id), {})

        row = {
            "participant_id": ann.get("participant_id", ""),
            "sample_id": ann.get("sample_id", f"{method}_{prompt_id}"),
            "method": method,
            "prompt_id": prompt_id,
            "category": prompt_info.get("category", ""),
            "prompt_text": prompt_info.get("prompt_text", ""),
            "overall": ann.get("overall", ""),
            "identity": ann.get("identity", ""),
            "geometry": ann.get("geometry", ""),
            "parts": ann.get("parts", ""),
            "material": ann.get("material", ""),
            "silhouette": ann.get("silhouette", ""),
            "usefulness": ann.get("usefulness", ""),
            "failure_tags": ann.get("failure_tags", ""),
            "clip_adjacent_sim": metric_info.get("clip_adjacent_sim", ""),
            "silhouette_overlap": metric_info.get("silhouette_overlap", ""),
            "color_variance": metric_info.get("color_variance", ""),
            "dino_adjacent_sim": metric_info.get("dino_adjacent_sim", ""),
        }
        merged.append(row)

    # Write
    if merged:
        fieldnames = list(merged[0].keys())
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(merged)
        print(f"Wrote {len(merged)} rows to {OUTPUT_CSV}")
    else:
        print("No rows to write.")


if __name__ == "__main__":
    main()
