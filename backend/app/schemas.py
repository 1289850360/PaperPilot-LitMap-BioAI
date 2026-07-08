from pydantic import BaseModel


class Evidence(BaseModel):
    section: str
    page_start: int
    page_end: int
    text: str


class PaperCard(BaseModel):
    task: list[str]
    datasets: list[str]
    models_or_methods: list[str]
    baselines: list[str]
    metrics: list[str]
    main_result: list[str]
    limitations: list[str]
    code_availability: list[str]
    evidence: dict[str, list[Evidence]]
    field_statuses: dict[str, str]
    verification_statuses: dict[str, str]


class PaperSummary(BaseModel):
    id: int
    title: str
    filename: str
    folder: str
    page_count: int
    abstract: str | None
    card: PaperCard
    created_at: str


class PaperFolderUpdate(BaseModel):
    folder: str


class PaperCardFieldUpdate(BaseModel):
    field: str
    values: list[str]
    status: str


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Evidence]
