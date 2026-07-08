"""Score PaperPilot structured extraction against a gold CSV.

The prediction CSV should be exported from the PaperPilot web UI.
The gold CSV should use the same wide format, with manually corrected field values.

Example:
    python evaluation/score_extraction.py --pred evaluation/predictions.csv --gold evaluation/gold.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable


DEFAULT_FIELDS = [
    "task",
    "datasets",
    "models_or_methods",
    "baselines",
    "metrics",
    "main_result",
    "limitations",
    "code_availability",
]


@dataclass
class FieldScore:
    field: str
    compared: int = 0
    gold_present: int = 0
    pred_present: int = 0
    exact_or_strong: int = 0
    partial: int = 0
    incorrect: int = 0
    missing: int = 0
    hallucinated: int = 0
    accuracy_points: float = 0.0
    gold_value_count: int = 0
    pred_value_count: int = 0
    matched_gold_values: int = 0
    matched_pred_values: int = 0
    missed_gold_values: int = 0
    unsupported_pred_values: int = 0

    @property
    def field_accuracy(self) -> float:
        return safe_divide(self.accuracy_points, self.compared)

    @property
    def missing_rate(self) -> float:
        return safe_divide(self.missing, self.gold_present)

    @property
    def hallucination_rate(self) -> float:
        return safe_divide(self.hallucinated, self.pred_present)

    @property
    def value_precision(self) -> float:
        return safe_divide(self.matched_pred_values, self.pred_value_count)

    @property
    def value_recall(self) -> float:
        return safe_divide(self.matched_gold_values, self.gold_value_count)

    @property
    def value_f1(self) -> float:
        precision = self.value_precision
        recall = self.value_recall
        return safe_divide(2 * precision * recall, precision + recall)


def main() -> None:
    args = parse_args()
    fields = args.fields or DEFAULT_FIELDS

    predictions = load_rows(args.pred)
    gold = load_rows(args.gold)
    pred_by_key = {row_key(row): row for row in predictions}
    gold_by_key = {row_key(row): row for row in gold}

    missing_predictions = sorted(set(gold_by_key) - set(pred_by_key))
    extra_predictions = sorted(set(pred_by_key) - set(gold_by_key))

    scores = {field: FieldScore(field=field) for field in fields}
    paper_count = 0

    for key, gold_row in gold_by_key.items():
        pred_row = pred_by_key.get(key)
        if not pred_row:
            continue
        paper_count += 1
        for field in fields:
            update_score(
                scores[field],
                pred_values=split_values(pred_row.get(field, "")),
                gold_values=split_values(gold_row.get(field, "")),
                strong_threshold=args.strong_threshold,
                partial_threshold=args.partial_threshold,
            )

    verification_counts = count_verification_statuses(predictions, fields)

    summary = build_summary(
        scores=scores.values(),
        paper_count=paper_count,
        missing_prediction_count=len(missing_predictions),
        extra_prediction_count=len(extra_predictions),
        fields=fields,
        verification_counts=verification_counts,
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.out_dir / "score_summary.json"
    per_field_path = args.out_dir / "per_field_scores.csv"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_per_field_scores(per_field_path, scores.values())

    print_summary(summary, scores.values())
    print()
    print(f"Wrote {summary_path}")
    print(f"Wrote {per_field_path}")

    if missing_predictions:
        print()
        print("Gold rows without matching predictions:")
        for key in missing_predictions[:10]:
            print(f"- {key}")
        if len(missing_predictions) > 10:
            print(f"- ... and {len(missing_predictions) - 10} more")

    if extra_predictions:
        print()
        print("Prediction rows not found in gold:")
        for key in extra_predictions[:10]:
            print(f"- {key}")
        if len(extra_predictions) > 10:
            print(f"- ... and {len(extra_predictions) - 10} more")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score PaperPilot extraction CSV against gold CSV.")
    parser.add_argument("--pred", required=True, type=Path, help="Prediction CSV exported from PaperPilot.")
    parser.add_argument("--gold", required=True, type=Path, help="Gold CSV with manually corrected fields.")
    parser.add_argument(
        "--fields",
        nargs="+",
        default=None,
        help="Fields to score. Defaults to all PaperPilot card fields.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("evaluation/results"),
        help="Directory for score_summary.json and per_field_scores.csv.",
    )
    parser.add_argument(
        "--strong-threshold",
        type=float,
        default=0.75,
        help="Similarity threshold for a full-credit match.",
    )
    parser.add_argument(
        "--partial-threshold",
        type=float,
        default=0.45,
        help="Similarity threshold for a half-credit match.",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = [clean_row(row) for row in reader]

    if not rows:
        raise ValueError(f"CSV has no rows: {path}")

    return rows


def clean_row(row: dict[str, str | None]) -> dict[str, str]:
    return {(key or "").strip(): (value or "").strip() for key, value in row.items()}


def row_key(row: dict[str, str]) -> str:
    paper_id = row.get("paper_id", "").strip()
    if paper_id:
        return f"id:{paper_id}"

    filename = row.get("filename", "").strip().lower()
    if filename:
        return f"filename:{filename}"

    title = row.get("title", "").strip().lower()
    if title:
        return f"title:{title}"

    raise ValueError("Every row needs at least one of paper_id, filename, or title.")


def split_values(value: str) -> list[str]:
    if not value.strip():
        return []
    parts = re.split(r"\s*\|\s*|\s*;\s*|\n+", value)
    return [part.strip() for part in parts if part.strip()]


def update_score(
    score: FieldScore,
    pred_values: list[str],
    gold_values: list[str],
    strong_threshold: float,
    partial_threshold: float,
) -> None:
    gold_present = bool(gold_values)
    pred_present = bool(pred_values)

    if gold_present:
        score.compared += 1
        score.gold_present += 1
        score.gold_value_count += len(gold_values)

    if pred_present:
        score.pred_present += 1
        score.pred_value_count += len(pred_values)

    if gold_present and not pred_present:
        score.missing += 1
        score.incorrect += 1
        score.missed_gold_values += len(gold_values)
        return

    if pred_present and not gold_present:
        score.hallucinated += 1
        score.unsupported_pred_values += len(pred_values)
        return

    if not gold_present and not pred_present:
        return

    matched_pred, matched_gold = match_values(pred_values, gold_values, strong_threshold)
    score.matched_pred_values += len(matched_pred)
    score.matched_gold_values += len(matched_gold)
    score.unsupported_pred_values += max(0, len(pred_values) - len(matched_pred))
    score.missed_gold_values += max(0, len(gold_values) - len(matched_gold))

    best_similarity = best_match_similarity(pred_values, gold_values)

    if best_similarity >= strong_threshold:
        score.exact_or_strong += 1
        score.accuracy_points += 1.0
    elif best_similarity >= partial_threshold:
        score.partial += 1
        score.accuracy_points += 0.5
    else:
        score.incorrect += 1

    if has_unsupported_prediction(pred_values, gold_values, strong_threshold):
        score.hallucinated += 1


def match_values(
    pred_values: list[str],
    gold_values: list[str],
    strong_threshold: float,
) -> tuple[set[int], set[int]]:
    candidates: list[tuple[float, int, int]] = []
    for pred_index, pred in enumerate(pred_values):
        for gold_index, gold in enumerate(gold_values):
            similarity = value_similarity(pred, gold)
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


def best_match_similarity(pred_values: Iterable[str], gold_values: Iterable[str]) -> float:
    best = 0.0
    for pred in pred_values:
        for gold in gold_values:
            best = max(best, value_similarity(pred, gold))
    return best


def value_similarity(pred: str, gold: str) -> float:
    pred_norm = normalize(pred)
    gold_norm = normalize(gold)
    if not pred_norm or not gold_norm:
        return 0.0
    if pred_norm == gold_norm or pred_norm in gold_norm or gold_norm in pred_norm:
        return 1.0
    return SequenceMatcher(None, pred_norm, gold_norm).ratio()


def has_unsupported_prediction(
    pred_values: Iterable[str],
    gold_values: Iterable[str],
    strong_threshold: float,
) -> bool:
    for pred in pred_values:
        if best_match_similarity([pred], gold_values) < strong_threshold:
            return True
    return False


def normalize(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def build_summary(
    scores: Iterable[FieldScore],
    paper_count: int,
    missing_prediction_count: int,
    extra_prediction_count: int,
    fields: list[str],
    verification_counts: dict[str, int],
) -> dict[str, object]:
    score_list = list(scores)
    compared = sum(score.compared for score in score_list)
    accuracy_points = sum(score.accuracy_points for score in score_list)
    gold_present = sum(score.gold_present for score in score_list)
    pred_present = sum(score.pred_present for score in score_list)
    missing = sum(score.missing for score in score_list)
    hallucinated = sum(score.hallucinated for score in score_list)
    gold_value_count = sum(score.gold_value_count for score in score_list)
    pred_value_count = sum(score.pred_value_count for score in score_list)
    matched_gold_values = sum(score.matched_gold_values for score in score_list)
    matched_pred_values = sum(score.matched_pred_values for score in score_list)
    value_precision = safe_divide(matched_pred_values, pred_value_count)
    value_recall = safe_divide(matched_gold_values, gold_value_count)
    value_f1 = safe_divide(2 * value_precision * value_recall, value_precision + value_recall)

    return {
        "paper_count": paper_count,
        "fields": fields,
        "compared_field_count": compared,
        "field_level_accuracy": safe_divide(accuracy_points, compared),
        "missing_rate": safe_divide(missing, gold_present),
        "hallucination_rate": safe_divide(hallucinated, pred_present),
        "value_precision": value_precision,
        "value_recall": value_recall,
        "value_f1": value_f1,
        "gold_value_count": gold_value_count,
        "pred_value_count": pred_value_count,
        "matched_gold_values": matched_gold_values,
        "matched_pred_values": matched_pred_values,
        "missing_prediction_rows": missing_prediction_count,
        "extra_prediction_rows": extra_prediction_count,
        "predicted_verification_counts": verification_counts,
    }


def count_verification_statuses(rows: list[dict[str, str]], fields: list[str]) -> dict[str, int]:
    counts = {"supported": 0, "weak": 0, "unsupported": 0, "missing": 0, "unknown": 0}
    for row in rows:
        status_map = parse_status_map(row.get("verification_statuses", ""))
        for field in fields:
            status = status_map.get(field)
            if not status:
                continue
            counts[status if status in counts else "unknown"] += 1
    return counts


def parse_status_map(value: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in value.split(";"):
        if ":" not in item:
            continue
        field, status = item.split(":", 1)
        result[field.strip()] = status.strip()
    return result


def write_per_field_scores(path: Path, scores: Iterable[FieldScore]) -> None:
    columns = [
        "field",
        "compared",
        "field_accuracy",
        "missing_rate",
        "hallucination_rate",
        "value_precision",
        "value_recall",
        "value_f1",
        "gold_value_count",
        "pred_value_count",
        "matched_gold_values",
        "matched_pred_values",
        "missed_gold_values",
        "unsupported_pred_values",
        "exact_or_strong",
        "partial",
        "incorrect",
        "missing",
        "hallucinated",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for score in scores:
            writer.writerow(
                {
                    "field": score.field,
                    "compared": score.compared,
                    "field_accuracy": round(score.field_accuracy, 4),
                    "missing_rate": round(score.missing_rate, 4),
                    "hallucination_rate": round(score.hallucination_rate, 4),
                    "value_precision": round(score.value_precision, 4),
                    "value_recall": round(score.value_recall, 4),
                    "value_f1": round(score.value_f1, 4),
                    "gold_value_count": score.gold_value_count,
                    "pred_value_count": score.pred_value_count,
                    "matched_gold_values": score.matched_gold_values,
                    "matched_pred_values": score.matched_pred_values,
                    "missed_gold_values": score.missed_gold_values,
                    "unsupported_pred_values": score.unsupported_pred_values,
                    "exact_or_strong": score.exact_or_strong,
                    "partial": score.partial,
                    "incorrect": score.incorrect,
                    "missing": score.missing,
                    "hallucinated": score.hallucinated,
                }
            )


def print_summary(summary: dict[str, object], scores: Iterable[FieldScore]) -> None:
    print("PaperPilot extraction evaluation")
    print("=" * 34)
    print(f"Papers compared:       {summary['paper_count']}")
    print(f"Fields compared:       {summary['compared_field_count']}")
    print(f"Field-level accuracy:  {format_rate(summary['field_level_accuracy'])}")
    print(f"Missing rate:          {format_rate(summary['missing_rate'])}")
    print(f"Hallucination rate:    {format_rate(summary['hallucination_rate'])}")
    print(f"Value precision:       {format_rate(summary['value_precision'])}")
    print(f"Value recall:          {format_rate(summary['value_recall'])}")
    print(f"Value F1:              {format_rate(summary['value_f1'])}")
    verification_counts = summary.get("predicted_verification_counts", {})
    if isinstance(verification_counts, dict) and any(verification_counts.values()):
        print(
            "Citation checks:       "
            + ", ".join(f"{key}={value}" for key, value in verification_counts.items() if value)
        )
    print()
    print("Per-field scores")
    print("-" * 34)
    for score in scores:
        print(
            f"{score.field:22} "
            f"acc={format_rate(score.field_accuracy):>7} "
            f"miss={format_rate(score.missing_rate):>7} "
            f"hall={format_rate(score.hallucination_rate):>7} "
            f"val_f1={format_rate(score.value_f1):>7}"
        )


def format_rate(value: object) -> str:
    return f"{float(value) * 100:.1f}%"


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


if __name__ == "__main__":
    main()
