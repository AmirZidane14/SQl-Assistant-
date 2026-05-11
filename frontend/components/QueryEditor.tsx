"use client";

import { useState, KeyboardEvent } from "react";

interface QueryEditorProps {
  onExecute?: () => void;
}

export default function QueryEditor({ onExecute }: QueryEditorProps) {
  const [query, setQuery] = useState("");

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      onExecute?.();
    }
  }

  return (
    <section className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-6">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
          Natural Language Query
        </h2>
        <span className="rounded-full bg-indigo-50 dark:bg-indigo-950 px-2.5 py-0.5 text-xs font-medium text-indigo-600 dark:text-indigo-400">
          English
        </span>
      </div>

      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your SQL query here... e.g. Show all customers from New York"
        className="w-full resize-none rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900 p-4 font-mono text-sm text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-colors min-h-32"
        rows={4}
      />

      <div className="mt-4 flex items-center gap-3">
        <button
          disabled
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white opacity-50 cursor-not-allowed transition-colors"
        >
          Generate SQL
        </button>
        <button
          onClick={() => setQuery("")}
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