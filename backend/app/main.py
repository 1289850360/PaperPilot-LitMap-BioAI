from pathlib import Path
from uuid import uuid4

import fitz
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response

from .config import UPLOAD_DIR
from .database import (
    delete_paper,
    find_duplicate_papers,
    get_chunks,
    get_paper,
    get_paper_file_path,
    init_db,
    insert_paper,
    list_papers,
    replace_paper_extraction,
    update_card_field,
    update_paper_folder,
)
from .schemas import AskRequest, AskResponse, PaperCardFieldUpdate, PaperFolderUpdate, PaperSummary
from .services.extractor import extract_card
from .services.pdf_parser import parse_pdf
from .services.qa import answer_question


app = FastAPI(title="PaperPilot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/papers", response_model=list[PaperSummary])
def papers() -> list[dict]:
    return list_papers()


@app.get("/papers/{paper_id}", response_model=PaperSummary)
def paper_detail(paper_id: int) -> dict:
    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@app.get("/papers/{paper_id}/file")
def paper_file(paper_id: int) -> FileResponse:
    file_path = get_paper_file_path(paper_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Paper not found")
    path = Path(file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF file not found")
    return FileResponse(
        path,
        media_type="application/pdf",
        filename=path.name,
        headers={"Content-Disposition": f'inline; filename="{path.name}"'},
    )


@app.get("/papers/{paper_id}/page/{page_number}")
def paper_page_image(paper_id: int, page_number: int) -> Response:
    file_path = get_paper_file_path(paper_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Paper not found")
    path = Path(file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF file not found")
    if page_number < 1:
        raise HTTPException(status_code=400, detail="Page number must be at least 1")

    doc = fitz.open(path)
    try:
        if page_number > doc.page_count:
            raise HTTPException(status_code=404, detail="Page not found")
        page = doc.load_page(page_number - 1)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), alpha=False)
        return Response(
            content=pixmap.tobytes("png"),
            media_type="image/png",
            headers={"Cache-Control": "public, max-age=3600"},
        )
    finally:
        doc.close()


@app.patch("/papers/{paper_id}/folder", response_model=PaperSummary)
def change_paper_folder(paper_id: int, request: PaperFolderUpdate) -> dict:
    paper = update_paper_folder(paper_id, request.folder)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@app.patch("/papers/{paper_id}/card-field", response_model=PaperSummary)
def change_card_field(paper_id: int, request: PaperCardFieldUpdate) -> dict:
    try:
        paper = update_card_field(
            paper_id,
            field=request.field,
            values=request.values,
            status=request.status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@app.post("/papers/{paper_id}/reextract", response_model=PaperSummary)
def reextract_paper(paper_id: int) -> dict:
    file_path = get_paper_file_path(paper_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Paper not found")
    path = Path(file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF file not found")

    parsed = parse_pdf(path)
    card = extract_card(parsed)
    paper = replace_paper_extraction(
        paper_id,
        title=parsed["title"],
        abstract=parsed["abstract"],
        card=card,
        chunks=parsed["chunks"],
    )
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@app.delete("/papers/{paper_id}")
def remove_paper(paper_id: int) -> dict[str, str]:
    file_path = delete_paper(paper_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Paper not found")
    path = Path(file_path)
    if path.exists():
        path.unlink()
    return {"status": "deleted"}


@app.post("/papers/upload", response_model=PaperSummary)
async def upload_paper(file: UploadFile = File(...), force: bool = Form(False)) -> dict:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    safe_name = Path(file.filename).name
    stored_name = f"{uuid4().hex}_{safe_name}"
    file_path = UPLOAD_DIR / stored_name
    file_path.write_bytes(await file.read())

    parsed = parse_pdf(file_path)
    duplicates = find_duplicate_papers(parsed["title"], safe_name)
    if duplicates and not force:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=409,
            detail={
                "code": "duplicate_paper",
                "message": "This paper may already exist.",
                "duplicates": [
                    {
                        "id": paper["id"],
                        "title": paper["title"],
                        "filename": paper["filename"],
                    }
                    for paper in duplicates[:3]
                ],
            },
        )
    card = extract_card(parsed)
    paper_id = insert_paper(
        title=parsed["title"],
        filename=safe_name,
        file_path=str(file_path),
        abstract=parsed["abstract"],
        card=card,
        chunks=parsed["chunks"],
    )
    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=500, detail="Paper was not saved")
    return paper


@app.post("/papers/{paper_id}/ask", response_model=AskResponse)
def ask_paper(paper_id: int, request: AskRequest) -> dict:
    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    chunks = get_chunks(paper_id)
    return answer_question(request.question, chunks)
