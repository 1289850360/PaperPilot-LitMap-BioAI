# Evaluation Plan

This document describes the planned evaluation for PaperPilot / LitMap-BioAI.

The goal is to test whether a schema-constrained, citation-verified literature mining pipeline can extract more reliable structured information from biomedical AI papers than direct LLM prompting or ordinary RAG.

## Research Question

Can citation-verified schema extraction reduce hallucinations and improve field-level reliability when mining biomedical AI and AI-for-science papers?

## Paper Set

Target size:

- 30-50 papers for the first evaluation

Target domains:

- biomedical AI
- AI for drug discovery
- computational biology
- protein design and structure prediction
- molecular docking
- medical imaging AI
- AI for science methods that report datasets, baselines, and evaluation metrics

Selection criteria:

- PDF is available
- paper has an identifiable task or research problem
- paper reports at least one dataset, benchmark, or evaluation metric
- paper contains enough method and result detail to support structured extraction

## Gold Standard Annotation

Each paper should be manually annotated with the following fields:

- task
- datasets
- models or methods
- baselines
- evaluation metrics
- main result
- limitations
- code availability

Each field should include:

- normalized answer text
- supporting citation text
- page number
- section name when available
- field status: present, missing, ambiguous, or not applicable

## Compared Methods

### Method A: Direct LLM Extraction

Input:

- full paper text or truncated paper text

Output:

- structured JSON fields

Expected weakness:

- may hallucinate fields
- may miss page-level evidence
- may overgeneralize from abstracts

### Method B: Ordinary RAG Extraction

Input:

- retrieved chunks per field

Output:

- structured JSON fields

Expected weakness:

- retrieval may miss the right evidence
- generated answers may not be strictly supported by retrieved text

### Method C: Schema-Constrained + Citation Verification

Input:

- section-aware chunks
- field-specific retrieval
- schema-constrained extraction
- citation verification step

Output:

- structured JSON fields
- evidence citations
- verification status per field

Expected advantage:

- fewer unsupported claims
- better missing-field detection
- more useful output for multi-paper comparison

## Metrics

### Field-Level Accuracy

Measures whether the extracted value matches the gold annotation.

Suggested scoring:

- 1.0: correct
- 0.5: partially correct
- 0.0: incorrect or unsupported

Report macro average across fields and papers.

### Citation Correctness

Measures whether the cited source text actually supports the extracted field.

Suggested labels:

- correct citation
- weak citation
- wrong citation
- no citation

### Hallucination Rate

Measures fields that are extracted but unsupported by the paper.

Formula:

```text
hallucination_rate = unsupported_extracted_fields / extracted_fields
```

### Missing Rate

Measures fields that exist in the gold annotation but are not extracted.

Formula:

```text
missing_rate = missed_gold_fields / gold_present_fields
```

### Evidence Coverage

Measures how often an extracted field includes usable evidence.

Formula:

```text
evidence_coverage = fields_with_valid_citations / extracted_fields
```

## Annotation Workflow

1. Collect PDFs and metadata.
2. Upload each paper into PaperPilot.
3. Export all annotations as CSV.
4. Manually correct the CSV into a gold-standard version.
5. Run each extraction method on the same paper set.
6. Compare method outputs against the gold set.
7. Summarize quantitative results and representative error cases.

## Error Analysis Categories

Track common failure modes:

- abstract-only extraction
- dataset confused with baseline
- metric extracted without result value
- method name missed because it appears only in figures or captions
- code availability hallucinated from related work or references
- citation points to a nearby but non-supporting sentence
- limitation extracted from generic discussion rather than actual limitation
- multiple datasets merged into one field

## Suggested Tables for the Final Report

### Dataset Summary

Columns:

- domain
- number of papers
- publication years
- average pages
- average chunks per paper

### Main Results

Columns:

- method
- field-level accuracy
- citation correctness
- hallucination rate
- missing rate
- evidence coverage

### Per-Field Results

Columns:

- field
- direct LLM accuracy
- RAG accuracy
- citation-verified accuracy
- most common error type

## Minimum Viable Evaluation

If time is limited, start with:

- 10 papers
- 4 fields: task, dataset, method, metrics
- 3 metrics: field-level accuracy, citation correctness, hallucination rate

Then expand to the full 30-50 paper benchmark.

## Demo Paper Angle

Possible framing:

> PaperPilot is a citation-grounded literature mining demo that converts biomedical AI papers into structured, verifiable paper cards and supports multi-paper comparison. The system is evaluated against direct LLM extraction and ordinary RAG using field-level accuracy, citation correctness, hallucination rate, and missing rate.
