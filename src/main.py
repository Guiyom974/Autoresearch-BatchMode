"""AutoResearch CLI entry point."""

import argparse
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


# ── Completion detection ──────────────────────────────────────────────────────

def _find_latest_experiment_dir(label: str, mode: str) -> Path | None:
    """Return the most recently created experiment directory for a given label and mode."""
    base = Path("experiments") / mode
    if not base.exists():
        return None
    matches = sorted(base.glob(f"{label} - *"))
    return matches[-1] if matches else None


def _is_experiment_complete(label: str, mode: str) -> bool:
    """Return True only if the experiment produced complete output artifacts on disk."""
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
        # Fallback: last run at least completed its evaluation
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


def _find_partial_breakthrough(label: str) -> tuple[Path, int] | None:
    """Return (base_dir, last_completed_iteration) for a partially-done breakthrough experiment.

    Returns None if no partial experiment exists or if the experiment is already complete.
    """
    folder = _find_latest_experiment_dir(label, "breakthrough")
    if folder is None:
        return None
    if (folder / "report.html").exists():
        return None  # fully complete
    completed_runs = [
        run for run in sorted(folder.glob("run_*"))
        if (run / "07_evaluation.md").exists()
        and len((run / "07_evaluation.md").read_text(encoding="utf-8", errors="replace")) > 50
    ]
    if not completed_runs:
        return None
    last_iter = int(completed_runs[-1].name.split("_")[-1])  # "run_003" → 3
    return folder, last_iter


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

        # ── Resume detection: scan experiment folders on disk ─────────────────
        already_done = [
            f for f in problem_files
            if _is_experiment_complete(label_from_problem_file(f), args.mode)
        ]
        resume = False

        if already_done:
            remaining = len(problem_files) - len(already_done)
            console.print(
                Panel(
                    f"[bold yellow]EXISTING RESULTS DETECTED[/bold yellow]\n\n"
                    f"  Complete : {len(already_done)} / {len(problem_files)}\n"
                    f"  Remaining: {remaining}\n\n"
                    f"Skipping completed experiments and continuing with the {remaining} missing.\n"
                    f"Type [bold]restart[/bold] to run everything from scratch instead.",
                    expand=False,
                )
            )

            choice = input("Press Enter to continue, or type 'restart': ").strip().lower()

            if choice == "restart":
                console.print("[cyan][>] Starting fresh — all problems will be re-run[/cyan]")
            else:
                resume = True
                console.print(
                    f"[cyan][>] Resuming — {len(already_done)} problem(s) will be skipped[/cyan]"
                )

        console.print(
            Panel(
                f"[bold]BATCH MODE[/bold]\n\n"
                f"Mode: {args.mode}\n"
                f"Folder: {batch_folder}\n"
                f"Files found: {len(problem_files)}",
                expand=False,
            )
        )

        results: list[dict] = []

        for problem_file in problem_files:
            filename = problem_file.name
            label = label_from_problem_file(problem_file)

            # Resume: skip fully completed problems
            if resume and _is_experiment_complete(label, args.mode):
                console.print(f"[dim][>] Skipping (already done): {filename}[/dim]")
                results.append({"file": filename, "status": "skipped"})
                continue

            console.print(f"\n[cyan][>] Processing:[/cyan] {filename}")

            try:
                problem_md = problem_file.read_text(encoding="utf-8")
                if args.mode == "standard":
                    run_standard_research(problem_md, label, session_config, llm)
                else:
                    if args.iterations < 1:
                        console.print("[red][!] Iterations must be >= 1[/red]")
                        sys.exit(1)
                    # Resume: pick up a partial breakthrough from its last completed iteration
                    existing_dir = None
                    start_iteration = 1
                    if resume:
                        partial = _find_partial_breakthrough(label)
                        if partial:
                            existing_dir, last_completed = partial
                            start_iteration = last_completed + 1
                            console.print(
                                f"[yellow][>] Resuming breakthrough at iteration "
                                f"{start_iteration} (iterations 1–{last_completed} already done)[/yellow]"
                            )
                    run_breakthrough_research(
                        problem_md, label, session_config, llm, args.iterations,
                        existing_dir=existing_dir, start_iteration=start_iteration,
                    )
                results.append({"file": filename, "status": "success"})

            except KeyboardInterrupt:
                console.print("\n[yellow][!] Batch interrupted (Ctrl+C)[/yellow]")
                results.append({"file": filename, "status": "interrupted"})
                _print_batch_summary(results)
                remaining = sum(
                    1 for f in problem_files
                    if f.name not in {r["file"] for r in results}
                )
                console.print(
                    f"[yellow]{remaining} problem(s) remaining.[/yellow]\n"
                    f"[yellow]Run the same command again — completed experiments will be detected "
                    f"automatically and skipped.[/yellow]"
                )
                sys.exit(0)

            except Exception as e:
                console.print(f"[red][!] Failed: {filename} — {e}[/red]")
                results.append({"file": filename, "status": f"failed: {e}"})

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
    """Run standard mode research."""
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
    existing_dir: Path | None = None,
    start_iteration: int = 1,
):
    """Run breakthrough mode research."""
    if existing_dir is not None:
        base_dir = existing_dir
    else:
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

    history = run_breakthrough_loop(
        problem_md, base_dir, llm, n_iterations=n_iterations, start_iteration=start_iteration
    )
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
