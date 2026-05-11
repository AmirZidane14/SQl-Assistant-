"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import QueryEditor from "@/components/QueryEditor";
import ResultsTable from "@/components/ResultsTable";
import { ExecutionStatus } from "@/types/query";

export default function Home() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [query, setQuery] = useState("");
  const [columns, setColumns] = useState<string[]>([]);
  const [rows, setRows] = useState<unknown[][]>([]);
  const [rowCount, setRowCount] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<ExecutionStatus>("idle");

  return (
    <div className="flex h-full">
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      <div className="flex flex-1 flex-col overflow-hidden">
        <Navbar />

        <main className="flex-1 overflow-y-auto p-6">
          <div className="mx-auto max-w-5xl space-y-6">
            <QueryEditor
              query={query}
              onQueryChange={setQuery}
              onResults={(cols, r, count) => {
                setColumns(cols);
                setRows(r);
                setRowCount(count);
                setError(null);
              }}
              onError={(err) => {
                setError(err);
                setColumns([]);
                setRows([]);
                setRowCount(0);
              }}
              onStatusChange={setStatus}
            />

            {error && status === "error" && (
              <div className="rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/30 px-4 py-3 text-sm text-red-700 dark:text-red-400">
                <span className="font-semibold">Error:</span> {error}
              </div>
            )}

            <ResultsTable
              columns={columns}
              rows={rows}
              rowCount={rowCount}
              error={error}
              isLoading={status === "loading"}
            />
          </div>
        </main>
      </div>
    </div>
  );
}