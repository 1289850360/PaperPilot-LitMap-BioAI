"""Value-level verifier and filter for PaperPilot prediction CSVs.

This is a local, non-LLM verifier. It re-opens each PDF, searches for evidence
for each extracted value, and filters values that do not pass field-specific
support rules.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

import fitz


FIELD_COLUMNS = ["task", "datasets", "models_or_methods", "metrics"]

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "this",
    "that",
    "over",
    "into",
    "using",
    "based",
    "model",
    "method",
    "methods",
    "prediction",
    "generation",
}

FIELD_CONTEXT = {
    "task": re.compile(
        r"\b(?:task|aim|goal|we|propose|present|predict|generate|design|dock|benchmark|evaluate)\b",
        re.I,
    ),
    "datasets": re.compile(
        r"\b(?:dataset|benchmark|test set|training set|split|suite|database|resource|evaluation)\b",
        re.I,
    ),
    "models_or_methods": re.compile(
        r"\b(?:we propose|we present|introduce|our|model|method|framework|architecture|module|"
        r"network|flow|diffusion|matching|scoring|guidance|conditioning|sampler|head|prior)\b",
        re.I,
    ),
    "metrics": re.compile(
        r"\b(?:metric|evaluate|evaluation|result|performance|score|accuracy|validity|"
        r"rmsd|tm-score|correlation|rmse|mae|runtime|speed|memory|diversity|novelty|"
        r"designability|success|percentile|below)\b|[%<>≤≥=]",
        re.I,
    ),
}

BROAD_VALUES = {
    "flow matching",
    "conditional flow matching",
    "continuous normalizing flow",
    "inference time",
    "runtime",
    "rmsd",
    "success rate",
    "physical validity",
}


@dataclass
class Verification:
    value: str
    status: str
    page: int
    reason: str
    snippet: str


def main() -> None:
    args = parse_args()
    predictions = load_rows(args.pred)
    manifest = {row["paper_id"]: Path(row["pdf_path"]) for row in load_rows(args.manifest)}

    filtered_rows: list[dict[str, str]] = []
    audit_rows: list[dict[str, str]] = []
    text_cache: dict[str, list[tuple[int, str]]] = {}

    for row in predictions:
        paper_id = row["paper_id"]
        pdf_path = manifest.get(paper_id)
        if not pdf_path or not pdf_path.exists():
            filtered_rows.append(row)
            continue
        pages = text_cache.setdefault(paper_id, extract_pages(pdf_path))
        filtered = dict(row)
        for field in FIELD_COLUMNS:
            values = split_values(row.get(field, ""))
            kept: list[str] = []
            for value in values:
                verification = verify_value(value, field, pages)
                audit_rows.append(
                    {
                        "paper_id": paper_id,
                        "field": field,
                        "value": value,
                        "status": verification.status,
                        "page": str(verification.page or ""),
                        "reason": verification.reason,
                        "snippet": verification.snippet,
                    }
                )
                if verification.status in {"supported", "weak"}:
                    kept.append(value)
            filtered[field] = " | ".join(kept)
        filtered_rows.append(filtered)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    write_csv(args.out, filtered_rows, list(predictions[0]))
    write_csv(args.audit, audit_rows, ["paper_id", "field", "value", "status", "page", "reason", "snippet"])
    print(f"Wrote {args.out}")
    print(f"Wrote {args.audit}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Filter prediction values using local PDF evidence.")
    parser.add_argument("--pred", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--audit", required=True, type=Path)
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


def extract_pages(path: Path) -> list[tuple[int, str]]:
    doc = fitz.open(path)
    try:
        return [(index, page.get_text("text")) for index, page in enumerate(doc, start=1)]
    finally:
        doc.close()


def split_values(value: str) -> list[str]:
    if not value.strip():
        return []
    return [part.strip() for part in re.split(r"\s*\|\s*|\s*;\s*|\n+", value) if part.strip()]


def verify_value(value: str, field: str, pages: list[tuple[int, str]]) -> Verification:
    candidates = evidence_candidates(value, pages)
    if not candidates:
        return Verification(value, "unsupported", 0, "no lexical evidence", "")

    context_re = FIELD_CONTEXT[field]
    best_page, best_snippet = candidates[0]
    if is_broad_value(value):
        for page, snippet in candidates:
            if context_re.search(snippet):
                return Verification(value, "supported", page, "broad value with field context", snippet)
        return Verification(value, "unsupported", best_page, "broad value lacks field context", best_snippet)

    for page, snippet in candidates:
        if context_re.search(snippet):
            return Verification(value, "supported", page, "lexical evidence with field context", snippet)

    return Verification(value, "weak", best_page, "lexical evidence without field context", best_snippet)


def evidence_candidates(value: str, pages: list[tuple[int, str]]) -> list[tuple[int, str]]:
    exact_patterns = literal_patterns(value)
    hits: list[tuple[int, str]] = []
    for page, text in pages:
        compact_text = re.sub(r"\s+", " ", text)
        for pattern in exact_patterns:
            match = pattern.search(compact_text)
            if match:
                hits.append((page, snippet_around(compact_text, match.start(), match.end())))
                break
        if len(hits) >= 5:
            return hits

    if hits:
        return hits

    tokens = meaningful_tokens(value)
    if len(tokens) < 2:
        return []
    for page, text in pages:
        norm = normalize(text)
        overlap = len(tokens & meaningful_tokens(norm)) / len(tokens)
        if overlap >= 0.75:
            hits.append((page, snippet_from_tokens(text, tokens)))
            if len(hits) >= 5:
                return hits
    return hits


def literal_patterns(value: str) -> list[re.Pattern[str]]:
    variants = {value}
    variants.add(value.replace("≤", "<="))
    variants.add(value.replace("Å", "A"))
    variants.add(value.replace(" / ", "/"))
    variants.add(value.replace("-", " "))
    patterns = []
    for variant in variants:
        clean = variant.strip()
        if clean:
            patterns.append(re.compile(re.escape(clean), re.I))
    return patterns


def snippet_around(text: str, start: int, end: int, radius: int = 260) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    return text[left:right].strip()[:700]


def snippet_from_tokens(text: str, tokens: set[str]) -> str:
    compact = re.sub(r"\s+", " ", text)
    lowered = compact.lower()
    positions = [lowered.find(token) for token in tokens if lowered.find(token) >= 0]
    if not positions:
        return compact[:700]
    pos = min(positions)
    return snippet_around(compact, pos, pos + 1)


def is_broad_value(value: str) -> bool:
    norm = normalize_label(value)
    if norm in BROAD_VALUES:
        return True
    return len(meaningful_tokens(value)) <= 2 and not re.search(r"[A-Z][a-z]+[A-Z]|[0-9]", value)


def meaningful_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.split(r"\s+", normalize(value))
        if len(token) >= 3 and token not in STOPWORDS
    }


def normalize_label(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower().replace("-", " ")).strip()


def normalize(value: str) -> str:
    value = value.lower().replace("≤", " ").replace("≥", " ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


if __name__ == "__main__":
    main()
