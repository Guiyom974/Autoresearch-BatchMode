"""Research loop orchestration (standard and breakthrough modes)."""

from pathlib import Path

import openai
from rich.console import Console
from rich.panel import Panel

from .experiment import ExperimentRunner
from .llm import LLMRouter
from .tracker import BreakthroughTracker, ExperimentTracker

console = Console()


def build_past_context(problem_md: str, llm: LLMRouter) -> str:
    """Build relevant past-experiment context for a new problem using a two-step filter.

    Step 1 — name filter: sends all experiment folder names to the context-assessment
    model and asks which ones are likely relevant based on their Category - Topic label alone.
    This is fast and requires no file I/O beyond a directory listing.

    Step 2 — content read: reads the final evaluation of each selected experiment's
    last run, then asks the model to extract the specific insight that applies to
    the current problem.

    Args:
        problem_md: Current problem statement
        llm: LLMRouter instance (uses its ollama_client directly)

    Returns:
        Formatted past-context string, or "" if nothing relevant found
    """
    experiments_dir = Path("experiments")
    if not experiments_dir.exists():
        return ""

    context_model = llm.config.get("context_assessment_model", "llama3.2:latest")

    # ── Step 1: collect experiment folder names (Category - Topic - timestamp) ──
    experiment_folders = []
    for mode_dir in sorted(experiments_dir.iterdir()):
        if not mode_dir.is_dir():
            continue
        for exp_dir in sorted(mode_dir.iterdir()):
            if not exp_dir.is_dir():
                continue
            # Only include folders that have at least one run
            if any(exp_dir.glob("run_*")):
                experiment_folders.append(exp_dir)

    if not experiment_folders:
        return ""

    folder_lines = "\n".join(
        f"{i + 1}. {f.parent.name}/{f.name}"
        for i, f in enumerate(experiment_folders)
    )

    console.print(
        f"[cyan][*] Step 1: Screening {len(experiment_folders)} experiment folder(s) "
        f"by name with {context_model}...[/cyan]"
    )

    name_filter_prompt = f"""You are a research assistant screening past experiments by name.

NEW RESEARCH PROBLEM (first 600 chars):
{problem_md[:600]}

PAST EXPERIMENT FOLDERS (numbered, format: mode/Category - Topic - timestamp):
{folder_lines}

TASK:
List the numbers of folders that are likely to contain findings relevant to the new problem.
A folder is relevant if its Category and Topic suggest the same or closely related research domain.
Be selective — only include folders where the topic overlap is clear.

Output ONLY a comma-separated list of folder numbers, e.g.: 3, 7, 12
If none are relevant, output: NONE"""

    try:
        name_resp = llm.ollama_client.chat.completions.create(
            model=context_model,
            messages=[{"role": "user", "content": name_filter_prompt}],
            temperature=0.1,
            extra_body={"options": {"num_ctx": 131_072}},
        )
        name_selection = name_resp.choices[0].message.content.strip()
    except openai.APIError as e:
        console.print(f"[yellow][!] Name-based screening failed ({e}) — skipping past context[/yellow]")
        return ""

    if "NONE" in name_selection.upper():
        console.print("[cyan][*] No relevant past experiments found by name[/cyan]")
        return ""

    # Parse selected indices
    import re as _re
    selected_indices = []
    for token in _re.split(r"[,\s]+", name_selection):
        token = token.strip().rstrip(".")
        try:
            idx = int(token) - 1
            if 0 <= idx < len(experiment_folders):
                selected_indices.append(idx)
        except ValueError:
            continue

    if not selected_indices:
        console.print("[cyan][*] Could not parse folder selection — skipping past context[/cyan]")
        return ""

    selected_folders = [experiment_folders[i] for i in selected_indices]
    console.print(
        f"[cyan][*] Step 2: Reading evaluations from {len(selected_folders)} selected "
        f"experiment(s)...[/cyan]"
    )

    # ── Step 2: read the last-run evaluation from each selected folder ──
    candidate_runs = []
    for exp_dir in selected_folders:
        runs = sorted(exp_dir.glob("run_*"))
        if not runs:
            continue
        last_run = runs[-1]
        eval_file = last_run / "07_evaluation.md"
        if not eval_file.exists():
            continue
        try:
            eval_text = eval_file.read_text(encoding="utf-8", errors="replace")[:700]
        except Exception:
            continue
        candidate_runs.append({
            "label": f"{exp_dir.parent.name}/{exp_dir.name}/{last_run.name}",
            "evaluation": eval_text,
        })

    if not candidate_runs:
        console.print("[cyan][*] Selected folders have no readable evaluations[/cyan]")
        return ""

    # Ask the context model to extract the specific insight for each candidate
    runs_text = ""
    for i, run in enumerate(candidate_runs, 1):
        runs_text += (
            f"\n--- EXPERIMENT {i}: {run['label']} ---\n"
            f"{run['evaluation']}\n"
        )

    insight_prompt = f"""You are a research assistant extracting relevant findings from past experiments.

NEW RESEARCH PROBLEM (first 600 chars):
{problem_md[:600]}

SELECTED PAST EXPERIMENTS:
{runs_text}

TASK:
For each experiment, extract the specific finding that is useful for the new problem.
Only include experiments whose findings genuinely inform a hypothesis or approach.

For EACH useful experiment output exactly one line:
EXP <number> | RELEVANT | <one sentence: what finding is useful and why>

Skip experiments with no usable finding. Be concise."""

    try:
        insight_resp = llm.ollama_client.chat.completions.create(
            model=context_model,
            messages=[{"role": "user", "content": insight_prompt}],
            temperature=0.2,
            extra_body={"options": {"num_ctx": 131_072}},
        )
        assessment = insight_resp.choices[0].message.content
    except openai.APIError as e:
        console.print(f"[yellow][!] Insight extraction failed ({e}) — skipping past context[/yellow]")
        return ""

    # Parse and build context string
    relevant_sections = []
    for line in assessment.splitlines():
        line = line.strip()
        if not line.startswith("EXP ") or "| RELEVANT |" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        try:
            run_idx = int(parts[0].replace("EXP", "").strip()) - 1
            insight = parts[2] if len(parts) > 2 else ""
            if 0 <= run_idx < len(candidate_runs):
                run = candidate_runs[run_idx]
                relevant_sections.append(
                    f"[Past finding — {run['label']}]\n"
                    f"Relevance: {insight}\n"
                    f"Details:\n{run['evaluation'][:500]}"
                )
        except (ValueError, IndexError):
            continue

    if not relevant_sections:
        console.print("[cyan][*] No relevant findings extracted from selected experiments[/cyan]")
        return ""

    console.print(f"[green][+][/green] {len(relevant_sections)} relevant past finding(s) added to context")
    header = "=== RELEVANT PRIOR FINDINGS (selected by AI review) ===\n"
    return header + "\n\n".join(relevant_sections)


def run_standard_loop(
    problem_md: str,
    experiment_dir: Path,
    llm: LLMRouter,
    tracker: ExperimentTracker,
    past_context: str = "",
) -> dict:
    """Run a single standard research loop.

    Args:
        problem_md: Problem statement (markdown)
        experiment_dir: Directory to save artifacts
        llm: LLMRouter instance
        tracker: ExperimentTracker instance
        past_context: Relevant findings from past runs (injected into hypothesis + code gen)

    Returns:
        Evaluation dict
    """
    console.print(Panel("[bold]RESEARCH LOOP: STANDARD MODE[/bold]", expand=False))

    # Step 1: Log problem
    tracker.log_step("problem", problem_md)
    tracker.log_meta({"mode": "standard"})

    # Step 2: Web search
    console.print("\n[bold cyan]Step 1: Web Search[/bold cyan]")

    queries = llm.generate_search_queries(problem_md)
    tracker.log_step("search_queries", "\n".join(queries))

    search_results = ""
    for query in queries:
        result = llm.web_search(query)
        search_results += f"\n### Query: {query}\n{result}\n"

    tracker.log_step("search_results", search_results)

    # Combine web search results with relevant prior findings
    full_context = search_results
    if past_context:
        full_context = past_context + "\n\n=== WEB SEARCH RESULTS ===\n" + search_results

    # Step 3: Formulate hypotheses
    console.print("\n[bold cyan]Step 2: Hypothesis Formulation[/bold cyan]")
    hypothesis_prompt = f"""Given this research problem, search results, and any relevant prior findings, propose 3-5 testable hypotheses:

PROBLEM:
{problem_md}

CONTEXT (web search + prior findings):
{full_context[:8000]}

For each hypothesis, explain:
1. The hypothesis statement
2. Why it's testable
3. What kind of experiment would test it
Note: If prior findings are present, build on them — do not repeat experiments that already produced clear results."""

    hypotheses = llm.reason(hypothesis_prompt)
    tracker.log_step("hypotheses", hypotheses)

    # Step 4: Generate experiment code
    console.print("\n[bold cyan]Step 3: Code Generation[/bold cyan]")
    runner = ExperimentRunner(llm, experiment_dir)
    code, output, success = runner.run_full_experiment(
        problem_md, hypotheses, full_context
    )

    tracker.log_step("experiment_code", code)
    tracker.log_step("run_output", output)

    # Step 5: Evaluate results
    console.print("\n[bold cyan]Step 4: Results Evaluation[/bold cyan]")
    evaluation = llm.evaluate(output, problem_md)

    eval_text = f"""## Evaluation Summary

**Breakthrough Achieved**: {evaluation.get('breakthrough_achieved', False)}
**Confidence**: {evaluation.get('confidence', 0.0):.1%}
**Publishability Score**: {evaluation.get('publishability_score', 0.0):.1f}/10

**Summary**:
{evaluation.get('summary', 'N/A')}

**Next Directions**:
{chr(10).join(f"- {d}" for d in evaluation.get('next_directions', []))}"""

    tracker.log_step("evaluation", eval_text)
    tracker.finalize(
        status="breakthrough" if evaluation.get("breakthrough_achieved") else "completed",
        evaluation=evaluation,
    )

    return evaluation


def run_breakthrough_loop(
    problem_md: str,
    base_dir: Path,
    llm: LLMRouter,
    n_iterations: int = 3,
) -> list[dict]:
    """Run breakthrough research loop with iterative problem reformulation.

    Args:
        problem_md: Initial problem statement
        base_dir: Base directory for breakthrough experiments
        llm: LLMRouter instance
        n_iterations: Max iterations (may stop early if breakthrough achieved)

    Returns:
        List of evaluation dicts from each iteration
    """
    console.print(Panel(f"[bold]RESEARCH LOOP: BREAKTHROUGH MODE ({n_iterations} iterations)[/bold]", expand=False))

    bt_tracker = BreakthroughTracker(base_dir, mode="breakthrough")
    history = []
    current_problem = problem_md

    for iteration in range(1, n_iterations + 1):
        console.print(f"\n[bold yellow]=== ITERATION {iteration}/{n_iterations} ===[/bold yellow]")

        # Create run directory
        run_dir = bt_tracker.create_run_dir(iteration)

        # Log original/reformulated problem
        is_reformulated = iteration > 1
        bt_tracker.log_problem_version(iteration, current_problem, modified=is_reformulated)

        # Assess past runs for relevant context
        console.print("\n[bold cyan]Step 0: Past Run Review[/bold cyan]")
        past_context = build_past_context(current_problem, llm)

        # Run standard loop
        tracker = ExperimentTracker(run_dir)
        evaluation = run_standard_loop(current_problem, run_dir, llm, tracker, past_context=past_context)
        history.append({"iteration": iteration, "evaluation": evaluation})

        # Check for breakthrough — requires LLM flag, confidence >= 90%, and publishability >= 7
        _CONFIDENCE_THRESHOLD = 0.90
        _PUBLISHABILITY_THRESHOLD = 7.0
        confidence = evaluation.get("confidence", 0.0)
        pub_score = evaluation.get("publishability_score", 0.0)
        is_breakthrough = (
            evaluation.get("breakthrough_achieved")
            and confidence >= _CONFIDENCE_THRESHOLD
            and pub_score >= _PUBLISHABILITY_THRESHOLD
        )

        if not is_breakthrough and evaluation.get("breakthrough_achieved"):
            console.print(
                f"\n[yellow][~] LLM flagged breakthrough but did not meet thresholds "
                f"(confidence={confidence:.0%}, publishability={pub_score:.1f}/10 "
                f"— need >={_CONFIDENCE_THRESHOLD:.0%} and >={_PUBLISHABILITY_THRESHOLD})[/yellow]"
            )

        if is_breakthrough:
            console.print(
                f"\n[bold green][+] BREAKTHROUGH ACHIEVED at iteration {iteration}![/bold green]"
            )
            bt_tracker.finalize(final_status="breakthrough")

            # Generate next-level problem using the evaluation model
            next_problem = llm.generate_next_problem(problem_md, evaluation)
            if next_problem:
                next_problem_path = Path("problem-new.md")
                next_problem_path.write_text(next_problem, encoding="utf-8")
                console.print(
                    f"[green][+][/green] Next problem saved to: [bold]{next_problem_path.resolve()}[/bold]"
                )
            return history

        # Reformulate problem for next iteration (if not last)
        if iteration < n_iterations:
            console.print("\n[bold cyan]Reformulating problem for next iteration...[/bold cyan]")

            # Only pass research-relevant summary, not execution errors
            summary = evaluation.get("summary", "No findings")
            next_dirs = evaluation.get("next_directions", [])
            experiment_output = (run_dir / "06_run_output.txt").read_text(encoding="utf-8") if (run_dir / "06_run_output.txt").exists() else ""

            # Strip infrastructure errors from output before sending to reformulation
            research_output = "\n".join(
                line for line in experiment_output.splitlines()
                if not any(kw in line for kw in ["FileNotFoundError", "Traceback", "Error:", "STDERR", ".py line"])
            )[:1500]

            reformulate_prompt = f"""You are a research director. Reformulate the research problem below to pursue a more promising direction based on experimental findings.

ORIGINAL TOPIC (do NOT change the domain — stay on this research subject):
{problem_md[:800]}

CURRENT PROBLEM STATEMENT:
{current_problem[:600]}

FINDINGS FROM THIS ITERATION:
{summary}

SUGGESTED NEXT DIRECTIONS:
{chr(10).join(f'- {d}' for d in next_dirs)}

RESEARCH OUTPUT (partial):
{research_output if research_output.strip() else "(experiment did not produce output — keep the same research domain, tighten scope)"}

TASK:
Write a new problem.md that:
1. Stays strictly within the original research domain (do NOT introduce unrelated topics)
2. Focuses on one of the suggested directions above
3. Uses the same markdown sections: Objective, Research Questions, Methodology, Success Criteria, Constraints
4. Is more specific and targeted than the previous version
5. Ignores any Python or file-system errors — focus only on the science"""

            current_problem = llm.reformulate(reformulate_prompt)

    # Finalize without breakthrough
    bt_tracker.finalize(final_status="completed")
    console.print("\n[yellow][!] Max iterations reached without breakthrough[/yellow]")
    return history
