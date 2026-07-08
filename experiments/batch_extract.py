"""Batch-run PaperPilot's heuristic extraction pipeline.

Example:
    python experiments/batch_extract.py --manifest experiments/sample_papers.csv --out-dir experiments/outputs
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

from run_heuristic_extraction import run_extraction


FIELD_KEYS = [
    "task",
    "datasets",
    "models_or_methods",
    "baselines",
    "metrics",
    "main_result",
    "limitations",
    "code_availability",
]


def main() -> None:
    args = parse_args()
    manifest_rows = load_manifest(args.manifest)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    prediction_rows: list[dict[str, Any]] = []
    for index, row in enumerate(manifest_rows, start=1):
        pdf_path = Path(row["pdf_path"]).expanduser()
        paper_id = row.get("paper_id") or f"paper_{index:03d}"
        print(f"[{index}/{len(manifest_rows)}] Extracting {pdf_path}")

        result = run_extraction(pdf_path)
        result["paper_id"] = paper_id
        result["notes"] = row.get("notes", "")

        json_path = args.out_dir / f"{safe_name(paper_id)}.json"
        json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        prediction_rows.append(to_prediction_row(paper_id, result))

    csv_path = args.out_dir / "heuristic_predictions.csv"
    write_prediction_csv(csv_path, prediction_rows)
    print(f"Wrote {csv_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch-run heuristic PaperPilot extraction.")
    parser.add_argument("--manifest", required=True, type=Path, help="CSV with at least a pdf_path column.")
    parser.add_argument("--out-dir", type=Path, default=Path("experiments/outputs"))
    return parser.parse_args()


def load_manifest(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        rows = [
            {key.strip(): (value or "").strip() for key, value in row.items() if key}
            for row in csv.DictReader(file)
        ]

    if not rows:
        raise ValueError(f"Manifest has no rows: {path}")
    if "pdf_path" not in rows[0]:
        raise ValueError("Manifest needs a pdf_path column.")
    return rows


def to_prediction_row(paper_id: str, result: dict[str, Any]) -> dict[str, Any]:
    card = result["card"]
    field_statuses = {field: "ai_extracted" for field in FIELD_KEYS}
    verification_statuses = card.get("verification_statuses", {})

    row: dict[str, Any] = {
        "paper_id": paper_id,
        "title": result["title"],
        "filename": result["filename"],
        "folder": "Experiments",
        "page_count": result["page_count"],
    }

    for field in FIELD_KEYS:
        row[field] = " | ".join(card.get(field, []))

    row["field_statuses"] = "; ".join(
        f"{field}:{field_statuses[field]}" for field in FIELD_KEYS
    )
    row["verification_statuses"] = "; ".join(
        f"{field}:{verification_statuses.get(field, 'missing')}" for field in FIELD_KEYS
    )
    return row


def write_prediction_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = [
        "paper_id",
        "title",
        "filename",
        "folder",
        "page_count",
        *FIELD_KEYS,
        "field_statuses",
        "verification_statuses",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-")
    return cleaned or "paper"


if __name__ == "__main__":
    main()
