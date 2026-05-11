export interface BackendStatus {
  connected: boolean;
  lastChecked: Date;
  error?: string;
}

export type ExecutionStatus = "idle" | "loading" | "success" | "error";

export interface QueryState {
  input: string;
  status: ExecutionStatus;
  error: string | null;
}

export interface QueryResult {
  valid: boolean;
  success: boolean;
  columns: string[];
  rows: unknown[][];
  count: number;
  error: string | null;
}

export interface ResultsState {
  columns: string[];
  rows: unknown[][];
  rowCount: number;
  isLoading: boolean;
  error: string | null;
}

export type NavItem = {
  label: string;
  icon: string;
  active?: boolean;
};