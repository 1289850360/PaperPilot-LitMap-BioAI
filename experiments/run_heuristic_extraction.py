"""Run PaperPilot's heuristic extraction pipeline on one PDF.

Example:
    python experiments/run_heuristic_extraction.py --pdf path/to/paper.pdf --out experiments/outputs/paper.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.extractor import extract_card  # noqa: E402
from app.services.pdf_parser import parse_pdf  # noqa: E402


def main() -> None:
    args = parse_args()
    result = run_extraction(args.pdf)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run heuristic PaperPilot extraction on one PDF.")
    parser.add_argument("--pdf", required=True, type=Path, help="Path to a PDF file.")
    parser.add_argument("--out", type=Path, help="Optional JSON output path.")
    return parser.parse_args()


def run_extraction(pdf_path: Path) -> dict[str, Any]:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file: {pdf_path}")

    parsed = parse_pdf(pdf_path)
    card = extract_card(parsed)

    return {
        "title": parsed["title"],
        "filename": pdf_path.name,
        "pdf_path": str(pdf_path),
        "abstract": parsed.get("abstract", ""),
        "page_count": page_count(parsed),
        "chunk_count": len(parsed.get("chunks", [])),
        "card": card,
    }


def page_count(parsed: dict[str, Any]) -> int:
    chunks = parsed.get("chunks", [])
    if not chunks:
        return 0
    return max(int(chunk.get("page_end", 0)) for chunk in chunks)


if __name__ == "__main__":
    main()
