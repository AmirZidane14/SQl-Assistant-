"use client";

import { useState, KeyboardEvent } from "react";
import { generateSQL } from "@/services/api";

interface NaturalLanguageInputProps {
  onGenerated: (sql: string, prompt: string) => void;
  onError: (error: string) => void;
}

const EXAMPLE_PROMPTS = [
  "Show all customers",
  "List top 5 products by price",
  "Find orders placed in the last 30 days",
];

export default function NaturalLanguageInput({ onGenerated, onError }: NaturalLanguageInputProps) {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleGenerate() {
    if (!prompt.trim()) return;

    setIsLoading(true);
    onError("");

    const result = await generateSQL(prompt);

    setIsLoading(false);

    if (!result.success) {
      onError(result.error || "Failed to generate SQL");
    } else {
      onGenerated(result.generated_sql, result.user_prompt);
    }
  }

  function handleClear() {
    setPrompt("");
    onError("");
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      handleGenerate();
    }
  }

  function insertExample(example: string) {
    setPrompt(example);
  }

  return (
    <section className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-6">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
          Ask in Plain English
        </h2>
        <span className="rounded-full bg-indigo-50 dark:bg-indigo-950 px-2.5 py-0.5 text-xs font-medium text-indigo-600 dark:text-indigo-400">
          AI Powered
        </span>
      </div>

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask your database in plain English... e.g. Show customers who spent more than 5000"
        className="w-full resize-none rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900 p-4 text-sm text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-colors min-h-24"
        rows={3}
      />

      <div className="mt-3">
        <p className="mb-2 text-xs text-zinc-400">Try an example:</p>
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_PROMPTS.map((example) => (
            <button
              key={example}
              onClick={() => insertExample(example)}
              className="rounded-full border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-1 text-xs text-zinc-600 dark:text-zinc-400 hover:border-indigo-300 hover:text-indigo-600 dark:hover:border-indigo-700 dark:hover:text-indigo-400 transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-4 flex items-center gap-3">
        <button
          onClick={handleGenerate}
          disabled={!prompt.trim() || isLoading}
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:bg-indigo-600"
        >
          {isLoading ? (
            <>
              <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Generating SQL...
            </>
          ) : (
            <>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Generate SQL
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
          Ctrl + Enter to generate
        </span>
      </div>
    </section>
  );
}