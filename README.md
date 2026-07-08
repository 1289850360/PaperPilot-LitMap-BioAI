# PaperPilot / LitMap-BioAI

PaperPilot, also called LitMap-BioAI, is a citation-grounded literature mining system for biomedical AI and AI-for-science papers.

It is not intended to be a simple "ChatGPT for PDFs" wrapper. The goal is to build a structured reading, extraction, comparison, and evaluation workflow for research papers. A user uploads PDF papers, the system parses the source text, extracts comparable fields, links answers back to source citations, and supports multi-paper comparison across tasks, datasets, models, baselines, metrics, results, limitations, and code availability.

This repository is currently an MVP web demo.

## Current Features

- Upload and parse research paper PDFs.
- Render original PDF pages in the browser, including figures, tables, equations, and page layout.
- Generate a structured paper card with:
  - task
  - datasets
  - models or methods
  - baselines
  - evaluation metrics
  - main result
  - limitations
  - code availability
- Show citation evidence for extracted fields.
- Show heuristic citation verification status for each extracted field: supported, weak support, unsupported, or missing.
- Ask paper-level questions with citation-grounded answers.
- Edit extracted fields manually and mark each field as AI extracted, needs review, verified, or missing.
- Re-extract saved papers after improving the local extraction pipeline.
- Save papers locally with SQLite.
- Delete duplicate or unwanted papers.
- Organize papers into folders.
- Search papers by title, dataset, method, metric, and extracted content.
- Compare selected papers in a multi-paper table.
- Export the current paper as Markdown.
- Export all annotations as CSV for later evaluation.
- Switch the UI between Chinese and English.

## Demo Status

The MVP is designed to run locally first. This makes it easier to develop the parsing, extraction, citation, and evaluation pipeline before adding production deployment, login, cloud storage, and stronger LLM infrastructure.

Current extraction and citation verification are lightweight heuristic baselines. The next research-grade version should add LLM-based schema extraction, vector retrieval, and stronger citation verification.

## Tech Stack

Frontend:

- Next.js
- React
- TypeScript
- lucide-react icons

Backend:

- Python
- FastAPI
- PyMuPDF
- SQLite
- Pydantic

Planned:

- Chroma or FAISS for vector retrieval
- OpenAI API or another LLM API for schema-constrained extraction
- PostgreSQL for deployable storage
- Evaluation scripts for field-level and citation-level scoring

## Project Structure

```text
backend/
  app/
    main.py                 FastAPI routes
    database.py             SQLite setup and queries
    schemas.py              API models
    services/
      pdf_parser.py         PyMuPDF parsing and section-aware chunking
      extractor.py          MVP structured field extraction
      qa.py                 MVP citation-grounded retrieval Q&A
      verifier.py           MVP citation verification status
  data/
    uploads/                Local uploaded PDFs
  requirements.txt

frontend/
  app/
    page.tsx                Main web UI
    layout.tsx
    globals.css
  components/
    PaperCard.tsx           Structured paper card
    CompareTable.tsx        Multi-paper comparison table
  lib/
    api.ts                  Backend API calls
    exporters.ts            Markdown and CSV export helpers
    i18n.ts                 Chinese and English UI text
    types.ts                Shared frontend types
  package.json

docs/
  ROADMAP.md
  EVALUATION_PLAN.md

scripts/
  start-all.ps1
  start-backend.ps1
  start-frontend.ps1
```

## Quick Start on Windows

From the project root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-all.ps1
```

Then open:

```text
http://127.0.0.1:3000
```

Backend health check:

```text
http://127.0.0.1:8000/health
```

Keep the terminal open while using the app. Press `Ctrl+C` to stop both frontend and backend.

## Manual Start

Use this if you want separate terminals for backend and frontend.

Terminal 1:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-backend.ps1
```

Terminal 2:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-frontend.ps1
```

Then open:

```text
http://127.0.0.1:3000
```

## Manual Setup Without Scripts

Backend:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd frontend
pnpm install
pnpm dev -- --hostname 127.0.0.1 --port 3000
```

If `pnpm` is not installed:

```powershell
npm install -g pnpm
```

## Environment Variables

Copy `.env.example` if you want a local `.env` file:

```powershell
Copy-Item .env.example .env
```

For the current MVP, no API key is required. `OPENAI_API_KEY` is reserved for the planned LLM extraction stage.

## How Another Person Can Try It

For a technical reviewer:

1. Clone the repository.
2. Install Python 3.11+ and Node.js LTS.
3. Run `powershell -ExecutionPolicy Bypass -File .\scripts\start-all.ps1`.
4. Open `http://127.0.0.1:3000`.
5. Upload one or more PDFs and inspect the extracted cards, citations, PDF preview, and compare table.

For a non-technical reviewer:

1. Prepare a short screen recording or demo video.
2. Include screenshots of the upload flow, paper card, citation evidence, PDF preview, and comparison table.
3. Provide a hosted demo later after deployment is added.

## Research Direction

The intended research contribution is a schema-constrained, citation-verified extraction pipeline for biomedical AI literature mining.

The planned evaluation compares:

- direct LLM extraction
- ordinary RAG extraction
- schema-constrained extraction with citation verification

Target metrics:

- field-level accuracy
- citation correctness
- hallucination rate
- missing rate

See [docs/EVALUATION_PLAN.md](docs/EVALUATION_PLAN.md) for details.

For tool and paper inspirations, see [docs/RELATED_WORK.md](docs/RELATED_WORK.md).

## Minimal Evaluation

After exporting annotations from the web UI, create a manually corrected gold CSV and run:

```powershell
python evaluation\score_extraction.py --pred evaluation\predictions.csv --gold evaluation\gold.csv
```

The evaluation script reports field-level accuracy, missing rate, hallucination rate, and per-field scores. See [evaluation/README.md](evaluation/README.md).

The first 5-paper pilot result is summarized in [evaluation/PILOT_RESULTS.md](evaluation/PILOT_RESULTS.md).

The latest local schema-aware extraction run improves the pilot value-level F1 from 18.0% to 77.6% on the same 5-paper set, with value precision reaching 85.2%. The comparison table is in [evaluation/baseline_comparison.md](evaluation/baseline_comparison.md).

A broader 23-paper benchmark has also been assembled. On this wider set, the same schema-aware local extractor drops to 42.8% value-level F1, which documents the current generalization limit and motivates value-level citation verification. See [evaluation/BENCHMARK_23_RESULTS.md](evaluation/BENCHMARK_23_RESULTS.md).

## Reproducible Experiments

The current heuristic extraction pipeline can also be run from the command line:

```powershell
python experiments\run_heuristic_extraction.py --pdf path\to\paper.pdf --out experiments\outputs\paper.json
```

For batch extraction:

```powershell
python experiments\batch_extract.py --manifest experiments\sample_papers.csv --out-dir experiments\outputs
```

For the direct LLM baseline:

```powershell
python experiments\run_direct_llm_extraction.py --manifest experiments\uploaded_papers_manifest.csv --out-dir experiments\outputs\direct_llm --dry-run
```

Remove `--dry-run` after adding `OPENAI_API_KEY` to `.env`.

See [experiments/README.md](experiments/README.md).

The first 5-paper flow-matching seed set is documented in [docs/SEED_PAPER_SET.md](docs/SEED_PAPER_SET.md). After downloading the two recommended papers, run:

```powershell
python experiments\batch_extract.py --manifest experiments\flow_matching_seed_manifest.csv --out-dir experiments\outputs
```

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Limitations

- This is an MVP, not a production service.
- There is no user login yet.
- Uploaded PDFs are stored locally.
- SQLite is used for local development.
- Extraction is currently heuristic and should be treated as a baseline.
- Citation grounding and heuristic verification exist, but robust LLM-based citation verification is still planned.

## License

No license has been selected yet. Add one before making the repository public.
