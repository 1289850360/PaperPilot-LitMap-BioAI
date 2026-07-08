# PaperPilot Evaluation

This folder contains the first minimal evaluation pipeline for PaperPilot / LitMap-BioAI.

The goal is to make the project measurable, not just usable. For a workshop-style project, the key claim should be tested with a small gold-standard dataset:

> Does citation-grounded structured extraction produce more reliable paper cards than simpler extraction baselines?

## Files

```text
evaluation/
  gold_template.csv        Gold annotation template
  score_extraction.py      Compare exported predictions against gold annotations
```

## Workflow

### 1. Export system predictions

In the PaperPilot web UI:

1. Upload and process several papers.
2. Click `Export CSV`.
3. Save the file as something like:

```text
evaluation/predictions.csv
```

The exported CSV is the system prediction file.

### 2. Create gold annotations

Copy the prediction file:

```powershell
Copy-Item evaluation\predictions.csv evaluation\gold.csv
```

Then manually correct `evaluation/gold.csv`.

For the first evaluation, focus on these four fields:

- `task`
- `datasets`
- `models_or_methods`
- `metrics`

Use ` | ` to separate multiple values in one cell.

Example:

```text
PDBBind | CrossDocked | CASF-2016
```

Leave a cell empty if the paper does not contain that field.

### 3. Score predictions

Run:

```powershell
python evaluation\score_extraction.py --pred evaluation\predictions.csv --gold evaluation\gold.csv
```

The script prints:

- field-level accuracy
- missing rate
- hallucination rate
- value-level precision
- value-level recall
- value-level F1
- predicted citation verification counts
- per-field scores

It also writes:

```text
evaluation/results/score_summary.json
evaluation/results/per_field_scores.csv
```

### 4. Compare baseline runs

After you have more than one scored run, create a comparison table:

```powershell
python evaluation\compare_results.py --runs heuristic=evaluation\results\score_summary.json direct_llm=evaluation\results_direct_llm\score_summary.json --out evaluation\baseline_comparison.md
```

This is useful for the workshop report because it turns multiple experiment outputs into one readable result table.

### 5. Generate error analysis

For each paper and field, list values that were missed or unsupported:

```powershell
python evaluation\error_analysis.py --pred experiments\outputs\schema_heuristic_v2\heuristic_predictions.csv --gold evaluation\gold.csv --fields task datasets models_or_methods metrics --out evaluation\error_analysis_schema_heuristic_v2.md
```

Use this file to decide whether the next improvement should target missing values, over-extraction, or schema normalization.

## Recommended First Experiment

Start small:

- 10 papers
- 4 fields: task, datasets, models_or_methods, metrics
- compare the current heuristic extractor against your manually corrected gold file

Then expand:

- 30-50 papers
- all 8 fields
- compare direct LLM, ordinary RAG, and citation-verified extraction

## Interpreting Scores

This script uses approximate text matching:

- exact or high-similarity match: `1.0`
- partial match: `0.5`
- no match: `0.0`

This is enough for the first workshop prototype. Later, you can add human labels for citation correctness and stricter field-level adjudication.

If the prediction CSV includes `verification_statuses`, the script also counts how many extracted fields are marked as `supported`, `weak`, `unsupported`, or `missing`.

Field-level accuracy answers:

```text
Did the system find at least one relevant value for this field?
```

Value-level precision, recall, and F1 answer:

```text
How many individual extracted values match the gold values?
```

The value-level metrics are stricter and better reflect over-extraction.
