#!/usr/bin/env python3
"""Backfill failures/ folder from existing experiment data."""

import json
from datetime import datetime
from pathlib import Path

from src.failure_logger import (
    FailureLogger,
    FAIL_CODE_GEN,
    FAIL_EXECUTION,
    FAIL_EVALUATION,
)


def extract_label_batch_ts(path_str: str) -> tuple[str, str]:
    """Extract label and batch timestamp from experiment path.

    Examples:
        .../20260325_151112/run_001 -> ("...", "20260325_151112")
    """
    parts = path_str.replace("\\", "/").split("/")
    for i, part in enumerate(parts):
        if len(part) == 15 and part[8] == "_" and part[:8].isdigit():
            # Found timestamp like 20260325_151112
            return "/".join(parts[:i]), part
    return "", ""


def backfill_failures():
    """Scan experiments and create failure logs."""
    experiments_dir = Path("experiments")
    failures_created = 0
    issues_found = 0

    # Collect failures by (batch_ts, label) to group by batch
    batch_failures = {}

    for mode_dir in sorted(experiments_dir.glob("*/")):
        if not mode_dir.is_dir():
            continue

        for exp_dir in sorted(mode_dir.glob("*/")):
            if not exp_dir.is_dir():
                continue

            if mode_dir.name == "standard":
                # Standard mode: single run
                issues = _check_run(exp_dir)
                if issues:
                    label = _extract_exp_label(exp_dir.name)
                    batch_ts, _ = extract_label_batch_ts(str(exp_dir))
                    batch_ts = exp_dir.name.split(" - ")[-1]  # Get timestamp from dir name
                    batch_key = (batch_ts, label)
                    if batch_key not in batch_failures:
                        batch_failures[batch_key] = []
                    batch_failures[batch_key].append((exp_dir, None, issues))
                    issues_found += 1

            elif mode_dir.name == "breakthrough":
                # Breakthrough mode: multiple runs
                for run_dir in sorted(exp_dir.glob("run_*")):
                    issues = _check_run(run_dir)
                    if issues:
                        label = _extract_exp_label(exp_dir.name)
                        batch_ts = exp_dir.name.split(" - ")[-1]
                        iteration = int(run_dir.name.split("_")[-1])
                        batch_key = (batch_ts, label)
                        if batch_key not in batch_failures:
                            batch_failures[batch_key] = []
                        batch_failures[batch_key].append((run_dir, iteration, issues))
                        issues_found += 1

    # Create failure logs grouped by batch
    for (batch_ts, label), runs in sorted(batch_failures.items()):
        logger = FailureLogger(
            problem_label=label,
            batch_run_ts=batch_ts,
            output_dir=Path("failures"),
        )

        for run_path, iteration, issues in runs:
            _log_run_issues(logger, run_path, iteration, issues)

        if logger.has_failures():
            result = logger.flush()
            if result:
                json_path, md_path = result
                try:
                    print(f"[+] Created: {md_path.name}")
                except UnicodeEncodeError:
                    print(f"[+] Created failure log")
                failures_created += 1

    print(f"\nSummary:")
    print(f"  Issues found: {issues_found}")
    print(f"  Failure logs created: {failures_created}")


def _extract_exp_label(dirname: str) -> str:
    """Extract label from experiment directory name.

    Examples:
        'Category - Topic - 20260325_151112' -> 'Category - Topic'
    """
    parts = dirname.rsplit(" - ", 1)
    return parts[0]


def _check_run(run_path: Path) -> dict | None:
    """Check if a run has failures. Return issue dict or None."""
    code_file = run_path / "05_experiment_code.py"
    output_file = run_path / "06_run_output.txt"
    eval_file = run_path / "07_evaluation.md"

    code_empty = code_file.exists() and code_file.stat().st_size == 0
    output_empty = output_file.exists() and output_file.stat().st_size == 0
    eval_empty = not eval_file.exists() or eval_file.stat().st_size < 50

    output_has_error = False
    if output_file.exists():
        try:
            content = output_file.read_text(encoding="utf-8", errors="replace")
            output_has_error = "[TIMEOUT]" in content or "[ERROR]" in content
        except Exception:
            pass

    if not (code_empty or output_empty or eval_empty or output_has_error):
        return None

    return {
        "code_empty": code_empty,
        "output_empty": output_empty,
        "eval_empty": eval_empty,
        "output_has_error": output_has_error,
    }


def _log_run_issues(
    logger: FailureLogger, run_path: Path, iteration: int | None, issues: dict
):
    """Log issues from a failed run."""
    code_file = run_path / "05_experiment_code.py"
    output_file = run_path / "06_run_output.txt"
    eval_file = run_path / "07_evaluation.md"
    problem_file = run_path / "01_problem.md"
    hypotheses_file = run_path / "04_hypotheses.md"

    # Read available data
    problem_md = ""
    try:
        if problem_file.exists():
            problem_md = problem_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        pass

    hypotheses = ""
    try:
        if hypotheses_file.exists():
            hypotheses = hypotheses_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        pass

    code = ""
    try:
        if code_file.exists() and code_file.stat().st_size > 0:
            code = code_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        pass

    output = ""
    try:
        if output_file.exists():
            output = output_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        pass

    evaluation = ""
    try:
        if eval_file.exists() and eval_file.stat().st_size > 0:
            evaluation = eval_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        pass

    # Determine failure type and log
    if issues["code_empty"]:
        logger.record(
            FAIL_CODE_GEN,
            step="generate_code",
            error="Code generation produced empty output",
            context={
                "problem_snippet": problem_md[:200],
                "hypotheses_snippet": hypotheses[:200],
            },
            artifacts={"code": code or "(empty)"} if code else {},
        )

    if issues["output_empty"] and not issues["code_empty"]:
        logger.record(
            FAIL_EXECUTION,
            step="run_full_experiment",
            error="Code execution produced empty output",
            context={"problem_snippet": problem_md[:200]},
            artifacts={
                "code": code[:500] if code else "(no code)",
                "output": output or "(empty)",
            },
        )

    if issues["output_has_error"]:
        logger.record(
            FAIL_EXECUTION,
            step="run_code",
            error=output[:500] if output else "Execution error",
            context={"problem_snippet": problem_md[:200]},
            artifacts={
                "code": code[:500] if code else "(no code)",
                "output": output[:500] if output else "(empty)",
            },
        )

    if issues["eval_empty"]:
        logger.record(
            FAIL_EVALUATION,
            step="evaluate_results",
            error="Evaluation produced no valid output",
            context={
                "problem_snippet": problem_md[:200],
                "output_snippet": output[:300] if output else "(empty)",
            },
        )


if __name__ == "__main__":
    backfill_failures()
