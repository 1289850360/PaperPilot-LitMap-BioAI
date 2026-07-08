"""Create a conservative gold-revision candidate set from verified predictions.

The script does not overwrite the original gold file. It creates:

- a revised gold CSV with high-confidence additions
- a review queue CSV for human curation
- a markdown report explaining what changed
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


DEFAULT_FIELDS = ["task", "datasets", "models_or_methods", "metrics"]

LOW_VALUE_METHOD_NAMES = {
    "alphafold 3",
    "alphafold3",
    "diffdock",
    "dynamicbind",
    "equibind",
    "plinder",
    "posebusters",
    "tankbind",
}

GENERIC_METRICS_FOR_REVIEW = {
    "binding affinity",
    "binding score",
    "diversity",
    "runtime",
    "success rate",
    "validity",
}


@dataclass
class Candidate:
    paper_id: str
    title: str
    field: str
    value: str
    status: str
    page: str
    decision: str
    reason: str
    snippet: str


def main() -> None:
    args = parse_args()
    fields = args.fields or DEFAULT_FIELDS

    gold_rows = load_rows(args.gold)
    pred_rows = load_rows(args.pred)
    audit_rows = load_rows(args.audit)

    gold_by_id = {row["paper_id"]: row for row in gold_rows}
    pred_by_id = {row["paper_id"]: row for row in pred_rows}
    audit_by_key = {
        (row["paper_id"], row["field"], normalize_label(row["value"])): row
        for row in audit_rows
    }

    revised_rows = [dict(row) for row in gold_rows]
    candidates: list[Candidate] = []
    additions_by_row_field: dict[tuple[str, str], list[str]] = defaultdict(list)

    for row in revised_rows:
        paper_id = row["paper_id"]
        pred = pred_by_id.get(paper_id)
        if not pred:
            continue
        for field in fields:
            gold_values = split_values(row.get(field, ""))
            for value in split_values(pred.get(field, "")):
                if has_match(value, gold_values):
                    continue
                audit = audit_by_key.get((paper_id, field, normalize_label(value)), {})
                status = audit.get("status", "")
                decision, reason = classify_candidate(field, value, status, audit.get("snippet", ""))
                candidates.append(
                    Candidate(
                        paper_id=paper_id,
                        title=row.get("title", ""),
                        field=field,
                        value=value,
                        status=status,
                        page=audit.get("page", ""),
                        decision=decision,
                        reason=reason,
                        snippet=audit.get("snippet", ""),
                    )
                )
                if decision == "add":
                    additions_by_row_field[(paper_id, field)].append(value)

    for row in revised_rows:
        paper_id = row["paper_id"]
        for field in fields:
            additions = additions_by_row_field.get((paper_id, field), [])
            if not additions:
                continue
            merged = split_values(row.get(field, ""))
            for value in additions:
                if not has_match(value, merged):
                    merged.append(value)
            row[field] = " | ".join(merged)
        note = row.get("review_notes", "")
        changed_fields = sorted({field for (pid, field) in additions_by_row_field if pid == paper_id})
        if changed_fields:
            suffix = f"Auto-refinement added high-confidence values for: {', '.join(changed_fields)}."
            row["review_notes"] = f"{note} {suffix}".strip()
            row["verification_status"] = "auto-refined; needs final human review"

    args.out_gold.parent.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_gold, revised_rows, list(gold_rows[0]))
    write_candidates(args.out_candidates, candidates)
    write_report(args.out_report, args, candidates, revised_rows, fields)

    print(f"Wrote {args.out_gold}")
    print(f"Wrote {args.out_candidates}")
    print(f"Wrote {args.out_report}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refine a gold CSV from verified PaperPilot predictions.")
    parser.add_argument("--gold", required=True, type=Path)
    parser.add_argument("--pred", required=True, type=Path)
    parser.add_argument("--audit", required=True, type=Path)
    parser.add_argument("--out-gold", required=True, type=Path)
    parser.add_argument("--out-candidates", required=True, type=Path)
    parser.add_argument("--out-report", required=True, type=Path)
    parser.add_argument("--fields", nargs="+", default=DEFAULT_FIELDS)
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [
            {(key or "").strip(): (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(file)
        ]


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_candidates(path: Path, candidates: list[Candidate]) -> None:
    columns = [
        "paper_id",
        "title",
        "field",
        "value",
        "status",
        "page",
        "decision",
        "reason",
        "snippet",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(candidate.__dict__)


def write_report(
    path: Path,
    args: argparse.Namespace,
    candidates: list[Candidate],
    revised_rows: list[dict[str, str]],
    fields: list[str],
) -> None:
    counts = defaultdict(int)
    by_field_decision = defaultdict(int)
    for candidate in candidates:
        counts[candidate.decision] += 1
        by_field_decision[(candidate.field, candidate.decision)] += 1

    lines = [
        "# Gold Refinement Report",
        "",
        "This report summarizes a conservative automatic refinement pass over the 23-paper gold annotation file.",
        "",
        "## Inputs",
        "",
        f"- Gold: `{args.gold}`",
        f"- Verified predictions: `{args.pred}`",
        f"- Value audit: `{args.audit}`",
        "",
        "## Outputs",
        "",
        f"- Revised gold candidate: `{args.out_gold}`",
        f"- Human review queue: `{args.out_candidates}`",
        "",
        "## Decision Counts",
        "",
        "| Decision | Count |",
        "|---|---:|",
    ]
    for decision in ["add", "review", "reject"]:
        lines.append(f"| {decision} | {counts[decision]} |")

    lines.extend(["", "## By Field", "", "| Field | Add | Review | Reject |", "|---|---:|---:|---:|"])
    for field in fields:
        lines.append(
            f"| {field} | {by_field_decision[(field, 'add')]} | "
            f"{by_field_decision[(field, 'review')]} | {by_field_decision[(field, 'reject')]} |"
        )

    lines.extend(
        [
            "",
            "## Curation Policy",
            "",
            "- `add`: supported by the PDF and specific enough to be safely merged into the revised gold candidate.",
            "- `review`: supported or weakly supported, but broad enough that a human should confirm whether it belongs in the schema.",
            "- `reject`: unsupported by the PDF evidence verifier.",
            "",
            "The revised gold file is still marked as needing final human review. It should be treated as a benchmark candidate, not a fully locked gold standard.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def classify_candidate(field: str, value: str, status: str, snippet: str) -> tuple[str, str]:
    normalized = normalize_label(value)
    if status == "unsupported":
        return "reject", "Value-level verifier did not find lexical evidence in the PDF."
    if status == "weak":
        return "review", "Only weak lexical evidence was found; human review required."
    if field == "task":
        return "review", "Task labels are interpretive and should be curated manually."
    if field == "datasets":
        return "add", "Supported dataset or benchmark value absent from the original gold row."
    if field == "models_or_methods":
        if normalized in LOW_VALUE_METHOD_NAMES:
            return "review", "This looks like a comparison/baseline/tool name; confirm before treating it as the paper method."
        if not own_method_context(snippet):
            return "review", "Method evidence does not clearly say it is the paper's proposed method."
        return "add", "Supported method/component with proposed-method context."
    if field == "metrics":
        if normalized in GENERIC_METRICS_FOR_REVIEW:
            return "review", "Generic metric label; confirm whether the paper reports it as a main evaluation metric."
        return "add", "Supported metric value absent from the original gold row."
    return "review", "Unknown field policy."


def own_method_context(snippet: str) -> bool:
    return bool(
        re.search(
            r"\b(?:we propose|we present|we introduce|we develop|we build|our|called|named|"
            r"architecture|module|framework|model|method)\b",
            snippet,
            re.I,
        )
    )


def split_values(value: str) -> list[str]:
    if not value.strip():
        return []
    return [part.strip() for part in re.split(r"\s*\|\s*|\s*;\s*|\n+", value) if part.strip()]


def has_match(candidate: str, values: list[str], threshold: float = 0.78) -> bool:
    candidate_norm = normalize_for_match(candidate)
    for value in values:
        value_norm = normalize_for_match(value)
        if candidate_norm == value_norm:
            return True
        if candidate_norm in value_norm or value_norm in candidate_norm:
            return True
        if SequenceMatcher(None, candidate_norm, value_norm).ratio() >= threshold:
            return True
    return False


def normalize_label(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower().replace("-", " ")).strip()


def normalize_for_match(value: str) -> str:
    value = value.lower().replace("≤", "<=").replace("≥", ">=").replace("å", "a")
    value = re.sub(r"[^a-z0-9<>=%]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


if __name__ == "__main__":
    main()
