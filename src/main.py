"""AutoResearch CLI entry point."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from . import config
from .llm import LLMRouter
from .reporter import generate_breakthrough_report
from .researcher import build_past_context, run_breakthrough_loop, run_standard_loop
from .tracker import ExperimentTracker

console = Console()

# Batch state is persisted here so interrupted runs can be resumed
_BATCH_STATE_FILE = Path("experiments") / ".batch_state.json"


# ── Batch state helpers ───────────────────────────────────────────────────────

def _load_batch_states() -> dict:
    """Load the full batch state registry from disk."""
    if not _BATCH_STATE_FILE.exists():
        return {}
    try:
        return json.loads(_BATCH_STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_batch_state(folder_key: str, state: dict) -> None:
    """Persist state for one batch folder (keyed by its resolved absolute path)."""
    states = _load_batch_states()
    states[folder_key] = state
    _BATCH_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    _BATCH_STATE_FILE.write_text(json.dumps(states, indent=2), encoding="utf-8")


def _clear_batch_state(folder_key: str) -> None:
    """Remove the state entry after a fully completed run."""
    states = _load_batch_states()
    if folder_key in states:
        del states[folder_key]
        _BATCH_STATE_FILE.write_text(json.dumps(states, indent=2), encoding="utf-8")


def _find_latest_experiment_dir(label: str, mode: str) -> Path | None:
    """Return the most recently created experiment directory for a given label and mode."""
    base = Path("experiments") / mode
    if not base.exists():
        return None
    matches = sorted(base.glob(f"{label} - *"))
    return matches[-1] if matches else None


def _is_experiment_complete(label: str, mode: str) -> bool:
    """Return True only if the experiment produced complete output artifacts on disk.

    Used to detect manually deleted files during a resume: even if a problem file
    is listed as 'completed' in the state, we re-run it when the key artifact is gone.
    """
    folder = _find_latest_experiment_dir(label, mode)
    if folder is None:
        return False
    if mode == "standard":
        eval_file = folder / "07_evaluation.md"
        try:
            return eval_file.exists() and len(
                eval_file.read_text(encoding="utf-8", errors="replace")
            ) > 50
        except Exception:
            return False
    else:  # breakthrough
        if (folder / "report.html").exists():
            return True
        # Fallback: check that the last run at least produced an evaluation
        runs = sorted(folder.glob("run_*"))
        if runs:
            eval_file = runs[-1] / "07_evaluation.md"
            try:
                return eval_file.exists() and len(
                    eval_file.read_text(encoding="utf-8", errors="replace")
                ) > 50
            except Exception:
                pass
        return False


# ── Reporting ─────────────────────────────────────────────────────────────────

def _print_batch_summary(results: list[dict]) -> None:
    """Render a formatted batch results table."""
    def tag(s: str) -> str:
        if s == "success":
            return "[green]  OK [/green]"
        if s == "skipped":
            return "[dim]SKIP[/dim]"
        if s == "interrupted":
            return "[yellow]INTR[/yellow]"
        return "[red]FAIL[/red]"

    body = "[bold]BATCH SUMMARY[/bold]\n\n" + "\n".join(
        f"  {tag(r['status'])}  {r['file']}  →  {r['status']}" for r in results
    )
    console.print("\n")
    console.print(Panel(body, expand=False))
    succeeded = sum(1 for r in results if r["status"] in ("success", "skipped"))
    console.print(f"[green]{succeeded}[/green] / {len(results)} succeeded (or skipped)")


# ── Label helper ──────────────────────────────────────────────────────────────

def label_from_problem_file(path: Path) -> str:
    """Extract a human-readable label from a problem file name.

    Examples:
        ``Mathematics - Prime Numbers - problem.md`` → ``Mathematics - Prime Numbers``
        ``problem.md`` → ``problem``
        ``my_research.md`` → ``my_research``

    Args:
        path: Path to the problem markdown file.

    Returns:
        Label string to use in experiment folder names.
    """
    stem = path.stem  # e.g. "Mathematics - Prime Numbers - problem"
    parts = stem.rsplit(" - ", 1)
    if len(parts) == 2 and parts[-1].lower() == "problem":
        return parts[0]
    return stem


# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="AutoResearch",
        description="AI Research Automation Tool - Autonomous research with web search and LLM reasoning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  launch.bat standard
    Run a single research pass on problem.md

  launch.bat standard --ollama-model mistral
    Use a specific Ollama model (skips model selection menu)

  launch.bat breakthrough --iterations 3
    Run 3 iterations with problem reformulation between each

  launch.bat breakthrough --iterations 5 --problem my_research.md
    Custom research problem with 5 breakthrough iterations

  launch.bat standard --batch problems/
    Run standard mode on every *problem.md in the problems/ folder

  launch.bat breakthrough --batch problems/ --iterations 5
    Run breakthrough mode (5 iterations) on every *problem.md in problems/

FEATURES:
  - Web search via Poe API (Gemini with web_search enabled)
  - Code generation & execution with local Ollama
  - Problem reformulation via Gemini-3.1-Pro
  - Full experiment tracking and HTML reports
        """,
    )

    parser.add_argument(
        "mode",
        nargs="?",
        choices=["standard", "breakthrough"],
        help="Research mode: 'standard' (single run) or 'breakthrough' (iterative with reformulation)",
    )

    parser.add_argument(
        "--problem",
        type=str,
        default=None,
        help="Path to problem file (default: ./problem.md). Cannot be combined with --batch.",
    )

    parser.add_argument(
        "--batch",
        type=str,
        default=None,
        metavar="FOLDER",
        help="Folder containing problem files. Run each *problem.md (or all .md) sequentially.",
    )

    parser.add_argument(
        "--ollama-model",
        type=str,
        default=None,
        help="Ollama model name (if not specified, user will be prompted)",
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
        help="Number of iterations for breakthrough mode (default: 3)",
    )

    args = parser.parse_args()

    # Show help if no mode specified
    if args.mode is None:
        parser.print_help()
        sys.exit(0)

    # Mutual exclusion: --problem and --batch cannot both be given
    if args.problem is not None and args.batch is not None:
        console.print("[red][!] --problem and --batch are mutually exclusive[/red]")
        sys.exit(1)

    # Validate environment
    config.validate_env()

    # Get session config (may prompt for model selection once, even in batch mode)
    session_config = config.get_session_config(ollama_model=args.ollama_model)

    # Initialize LLM router
    llm = LLMRouter(session_config)

    # ── Batch mode ────────────────────────────────────────────────────────────
    if args.batch is not None:
        batch_folder = Path(args.batch)
        if not batch_folder.is_dir():
            console.print(f"[red][!] Batch folder not found: {batch_folder}[/red]")
            sys.exit(1)

        # Prefer files matching *problem.md; fall back to all .md files
        problem_files = sorted(batch_folder.glob("*problem.md"))
        if not problem_files:
            problem_files = sorted(batch_folder.glob("*.md"))

        if not problem_files:
            console.print(f"[red][!] No .md files found in {batch_folder}[/red]")
            sys.exit(1)

        # ── Resume detection ──────────────────────────────────────────────────
        folder_key = str(batch_folder.resolve())
        prev_state = _load_batch_states().get(folder_key)
        completed_files: set[str] = set()
        failed_files: set[str] = set()
        resume = False

        if prev_state:
            n_done = len(prev_state.get("completed", []))
            n_failed = len(prev_state.get("failed", []))
            prev_updated = prev_state.get("updated_at", prev_state.get("started_at", "?"))
            prev_mode = prev_state.get("mode", "?")
            prev_iters = prev_state.get("iterations", "?")

            console.print(
                Panel(
                    f"[bold yellow]PREVIOUS BATCH STATE FOUND[/bold yellow]\n\n"
                    f"  Last updated  : {prev_updated}\n"
                    f"  Mode          : {prev_mode}  (iterations: {prev_iters})\n"
                    f"  Completed     : {n_done} / {len(problem_files)}\n"
                    f"  Failed        : {n_failed}\n\n"
                    f"[bold](r)[/bold] Resume  — skip completed problems, re-run the rest\n"
                    f"[bold](s)[/bold] Restart — clear state, start from scratch\n"
                    f"[bold](c)[/bold] Cancel",
                    expand=False,
                )
            )

            while True:
                choice = input("Choice (r/s/c): ").strip().lower()
                if choice in ("r", "s", "c"):
                    break
                console.print("[yellow]Please enter r, s, or c[/yellow]")

            if choice == "c":
                console.print("[yellow]Cancelled.[/yellow]")
                sys.exit(0)
            elif choice == "r":
                resume = True
                completed_files = set(prev_state.get("completed", []))
                failed_files = set(prev_state.get("failed", []))
                console.print(
                    f"[cyan][>] Resuming — {len(completed_files)} problem(s) will be skipped "
                    f"(unless their output files were deleted)[/cyan]"
                )
            else:
                _clear_batch_state(folder_key)
                console.print("[cyan][>] Starting fresh[/cyan]")

        console.print(
            Panel(
                f"[bold]BATCH MODE[/bold]\n\n"
                f"Mode: {args.mode}\n"
                f"Folder: {batch_folder}\n"
                f"Files found: {len(problem_files)}",
                expand=False,
            )
        )

        # Initialise (or continue) persisted state
        now = datetime.now().isoformat(timespec="seconds")
        state: dict = {
            "mode": args.mode,
            "iterations": args.iterations,
            "batch_folder": str(batch_folder.resolve()),
            "started_at": (prev_state.get("started_at", now) if resume and prev_state else now),
            "updated_at": now,
            "completed": list(completed_files),
            "failed": list(failed_files),
        }
        _save_batch_state(folder_key, state)

        results: list[dict] = []

        for problem_file in problem_files:
            filename = problem_file.name
            label = label_from_problem_file(problem_file)

            # Resume: skip completed problems — but re-run if output was manually deleted
            if resume and filename in completed_files:
                if _is_experiment_complete(label, args.mode):
                    console.print(f"[dim][>] Skipping (already done): {filename}[/dim]")
                    results.append({"file": filename, "status": "skipped"})
                    continue
                else:
                    console.print(
                        f"[yellow][>] Re-running (output missing or incomplete): {filename}[/yellow]"
                    )
                    completed_files.discard(filename)

            console.print(f"\n[cyan][>] Processing:[/cyan] {filename}")

            try:
                problem_md = problem_file.read_text(encoding="utf-8")
                if args.mode == "standard":
                    run_standard_research(problem_md, label, session_config, llm)
                else:
                    if args.iterations < 1:
                        console.print("[red][!] Iterations must be >= 1[/red]")
                        sys.exit(1)
                    run_breakthrough_research(
                        problem_md, label, session_config, llm, args.iterations
                    )

                results.append({"file": filename, "status": "success"})
                completed_files.add(filename)
                failed_files.discard(filename)

            except KeyboardInterrupt:
                console.print("\n[yellow][!] Batch interrupted (Ctrl+C)[/yellow]")
                results.append({"file": filename, "status": "interrupted"})
                state.update({
                    "updated_at": datetime.now().isoformat(timespec="seconds"),
                    "completed": list(completed_files),
                    "failed": list(failed_files),
                })
                _save_batch_state(folder_key, state)
                _print_batch_summary(results)
                remaining = sum(
                    1 for f in problem_files
                    if f.name not in {r["file"] for r in results}
                )
                console.print(
                    f"[yellow]Progress saved. {remaining} problem(s) remaining.[/yellow]\n"
                    f"[yellow]Run the same command again to resume from here.[/yellow]"
                )
                sys.exit(0)

            except Exception as e:
                console.print(f"[red][!] Failed: {filename} — {e}[/red]")
                results.append({"file": filename, "status": f"failed: {e}"})
                failed_files.add(filename)
                completed_files.discard(filename)

            # Persist progress after every problem (success or failure)
            state.update({
                "updated_at": datetime.now().isoformat(timespec="seconds"),
                "completed": list(completed_files),
                "failed": list(failed_files),
            })
            _save_batch_state(folder_key, state)

        # All problems processed — remove state so the next run starts fresh
        _clear_batch_state(folder_key)
        _print_batch_summary(results)
        succeeded = sum(1 for r in results if r["status"] in ("success", "skipped"))
        sys.exit(0 if succeeded == len(results) else 1)

    # ── Single-file mode ──────────────────────────────────────────────────────
    problem_path = args.problem if args.problem is not None else "problem.md"
    problem_file = Path(problem_path)
    if not problem_file.exists():
        console.print(f"[red][!] Problem file not found: {problem_file}[/red]")
        sys.exit(1)

    problem_md = problem_file.read_text(encoding="utf-8")
    console.print(f"[green][+][/green] Loaded problem from {problem_path}")

    label = label_from_problem_file(problem_file)

    try:
        if args.mode == "standard":
            run_standard_research(problem_md, label, session_config, llm)
        else:  # breakthrough
            if args.iterations < 1:
                console.print("[red][!] Iterations must be >= 1[/red]")
                sys.exit(1)
            run_breakthrough_research(
                problem_md, label, session_config, llm, args.iterations
            )

    except KeyboardInterrupt:
        console.print("\n[yellow][!] Research interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red][!] Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ── Research runners ──────────────────────────────────────────────────────────

def run_standard_research(problem_md: str, label: str, session_config: dict, llm: LLMRouter):
    """Run standard mode research.

    Args:
        problem_md: Problem statement
        label: Label derived from the problem file name (used in folder naming)
        session_config: Session configuration dict
        llm: LLMRouter instance
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_dir = Path("experiments") / "standard" / f"{label} - {timestamp}"
    experiment_dir.mkdir(parents=True, exist_ok=True)

    console.print(
        Panel(
            f"[bold]STANDARD MODE RESEARCH[/bold]\n\n"
            f"Problem: {label}\n"
            f"Results: {experiment_dir}",
            expand=False,
        )
    )

    past_context = build_past_context(problem_md, llm)
    tracker = ExperimentTracker(experiment_dir)
    evaluation = run_standard_loop(problem_md, experiment_dir, llm, tracker, past_context=past_context)

    console.print(
        Panel(
            f"[bold green]✓ RESEARCH COMPLETE[/bold green]\n\n"
            f"Results saved to: {experiment_dir}\n"
            f"Status: {tracker.meta.get('status', 'completed')}\n"
            f"Breakthrough: {evaluation.get('breakthrough_achieved', False)}",
            expand=False,
        )
    )


def run_breakthrough_research(
    problem_md: str,
    label: str,
    session_config: dict,
    llm: LLMRouter,
    n_iterations: int,
):
    """Run breakthrough mode research.

    Args:
        problem_md: Initial problem statement
        label: Label derived from the problem file name (used in folder naming)
        session_config: Session configuration dict
        llm: LLMRouter instance
        n_iterations: Number of iterations
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = Path("experiments") / "breakthrough" / f"{label} - {timestamp}"
    base_dir.mkdir(parents=True, exist_ok=True)

    console.print(
        Panel(
            f"[bold]BREAKTHROUGH MODE RESEARCH[/bold]\n\n"
            f"Problem: {label}\n"
            f"Iterations: {n_iterations}\n"
            f"Results: {base_dir}",
            expand=False,
        )
    )

    history = run_breakthrough_loop(problem_md, base_dir, llm, n_iterations=n_iterations)
    report_file = generate_breakthrough_report(base_dir, problem_title=f"Research: {label}")

    breakthrough_achieved = any(r["evaluation"].get("breakthrough_achieved") for r in history)
    status = "BREAKTHROUGH" if breakthrough_achieved else "COMPLETED"

    console.print(
        Panel(
            f"[bold green]✓ BREAKTHROUGH RESEARCH COMPLETE[/bold green]\n\n"
            f"Iterations: {len(history)}/{n_iterations}\n"
            f"Status: {status}\n"
            f"Results: {base_dir}\n"
            f"Report: {report_file}",
            expand=False,
        )
    )

    console.print(f"\n[cyan]Open report in browser:[/cyan]\n  {report_file.resolve()}")


if __name__ == "__main__":
    main()
