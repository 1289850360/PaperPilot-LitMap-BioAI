"use client";

import { Check, Edit3, X } from "lucide-react";
import { useState } from "react";
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

const FIELD_STATUSES: FieldStatus[] = ["ai_extracted", "needs_review", "verified", "missing"];

type FieldLabels = Record<PaperFieldKey, string>;

export function PaperCard({
  paper,
  fieldLabels,
  emptyLabel,
  evidenceLabel,
  hideEvidenceLabel,
  citationLabel,
  openPageLabel,
  editLabel,
  cancelLabel,
  saveLabel,
  oneItemPerLineLabel,
  statusLabels,
  verificationLabels,
  onOpenPage,
  onSaveField,
}: {
  paper: PaperSummary;
  fieldLabels: FieldLabels;
  emptyLabel: string;
  evidenceLabel: string;
  hideEvidenceLabel: string;
  citationLabel: (section: string, pageStart: number, pageEnd: number) => string;
  openPageLabel: string;
  editLabel: string;
  cancelLabel: string;
  saveLabel: string;
  oneItemPerLineLabel: string;
  statusLabels: Record<FieldStatus, string>;
  verificationLabels: Record<VerificationStatus, string>;
  onOpenPage: (page: number) => void;
  onSaveField: (field: PaperFieldKey, values: string[], status: FieldStatus) => Promise<void>;
}) {
  const [openFields, setOpenFields] = useState<Partial<Record<PaperFieldKey, boolean>>>({});
  const [editingField, setEditingField] = useState<PaperFieldKey | null>(null);
  const [draftText, setDraftText] = useState("");
  const [draftStatus, setDraftStatus] = useState<FieldStatus>("ai_extracted");
  const [savingField, setSavingField] = useState<PaperFieldKey | null>(null);

  function startEditing(field: PaperFieldKey, values: string[], status: FieldStatus) {
    setEditingField(field);
    setDraftText(values.join("\n"));
    setDraftStatus(status);
  }

  async function saveField(field: PaperFieldKey) {
    const values = draftText
      .split("\n")
      .map((value) => value.trim())
      .filter(Boolean);
    setSavingField(field);
    try {
      await onSaveField(field, values, draftStatus);
      setEditingField(null);
    } finally {
      setSavingField(null);
    }
  }

  return (
    <article className="paper-card">
      <div className="paper-header">
        <div>
          <p className="file-name">{paper.filename}</p>
          <h2>{paper.title}</h2>
        </div>
        <span className="paper-id">#{paper.id}</span>
      </div>
      {paper.abstract ? <p className="abstract">{paper.abstract}</p> : null}
      <div className="field-grid">
        {FIELD_KEYS.map((key) => {
          const values = paper.card[key] as string[];
          const status = paper.card.field_statuses[key] ?? "ai_extracted";
          const verification = paper.card.verification_statuses?.[key] ?? "missing";
          const evidence = paper.card.evidence[key] ?? [];
          const isOpen = Boolean(openFields[key]);
          const isEditing = editingField === key;
          return (
            <section className="field" key={key}>
              <div className="field-title-row">
                <div>
                  <h3>{fieldLabels[key]}</h3>
                  <div className="field-badge-row">
                    <span className={`status-badge status-${status}`}>{statusLabels[status]}</span>
                    <span className={`verification-badge verification-${verification}`}>
                      {verificationLabels[verification]}
                    </span>
                  </div>
                </div>
                <div className="field-actions">
                  {evidence.length ? (
                    <button
                      className="evidence-toggle"
                      onClick={() => setOpenFields((fields) => ({ ...fields, [key]: !isOpen }))}
                      type="button"
                    >
                      {isOpen ? hideEvidenceLabel : evidenceLabel}
                    </button>
                  ) : null}
                  <button
                    className="icon-text-button"
                    onClick={() => startEditing(key, values, status)}
                    type="button"
                  >
                    <Edit3 size={14} />
                    <span>{editLabel}</span>
                  </button>
                </div>
              </div>

              {isEditing ? (
                <div className="field-editor">
                  <textarea
                    aria-label={fieldLabels[key]}
                    onChange={(event) => setDraftText(event.target.value)}
                    placeholder={oneItemPerLineLabel}
                    value={draftText}
                  />
                  <div className="field-editor-footer">
                    <select
                      onChange={(event) => setDraftStatus(event.target.value as FieldStatus)}
                      value={draftStatus}
                    >
                      {FIELD_STATUSES.map((item) => (
                        <option key={item} value={item}>
                          {statusLabels[item]}
                        </option>
                      ))}
                    </select>
                    <div className="field-editor-actions">
                      <button
                        className="ghost-button"
                        onClick={() => setEditingField(null)}
                        type="button"
                      >
                        <X size={15} />
                        <span>{cancelLabel}</span>
                      </button>
                      <button
                        className="save-field-button"
                        disabled={savingField === key}
                        onClick={() => saveField(key)}
                        type="button"
                      >
                        <Check size={15} />
                        <span>{saveLabel}</span>
                      </button>
                    </div>
                  </div>
                </div>
              ) : values.length ? (
                <ul>
                  {values.slice(0, 4).map((value) => (
                    <li key={value}>{value}</li>
                  ))}
                </ul>
              ) : (
                <p className="empty">{emptyLabel}</p>
              )}

              {isOpen ? (
                <div className="field-evidence-list">
                  {evidence.map((item, index) => (
                    <blockquote key={`${key}-${item.page_start}-${index}`}>
                      <button
                        className="citation-jump-button"
                        onClick={() => onOpenPage(item.page_start)}
                        title={openPageLabel}
                        type="button"
                      >
                        {citationLabel(item.section, item.page_start, item.page_end)}
                      </button>
                      <span>{item.text}</span>
                    </blockquote>
                  ))}
                </div>
              ) : null}
            </section>
          );
        })}
      </div>
    </article>
  );
}
