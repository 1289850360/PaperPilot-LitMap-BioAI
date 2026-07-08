"""Apply curated task/method review decisions to the auto-refined gold file.

This pass is intentionally explicit: each accepted task or method review item is
listed in ACCEPTED_REVIEW_VALUES. All other task/method review values remain out
of the gold file and are recorded in the decision log.
"""

from __future__ import annotations

import argparse
import csv
import re
from difflib import SequenceMatcher
from pathlib import Path


TARGET_FIELDS = {"task", "models_or_methods"}

ACCEPTED_REVIEW_VALUES = {
    # EquiBind
    ("paper_007", "task", "protein-ligand binding pose prediction"),
    ("paper_007", "task", "direct-shot molecular docking"),
    ("paper_007", "task", "rigid receptor blind docking"),
    # DiffDock
    ("paper_008", "task", "confidence-ranked ligand pose generation"),
    # FrameFlow / motif scaffolding / DockGen-family tasks
    ("paper_010", "task", "protein structure generation"),
    ("paper_012", "task", "functional protein design"),
    ("paper_013", "task", "protein-ligand docking generalization"),
    ("paper_013", "task", "confidence-guided molecular docking"),
    # Molecule/protein generation papers
    ("paper_014", "task", "atom-and-bond generation"),
    ("paper_014", "task", "flow matching for molecule generation"),
    ("paper_015", "task", "inverse folding"),
    ("paper_016", "task", "molecular graph and geometry generation"),
    ("paper_016", "task", "flow matching for molecule generation"),
    ("paper_018", "task", "protein-ligand complex generation"),
    ("paper_018", "task", "ligand conformation and protein backbone generation"),
    ("paper_019", "task", "pocket-conditioned ligand generation"),
    ("paper_019", "task", "protein-ligand interaction-guided molecule generation"),
    ("paper_020", "task", "pocket-conditioned molecule design"),
    ("paper_021", "task", "physical validity assessment for generated ligand poses"),
    # Method components that are genuinely used by the target paper.
    ("paper_002", "models_or_methods", "continuous normalizing flow"),
    ("paper_005", "models_or_methods", "conditional flow matching"),
    ("paper_010", "models_or_methods", "conditional flow matching"),
    ("paper_016", "models_or_methods", "conditional flow matching"),
    ("paper_018", "models_or_methods", "Riemannian flow matching"),
    ("paper_019", "models_or_methods", "self-conditioning"),
    ("paper_020", "models_or_methods", "fragment-based ligand generation"),
    ("paper_024", "models_or_methods", "confidence head"),
}


def main() -> None:
    args = parse_args()
    gold_rows = load_rows(args.gold)
    candidates = load_rows(args.candidates)

    decisions: list[dict[str, str]] = []
    accepted_by_row: dict[tuple[str, str], list[str]] = {}

    for row in candidates:
        if row.get("decision") != "review" or row.get("field") not in TARGET_FIELDS:
            continue
        key = (row["paper_id"], row["field"], row["value"])
        decision, rationale = classify_review_value(row, key)
        decisions.append(
            {
                "paper_id": row["paper_id"],
                "title": row.get("title", ""),
                "field": row["field"],
                "value": row["value"],
                "status": row.get("status", ""),
                "page": row.get("page", ""),
                "manual_decision": decision,
                "rationale": rationale,
                "snippet": row.get("snippet", ""),
            }
        )
        if decision == "accept":
            accepted_by_row.setdefault((row["paper_id"], row["field"]), []).append(row["value"])

    revised = [dict(row) for row in gold_rows]
    for row in revised:
        changed_fields: list[str] = []
        for field in TARGET_FIELDS:
            additions = accepted_by_row.get((row["paper_id"], field), [])
            if not additions:
                continue
            values = split_values(row.get(field, ""))
            for value in additions:
                if not has_match(value, values):
                    values.append(value)
            row[field] = " | ".join(values)
            changed_fields.append(field)
        if changed_fields:
            note = row.get("review_notes", "")
            suffix = "Manual v2 review accepted task/method values for: " + ", ".join(sorted(changed_fields)) + "."
            row["review_notes"] = f"{note} {suffix}".strip()
            row["verification_status"] = "auto-refined + manual task/method review v2"

    args.out_gold.parent.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_gold, revised, list(gold_rows[0]))
    write_csv(
        args.out_decisions,
        decisions,
        [
            "paper_id",
            "title",
            "field",
            "value",
            "status",
            "page",
            "manual_decision",
            "rationale",
            "snippet",
        ],
    )
    write_report(args.out_report, args, decisions)

    print(f"Wrote {args.out_gold}")
    print(f"Wrote {args.out_decisions}")
    print(f"Wrote {args.out_report}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply curated task/method review decisions.")
    parser.add_argument("--gold", required=True, type=Path)
    parser.add_argument("--candidates", required=True, type=Path)
    parser.add_argument("--out-gold", required=True, type=Path)
    parser.add_argument("--out-decisions", required=True, type=Path)
    parser.add_argument("--out-report", required=True, type=Path)
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


def write_report(path: Path, args: argparse.Namespace, decisions: list[dict[str, str]]) -> None:
    accepted = [row for row in decisions if row["manual_decision"] == "accept"]
    rejected = [row for row in decisions if row["manual_decision"] == "reject"]
    lines = [
        "# Manual Gold Review v2",
        "",
        "This pass manually reviews only `task` and `models_or_methods` values that were previously marked as `review`.",
        "",
        "## Inputs",
        "",
        f"- Starting gold: `{args.gold}`",
        f"- Review queue: `{args.candidates}`",
        "",
        "## Outputs",
        "",
        f"- Revised gold v2: `{args.out_gold}`",
        f"- Decision log: `{args.out_decisions}`",
        "",
        "## Summary",
        "",
        "| Manual decision | Count |",
        "|---|---:|",
        f"| accept | {len(accepted)} |",
        f"| reject | {len(rejected)} |",
        "",
        "## Acceptance Policy",
        "",
        "- Accept task values when they describe the paper's main research problem or an explicitly claimed capability.",
        "- Accept method values when they are part of the paper's own model, training objective, or core pipeline.",
        "- Reject baseline names, datasets, metrics, related-work citations, bibliography hits, journal metadata, and overly broad field labels.",
        "",
        "## Accepted Values",
        "",
        "| Paper | Field | Value |",
        "|---|---|---|",
    ]
    for row in accepted:
        lines.append(f"| {row['paper_id']} | {row['field']} | {row['value']} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def classify_review_value(row: dict[str, str], key: tuple[str, str, str]) -> tuple[str, str]:
    if key in ACCEPTED_REVIEW_VALUES:
        return "accept", "Accepted as a main task or own method/component after manual review."
    field = row["field"]
    value = row["value"]
    if field == "task" and re.search(r"https?://|nature$|vol \d+|june \d{4}", value, re.I):
        return "reject", "PDF metadata or parsing noise, not a scientific task."
    if field == "models_or_methods":
        return "reject", "Baseline, related-work method, dataset/benchmark name, metric, or insufficient own-method evidence."
    return "reject", "Too broad, weakly supported, or not central enough for the benchmark gold schema."


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


def normalize_for_match(value: str) -> str:
    value = value.lower().replace("≤", "<=").replace("≥", ">=").replace("å", "a")
    value = re.sub(r"[^a-z0-9<>=%]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


if __name__ == "__main__":
    main()
