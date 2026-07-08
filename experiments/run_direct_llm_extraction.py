"""Run a direct-LLM extraction baseline for PaperPilot.

This baseline sends the paper text directly to an LLM and asks for structured
fields without retrieval or citation verification. It is intended as a simple
comparison point against the heuristic and future RAG/citation-verified methods.

Examples:
    python experiments/run_direct_llm_extraction.py --manifest experiments/uploaded_papers_manifest.csv --out-dir experiments/outputs/direct_llm --dry-run
    python experiments/run_direct_llm_extraction.py --manifest experiments/uploaded_papers_manifest.csv --out-dir experiments/outputs/direct_llm --model gpt-4o-mini
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.pdf_parser import parse_pdf  # noqa: E402


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
    load_env_file(ROOT / ".env")
    manifest_rows = load_manifest(args.manifest)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    prediction_rows: list[dict[str, Any]] = []
    for index, row in enumerate(manifest_rows, start=1):
        pdf_path = Path(row["pdf_path"]).expanduser()
        paper_id = row.get("paper_id") or f"paper_{index:03d}"
        print(f"[{index}/{len(manifest_rows)}] Preparing direct LLM baseline for {pdf_path}")

        parsed = parse_pdf(pdf_path)
        prompt = build_prompt(parsed, max_chars=args.max_chars)

        if args.dry_run:
            prompt_path = args.out_dir / f"{safe_name(paper_id)}_prompt.txt"
            prompt_path.write_text(prompt, encoding="utf-8")
            result = empty_result(parsed, pdf_path)
            result["dry_run_prompt_path"] = str(prompt_path)
        else:
            result = call_openai(prompt=prompt, model=args.model)
            result["title"] = parsed["title"]
            result["filename"] = pdf_path.name
            result["page_count"] = page_count(parsed)

        result["paper_id"] = paper_id
        json_path = args.out_dir / f"{safe_name(paper_id)}.json"
        json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        prediction_rows.append(to_prediction_row(paper_id, result))

    csv_path = args.out_dir / "direct_llm_predictions.csv"
    write_prediction_csv(csv_path, prediction_rows)
    print(f"Wrote {csv_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run direct-LLM extraction baseline.")
    parser.add_argument("--manifest", required=True, type=Path, help="CSV with at least a pdf_path column.")
    parser.add_argument("--out-dir", type=Path, default=Path("experiments/outputs/direct_llm"))
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        help="OpenAI model name. Can also be set with OPENAI_MODEL.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=45000,
        help="Maximum number of source characters sent to the LLM.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write prompts and empty CSV rows without calling the API.",
    )
    return parser.parse_args()


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


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


def build_prompt(parsed: dict[str, Any], max_chars: int) -> str:
    source_text = source_text_for_prompt(parsed, max_chars=max_chars)
    schema = {
        "task": ["..."],
        "datasets": ["..."],
        "models_or_methods": ["..."],
        "baselines": ["..."],
        "metrics": ["..."],
        "main_result": ["..."],
        "limitations": ["..."],
        "code_availability": ["..."],
    }
    return f"""You are extracting structured information from a biomedical AI paper.

Return JSON only. Do not include markdown.

Use document-level evidence from the source text. Prefer canonical names.
Extract concise normalized values. If a field is not supported, return an empty list.

Field definitions:
- task: main scientific or engineering tasks solved by the paper.
- datasets: named datasets, benchmarks, evaluation sets, or important splits.
- models_or_methods: proposed method, central model family, and key method components.
- baselines: comparison methods, baseline systems, and reference tools.
- metrics: evaluation metrics, success criteria, and efficiency measures.
- main_result: main quantitative or qualitative results.
- limitations: stated limitations or clear failure modes.
- code_availability: code, repository, implementation, or data availability statements.

Expected JSON schema:
{json.dumps(schema, indent=2)}

Paper title:
{parsed.get("title", "")}

Abstract:
{parsed.get("abstract", "")}

Source text:
{source_text}
"""


def source_text_for_prompt(parsed: dict[str, Any], max_chars: int) -> str:
    chunks = parsed.get("chunks", [])
    parts: list[str] = []
    total = 0
    for chunk in chunks:
        label = f"[p. {chunk.get('page_start')}-{chunk.get('page_end')}, {chunk.get('section')}]"
        text = re.sub(r"\s+", " ", str(chunk.get("text", ""))).strip()
        piece = f"{label}\n{text}\n"
        if total + len(piece) > max_chars:
            remaining = max_chars - total
            if remaining > 500:
                parts.append(piece[:remaining])
            break
        parts.append(piece)
        total += len(piece)
    return "\n".join(parts)


def call_openai(prompt: str, model: str) -> dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env or run with --dry-run.")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a careful scientific information extraction system.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content or "{}"
    payload = json.loads(content)
    return normalize_payload(payload)


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    card: dict[str, list[str]] = {}
    for field in FIELD_KEYS:
        raw = payload.get(field, [])
        if isinstance(raw, str):
            values = split_values(raw)
        elif isinstance(raw, list):
            values = [str(item).strip() for item in raw if str(item).strip()]
        else:
            values = []
        card[field] = dedupe(values)
    return {"card": card}


def empty_result(parsed: dict[str, Any], pdf_path: Path) -> dict[str, Any]:
    return {
        "title": parsed["title"],
        "filename": pdf_path.name,
        "page_count": page_count(parsed),
        "card": {field: [] for field in FIELD_KEYS},
    }


def to_prediction_row(paper_id: str, result: dict[str, Any]) -> dict[str, Any]:
    card = result.get("card", {})
    row: dict[str, Any] = {
        "paper_id": paper_id,
        "title": result.get("title", ""),
        "filename": result.get("filename", ""),
        "folder": "Direct LLM",
        "page_count": result.get("page_count", 0),
    }
    for field in FIELD_KEYS:
        row[field] = " | ".join(card.get(field, []))
    row["field_statuses"] = "; ".join(f"{field}:ai_extracted" for field in FIELD_KEYS)
    row["verification_statuses"] = "; ".join(f"{field}:unknown" for field in FIELD_KEYS)
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


def page_count(parsed: dict[str, Any]) -> int:
    chunks = parsed.get("chunks", [])
    if not chunks:
        return 0
    return max(int(chunk.get("page_end", 0)) for chunk in chunks)


def split_values(value: str) -> list[str]:
    parts = re.split(r"\s*\|\s*|\s*;\s*|\n+", value)
    return [part.strip() for part in parts if part.strip()]


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = re.sub(r"\s+", " ", value.lower()).strip()
        if key and key not in seen:
            seen.add(key)
            result.append(value)
    return result


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-")
    return cleaned or "paper"


if __name__ == "__main__":
    main()
