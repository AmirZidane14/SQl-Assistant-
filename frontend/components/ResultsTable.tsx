"use client";

import { useState } from "react";

interface ResultsTableProps {
  columns: string[];
  rows: unknown[][];
  rowCount: number;
  error: string | null;
  isLoading: boolean;
}

export default function ResultsTable({
  columns,
  rows,
  rowCount,
  error,
  isLoading,
}: ResultsTableProps) {
  const [sortColumn, setSortColumn] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");

  function handleSort(col: string) {
    if (sortColumn === col) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(col);
      setSortDir("asc");
    }
  }

  const sortedRows = [...rows];
  if (sortColumn !== null) {
    const colIndex = columns.indexOf(sortColumn);
    sortedRows.sort((a, b) => {
      const valA = a[colIndex];
      const valB = b[colIndex];
      if (valA == null) return 1;
      if (valB == null) return -1;
      if (typeof valA === "number" && typeof valB === "number") {
        return sortDir === "asc" ? valA - valB : valB - valA;
      }
      const strA = String(valA);
      const strB = String(valB);
      return sortDir === "asc" ? strA.localeCompare(strB) : strB.localeCompare(strA);
    });
  }

  if (isLoading) {
    return (
      <section className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-8">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <svg className="mb-3 h-8 w-8 animate-spin text-indigo-500" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <p className="text-sm text-zinc-500">Executing query...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="rounded-xl border border-red-200 dark:border-red-800 bg-white dark:bg-zinc-950 p-8">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="mb-1 text-sm font-semibold text-red-600 dark:text-red-400">
            Query Error
          </h3>
          <p className="text-xs text-zinc-400 max-w-md">{error}</p>
        </div>
      </section>
    );
  }

  if (columns.length === 0 && rows.length === 0) {
    return (
      <section className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-8">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="mb-1 text-sm font-semibold text-zinc-700 dark:text-zinc-300">
            No query executed yet
          </h3>
          <p className="text-xs text-zinc-400">
            Write a query above and click Execute to see results
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 overflow-hidden">
      <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 px-5 py-3">
        <p className="text-xs font-medium text-zinc-600 dark:text-zinc-400">
          {rowCount > 0 ? (
            <>Query returned <span className="font-semibold text-indigo-600 dark:text-indigo-400">{rowCount}</span> {rowCount === 1 ? "row" : "rows"}</>
          ) : (
            "Query returned 0 rows"
          )}
        </p>
        <p className="text-xs text-zinc-400">
          Click column headers to sort
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900">
              {columns.map((col) => (
                <th
                  key={col}
                  onClick={() => handleSort(col)}
                  className="cursor-pointer select-none px-4 py-3 text-left font-medium text-zinc-600 dark:text-zinc-400 hover:text-indigo-600 dark:hover:text-indigo-400 whitespace-nowrap"
                >
                  <span className="flex items-center gap-1">
                    {col}
                    {sortColumn === col && (
                      <span className="text-indigo-500">{sortDir === "asc" ? "↑" : "↓"}</span>
                    )}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedRows.map((row, i) => (
              <tr
                key={i}
                className="border-b border-zinc-100 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-900"
              >
                {row.map((cell, j) => (
                  <td
                    key={j}
                    className="px-4 py-2.5 text-zinc-700 dark:text-zinc-300 whitespace-nowrap"
                  >
                    {cell === null ? (
                      <span className="text-zinc-400 italic">null</span>
                    ) : (
                      String(cell)
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}