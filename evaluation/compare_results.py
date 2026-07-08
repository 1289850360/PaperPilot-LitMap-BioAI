"""Compare multiple PaperPilot score_summary.json files.

Example:
    python evaluation/compare_results.py --runs heuristic=evaluation/results/score_summary.json direct_llm=evaluation/results_direct_llm/score_summary.json --out evaluation/baseline_comparison.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


METRICS = [
    ("field_level_accuracy", "Field accuracy"),
    ("value_precision", "Value precision"),
    ("value_recall", "Value recall"),
    ("value_f1", "Value F1"),
    ("missing_rate", "Missing rate"),
    ("hallucination_rate", "Hallucination rate"),
]


def main() -> None:
    args = parse_args()
    runs = [load_run(spec) for spec in args.runs]
    markdown = build_markdown(runs)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markdown, encoding="utf-8")
    print(f"Wrote {args.out}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare PaperPilot evaluation summaries.")
    parser.add_argument(
        "--runs",
        nargs="+",
        required=True,
        help="Named score summaries, e.g. heuristic=evaluation/results/score_summary.json",
    )
    parser.add_argument("--out", type=Path, default=Path("evaluation/baseline_comparison.md"))
    return parser.parse_args()


def load_run(spec: str) -> dict[str, Any]:
    if "=" not in spec:
        raise ValueError(f"Run must be formatted as name=path: {spec}")
    name, raw_path = spec.split("=", 1)
    path = Path(raw_path)
    if not path.exists():
        raise FileNotFoundError(f"Score summary not found for {name}: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {"name": name, "path": str(path), "summary": payload}


def build_markdown(runs: list[dict[str, Any]]) -> str:
    lines = [
        "# Baseline Comparison",
        "",
        "| Run | Papers | Fields | Field accuracy | Value precision | Value recall | Value F1 | Missing rate | Hallucination rate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for run in runs:
        summary = run["summary"]
        lines.append(
            "| {name} | {papers} | {fields} | {field_accuracy} | {precision} | {recall} | {f1} | {missing} | {hallucination} |".format(
                name=run["name"],
                papers=summary.get("paper_count", 0),
                fields=summary.get("compared_field_count", 0),
                field_accuracy=percent(summary.get("field_level_accuracy", 0)),
                precision=percent(summary.get("value_precision", 0)),
                recall=percent(summary.get("value_recall", 0)),
                f1=percent(summary.get("value_f1", 0)),
                missing=percent(summary.get("missing_rate", 0)),
                hallucination=percent(summary.get("hallucination_rate", 0)),
            )
        )

    lines.extend(["", "## Source Files", ""])
    for run in runs:
        lines.append(f"- {run['name']}: `{run['path']}`")
    lines.append("")

    lines.extend(["## Notes", ""])
    lines.append("- Higher field accuracy, value precision, value recall, and value F1 are better.")
    lines.append("- Lower missing rate and hallucination rate are better.")
    lines.append("- Direct LLM citation status is expected to be `unknown` unless a verifier is added.")
    lines.append("")
    return "\n".join(lines)


def percent(value: Any) -> str:
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return "n/a"


if __name__ == "__main__":
    main()
