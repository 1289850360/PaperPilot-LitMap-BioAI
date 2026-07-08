"""Generate error analysis for PaperPilot extraction runs.

The report lists matched, missed, and unsupported values per paper and field.

Example:
    python evaluation/error_analysis.py --pred experiments/outputs/schema_heuristic_v2/heuristic_predictions.csv --gold evaluation/gold.csv --fields task datasets models_or_methods metrics --out evaluation/error_analysis_schema_heuristic_v2.md
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from score_extraction import dedupe_values_by_schema, load_rows, row_key, split_values, value_similarity


def main() -> None:
    args = parse_args()
    pred_rows = {row_key(row): row for row in load_rows(args.pred)}
    gold_rows = {row_key(row): row for row in load_rows(args.gold)}

    lines = ["# Error Analysis", ""]
    lines.append(f"Prediction file: `{args.pred}`")
    lines.append(f"Gold file: `{args.gold}`")
    lines.append("")

    csv_rows: list[dict[str, str]] = []
    for key, gold_row in gold_rows.items():
        pred_row = pred_rows.get(key)
        if not pred_row:
            continue
        title = gold_row.get("title") or pred_row.get("title") or key
        lines.extend([f"## {title}", ""])
        for field in args.fields:
            pred_values = split_values(pred_row.get(field, ""))
            gold_values = split_values(gold_row.get(field, ""))
            pred_values = dedupe_values_by_schema(field, pred_values)
            gold_values = dedupe_values_by_schema(field, gold_values)
            matched_pred, matched_gold = match_values(field, pred_values, gold_values, args.strong_threshold)
            unsupported = [value for index, value in enumerate(pred_values) if index not in matched_pred]
            missed = [value for index, value in enumerate(gold_values) if index not in matched_gold]

            csv_rows.append(
                {
                    "paper_key": key,
                    "title": title,
                    "field": field,
                    "matched_pred_count": str(len(matched_pred)),
                    "pred_count": str(len(pred_values)),
                    "gold_count": str(len(gold_values)),
                    "unsupported_predictions": " | ".join(unsupported),
                    "missed_gold_values": " | ".join(missed),
                }
            )

            if not unsupported and not missed:
                continue
            lines.append(f"### {field}")
            if unsupported:
                lines.append("")
                lines.append("Unsupported predictions:")
                lines.extend(f"- {value}" for value in unsupported)
            if missed:
                lines.append("")
                lines.append("Missed gold values:")
                lines.extend(f"- {value}" for value in missed)
            lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")

    csv_path = args.out.with_suffix(".csv")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "paper_key",
                "title",
                "field",
                "matched_pred_count",
                "pred_count",
                "gold_count",
                "unsupported_predictions",
                "missed_gold_values",
            ],
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"Wrote {args.out}")
    print(f"Wrote {csv_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate extraction error analysis.")
    parser.add_argument("--pred", required=True, type=Path)
    parser.add_argument("--gold", required=True, type=Path)
    parser.add_argument("--fields", nargs="+", required=True)
    parser.add_argument("--out", type=Path, default=Path("evaluation/error_analysis.md"))
    parser.add_argument("--strong-threshold", type=float, default=0.75)
    return parser.parse_args()


def match_values(
    field: str,
    pred_values: list[str],
    gold_values: list[str],
    strong_threshold: float,
) -> tuple[set[int], set[int]]:
    candidates: list[tuple[float, int, int]] = []
    for pred_index, pred in enumerate(pred_values):
        for gold_index, gold in enumerate(gold_values):
            similarity = value_similarity(pred, gold, field)
            if similarity >= strong_threshold:
                candidates.append((similarity, pred_index, gold_index))

    matched_pred: set[int] = set()
    matched_gold: set[int] = set()
    for _, pred_index, gold_index in sorted(candidates, reverse=True):
        if pred_index in matched_pred or gold_index in matched_gold:
            continue
        matched_pred.add(pred_index)
        matched_gold.add(gold_index)
    return matched_pred, matched_gold


if __name__ == "__main__":
    main()
