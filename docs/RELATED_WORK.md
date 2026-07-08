# Related Work and Design Inspiration

This document collects tools and papers that can inform the design and workshop positioning of PaperPilot / LitMap-BioAI.

The goal is not to copy existing systems. The goal is to understand the landscape and make PaperPilot's contribution sharper:

> PaperPilot focuses on citation-grounded, schema-constrained extraction and comparison of biomedical AI papers, with an explicit evaluation pipeline for field accuracy, citation correctness, hallucination rate, and missing rate.

## 1. Scholarly PDF Parsing

### GROBID

GROBID is a mature machine learning system for extracting and restructuring scholarly PDFs into TEI XML. It supports metadata extraction, references, citation contexts, full-text structure, figures, tables, and PDF coordinates.

Useful ideas for PaperPilot:

- switch from plain text-only parsing to richer document structure later
- preserve section labels and page coordinates
- extract references and citation contexts
- treat PDF parsing as an evaluable subsystem

Reference:

- GROBID Documentation: <https://grobid.readthedocs.io/en/latest/Introduction/>

### PDF Information Extraction Benchmarks

Recent PDF extraction benchmarks show that academic PDF parsing is still difficult, especially for tables, equations, lists, footers, and document layout. This supports a careful design choice: PaperPilot should not pretend PDF parsing is solved.

Useful ideas for PaperPilot:

- report PDF parsing limitations honestly
- keep the original PDF preview in the UI so users can verify extracted text
- later compare PyMuPDF-only parsing against GROBID or another parser

Reference:

- Meuschke et al., "A Benchmark of PDF Information Extraction Tools using a Multi-Task and Multi-Domain Evaluation Framework for Academic Documents": <https://arxiv.org/abs/2303.09957>

## 2. Scientific RAG and Citation-Grounded QA

### PaperQA

PaperQA frames scientific literature QA as a retrieval-augmented agent problem. It retrieves from full-text scientific articles, assesses source relevance, and produces answers grounded in literature.

Useful ideas for PaperPilot:

- use RAG as one baseline
- evaluate against gold answers rather than relying on subjective impressions
- require source passages for scientific answers
- build a harder benchmark than generic QA by requiring full-paper retrieval and synthesis

Reference:

- Lala et al., "PaperQA: Retrieval-Augmented Generative Agent for Scientific Research": <https://arxiv.org/abs/2312.07559>

### SQuAI

SQuAI is a scientific QA system that uses multi-agent RAG, hybrid retrieval, inline citations, and supporting sentences.

Useful ideas for PaperPilot:

- separate complex questions into sub-questions later
- use hybrid sparse-dense retrieval
- provide supporting sentences, not just citation labels
- evaluate faithfulness and contextual relevance

Reference:

- Besrour et al., "SQuAI: Scientific Question-Answering with Multi-Agent Retrieval-Augmented Generation": <https://arxiv.org/abs/2510.15682>

### BioRAGent

BioRAGent is an interactive biomedical RAG system for scientific Q&A. It emphasizes transparency through citation links and generated query expansion.

Useful ideas for PaperPilot:

- make retrieval behavior visible to users
- expose source links or evidence snippets for each answer
- support biomedical-specific search and terminology expansion later

Reference:

- Ateia and Kruschwitz, "BioRAGent: A Retrieval-Augmented Generation System for Showcasing Generative Query Expansion and Domain-Specific Search for Scientific Q&A": <https://arxiv.org/abs/2412.12358>

## 3. Literature Review and Research Assistant Tools

### Elicit

Elicit is a research assistant for literature search, systematic review, screening, and data extraction. Its product direction is important because it shows that researchers want traceable and auditable literature review workflows, not only chat interfaces.

Useful ideas for PaperPilot:

- make extraction tables first-class UI objects
- support systematic review style workflows
- make every extraction auditable
- report extraction accuracy and screening performance

Reference:

- Elicit official website: <https://elicit.com/>

### Scholarcy

Scholarcy summarizes papers into structured flashcards and helps readers organize summaries, key findings, references, figures, and tables.

Useful ideas for PaperPilot:

- paper cards are a strong interaction pattern
- consistent summaries help compare many papers
- export matters because researchers work across tools
- figure/table awareness improves scientific reading

Reference:

- Scholarcy official website: <https://www.scholarcy.com/>

### Semantic Reader and Scim

Semantic Reader and Scim explore augmented scientific reading, such as skimming highlights and citation-aware reading aids.

Useful ideas for PaperPilot:

- help users skim, not just chat
- highlight diverse paper regions, not only the abstract
- make citations and evidence visible inside the reading workflow
- add user-adjustable density or filters later

References:

- Fok et al., "Scim: Intelligent Skimming Support for Scientific Papers": <https://arxiv.org/abs/2205.04561>
- Semantic Scholar Open Data Platform: <https://arxiv.org/abs/2301.10140>

## 4. Structured Scholarly Knowledge and Multi-Paper Comparison

### Open Research Knowledge Graph

The Open Research Knowledge Graph (ORKG) represents scholarly contributions as structured, machine-actionable knowledge. It also supports comparison of research contributions.

Useful ideas for PaperPilot:

- structure papers as comparable research contributions
- use fields like problem, materials, methods, and results
- support multi-paper comparison as a core feature
- think beyond one-paper PDF reading toward reusable scholarly knowledge

References:

- Jaradeh et al., "Open Research Knowledge Graph: Next Generation Infrastructure for Semantic Scholarly Knowledge": <https://arxiv.org/abs/1901.10816>
- Oelen et al., "Generate FAIR Literature Surveys with Scholarly Knowledge Graphs": <https://arxiv.org/abs/2006.01747>

### S2ORC and Semantic Scholar Open Data

S2ORC and the Semantic Scholar Open Data Platform show how large-scale scholarly corpora can expose metadata, structured full text, citations, figures, tables, summaries, and embeddings.

Useful ideas for PaperPilot:

- use scholarly metadata and citation graphs later
- enrich local PDFs with external metadata
- connect papers through citations, datasets, methods, and metrics
- design exports that could later become a small domain-specific corpus

References:

- Lo et al., "S2ORC: The Semantic Scholar Open Research Corpus": <https://arxiv.org/abs/1911.02782>
- Kinney et al., "The Semantic Scholar Open Data Platform": <https://arxiv.org/abs/2301.10140>

## 5. What PaperPilot Should Borrow

### From GROBID

Borrow:

- structured parsing mindset
- section, citation, figure, table, and coordinate awareness

Do not copy:

- trying to build a full PDF parser from scratch

PaperPilot implication:

- PyMuPDF is fine for the MVP, but GROBID can become an optional parser backend later.

### From PaperQA and SQuAI

Borrow:

- RAG baselines
- citation-grounded answers
- evaluation against scientific QA tasks

Do not copy:

- only solving open-ended QA

PaperPilot implication:

- the distinctive angle should be structured extraction plus citation verification, not just question answering.

### From Elicit

Borrow:

- extraction table workflow
- systematic-review mindset
- traceable and auditable evidence

Do not copy:

- becoming a broad commercial literature review platform

PaperPilot implication:

- focus on biomedical AI papers and the fields that matter for method comparison.

### From ORKG

Borrow:

- machine-actionable paper contributions
- multi-paper comparison
- FAIR literature survey framing

Do not copy:

- full semantic web infrastructure at the MVP stage

PaperPilot implication:

- a CSV/JSON structured card is enough for the first research prototype.

## 6. PaperPilot's Differentiation

PaperPilot can be positioned as:

1. More structured than PDF chat tools.
2. More evidence-focused than simple paper summarizers.
3. More domain-specific than general research assistants.
4. More evaluation-oriented than many lightweight literature mining demos.
5. More practical for biomedical AI comparison than pure citation graph tools.

Recommended workshop contribution:

> We present PaperPilot, a citation-grounded literature mining prototype for biomedical AI papers. The system converts PDFs into structured, editable paper cards, links extracted fields to source evidence, supports multi-paper comparison, and includes a benchmark workflow for evaluating field-level accuracy, citation correctness, hallucination rate, and missing rate.

## 7. Suggested Next Features Inspired by Related Work

High priority:

- citation verification status per extracted field
- direct LLM vs RAG vs citation-verified extraction baselines
- evidence-aware evaluation report
- dataset/method/metric filters in the comparison table

Medium priority:

- optional GROBID parser backend
- vector retrieval with hybrid sparse-dense search
- research map by dataset, method, metric, and citation relation
- sample library for a public read-only demo

Later:

- external metadata enrichment from Semantic Scholar or OpenAlex
- contribution graph export
- PRISMA-style screening workflow
- domain-specific extraction templates for drug discovery, medical imaging, and protein design
