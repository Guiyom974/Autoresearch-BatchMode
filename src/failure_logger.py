"""Failure logging for batch mode — writes failures/ JSON + Markdown per problem."""

import json
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Failure type constants — kept as strings for JSON readability
FAIL_CODE_GEN = "code_generation"
FAIL_EXECUTION = "execution"
FAIL_EVALUATION = "evaluation"
FAIL_API = "api_error"
FAIL_BATCH = "batch_level"
FAIL_TRUNCATION = "code_truncation"
FAIL_POLICY = "policy_block"


class FailureLogger:
    """Accumulates failure events for one problem and writes JSON + Markdown on flush().

    Usage:
        logger = FailureLogger(problem_label="Math - Primes", batch_run_ts="20260407_120000")
        logger.record(FAIL_API, step="web_search", error="Rate limit", context={...})
        logger.record_retry_sequence(FAIL_CODE_GEN, attempts=[...])
        logger.flush()   # writes failures/20260407_120000_Math-Primes.{json,md}
    """

    def __init__(self, problem_label: str, batch_run_ts: str, output_dir: Path | None = None):
        self.problem_label = problem_label
        self.batch_run_ts = batch_run_ts
        # Always relative to cwd — matches ExperimentTracker convention
        self.output_dir = Path(output_dir) if output_dir else Path("failures")
        self._events: list[dict] = []
        self._flushed = False

    # ── Core recording ────────────────────────────────────────────────────────

    def record(
        self,
        failure_type: str,
        *,
        step: str,
        error: str,
        context: dict[str, Any] | None = None,
        artifacts: dict[str, str] | None = None,  # {"code": "...", "output": "..."}
        exc: BaseException | None = None,
    ) -> None:
        """Record a single failure event.

        Args:
            failure_type: One of the FAIL_* constants
            step: Human-readable step name, e.g. "code_generation", "run_attempt_2"
            error: Short error message
            context: Arbitrary dict of contextual data (problem snippet, model, etc.)
            artifacts: Named text blobs to preserve (code, output, prompt snippets)
            exc: Live exception — traceback will be captured automatically
        """
        event: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "type": failure_type,
            "step": step,
            "error": error,
        }
        if context:
            event["context"] = context
        if artifacts:
            event["artifacts"] = {k: v[:4000] for k, v in artifacts.items()}  # cap artifact size
        if exc is not None:
            event["traceback"] = traceback.format_exc()
        self._events.append(event)

    def record_retry_sequence(
        self,
        failure_type: str,
        *,
        step: str,
        attempts: list[dict[str, Any]],  # [{attempt: 1, error: "...", code: "..."}]
        context: dict[str, Any] | None = None,
    ) -> None:
        """Record a multi-attempt retry sequence as a single consolidated log entry.

        Each attempt dict should contain at minimum: attempt (int), error (str).
        Optional keys: code (str), output (str), strategy (str).
        """
        event: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "type": failure_type,
            "step": step,
            "error": f"{len(attempts)} attempt(s) all failed",
            "retry_sequence": [
                {
                    "attempt": a.get("attempt", i + 1),
                    "strategy": a.get("strategy", "default"),
                    "error": a.get("error", "")[:500],
                    "code_preview": a.get("code", "")[:300],
                    "output_preview": a.get("output", "")[:300],
                }
                for i, a in enumerate(attempts)
            ],
        }
        if context:
            event["context"] = context
        self._events.append(event)

    def record_batch_exception(self, problem_file: str, exc: BaseException) -> None:
        """Convenience method for the outermost batch except block."""
        self.record(
            FAIL_BATCH,
            step="batch_orchestration",
            error=str(exc),
            context={"problem_file": problem_file},
            exc=exc,
        )

    # ── Output ────────────────────────────────────────────────────────────────

    def has_failures(self) -> bool:
        return len(self._events) > 0

    def flush(self) -> tuple[Path, Path] | None:
        """Write JSON and Markdown files. Returns (json_path, md_path) or None if no events."""
        if not self._events:
            return None
        if self._flushed:
            # Re-flush allowed (batch exception may call after internal flush)
            pass

        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # Sanitise label for filename: replace spaces and special chars
            safe_label = self.problem_label.replace(" ", "-").replace("/", "-")
            stem = f"{self.batch_run_ts}_{safe_label}"

            json_path = self.output_dir / f"{stem}.json"
            md_path = self.output_dir / f"{stem}.md"

            payload = {
                "schema_version": "1.0",
                "problem_label": self.problem_label,
                "batch_run_ts": self.batch_run_ts,
                "failure_count": len(self._events),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "failures": self._events,
            }
            json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            md_path.write_text(self._render_markdown(payload), encoding="utf-8")

            self._flushed = True
            return json_path, md_path
        except Exception:
            # Failure to log must never crash the batch run
            return None

    # ── Markdown rendering ────────────────────────────────────────────────────

    def _render_markdown(self, payload: dict) -> str:
        lines = [
            f"# Failure Report: {payload['problem_label']}",
            f"",
            f"**Batch Run**: `{payload['batch_run_ts']}`  ",
            f"**Generated**: {payload['generated_at']}  ",
            f"**Total Failures**: {payload['failure_count']}",
            f"",
            "---",
            "",
        ]
        for i, event in enumerate(payload["failures"], 1):
            lines += [
                f"## Failure {i}: {event['type']} — {event['step']}",
                f"",
                f"- **Timestamp**: {event['ts']}",
                f"- **Error**: {event['error']}",
                "",
            ]
            if ctx := event.get("context"):
                lines.append("**Context**:")
                lines.append("```")
                lines.append(json.dumps(ctx, indent=2))
                lines.append("```")
                lines.append("")

            if seq := event.get("retry_sequence"):
                lines.append(f"**Retry Sequence** ({len(seq)} attempts):")
                for a in seq:
                    lines.append(f"")
                    lines.append(f"### Attempt {a['attempt']} — strategy: `{a['strategy']}`")
                    lines.append(f"- Error: {a['error']}")
                    if a.get("code_preview"):
                        lines.append("```python")
                        lines.append(a["code_preview"])
                        lines.append("```")
                    if a.get("output_preview"):
                        lines.append("```")
                        lines.append(a["output_preview"])
                        lines.append("```")
                lines.append("")

            if arts := event.get("artifacts"):
                for name, content in arts.items():
                    lines.append(f"**Artifact: {name}**")
                    ext = "python" if "code" in name else ""
                    lines.append(f"```{ext}")
                    lines.append(content)
                    lines.append("```")
                    lines.append("")

            if tb := event.get("traceback"):
                lines.append("**Traceback**:")
                lines.append("```")
                lines.append(tb)
                lines.append("```")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)
