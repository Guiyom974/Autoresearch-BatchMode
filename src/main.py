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

  launch.bat standard --ollama-model llama3.2
    Use a specific Ollama model (skips model selection menu)

  launch.bat breakthrough --iterations 3
    Run 3 iterations with problem reformulation between each

  launch.bat breakthrough --iterations 5 --problem my_research.md
    Custom research problem with 5 breakthrough iterations

  launch.bat standard --batch "problem a/"
    Run standard mode on every *problem.md in the problem a/ folder

  launch.bat breakthrough --batch "problem a/" --iterations 5
    Run breakthrough mode (5 iterations) on every *problem.md in problem a/

FEATURES:
  - Web search via cloud API (Poe Web-Search model or any provider with browsing)
  - Code generation & execution with local Ollama
  - Problem reformulation via cloud API
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

    # Get session config (may prompt for Ollama model once, even in batch mode)
    session_config = config.get_session_config(ollama_model=args.ollama_model)

    # Initialize LLM router
    llm = LLMRouter(session_config)

    # ── Batch mode ──────────────────────────────────────────────────────────
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
            console.print(f"\n[cyan][>] Processing:[/cyan] {problem_file.name}")
            label = label_from_problem_file(problem_file)
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
                results.append({"file": problem_file.name, "status": "success"})
            except KeyboardInterrupt:
                console.print("\n[yellow][!] Batch interrupted by user[/yellow]")
                results.append({"file": problem_file.name, "status": "interrupted"})
                break
            except Exception as e:
                console.print(f"[red][!] Failed: {problem_file.name} — {e}[/red]")
                results.append({"file": problem_file.name, "status": f"failed: {e}"})

        # Batch summary
        console.print("\n")
        console.print(
            Panel(
                "[bold]BATCH SUMMARY[/bold]\n\n"
                + "\n".join(
                    f"  {'[green]OK [/green]' if r['status'] == 'success' else '[red]ERR[/red]'} "
                    f"{r['file']}  →  {r['status']}"
                    for r in results
                ),
                expand=False,
            )
        )
        succeeded = sum(1 for r in results if r["status"] == "success")
        console.print(f"[green]{succeeded}[/green] / {len(results)} succeeded")
        sys.exit(0 if succeeded == len(results) else 1)

    # ── Single-file mode ─────────────────────────────────────────────────────
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


def run_standard_research(problem_md: str, label: str, session_config: dict, llm: LLMRouter):
    """Run standard mode research.

    Args:
        problem_md: Problem statement
        label: Label derived from the problem file name (used in folder naming)
        session_config: Session configuration dict
        llm: LLMRouter instance
    """
    # Create experiment directory
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

    # Assess past runs for relevant context
    past_context = build_past_context(problem_md, llm)

    # Run research
    tracker = ExperimentTracker(experiment_dir)
    evaluation = run_standard_loop(problem_md, experiment_dir, llm, tracker, past_context=past_context)

    # Print summary
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
    # Create breakthrough directory
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

    # Run breakthrough loop
    history = run_breakthrough_loop(problem_md, base_dir, llm, n_iterations=n_iterations)

    # Generate report
    report_file = generate_breakthrough_report(base_dir, problem_title=f"Research: {label}")

    # Print summary
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
