export type Evidence = {
  section: string;
  page_start: number;
  page_end: number;
  text: string;
};

export type PaperCard = {
  task: string[];
  datasets: string[];
  models_or_methods: string[];
  baselines: string[];
  metrics: string[];
  main_result: string[];
  limitations: string[];
  code_availability: string[];
  evidence: Record<string, Evidence[]>;
  field_statuses: Record<string, FieldStatus>;
  verification_statuses: Record<string, VerificationStatus>;
};

export type PaperFieldKey =
  | "task"
  | "datasets"
  | "models_or_methods"
  | "baselines"
  | "metrics"
  | "main_result"
  | "limitations"
  | "code_availability";

export type FieldStatus = "ai_extracted" | "needs_review" | "verified" | "missing";

export type VerificationStatus = "supported" | "weak" | "unsupported" | "missing";

export type PaperSummary = {
  id: number;
  title: string;
  filename: string;
  folder: string;
  page_count: number;
  abstract: string | null;
  card: PaperCard;
  created_at: string;
};

export type AskResponse = {
  answer: string;
  citations: Evidence[];
};
