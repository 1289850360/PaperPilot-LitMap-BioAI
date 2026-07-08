"use client";

import { Search } from "lucide-react";
import { useMemo, useState } from "react";
import type { FieldStatus, PaperFieldKey, PaperSummary, VerificationStatus } from "../lib/types";

const FIELD_KEYS: PaperFieldKey[] = [
  "task",
  "datasets",
  "models_or_methods",
  "baselines",
  "metrics",
  "main_result",
  "limitations",
  "code_availability",
];

const CHIP_FIELDS = new Set<PaperFieldKey>(["datasets", "models_or_methods", "metrics"]);

export function CompareTable({
  papers,
  fieldLabels,
  statusLabels,
  verificationLabels,
  emptyLabel,
  searchPlaceholder,
  titleLabel,
  hintLabel,
  openLabel,
  noResultsLabel,
  titleHeader,
  folderHeader,
  statusHeader,
  uncategorizedLabel,
  onOpenPaper,
}: {
  papers: PaperSummary[];
  fieldLabels: Record<PaperFieldKey, string>;
  statusLabels: Record<FieldStatus, string>;
  verificationLabels: Record<VerificationStatus, string>;
  emptyLabel: string;
  searchPlaceholder: string;
  titleLabel: string;
  hintLabel: string;
  openLabel: string;
  noResultsLabel: string;
  titleHeader: string;
  folderHeader: string;
  statusHeader: string;
  uncategorizedLabel: string;
  onOpenPaper: (paperId: number) => void;
}) {
  const [query, setQuery] = useState("");

  const filteredPapers = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) return papers;
    return papers.filter((paper) => compareSearchText(paper).includes(normalized));
  }, [papers, query]);

  return (
    <section className="compare-panel">
      <div className="compare-header">
        <div>
          <h2>{titleLabel}</h2>
          <p>{hintLabel}</p>
        </div>
        <div className="compare-search">
          <Search size={16} />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder={searchPlaceholder}
          />
        </div>
      </div>

      <div className="compare-table-wrap">
        <table className="compare-table">
          <thead>
            <tr>
              <th>{titleHeader}</th>
              <th>{folderHeader}</th>
              {FIELD_KEYS.map((field) => (
                <th key={field}>{fieldLabels[field]}</th>
              ))}
              <th>{statusHeader}</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {filteredPapers.map((paper) => (
              <tr key={paper.id}>
                <td className="compare-title-cell">
                  <strong>{paper.title}</strong>
                  <span>{paper.filename}</span>
                </td>
                <td>{paper.folder === "Uncategorized" ? uncategorizedLabel : paper.folder}</td>
                {FIELD_KEYS.map((field) => (
                  <td key={`${paper.id}-${field}`}>
                    <FieldCell
                      compact={CHIP_FIELDS.has(field)}
                      values={paper.card[field]}
                      emptyLabel={emptyLabel}
                    />
                  </td>
                ))}
                <td>
                  <StatusSummary
                    paper={paper}
                    statusLabels={statusLabels}
                    verificationLabels={verificationLabels}
                  />
                </td>
                <td>
                  <button
                    className="compare-open-button"
                    onClick={() => onOpenPaper(paper.id)}
                    type="button"
                  >
                    {openLabel}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!filteredPapers.length ? <p className="compare-empty">{noResultsLabel}</p> : null}
      </div>
    </section>
  );
}

function FieldCell({
  values,
  emptyLabel,
  compact,
}: {
  values: string[];
  emptyLabel: string;
  compact: boolean;
}) {
  if (!values.length) {
    return <span className="compare-muted">{emptyLabel}</span>;
  }
  if (!compact) {
    return (
      <div className="compare-text-list">
        {values.slice(0, 2).map((value) => (
          <p key={value}>{value}</p>
        ))}
        {values.length > 2 ? <span className="compare-muted">+{values.length - 2}</span> : null}
      </div>
    );
  }
  return (
    <div className="compare-chip-list">
      {values.slice(0, 3).map((value) => (
        <span className="compare-chip" key={value}>
          {value}
        </span>
      ))}
      {values.length > 3 ? <span className="compare-muted">+{values.length - 3}</span> : null}
    </div>
  );
}

function StatusSummary({
  paper,
  statusLabels,
  verificationLabels,
}: {
  paper: PaperSummary;
  statusLabels: Record<FieldStatus, string>;
  verificationLabels: Record<VerificationStatus, string>;
}) {
  const counts = new Map<FieldStatus, number>();
  const verificationCounts = new Map<VerificationStatus, number>();
  for (const field of FIELD_KEYS) {
    const status = paper.card.field_statuses[field] ?? "ai_extracted";
    const verification = paper.card.verification_statuses?.[field] ?? "missing";
    counts.set(status, (counts.get(status) ?? 0) + 1);
    verificationCounts.set(verification, (verificationCounts.get(verification) ?? 0) + 1);
  }
  return (
    <div className="compare-status-list">
      {Array.from(counts.entries()).map(([status, count]) => (
        <span className={`status-badge status-${status}`} key={status}>
          {statusLabels[status]} {count}
        </span>
      ))}
      {Array.from(verificationCounts.entries()).map(([status, count]) => (
        <span className={`verification-badge verification-${status}`} key={status}>
          {verificationLabels[status]} {count}
        </span>
      ))}
    </div>
  );
}

function compareSearchText(paper: PaperSummary) {
  return [
    paper.title,
    paper.filename,
    paper.folder,
    paper.abstract ?? "",
    ...FIELD_KEYS.flatMap((field) => paper.card[field]),
  ]
    .join(" ")
    .toLowerCase();
}
