import json
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator

from .config import DB_PATH
from .services.verifier import build_verification_statuses


CARD_FIELD_KEYS = {
    "task",
    "datasets",
    "models_or_methods",
    "baselines",
    "metrics",
    "main_result",
    "limitations",
    "code_availability",
}

FIELD_STATUSES = {"ai_extracted", "needs_review", "verified", "missing"}


def normalize_lookup_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                folder TEXT NOT NULL DEFAULT 'Uncategorized',
                abstract TEXT,
                card_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(papers)").fetchall()
        }
        if "folder" not in columns:
            conn.execute(
                "ALTER TABLE papers ADD COLUMN folder TEXT NOT NULL DEFAULT 'Uncategorized'"
            )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id INTEGER NOT NULL,
                section TEXT NOT NULL,
                page_start INTEGER NOT NULL,
                page_end INTEGER NOT NULL,
                text TEXT NOT NULL,
                FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE
            )
            """
        )


def insert_paper(
    *,
    title: str,
    filename: str,
    file_path: str,
    abstract: str,
    card: dict[str, Any],
    chunks: list[dict[str, Any]],
) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO papers (title, filename, file_path, folder, abstract, card_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (title, filename, file_path, "Uncategorized", abstract, json.dumps(card), utc_now()),
        )
        paper_id = int(cursor.lastrowid)
        conn.executemany(
            """
            INSERT INTO chunks (paper_id, section, page_start, page_end, text)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    paper_id,
                    chunk["section"],
                    chunk["page_start"],
                    chunk["page_end"],
                    chunk["text"],
                )
                for chunk in chunks
            ],
        )
        return paper_id


def list_papers() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, filename, file_path, folder, abstract, card_json, created_at
            FROM papers
            ORDER BY id DESC
            """
        ).fetchall()
    return [paper_from_row(row) for row in rows]


def find_duplicate_papers(title: str, filename: str) -> list[dict[str, Any]]:
    title_key = normalize_lookup_text(title)
    filename_key = normalize_lookup_text(filename)
    candidates = list_papers()
    duplicates: list[dict[str, Any]] = []
    for paper in candidates:
        candidate_title = normalize_lookup_text(paper["title"])
        candidate_filename = normalize_lookup_text(paper["filename"])
        same_filename = filename_key and filename_key == candidate_filename
        same_title = title_key and title_key == candidate_title
        title_contains = (
            len(title_key) > 24
            and len(candidate_title) > 24
            and (title_key in candidate_title or candidate_title in title_key)
        )
        if same_filename or same_title or title_contains:
            duplicates.append(paper)
    return duplicates


def get_paper(paper_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, title, filename, file_path, folder, abstract, card_json, created_at
            FROM papers
            WHERE id = ?
            """,
            (paper_id,),
        ).fetchone()
    return paper_from_row(row) if row else None


def get_paper_file_path(paper_id: int) -> str | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT file_path FROM papers WHERE id = ?",
            (paper_id,),
        ).fetchone()
    return str(row["file_path"]) if row else None


def get_pdf_page_count(file_path: str) -> int:
    try:
        import fitz

        doc = fitz.open(file_path)
        try:
            return int(doc.page_count)
        finally:
            doc.close()
    except Exception:
        return 1


def get_chunks(paper_id: int) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, section, page_start, page_end, text
            FROM chunks
            WHERE paper_id = ?
            ORDER BY id ASC
            """,
            (paper_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def update_paper_folder(paper_id: int, folder: str) -> dict[str, Any] | None:
    clean_folder = folder.strip() or "Uncategorized"
    with get_connection() as conn:
        conn.execute(
            "UPDATE papers SET folder = ? WHERE id = ?",
            (clean_folder, paper_id),
        )
    return get_paper(paper_id)


def replace_paper_extraction(
    paper_id: int,
    *,
    title: str,
    abstract: str,
    card: dict[str, Any],
    chunks: list[dict[str, Any]],
) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM papers WHERE id = ?",
            (paper_id,),
        ).fetchone()
        if not row:
            return None
        conn.execute(
            """
            UPDATE papers
            SET title = ?, abstract = ?, card_json = ?
            WHERE id = ?
            """,
            (title, abstract, json.dumps(card), paper_id),
        )
        conn.execute("DELETE FROM chunks WHERE paper_id = ?", (paper_id,))
        conn.executemany(
            """
            INSERT INTO chunks (paper_id, section, page_start, page_end, text)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    paper_id,
                    chunk["section"],
                    chunk["page_start"],
                    chunk["page_end"],
                    chunk["text"],
                )
                for chunk in chunks
            ],
        )
    return get_paper(paper_id)


def update_card_field(
    paper_id: int,
    field: str,
    values: list[str],
    status: str,
) -> dict[str, Any] | None:
    if field not in CARD_FIELD_KEYS:
        raise ValueError("Unknown card field")
    if status not in FIELD_STATUSES:
        raise ValueError("Unknown field status")

    clean_values = [value.strip() for value in values if value.strip()]
    with get_connection() as conn:
        row = conn.execute(
            "SELECT card_json FROM papers WHERE id = ?",
            (paper_id,),
        ).fetchone()
        if not row:
            return None
        card = ensure_card_metadata(json.loads(row["card_json"]))
        card[field] = clean_values
        card["field_statuses"][field] = status
        card["verification_statuses"][field] = build_verification_statuses(card)[field]
        conn.execute(
            "UPDATE papers SET card_json = ? WHERE id = ?",
            (json.dumps(card), paper_id),
        )
    return get_paper(paper_id)


def delete_paper(paper_id: int) -> str | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT file_path FROM papers WHERE id = ?",
            (paper_id,),
        ).fetchone()
        if not row:
            return None
        file_path = str(row["file_path"])
        conn.execute("DELETE FROM chunks WHERE paper_id = ?", (paper_id,))
        conn.execute("DELETE FROM papers WHERE id = ?", (paper_id,))
        return file_path


def paper_from_row(row: sqlite3.Row) -> dict[str, Any]:
    paper = dict(row)
    paper["card"] = ensure_card_metadata(json.loads(paper.pop("card_json")))
    paper["page_count"] = get_pdf_page_count(paper["file_path"])
    paper.pop("file_path", None)
    return paper


def ensure_card_metadata(card: dict[str, Any]) -> dict[str, Any]:
    card.setdefault("evidence", {})
    statuses = card.setdefault("field_statuses", {})
    verification_statuses = card.setdefault("verification_statuses", {})
    computed_verification_statuses = build_verification_statuses(card)
    for field in CARD_FIELD_KEYS:
        card.setdefault(field, [])
        statuses.setdefault(field, "ai_extracted")
        verification_statuses.setdefault(field, computed_verification_statuses[field])
    return card
