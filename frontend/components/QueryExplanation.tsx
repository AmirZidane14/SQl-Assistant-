"use client";

interface QueryExplanationProps {
  explanation: string;
  prompt: string;
}

export default function QueryExplanation({ explanation, prompt }: QueryExplanationProps) {
  if (!explanation) return null;

  return (
    <div className="rounded-lg border border-indigo-200 dark:border-indigo-800/50 bg-indigo-50 dark:bg-indigo-950/20 px-4 py-3">
      <div className="flex items-start gap-3">
        <div className="mt-0.5 shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <p className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 mb-0.5">
            What this query does
          </p>
          <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">
            {explanation}
          </p>
        </div>
      </div>
    </div>
  );
}