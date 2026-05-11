"use client";

import { useState, KeyboardEvent } from "react";
import { executeQuery } from "@/services/api";
import { ExecutionStatus } from "@/types/query";

interface QueryEditorProps {
  query: string;
  onQueryChange: (query: string) => void;
  onResults: (columns: string[], rows: unknown[][], count: number) => void;
  onError: (error: string) => void;
  onStatusChange: (status: ExecutionStatus) => void;
}

export default function QueryEditor({
  query,
  onQueryChange,
  onResults,
  onError,
  onStatusChange,
}: QueryEditorProps) {
  const [isLoading, setIsLoading] = useState(false);

  async function handleExecute() {
    if (!query.trim()) return;

    setIsLoading(true);
    onStatusChange("loading");
    onError("");

    const result = await executeQuery(query);

    setIsLoading(false);

    if (!result.valid || !result.success) {
      onStatusChange("error");
      onError(result.error || "Query validation failed");
    } else {
      onStatusChange("success");
      onResults(result.columns, result.rows, result.count);
    }
  }

  function handleClear() {
    onQueryChange("");
    onStatusChange("idle");
    onError("");
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      handleExecute();
    }
  }

  return (
    <section className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-6">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
          SQL Query
        </h2>
        <span className="rounded-full bg-zinc-100 dark:bg-zinc-800 px-2.5 py-0.5 text-xs font-medium text-zinc-600 dark:text-zinc-400">
          SELECT only
        </span>
      </div>

      <textarea
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="SELECT * FROM customers LIMIT 10"
        className="w-full resize-none rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900 p-4 font-mono text-sm text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-colors min-h-32"
        rows={5}
      />

      <div className="mt-4 flex items-center gap-3">
        <button
          onClick={handleExecute}
          disabled={!query.trim() || isLoading}
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:bg-indigo-600"
        >
          {isLoading ? (
            <>
              <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Executing...
            </>
          ) : (
            <>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Execute Query
            </>
          )}
        </button>

        <button
          onClick={handleClear}
          className="rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-2 text-sm font-medium text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
        >
          Clear
        </button>

        <span className="ml-auto text-xs text-zinc-400">
          Ctrl + Enter to execute
        </span>
      </div>
    </section>
  );
}