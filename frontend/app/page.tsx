"use client";

import { useState, KeyboardEvent } from "react";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import ResultsTable from "@/components/ResultsTable";
import SchemaExplorer from "@/components/SchemaExplorer";
import NaturalLanguageInput from "@/components/NaturalLanguageInput";
import GeneratedSQLPreview from "@/components/GeneratedSQLPreview";
import QueryExplanation from "@/components/QueryExplanation";
import WorkflowActions from "@/components/WorkflowActions";
import { workflowPreview, workflowExecute } from "@/services/api";

export type WorkflowState =
  | "idle"
  | "generating"
  | "previewing"
  | "editing"
  | "executing"
  | "success"
  | "error";

interface HistoryEntry {
  prompt: string;
  sql: string;
  timestamp: Date;
}

export default function Home() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [activeView, setActiveView] = useState<string>("Query Console");

  const [workflowState, setWorkflowState] = useState<WorkflowState>("idle");
  const [prompt, setPrompt] = useState("");
  const [generatedSql, setGeneratedSql] = useState("");
  const [explanation, setExplanation] = useState("");
  const [workflowError, setWorkflowError] = useState<string | null>(null);

  const [query, setQuery] = useState("");
  const [columns, setColumns] = useState<string[]>([]);
  const [rows, setRows] = useState<unknown[][]>([]);
  const [rowCount, setRowCount] = useState(0);
  const [queryError, setQueryError] = useState<string | null>(null);

  const [history, setHistory] = useState<HistoryEntry[]>([]);

  async function handlePreview(p: string) {
    setPrompt(p);
    setWorkflowState("generating");
    setWorkflowError(null);

    const result = await workflowPreview(p);

    if (!result.success) {
      setWorkflowState("error");
      setWorkflowError(result.error || "Failed to generate SQL");
      setGeneratedSql("");
      setExplanation("");
    } else {
      setWorkflowState("previewing");
      setGeneratedSql(result.generated_sql);
      setExplanation(result.explanation || "");
      setWorkflowError(result.valid ? null : result.error);
      setHistory((prev) => [
        { prompt: p, sql: result.generated_sql, timestamp: new Date() },
        ...prev.slice(0, 4),
      ]);
    }
  }

  async function handleRegenerate() {
    if (!prompt) return;
    setGeneratedSql("");
    setExplanation("");
    await handlePreview(prompt);
  }

  async function handleExecute(sql: string) {
    setQuery(sql);
    setWorkflowState("executing");
    setQueryError(null);

    const result = await workflowExecute(sql);

    if (!result.success) {
      setWorkflowState("error");
      setQueryError(result.error || "Query execution failed");
      setColumns([]);
      setRows([]);
      setRowCount(0);
    } else {
      setWorkflowState("success");
      setColumns(result.columns);
      setRows(result.rows);
      setRowCount(result.count);
    }
  }

  async function handleManualExecute() {
    if (!query.trim()) return;
    await handleExecute(query.trim());
  }

  function handleDiscard() {
    setGeneratedSql("");
    setExplanation("");
    setWorkflowState("idle");
  }

  function handleClear() {
    setPrompt("");
    setGeneratedSql("");
    setExplanation("");
    setWorkflowState("idle");
    setWorkflowError(null);
    setQuery("");
    setColumns([]);
    setRows([]);
    setRowCount(0);
    setQueryError(null);
  }

  function handleToggleEdit() {
    if (workflowState === "editing") {
      setWorkflowState("previewing");
    } else {
      setWorkflowState("editing");
    }
  }

  function handleManualKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      handleManualExecute();
    }
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
                  onPreview={handlePreview}
                  isLoading={workflowState === "generating"}
                />

                {(workflowState === "generating" ||
                  workflowState === "previewing" ||
                  workflowState === "editing" ||
                  workflowState === "executing" ||
                  workflowState === "error") && (
                  <>
                    <GeneratedSQLPreview
                      sql={generatedSql}
                      prompt={prompt}
                      explanation={explanation}
                      error={workflowError}
                      isLoading={workflowState === "generating"}
                    />

                    {(workflowState === "previewing" || workflowState === "editing") && explanation && (
                      <QueryExplanation explanation={explanation} prompt={prompt} />
                    )}

                    <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-6">
                      <div className="mb-4 flex items-center justify-between">
                        <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
                          SQL Query
                        </h2>
                        <span className="rounded-full bg-zinc-100 dark:bg-zinc-800 px-2.5 py-0.5 text-xs font-medium text-zinc-600 dark:text-zinc-400">
                          Manual or AI-generated
                        </span>
                      </div>

                      <textarea
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={handleManualKeyDown}
                        placeholder="Generated SQL will appear here, or write your own query..."
                        className="w-full resize-none rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900 p-4 font-mono text-sm text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-colors min-h-32"
                        rows={5}
                      />

                      <WorkflowActions
                        onUseQuery={() => generatedSql && setQuery(generatedSql)}
                        onRegenerate={handleRegenerate}
                        onDiscard={handleDiscard}
                        onExecute={() => handleExecute(query)}
                        onClear={handleClear}
                        isGenerated={workflowState === "previewing"}
                        isExecuting={workflowState === "executing"}
                        isEditing={workflowState === "editing"}
                        onToggleEdit={handleToggleEdit}
                      />
                    </div>
                  </>
                )}

                {queryError && (
                  <div className="rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/30 px-4 py-3 text-sm text-red-700 dark:text-red-400">
                    <span className="font-semibold">Error:</span> {queryError}
                  </div>
                )}

                <ResultsTable
                  columns={columns}
                  rows={rows}
                  rowCount={rowCount}
                  error={workflowState === "error" && !queryError ? workflowError : null}
                  isLoading={workflowState === "executing"}
                />

                {history.length > 0 && (
                  <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 overflow-hidden">
                    <div className="border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 px-5 py-3">
                      <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
                        Recent Queries
                      </p>
                    </div>
                    <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
                      {history.map((entry, i) => (
                        <button
                          key={i}
                          onClick={() => {
                            setQuery(entry.sql);
                            setGeneratedSql(entry.sql);
                            setWorkflowState("previewing");
                          }}
                          className="flex w-full items-center gap-3 px-5 py-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-colors"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 shrink-0 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <div className="min-w-0 flex-1">
                            <p className="text-xs text-zinc-500 truncate">{entry.prompt}</p>
                            <p className="text-sm font-mono text-zinc-700 dark:text-zinc-300 truncate">{entry.sql}</p>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}

            {activeView === "Schema Explorer" && <SchemaExplorer />}
          </div>
        </main>
      </div>
    </div>
  );
}