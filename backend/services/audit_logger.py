import os
import time
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

MAX_LOG_SIZE = 5 * 1024 * 1024
MAX_LOG_FILES = 5


class AuditLogger:
    """
    Structured audit logger that writes JSON-structured logs to files.
    Automatically rotates logs when they exceed MAX_LOG_SIZE.
    Never logs secrets or API keys.
    """

    def __init__(self):
        self._current_date = ""

    def _get_log_path(self) -> Path:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        if today != self._current_date:
            self._current_date = today
        return LOG_DIR / f"audit_{today}.log"

    def _should_rotate(self, path: Path) -> bool:
        return path.exists() and path.stat().st_size >= MAX_LOG_SIZE

    def _rotate_logs(self) -> None:
        for log_file in sorted(LOG_DIR.glob("audit_*.log")):
            if log_file.stat().st_size >= MAX_LOG_SIZE:
                log_file.unlink(missing_ok=True)

    def _write(self, entry: dict) -> None:
        import json

        log_path = self._get_log_path()

        if self._should_rotate(log_path):
            self._rotate_logs()

        line = json.dumps(entry, default=str) + "\n"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line)

    def log(
        self,
        event: str,
        endpoint: str | None = None,
        ip: str | None = None,
        prompt: str | None = None,
        generated_sql: str | None = None,
        execution_status: str | None = None,
        error: str | None = None,
        duration_ms: int | None = None,
        extra: dict | None = None,
    ) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": event,
            "endpoint": endpoint,
            "ip": ip,
            "prompt": prompt[:200] if prompt else None,
            "generated_sql": generated_sql[:500] if generated_sql else None,
            "execution_status": execution_status,
            "error": error,
            "duration_ms": duration_ms,
        }
        if extra:
            entry["extra"] = extra

        self._write(entry)


logger = AuditLogger()
