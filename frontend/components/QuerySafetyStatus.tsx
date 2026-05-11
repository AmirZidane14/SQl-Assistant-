"use client";

import { useState, useEffect } from "react";

interface SecurityStatus {
  rate_limiting: boolean;
  audit_logging: boolean;
  prompt_guard: boolean;
  sql_guard: boolean;
  security_headers: boolean;
  query_timeout_seconds: number;
  max_query_length: number;
  max_joins: number;
  max_nested_selects: number;
  rate_limits: Record<string, number>;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function QuerySafetyStatus() {
  const [status, setStatus] = useState<SecurityStatus | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/admin/security-status`)
      .then((r) => r.json())
      .then(setStatus)
      .catch(() => {});
  }, []);

  if (!status) return null;

  const items = [
    { label: "Rate Limiting", enabled: status.rate_limiting, detail: `${status.rate_limits?.ai_requests_per_minute || 30}/min` },
    { label: "Prompt Guard", enabled: status.prompt_guard, detail: "Injection protection" },
    { label: "SQL Guard", enabled: status.sql_guard, detail: `Max ${status.max_joins} JOINs, ${status.max_nested_selects} nested SELECTs` },
    { label: "Security Headers", enabled: status.security_headers, detail: "X-Frame-Options, CSP" },
    { label: "Query Timeout", enabled: true, detail: `${status.query_timeout_seconds}s max` },
  ];

  return (
    <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 overflow-hidden">
      <div className="border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 px-5 py-3">
        <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
          Security & Safety Features
        </p>
      </div>
      <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
        {items.map((item) => (
          <div key={item.label} className="flex items-center justify-between px-5 py-3">
            <div className="flex items-center gap-2">
              <div className={`h-2 w-2 rounded-full ${item.enabled ? "bg-emerald-500" : "bg-red-500"}`} />
              <span className="text-sm text-zinc-700 dark:text-zinc-300">{item.label}</span>
            </div>
            <span className="text-xs text-zinc-400">{item.detail}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
