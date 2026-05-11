"use client";

interface RateLimitErrorProps {
  message?: string;
}

export default function RateLimitError({ message }: RateLimitErrorProps) {
  return (
    <div className="rounded-lg border border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-950/30 px-5 py-4">
      <div className="flex items-start gap-3">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-orange-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <p className="text-sm font-semibold text-orange-700 dark:text-orange-400">
            Rate Limit Exceeded
          </p>
          <p className="mt-1 text-xs text-orange-600 dark:text-orange-300">
            {message || "You've made too many requests. Please wait about 1 minute before trying again."}
          </p>
        </div>
      </div>
    </div>
  );
}
