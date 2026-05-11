"use client";

import StatusBadge from "./StatusBadge";

interface NavbarProps {
  activeView?: string;
}

const VIEW_TITLES: Record<string, { title: string; subtitle: string }> = {
  "Query Console": { title: "Query Console", subtitle: "Write SQL queries and view results" },
  "Schema Explorer": { title: "Schema Explorer", subtitle: "Browse database structure and relationships" },
  "Query History": { title: "Query History", subtitle: "View and re-run past queries" },
  "Settings": { title: "Settings", subtitle: "Configure your assistant" },
};

export default function Navbar({ activeView = "Query Console" }: NavbarProps) {
  const info = VIEW_TITLES[activeView] || VIEW_TITLES["Query Console"];

  return (
    <header className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 px-6 py-3">
      <div>
        <h1 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
          {info.title}
        </h1>
        <p className="text-xs text-zinc-400">
          {info.subtitle}
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