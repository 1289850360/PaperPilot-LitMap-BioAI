import type { FieldStatus, PaperFieldKey, PaperSummary, VerificationStatus } from "./types";

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

type ExportLabels = {
  fields: Record<PaperFieldKey, string>;
  statusLabels: Record<FieldStatus, string>;
  verificationLabels: Record<VerificationStatus, string>;
  uncategorized: string;
};

export function downloadTextFile(filename: string, content: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

export function buildPaperMarkdown(paper: PaperSummary, labels: ExportLabels) {
  const lines: string[] = [
    `# ${paper.title}`,
    "",
    `- Paper ID: ${paper.id}`,
    `- Filename: ${paper.filename}`,
    `- Folder: ${displayFolder(paper.folder, labels.uncategorized)}`,
    `- Pages: ${paper.page_count}`,
    `- Created at: ${paper.created_at}`,
    "",
  ];

  if (paper.abstract) {
    lines.push("## Abstract", "", paper.abstract, "");
  }

  lines.push("## Structured Fields", "");
  for (const field of FIELD_KEYS) {
    const values = paper.card[field];
    const status = paper.card.field_statuses[field] ?? "ai_extracted";
    const verification = paper.card.verification_statuses?.[field] ?? "missing";
    const evidence = paper.card.evidence[field] ?? [];
    lines.push(`### ${labels.fields[field]}`, "", `Status: ${labels.statusLabels[status]}`, "");
    lines.push(`Citation check: ${labels.verificationLabels[verification]}`, "");
    if (values.length) {
      for (const value of values) {
        lines.push(`- ${value}`);
      }
    } else {
      lines.push("- Not found");
    }
    if (evidence.length) {
      lines.push("", "Evidence:");
      for (const item of evidence) {
        const pageRange =
          item.page_start === item.page_end ? `${item.page_start}` : `${item.page_start}-${item.page_end}`;
        lines.push(`- p. ${pageRange}, ${item.section}: ${item.text}`);
      }
    }
    lines.push("");
  }

  return lines.join("\n");
}

export function buildPapersCsv(papers: PaperSummary[], labels: ExportLabels) {
  const columns = [
    "paper_id",
    "title",
    "filename",
    "folder",
    "page_count",
    ...FIELD_KEYS,
    "field_statuses",
    "verification_statuses",
  ];
  const rows = papers.map((paper) => {
    const statuses = FIELD_KEYS.map((field) => {
      const status = paper.card.field_statuses[field] ?? "ai_extracted";
      return `${field}:${status}`;
    }).join("; ");
    const verificationStatuses = FIELD_KEYS.map((field) => {
      const status = paper.card.verification_statuses?.[field] ?? "missing";
      return `${field}:${status}`;
    }).join("; ");
    return [
      paper.id,
      paper.title,
      paper.filename,
      displayFolder(paper.folder, labels.uncategorized),
      paper.page_count,
      ...FIELD_KEYS.map((field) => paper.card[field].join(" | ")),
      statuses,
      verificationStatuses,
    ];
  });
  return "\uFEFF" + [columns, ...rows].map((row) => row.map(csvCell).join(",")).join("\n");
}

export function safeExportName(value: string) {
  const cleaned = value
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
  return cleaned || "paperpilot-export";
}

function csvCell(value: string | number) {
  const text = String(value);
  return `"${text.replace(/"/g, '""')}"`;
}

function displayFolder(folder: string, uncategorized: string) {
  return folder === "Uncategorized" ? uncategorized : folder;
}
