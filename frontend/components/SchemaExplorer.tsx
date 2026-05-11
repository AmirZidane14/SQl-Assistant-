"use client";

import { useState, useEffect } from "react";

interface ColumnInfo {
  name: string;
  type: string;
  nullable: boolean;
  primary_key: boolean;
  foreign_key: boolean;
  foreign_key_ref: string | null;
}

interface RelationshipInfo {
  source_table: string;
  source_column: string;
  target_table: string;
  target_column: string;
  description: string;
}

interface TableInfo {
  name: string;
  columns: ColumnInfo[];
  relationships: RelationshipInfo[];
}

interface SchemaResponse {
  tables: TableInfo[];
  total_tables: number;
  total_columns: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function SchemaExplorer() {
  const [tables, setTables] = useState<TableInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [expandedTables, setExpandedTables] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetchSchema();
  }, []);

  async function fetchSchema() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/schema`);
      if (!res.ok) throw new Error("Failed to fetch schema");
      const data: SchemaResponse = await res.json();
      setTables(data.tables);
    } catch {
      setError("Unable to connect to backend. Make sure the server is running.");
    } finally {
      setLoading(false);
    }
  }

  async function handleRefresh() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/schema/refresh`, { method: "POST" });
      if (!res.ok) throw new Error("Failed to refresh schema");
      await fetchSchema();
    } catch {
      setError("Failed to refresh schema cache.");
    } finally {
      setLoading(false);
    }
  }

  function toggleTable(name: string) {
    setExpandedTables((prev) => {
      const next = new Set(prev);
      if (next.has(name)) {
        next.delete(name);
      } else {
        next.add(name);
      }
      return next;
    });
  }

  const filteredTables = tables.filter((table) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    if (table.name.toLowerCase().includes(q)) return true;
    return table.columns.some((col) => col.name.toLowerCase().includes(q));
  });

  if (loading && tables.length === 0) {
    return (
      <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-8">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <svg className="mb-3 h-8 w-8 animate-spin text-indigo-500" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <p className="text-sm text-zinc-500">Loading schema...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-red-200 dark:border-red-800 bg-white dark:bg-zinc-950 p-8">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="mb-1 text-sm font-semibold text-red-600 dark:text-red-400">Connection Error</h3>
          <p className="text-xs text-zinc-400">{error}</p>
          <button onClick={fetchSchema} className="mt-4 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 overflow-hidden">
      <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 px-5 py-3">
        <div className="flex items-center gap-3">
          <span className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
            Database Schema
          </span>
          <span className="rounded-full bg-zinc-100 dark:bg-zinc-800 px-2 py-0.5 text-xs text-zinc-500">
            {tables.length} tables
          </span>
        </div>
        <button
          onClick={handleRefresh}
          disabled={loading}
          className="flex items-center gap-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-1.5 text-xs font-medium text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800 disabled:opacity-50 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh
        </button>
      </div>

      <div className="border-b border-zinc-200 dark:border-zinc-800 px-5 py-3">
        <div className="relative">
          <svg xmlns="http://www.w3.org/2000/svg" className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search tables or columns..."
            className="w-full rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900 py-2 pl-9 pr-4 text-sm text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          />
        </div>
      </div>

      <div className="max-h-[500px] overflow-y-auto">
        {filteredTables.length === 0 && !loading ? (
          <div className="flex flex-col items-center justify-center py-12 text-center px-5">
            <p className="text-sm text-zinc-500">No tables found matching &quot;{search}&quot;</p>
          </div>
        ) : (
          <div className="p-3 space-y-1">
            {filteredTables.map((table) => {
              const isExpanded = expandedTables.has(table.name);
              const fkColumns = table.columns.filter((c) => c.foreign_key);

              return (
                <div key={table.name} className="rounded-lg border border-zinc-100 dark:border-zinc-800 overflow-hidden">
                  <button
                    onClick={() => toggleTable(table.name)}
                    className="flex w-full items-center justify-between px-4 py-2.5 bg-zinc-50 dark:bg-zinc-900 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors text-left"
                  >
                    <div className="flex items-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                      </svg>
                      <span className="text-sm font-medium text-zinc-800 dark:text-zinc-200">{table.name}</span>
                      <span className="text-xs text-zinc-400">{table.columns.length} cols</span>
                    </div>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className={`h-4 w-4 text-zinc-400 transition-transform duration-200 ${isExpanded ? "rotate-180" : ""}`}
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {isExpanded && (
                    <div className="bg-white dark:bg-zinc-950 divide-y divide-zinc-100 dark:divide-zinc-800">
                      {table.columns.map((col) => (
                        <div key={col.name} className="flex items-center gap-3 px-4 py-2">
                          <span className="text-xs font-mono font-medium text-zinc-700 dark:text-zinc-300 w-36 shrink-0 truncate">{col.name}</span>
                          <span className="text-xs text-zinc-400 w-24 shrink-0">{col.type.replace("()", "")}</span>
                          <div className="flex items-center gap-1.5 shrink-0">
                            {col.primary_key && (
                              <span className="rounded-full bg-amber-100 dark:bg-amber-900/30 px-2 py-0.5 text-xs font-medium text-amber-700 dark:text-amber-400">PK</span>
                            )}
                            {col.foreign_key && (
                              <span className="rounded-full bg-blue-100 dark:bg-blue-900/30 px-2 py-0.5 text-xs font-medium text-blue-700 dark:text-blue-400">FK</span>
                            )}
                            {!col.nullable && !col.primary_key && (
                              <span className="rounded-full bg-zinc-100 dark:bg-zinc-800 px-2 py-0.5 text-xs text-zinc-500">NOT NULL</span>
                            )}
                          </div>
                          {col.foreign_key && col.foreign_key_ref && (
                            <span className="text-xs text-zinc-400 truncate">
                              <span className="text-blue-500 dark:text-blue-400">→</span> {col.foreign_key_ref}
                            </span>
                          )}
                        </div>
                      ))}

                      {fkColumns.length > 0 && (
                        <div className="px-4 py-2 bg-zinc-50 dark:bg-zinc-900">
                          <p className="text-xs font-medium text-zinc-500 mb-1">RELATIONSHIPS</p>
                          {fkColumns.map((col) => (
                            <p key={col.name} className="text-xs text-zinc-400">
                              <span className="font-mono text-indigo-600 dark:text-indigo-400">{table.name}.{col.name}</span>
                              {" → "}
                              <span className="text-zinc-600 dark:text-zinc-400">{col.foreign_key_ref}</span>
                            </p>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}