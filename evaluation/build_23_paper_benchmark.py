"""Build the 23-paper benchmark gold file and extraction manifest."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED_GOLD = ROOT / "evaluation" / "gold.csv"
BATCH_GOLD = ROOT / "evaluation" / "gold_batch1_candidate_cleaned.csv"
SEED_MANIFEST = ROOT / "experiments" / "uploaded_papers_manifest.csv"
UPLOAD_DIR = ROOT / "backend" / "data" / "uploads"
TANKBIND_FALLBACK = ROOT / "work" / "pdf_check" / "paper_022_tankbind.pdf"

OUT_GOLD = ROOT / "evaluation" / "gold_23_paper_benchmark.csv"
OUT_MANIFEST = ROOT / "experiments" / "benchmark_23_manifest.csv"
OUT_SUMMARY = ROOT / "evaluation" / "BENCHMARK_23_SUMMARY.md"

FIELD_COLUMNS = ["task", "datasets", "models_or_methods", "metrics"]


def main() -> None:
    seed_rows = load_rows(SEED_GOLD)
    batch_rows = load_rows(BATCH_GOLD)
    seed_manifest = load_rows(SEED_MANIFEST)

    combined_gold = build_combined_gold(seed_rows, batch_rows, seed_manifest)
    manifest_rows, missing = build_manifest(seed_manifest, batch_rows)

    write_csv(OUT_GOLD, combined_gold, gold_columns())
    write_csv(OUT_MANIFEST, manifest_rows, ["pdf_path", "paper_id", "notes"])
    OUT_SUMMARY.write_text(
        build_summary(combined_gold, manifest_rows, missing),
        encoding="utf-8",
    )

    print(f"Wrote {OUT_GOLD}")
    print(f"Wrote {OUT_MANIFEST}")
    print(f"Wrote {OUT_SUMMARY}")
    if missing:
        print("Missing PDFs:")
        for item in missing:
            print(f"- {item}")


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [
            {(key or "").strip(): (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(file)
        ]


def build_combined_gold(
    seed_rows: list[dict[str, str]],
    batch_rows: list[dict[str, str]],
    seed_manifest: list[dict[str, str]],
) -> list[dict[str, str]]:
    filename_by_seed_id = {
        row["paper_id"]: Path(row["pdf_path"]).name.split("_", 1)[-1]
        for row in seed_manifest
    }
    combined: list[dict[str, str]] = []
    for row in seed_rows:
        combined.append(
            {
                "paper_id": row["paper_id"],
                "title": row["title"],
                "filename": filename_by_seed_id.get(row["paper_id"], ""),
                "folder": "5-paper seed gold",
                "paper_type": "flow-matching docking seed paper",
                "task": normalize_values(row.get("task", "")),
                "datasets": normalize_values(row.get("datasets", "")),
                "models_or_methods": normalize_values(row.get("models_or_methods", "")),
                "metrics": normalize_values(row.get("metrics", "")),
                "review_notes": row.get("review_notes", ""),
                "verification_status": "verified seed gold",
            }
        )
    for row in batch_rows:
        combined.append({column: row.get(column, "") for column in gold_columns()})
    return sorted(combined, key=lambda item: item["paper_id"])


def build_manifest(
    seed_manifest: list[dict[str, str]],
    batch_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[str]]:
    rows = [
        {
            "pdf_path": row["pdf_path"],
            "paper_id": row["paper_id"],
            "notes": row.get("notes", ""),
        }
        for row in seed_manifest
    ]

    missing: list[str] = []
    for row in batch_rows:
        pdf_path = find_pdf(row["filename"], row["paper_id"])
        if pdf_path is None:
            missing.append(f"{row['paper_id']} {row['filename']}")
            continue
        rows.append(
            {
                "pdf_path": str(pdf_path),
                "paper_id": row["paper_id"],
                "notes": row["title"],
            }
        )
    return sorted(rows, key=lambda item: item["paper_id"]), missing


def find_pdf(filename: str, paper_id: str) -> Path | None:
    matches = sorted(UPLOAD_DIR.glob(f"*_{filename}"))
    if matches:
        return matches[0].resolve()
    direct_matches = sorted(UPLOAD_DIR.glob(filename))
    if direct_matches:
        return direct_matches[0].resolve()
    if paper_id == "paper_022" and TANKBIND_FALLBACK.exists():
        return TANKBIND_FALLBACK.resolve()
    return None


def normalize_values(value: str) -> str:
    if not value.strip():
        return ""
    pieces: list[str] = []
    for chunk in value.replace(";", "|").split("|"):
        clean = chunk.strip()
        if clean:
            pieces.append(clean)
    return " | ".join(dedupe(pieces))


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = " ".join(value.lower().replace("-", " ").split())
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def build_summary(
    gold_rows: list[dict[str, str]],
    manifest_rows: list[dict[str, str]],
    missing: list[str],
) -> str:
    paper_types: dict[str, int] = {}
    for row in gold_rows:
        paper_type = row.get("paper_type", "unknown")
        paper_types[paper_type] = paper_types.get(paper_type, 0) + 1

    lines = [
        "# 23-Paper Benchmark Summary",
        "",
        f"- Gold rows: {len(gold_rows)}",
        f"- Manifest rows with PDFs: {len(manifest_rows)}",
        f"- Missing PDFs: {len(missing)}",
        "",
        "## Files",
        "",
        f"- Gold: `{OUT_GOLD.relative_to(ROOT)}`",
        f"- Manifest: `{OUT_MANIFEST.relative_to(ROOT)}`",
        "",
        "## Paper Types",
        "",
    ]
    for paper_type, count in sorted(paper_types.items()):
        lines.append(f"- {paper_type}: {count}")

    lines.extend(["", "## Missing PDFs", ""])
    if missing:
        lines.extend(f"- {item}" for item in missing)
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def gold_columns() -> list[str]:
    return [
        "paper_id",
        "title",
        "filename",
        "folder",
        "paper_type",
        *FIELD_COLUMNS,
        "review_notes",
        "verification_status",
    ]


if __name__ == "__main__":
    main()
