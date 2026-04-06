"""Experiment tracking and artifact logging."""

import json
from datetime import datetime
from pathlib import Path

from rich.console import Console

console = Console()


class ExperimentTracker:
    """Tracks and logs all steps of a research experiment."""

    def __init__(self, experiment_dir: Path):
        """Initialize tracker for an experiment directory.

        Args:
            experiment_dir: Path to experiment folder
        """
        self.experiment_dir = Path(experiment_dir)
        self.experiment_dir.mkdir(parents=True, exist_ok=True)
        self.step_counter = 0
        self.meta = {
            "start_time": datetime.now().isoformat(),
            "mode": None,
            "models": {},
            "status": "in_progress",
        }

    def log_step(self, name: str, content: str, step_name: str = None) -> Path:
        """Log a research step to disk.

        Args:
            name: Step name (e.g., "search_results", "experiment_code")
            content: Step content (markdown, python, or text)
            step_name: Custom step description

        Returns:
            Path to written file
        """
        self.step_counter += 1

        # Determine file extension based on content type
        if content.strip().startswith("import ") or content.strip().startswith("from "):
            ext = ".py"
        elif name in ["experiment_code"]:
            ext = ".py"
        elif name in ["run_output", "error"]:
            ext = ".txt"
        else:
            ext = ".md"

        filename = (
            f"{self.step_counter:02d}_{name}{ext}"
            if not step_name
            else f"{self.step_counter:02d}_{step_name}{ext}"
        )
        filepath = self.experiment_dir / filename

        filepath.write_text(content, encoding="utf-8")
        console.print(f"[dim]  saved: {filename}[/dim]")

        return filepath

    def log_meta(self, meta_updates: dict) -> None:
        """Update experiment metadata.

        Args:
            meta_updates: Dict of metadata to update/merge
        """
        self.meta.update(meta_updates)

    def finalize(self, status: str = "completed", evaluation: dict = None) -> None:
        """Finalize and save experiment metadata.

        Args:
            status: Final status ("completed", "failed", "breakthrough")
            evaluation: Evaluation dict with results
        """
        self.meta["end_time"] = datetime.now().isoformat()
        self.meta["status"] = status

        if evaluation:
            self.meta["evaluation"] = evaluation

        meta_file = self.experiment_dir / "meta.json"
        meta_file.write_text(json.dumps(self.meta, indent=2), encoding="utf-8")

        console.print(
            f"[dim]  meta: {self.step_counter} steps, status={status}[/dim]"
        )


class BreakthroughTracker:
    """Tracks breakthrough mode experiments with iteration history."""

    def __init__(self, base_dir: Path, mode: str = "breakthrough"):
        """Initialize breakthrough tracker.

        Args:
            base_dir: Base directory for breakthrough experiments
            mode: "breakthrough" or "standard"
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir = self.base_dir / "history"
        self.history_dir.mkdir(exist_ok=True)
        self.mode = mode
        self.iteration = 0
        self.meta = {
            "start_time": datetime.now().isoformat(),
            "mode": mode,
            "iterations": [],
        }

    def create_run_dir(self, iteration: int) -> Path:
        """Create directory for a specific iteration run.

        Args:
            iteration: Iteration number (1-indexed)

        Returns:
            Path to run directory
        """
        self.iteration = iteration
        run_dir = self.base_dir / f"run_{iteration:03d}"
        run_dir.mkdir(exist_ok=True)
        return run_dir

    def log_problem_version(
        self, iteration: int, problem_md: str, modified: bool = False
    ) -> None:
        """Log a version of the problem statement.

        Args:
            iteration: Iteration number
            problem_md: Problem statement content
            modified: True if this is a reformulated version
        """
        marker = "[REFORMULATED]" if modified else "[ORIGINAL]"
        timestamp = datetime.now().isoformat()

        # Append to history file
        history_file = self.history_dir / "problem_versions.md"
        with open(history_file, "a", encoding="utf-8") as f:
            f.write(f"\n## Iteration {iteration} {marker}\n")
            f.write(f"Timestamp: {timestamp}\n\n")
            f.write(problem_md)
            f.write("\n\n---\n")

        console.print(f"[dim]  history: problem v{iteration} saved[/dim]")

    def finalize(self, final_status: str = "completed") -> None:
        """Finalize breakthrough experiment.

        Args:
            final_status: Final status
        """
        self.meta["end_time"] = datetime.now().isoformat()
        self.meta["final_status"] = final_status
        self.meta["total_iterations"] = self.iteration

        meta_file = self.base_dir / "meta.json"
        meta_file.write_text(json.dumps(self.meta, indent=2), encoding="utf-8")

        console.print(
            f"[dim]  meta: {self.iteration} iterations, status={final_status}[/dim]"
        )
