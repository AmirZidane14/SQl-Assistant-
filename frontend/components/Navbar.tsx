"use client";

import StatusBadge from "./StatusBadge";

export default function Navbar() {
  return (
    <header className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 px-6 py-3">
      <div>
        <h1 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
          Query Console
        </h1>
        <p className="text-xs text-zinc-400">
          Ask questions in plain English, get SQL
        </p>
      </div>

      <div className="flex items-center gap-4">
        <StatusBadge />
        <button className="rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-1.5 text-xs font-medium text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors">
          Clear Cache
        </button>
      </div>
    </header>
  );
}