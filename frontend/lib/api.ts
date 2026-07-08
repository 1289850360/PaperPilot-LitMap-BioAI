import type { AskResponse, FieldStatus, PaperFieldKey, PaperSummary } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type DuplicateCandidate = {
  id: number;
  title: string;
  filename: string;
};

export class DuplicatePaperError extends Error {
  duplicates: DuplicateCandidate[];

  constructor(message: string, duplicates: DuplicateCandidate[]) {
    super(message);
    this.name = "DuplicatePaperError";
    this.duplicates = duplicates;
  }
}

export async function fetchPapers(): Promise<PaperSummary[]> {
  const response = await fetch(`${API_URL}/papers`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to fetch papers");
  }
  return response.json();
}

export function getPaperFileUrl(paperId: number, page = 1): string {
  return `${API_URL}/papers/${paperId}/file#page=${page}`;
}

export function getPaperPageImageUrl(paperId: number, page = 1): string {
  return `${API_URL}/papers/${paperId}/page/${page}`;
}

export async function uploadPaper(file: File, force = false): Promise<PaperSummary> {
  const form = new FormData();
  form.append("file", file);
  form.append("force", String(force));
  const response = await fetch(`${API_URL}/papers/upload`, {
    method: "POST",
    body: form,
  });
  if (!response.ok) {
    const contentType = response.headers.get("content-type") ?? "";
    if (response.status === 409 && contentType.includes("application/json")) {
      const payload = await response.json();
      if (payload.detail?.code === "duplicate_paper") {
        throw new DuplicatePaperError(
          payload.detail.message ?? "Duplicate paper",
          payload.detail.duplicates ?? [],
        );
      }
    }
    const message = await response.text();
    throw new Error(message || "Upload failed");
  }
  return response.json();
}

export async function updatePaperFolder(paperId: number, folder: string): Promise<PaperSummary> {
  const response = await fetch(`${API_URL}/papers/${paperId}/folder`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ folder }),
  });
  if (!response.ok) {
    throw new Error("Folder update failed");
  }
  return response.json();
}

export async function updatePaperCardField(
  paperId: number,
  field: PaperFieldKey,
  values: string[],
  status: FieldStatus,
): Promise<PaperSummary> {
  const response = await fetch(`${API_URL}/papers/${paperId}/card-field`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ field, values, status }),
  });
  if (!response.ok) {
    throw new Error("Field update failed");
  }
  return response.json();
}

export async function reextractPaper(paperId: number): Promise<PaperSummary> {
  const response = await fetch(`${API_URL}/papers/${paperId}/reextract`, {
    method: "POST",
  });
  if (!response.ok) {
    throw new Error("Re-extraction failed");
  }
  return response.json();
}

export async function deletePaper(paperId: number): Promise<void> {
  const response = await fetch(`${API_URL}/papers/${paperId}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error("Delete failed");
  }
}

export async function askPaper(paperId: number, question: string): Promise<AskResponse> {
  const response = await fetch(`${API_URL}/papers/${paperId}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!response.ok) {
    throw new Error("Question failed");
  }
  return response.json();
}
