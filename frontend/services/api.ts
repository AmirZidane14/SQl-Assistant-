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

export interface GenerateSQLResponse {
  success: boolean;
  user_prompt: string;
  generated_sql: string;
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

export async function generateSQL(prompt: string): Promise<GenerateSQLResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/ai/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      return {
        success: false,
        user_prompt: prompt,
        generated_sql: "",
        error: "Unable to connect to backend",
      };
    }

    const data: GenerateSQLResponse = await response.json();
    return data;
  } catch {
    return {
      success: false,
      user_prompt: prompt,
      generated_sql: "",
      error: "Unable to connect to backend",
    };
  }
}