"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import QueryEditor from "@/components/QueryEditor";
import ResultsTable from "@/components/ResultsTable";
import SchemaExplorer from "@/components/SchemaExplorer";
import NaturalLanguageInput from "@/components/NaturalLanguageInput";
import GeneratedSQLPreview from "@/components/GeneratedSQLPreview";
import { ExecutionStatus } from "@/types/query";

export default function Home() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [activeView, setActiveView] = useState<string>("Query Console");
  const [query, setQuery] = useState("");
  const [generatedSql, setGeneratedSql] = useState("");
  const [generatedPrompt, setGeneratedPrompt] = useState("");
  const [columns, setColumns] = useState<string[]>([]);
  const [rows, setRows] = useState<unknown[][]>([]);
  const [rowCount, setRowCount] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<ExecutionStatus>("idle");

  function handleGenerated(sql: string, prompt: string) {
    setGeneratedSql(sql);
    setGeneratedPrompt(prompt);
    setError(null);
    setStatus("idle");
  }

  function handleGenerationError(err: string) {
    setError(err);
    setGeneratedSql("");
    setGeneratedPrompt("");
    setStatus("error");
  }

  function handleUseQuery(sql: string) {
    setQuery(sql);
    setGeneratedSql("");
    setGeneratedPrompt("");
    setError(null);
    setStatus("idle");
  }

  function handleDiscard() {
    setGeneratedSql("");
    setGeneratedPrompt("");
  }

  return (
    <div className="flex h-full">
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
        activeView={activeView}
        onViewChange={setActiveView}
      />

      <div className="flex flex-1 flex-col overflow-hidden">
        <Navbar activeView={activeView} />

        <main className="flex-1 overflow-y-auto p-6">
          <div className="mx-auto max-w-5xl space-y-6">
            {activeView === "Query Console" && (
              <>
                <NaturalLanguageInput
                  onGenerated={handleGenerated}
                  onError={handleGenerationError}
                />

                {generatedSql && (
                  <GeneratedSQLPreview
                    sql={generatedSql}
                    prompt={generatedPrompt}
                    onUseQuery={handleUseQuery}
                    onDiscard={handleDiscard}
                    error={status === "error" ? error : null}
                  />
                )}

                <QueryEditor
                  query={query}
                  onQueryChange={setQuery}
                  onResults={(cols, r, count) => {
                    setColumns(cols);
                    setRows(r);
                    setRowCount(count);
                    setError(null);
                    setStatus("success");
                  }}
                  onError={(err) => {
                    setError(err);
                    setColumns([]);
                    setRows([]);
                    setRowCount(0);
                    setStatus("error");
                  }}
                  onStatusChange={setStatus}
                />

                {error && status === "error" && !generatedSql && (
                  <div className="rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/30 px-4 py-3 text-sm text-red-700 dark:text-red-400">
                    <span className="font-semibold">Error:</span> {error}
                  </div>
                )}

                <ResultsTable
                  columns={columns}
                  rows={rows}
                  rowCount={rowCount}
                  error={status === "error" && columns.length === 0 ? error : null}
                  isLoading={status === "loading"}
                />
              </>
            )}

            {activeView === "Schema Explorer" && <SchemaExplorer />}
          </div>
        </main>
      </div>
    </div>
  );
}