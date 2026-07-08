import re
from pathlib import Path

import fitz


SECTION_RE = re.compile(
    r"^(abstract|introduction|background|related work|methods?|materials and methods|"
    r"experiments?|results?|discussion|conclusion|limitations?|references)\b",
    re.IGNORECASE,
)


def parse_pdf(path: Path) -> dict:
    doc = fitz.open(path)
    pages: list[dict] = []
    for index, page in enumerate(doc, start=1):
        text = page.get_text("text")
        pages.append({"page": index, "text": normalize_text(text)})

    full_text = "\n".join(page["text"] for page in pages)
    title = guess_title(pages)
    abstract = guess_abstract(full_text)
    chunks = section_aware_chunks(pages)
    return {"title": title, "abstract": abstract, "chunks": chunks}


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def guess_title(pages: list[dict]) -> str:
    first_page = pages[0]["text"] if pages else ""
    candidates = [
        line.strip()
        for line in first_page.splitlines()
        if 20 <= len(line.strip()) <= 220
    ]
    for line in candidates[:8]:
        lower = line.lower()
        if not lower.startswith(("abstract", "introduction", "arxiv", "doi")):
            return line
    return candidates[0] if candidates else "Untitled paper"


def guess_abstract(full_text: str) -> str:
    match = re.search(
        r"\babstract\b\s*(.*?)(?=\n\s*(?:1\.?\s*)?introduction\b|\n\s*keywords?\b)",
        full_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""
    return compact(match.group(1), limit=1800)


def section_aware_chunks(
    pages: list[dict],
    max_chars: int = 1800,
    overlap_chars: int = 200,
) -> list[dict]:
    chunks: list[dict] = []
    section = "Front matter"
    buffer = ""
    page_start = 1
    page_end = 1

    for page in pages:
        page_no = page["page"]
        for raw_line in page["text"].splitlines():
            line = raw_line.strip()
            if not line:
                continue
            maybe_section = detect_section(line)
            if maybe_section:
                if buffer:
                    chunks.extend(split_chunk(buffer, section, page_start, page_end, max_chars, overlap_chars))
                    buffer = ""
                section = maybe_section
                page_start = page_no
            if not buffer:
                page_start = page_no
            page_end = page_no
            buffer += line + "\n"
            if len(buffer) >= max_chars:
                chunks.extend(split_chunk(buffer, section, page_start, page_end, max_chars, overlap_chars))
                buffer = buffer[-overlap_chars:]

    if buffer.strip():
        chunks.extend(split_chunk(buffer, section, page_start, page_end, max_chars, overlap_chars))
    return chunks


def detect_section(line: str) -> str | None:
    cleaned = re.sub(r"^\d+(\.\d+)*\.?\s+", "", line).strip()
    if len(cleaned) > 80:
        return None
    match = SECTION_RE.match(cleaned)
    if not match:
        return None
    return cleaned.title()


def split_chunk(
    text: str,
    section: str,
    page_start: int,
    page_end: int,
    max_chars: int,
    overlap_chars: int,
) -> list[dict]:
    text = compact(text)
    if len(text) <= max_chars:
        return [
            {
                "section": section,
                "page_start": page_start,
                "page_end": page_end,
                "text": text,
            }
        ]

    pieces = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        pieces.append(
            {
                "section": section,
                "page_start": page_start,
                "page_end": page_end,
                "text": text[start:end],
            }
        )
        if end == len(text):
            break
        start = max(0, end - overlap_chars)
    return pieces


def compact(text: str, limit: int | None = None) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    if limit and len(value) > limit:
        return value[:limit].rsplit(" ", 1)[0] + "..."
    return value
