"use client";

import { useState, useEffect } from "react";
import { checkBackendHealth } from "@/services/api";

export default function StatusBadge() {
  const [connected, setConnected] = useState<boolean | null>(null);

  useEffect(() => {
    async function ping() {
      const health = await checkBackendHealth();
      setConnected(health !== null && health.status === "running");
    }

    ping();
    const interval = setInterval(ping, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center gap-2">
      {connected === null ? (
        <span className="flex items-center gap-1.5 text-xs text-zinc-400">
          <span className="h-2 w-2 rounded-full bg-zinc-400 animate-pulse" />
          Checking...
        </span>
      ) : connected ? (
        <span className="flex items-center gap-1.5 text-xs text-emerald-500">
          <span className="h-2 w-2 rounded-full bg-emerald-500" />
          Connected
        </span>
      ) : (
        <span className="flex items-center gap-1.5 text-xs text-red-500">
          <span className="h-2 w-2 rounded-full bg-red-500" />
          Disconnected
        </span>
      )}
    </div>
  );
}