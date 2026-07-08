# PaperPilot Experiments

This folder contains reproducible experiment scripts for PaperPilot / LitMap-BioAI.

The web app is useful for interactive reading and annotation. The experiment scripts are useful for workshop-style evaluation because they let you run the same extraction pipeline on a fixed set of PDFs and save machine-readable outputs.

## Current Pipeline

The first experiment pipeline is:

```text
PDF -> PyMuPDF parser -> heuristic schema extractor -> heuristic citation verifier -> JSON/CSV output
```

This is the baseline that later methods should be compared against:

- direct LLM extraction
- ordinary RAG extraction
- schema-constrained LLM extraction with citation verification

## Single Paper Extraction

Run:

```powershell
python experiments\run_heuristic_extraction.py --pdf path\to\paper.pdf --out experiments\outputs\paper.json
```

The output JSON includes:

- title
- filename
- abstract
- page count
- structured card fields
- evidence snippets
- citation verification statuses

## Batch Extraction

Create a CSV file like:

```csv
pdf_path,paper_id,notes
C:\path\to\paper1.pdf,paper_001,ForceFM
C:\path\to\paper2.pdf,paper_002,NeuralPLexer3
```

Then run:

```powershell
python experiments\batch_extract.py --manifest experiments\sample_papers.csv --out-dir experiments\outputs
```

This writes one JSON file per paper and one combined CSV:

```text
experiments/outputs/heuristic_predictions.csv
```

You can then copy that CSV into the evaluation folder and manually correct a gold file:

```powershell
Copy-Item experiments\outputs\heuristic_predictions.csv evaluation\predictions.csv
Copy-Item evaluation\predictions.csv evaluation\gold.csv
python evaluation\score_extraction.py --pred evaluation\predictions.csv --gold evaluation\gold.csv
```

## Direct LLM Baseline

The direct LLM baseline sends paper text directly to an LLM and asks for the same structured fields. It does not do retrieval or citation verification, so it is a useful comparison point for the citation-grounded pipeline.

First, test the prompt generation without spending API credits:

```powershell
python experiments\run_direct_llm_extraction.py --manifest experiments\uploaded_papers_manifest.csv --out-dir experiments\outputs\direct_llm --dry-run
```

This writes prompt files and an empty prediction CSV so you can inspect what would be sent to the model.

To run the real baseline, add your API key to `.env`:

```powershell
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

Then run:

```powershell
python experiments\run_direct_llm_extraction.py --manifest experiments\uploaded_papers_manifest.csv --out-dir experiments\outputs\direct_llm
```

The output CSV will be:

```text
experiments/outputs/direct_llm/direct_llm_predictions.csv
```

Score it against the current gold file:

```powershell
python evaluation\score_extraction.py --pred experiments\outputs\direct_llm\direct_llm_predictions.csv --gold evaluation\gold.csv --fields task datasets models_or_methods metrics --out-dir evaluation\results_direct_llm
```

Then compare the heuristic and direct LLM runs:

```powershell
python evaluation\compare_results.py --runs heuristic=evaluation\results\score_summary.json direct_llm=evaluation\results_direct_llm\score_summary.json --out evaluation\baseline_comparison.md
```

## Why This Matters

For a workshop paper, the important claim is not only that PaperPilot has a nice interface. The important claim is that the extraction pipeline can be evaluated and compared.

This folder is the bridge from product demo to research prototype.
