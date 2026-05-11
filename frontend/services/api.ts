const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface HealthResponse {
  status: string;
}

interface TablesResponse {
  tables: string[];
  count: number;
}

export interface ExecuteQueryResponse {
  valid: boolean;
  success: boolean;
  columns: string[];
  rows: unknown[][];
  count: number;
  error: string | null;
}

export async function checkBackendHealth(): Promise<HealthResponse | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
    });

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch {
    return null;
  }
}

export async function getTables(): Promise<string[] | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/tables`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
    });

    if (!response.ok) {
      return null;
    }

    const data: TablesResponse = await response.json();
    return data.tables;
  } catch {
    return null;
  }
}

export async function executeQuery(sql: string): Promise<ExecuteQueryResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: sql }),
    });

    if (!response.ok) {
      return {
        valid: false,
        success: false,
        columns: [],
        rows: [],
        count: 0,
        error: "Unable to connect to backend",
      };
    }

    const data: ExecuteQueryResponse = await response.json();
    return data;
  } catch {
    return {
      valid: false,
      success: false,
      columns: [],
      rows: [],
      count: 0,
      error: "Unable to connect to backend",
    };
  }
}