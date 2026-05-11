export interface BackendStatus {
  connected: boolean;
  lastChecked: Date;
  error?: string;
}

export interface QueryState {
  input: string;
  isExecuting: boolean;
  error: string | null;
}

export interface ResultsState {
  columns: string[];
  rows: Record<string, unknown>[];
  rowCount: number;
  isLoading: boolean;
}

export type NavItem = {
  label: string;
  icon: string;
  active?: boolean;
};