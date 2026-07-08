"""Prepare a clean candidate gold file from manually reviewed annotations."""

from __future__ import annotations

import csv
from pathlib import Path


INPUT = Path("evaluation/flow_matching_candidate_annotations_batch1_verified_v2.csv")
OUTPUT = Path("evaluation/gold_batch1_candidate_cleaned.csv")
REVIEW = Path("evaluation/ANNOTATION_BATCH1_REVIEW.md")

FIELD_COLUMNS = ["task", "datasets", "models_or_methods", "metrics"]
PDF_CHECKED_IDS = {"paper_015", "paper_022"}


def main() -> None:
    rows = load_rows(INPUT)
    included = [row for row in rows if normalize_flag(row["include_in_benchmark"]) == "yes"]
    excluded = [row for row in rows if normalize_flag(row["include_in_benchmark"]) != "yes"]

    cleaned_rows = [clean_row(row) for row in included]
    write_csv(OUTPUT, cleaned_rows)
    REVIEW.write_text(build_review(rows, included, excluded, cleaned_rows), encoding="utf-8")

    print(f"Wrote {OUTPUT}")
    print(f"Wrote {REVIEW}")


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [
            {(key or "").strip(): (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(file)
        ]


def clean_row(row: dict[str, str]) -> dict[str, str]:
    clean = {
        "paper_id": row["paper_id"],
        "title": row["title"],
        "filename": row["filename"],
        "paper_type": row["paper_type"],
        "folder": "Batch 1 candidate gold",
    }
    for field in FIELD_COLUMNS:
        clean[field] = normalize_values(override_value(row, field))
    clean["review_notes"] = row["review_notes"]
    clean["verification_status"] = row["verification_status"]
    clean["needs_pdf_check"] = needs_pdf_check(row)
    return clean


def override_value(row: dict[str, str], field: str) -> str:
    paper_id = row["paper_id"]
    if paper_id == "paper_015" and field == "datasets":
        return (
            "PDB; filtered AlphaFold2 synthetic structures from SwissProt; "
            "ATLAS molecular-dynamics trajectory evaluation set; "
            "24 single-chain motif scaffolding benchmark; "
            "VHH nanobody scaffold design benchmark / Structural Antibody Database"
        )
    if paper_id == "paper_015" and field == "metrics":
        return (
            "designability; diversity; novelty; scRMSD; TM-score; secondary-structure diversity; "
            "motif scRMSD; number of solved motif scaffolds; pairwise RMSD Pearson correlation; "
            "global RMSF Pearson correlation; per-target RMSF Pearson correlation; PCA W2 distance; "
            "time per sample"
        )
    if paper_id == "paper_022" and field == "metrics":
        return (
            "ligand RMSD; centroid distance; RMSD percentiles; percentage of predictions below 2 Å; "
            "percentage of predictions below 5 Å; RMSE; Pearson correlation; Spearman correlation; "
            "MAE; runtime; number of parameters"
        )
    if paper_id == "paper_022" and field == "datasets":
        return "PDBBind; PDBBind 2019 time split; PDBBind affinity benchmark"
    return row[field]


def normalize_values(value: str) -> str:
    values = [normalize_value(item.strip()) for item in value.split(";") if item.strip()]
    return " | ".join(dedupe(values))


def normalize_value(value: str) -> str:
    replacements = {
        "PDBbind": "PDBBind",
        "PDBBind time-based split": "PDBBind time split",
        "percentage below 2 Å": "percentage of predictions below 2 Å",
        "percentage below 5 Å": "percentage of predictions below 5 Å",
        "runtime / inference speed": "runtime / inference speed",
    }
    result = value
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = " ".join(value.lower().replace("-", " ").split())
        if key and key not in seen:
            seen.add(key)
            result.append(value)
    return result


def normalize_flag(value: str) -> str:
    return value.strip().lower()


def needs_pdf_check(row: dict[str, str]) -> str:
    if row["paper_id"] in PDF_CHECKED_IDS:
        return "no"
    text = f"{row['review_notes']} {row['verification_status']}".lower()
    if any(marker in text for marker in ["need final", "needs final", "manual check"]):
        return "yes"
    return "no"


def build_review(
    rows: list[dict[str, str]],
    included: list[dict[str, str]],
    excluded: list[dict[str, str]],
    cleaned_rows: list[dict[str, str]],
) -> str:
    needs_check = [row for row in cleaned_rows if row["needs_pdf_check"] == "yes"]
    type_counts: dict[str, int] = {}
    for row in included:
        type_counts[row["paper_type"]] = type_counts.get(row["paper_type"], 0) + 1

    lines = [
        "# Batch 1 Annotation Review",
        "",
        "## Summary",
        "",
        f"- Candidate rows: {len(rows)}",
        f"- Included in benchmark: {len(included)}",
        f"- Excluded from benchmark: {len(excluded)}",
        f"- Rows needing final PDF check: {len(needs_check)}",
        "",
        "## Output Files",
        "",
        f"- Cleaned candidate gold: `{OUTPUT}`",
        f"- Source copy: `{INPUT}`",
        "",
        "## Benchmark Scope",
        "",
        "This batch is broader than the original 5-paper flow-matching docking seed set. It contains flow-matching models, non-flow docking baselines, dataset/evaluation resources, and docking validation suites.",
        "",
        "Recommended framing:",
        "",
        "> Batch 1 evaluates a broader flow-matching and biomolecular-structure literature set, including docking, protein generation, molecule generation, dataset resources, and non-flow baseline systems.",
        "",
        "Do not describe this batch as only protein-ligand flow matching docking papers.",
        "",
        "## Included Paper Types",
        "",
    ]
    for paper_type, count in sorted(type_counts.items()):
        lines.append(f"- {paper_type}: {count}")

    lines.extend(["", "## Excluded Rows", ""])
    if excluded:
        for row in excluded:
            lines.append(f"- {row['paper_id']}: {row['title']} ({row['paper_type']})")
    else:
        lines.append("- None")

    lines.extend(["", "## Rows Needing PDF Check", ""])
    if needs_check:
        for row in needs_check:
            lines.append(
                f"- {row['paper_id']}: {row['title']} -- {row['verification_status']}"
            )
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Recommended Fixes Applied",
            "",
            "- Kept the original candidate file unchanged.",
            "- Created a cleaned candidate gold file using ` | ` as the value separator.",
            "- Removed the excluded computer-vision PoseBench row from the cleaned gold file.",
            "- Added `folder`, `paper_type`, `verification_status`, and `needs_pdf_check` metadata columns.",
            "- Preserved `review_notes` so uncertain annotation decisions remain auditable.",
            "- PDF-checked `paper_015` and `paper_022`, then applied targeted dataset/metric corrections.",
            "",
            "## PDF Requirement",
            "",
            "PDFs are not required for schema-level cleanup. PDFs are required before treating this as final gold, especially for rows marked `needs_pdf_check=yes`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    columns = [
        "paper_id",
        "title",
        "filename",
        "folder",
        "paper_type",
        *FIELD_COLUMNS,
        "review_notes",
        "verification_status",
        "needs_pdf_check",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
