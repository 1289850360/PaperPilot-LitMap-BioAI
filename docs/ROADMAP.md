# Roadmap

PaperPilot / LitMap-BioAI is being developed in stages. The project should grow from a local MVP into a reproducible web demo and, later, a small research prototype suitable for a technical report, workshop submission, student conference demo, or graduate application portfolio.

## Project Goal

Build a citation-grounded literature mining system for biomedical AI and AI-for-science papers.

The system should support:

- structured paper reading
- information extraction
- citation-grounded question answering
- manual correction and annotation
- multi-paper comparison
- exportable reports
- evaluation against gold-standard annotations

## Stage 0: Local MVP Skeleton

Status: completed

Implemented:

- FastAPI backend
- Next.js frontend
- PyMuPDF PDF parsing
- SQLite persistence
- local PDF upload
- paper metadata storage
- section-aware text chunks
- heuristic structured extraction
- citation-grounded Q&A baseline
- Chinese and English UI

## Stage 1: Usable Paper Reading Demo

Status: mostly completed

Implemented:

- structured paper cards
- field-level evidence display
- PDF page preview with figures and page layout
- page navigation
- citation-to-page jumping
- field editing
- per-field annotation status
- heuristic citation verification status per field
- folder organization
- duplicate-paper warning
- delete paper action
- search across papers and fields
- Markdown export for one paper
- CSV export for all annotations
- multi-paper comparison table
- manual paper selection for comparison

Remaining polish:

- add loading states for PDF preview failures
- improve mobile layout
- add sample demo data
- add screenshot assets for GitHub README

## Stage 2: Reproducible GitHub Project

Status: mostly completed

Completed:

- improve README
- add quick-start script
- document environment variables
- add evaluation plan
- add related work notes
- add heuristic extraction experiment scripts
- add first 5-paper flow-matching seed set

Remaining tasks:

- add deployment notes
- add example paper workflow
- add screenshots or demo video
- select a license before making the repository public

## Stage 3: LLM Extraction Pipeline

Status: started

Completed:

- add direct LLM extraction baseline script
- add dry-run prompt inspection mode
- export direct LLM predictions in the same CSV shape as evaluation scripts
- add schema-aware local extraction v2 for task, dataset, method, and metric fields
- iterate schema-aware local extraction through v5 on the 5-paper pilot set
- add error-analysis reports for missed and unsupported values

Tasks:

- define a strict JSON schema for paper cards
- retrieve evidence per field
- require source citation for every extracted claim
- replace the MVP heuristic verifier with a stronger LLM verifier
- check whether evidence supports the field
- mark unsupported fields as unsupported, weak, or missing
- expose extraction confidence or verification explanations in the UI

Candidate pipeline:

1. Parse PDF into pages and sections.
2. Chunk text with section and page metadata.
3. Retrieve candidate evidence for each schema field.
4. Ask the LLM to extract field values from evidence only.
5. Verify each extracted value against citation text.
6. Store values, citations, and verification status.

## Stage 4: Vector Retrieval

Status: planned

Tasks:

- add embeddings
- compare Chroma and FAISS for local development
- store chunk embeddings
- support field-specific retrieval
- support question answering across a paper
- later support question answering across multiple papers

## Stage 5: Evaluation Benchmark

Status: planned

Tasks:

- collect 30-50 biomedical AI papers
- create gold annotations
- export and clean annotation CSV files
- implement scoring scripts
- compare direct LLM, ordinary RAG, and citation-verified extraction
- report field-level accuracy, citation correctness, hallucination rate, and missing rate

See `docs/EVALUATION_PLAN.md`.

## Stage 6: Research Map

Status: planned

Possible features:

- filter papers by dataset, method, metric, and task
- show method families such as diffusion, flow matching, graph neural networks, transformers, and docking models
- show dataset usage across papers
- show metric usage across papers
- build a lightweight visual map of paper relationships
- export a literature review summary

## Stage 7: Deployment

Status: planned

Possible deployment path:

- frontend: Vercel
- backend: Render, Railway, Fly.io, or a small VPS
- database: PostgreSQL
- file storage: local persistent volume for first demo, then object storage if needed
- public demo mode: read-only sample library plus optional upload route

Recommended public demo strategy:

1. Start with a read-only demo containing several preloaded papers.
2. Add upload only after storage, file limits, and abuse controls are clear.
3. Keep a local full version for development and evaluation.

## Stage 8: Demo Paper or Technical Report

Status: planned

Deliverables:

- hosted demo
- GitHub repository
- technical report
- evaluation report
- short demo video
- related work summary based on `docs/RELATED_WORK.md`

Possible report structure:

1. Motivation
2. Related work
3. System design
4. Extraction schema
5. Citation verification pipeline
6. User interface
7. Evaluation setup
8. Results
9. Error analysis
10. Limitations and future work
