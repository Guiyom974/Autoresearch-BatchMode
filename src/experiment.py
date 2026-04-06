"""Experiment execution and code generation."""

import os
import re
import subprocess
from pathlib import Path

from rich.console import Console

from .llm import LLMRouter

console = Console()

CODE_TAG = "!@#$"


def _extract_tagged_code(text: str) -> str:
    """Extract code between !@#$ tags.

    Strategy order (most to least reliable):
    1. Last complete !@#$...!@#$ pair — model may echo template first, answer is last
    2. Everything after the LAST lone !@#$ tag (model forgot closing tag)
    3. Last ```python...``` block
    4. Last ```...``` block
    5. Raw text stripped of any stray !@#$ markers
    """
    # Strategy 1: complete pairs — take LAST
    matches = re.findall(r'!@#\$(.*?)!@#\$', text, re.DOTALL)
    if matches:
        return matches[-1].strip()

    # Strategy 2: unclosed tag — take everything after the LAST !@#$
    if "!@#$" in text:
        after = text.rsplit("!@#$", 1)[-1].strip()
        if after and len(after) > 20:
            return after

    # Strategy 3: last ```python block
    if "```python" in text:
        parts = text.split("```python")
        candidate = parts[-1].split("```")[0].strip()
        if candidate:
            return candidate

    # Strategy 4: last ``` block
    if "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            candidate = parts[-2].strip()
            if candidate:
                return candidate

    # Strategy 5: strip any stray !@#$ markers from raw text
    return text.replace("!@#$", "").strip()


_POLICY_BLOCK_PHRASES = (
    "blocked for potentially violating",
    "safety policies",
    "i apologize for any inconvenience",
    "content policy",
    "i cannot",
    "i'm unable to",
    "i am unable to",
)

_HTML_ERROR_MARKERS = (
    "<html",
    "<!doctype",
    "<head>",
    "<h1>502",
    "<h1>503",
    "<h1>504",
    "<h1>500",
    "bad gateway",
    "service unavailable",
)


def _is_failed_code(code: str) -> bool:
    """Return True if code is an error placeholder, policy block, HTML error, or API sentinel."""
    stripped = code.strip()
    lower = stripped.lower()
    return (
        stripped.startswith("# Failed")
        or stripped.startswith("# TRUNCATED")
        or stripped.startswith("API error:")
        or stripped.startswith("Failed to")
        or len(stripped) < 20
        or any(phrase in lower for phrase in _POLICY_BLOCK_PHRASES)
        or any(marker in lower[:500] for marker in _HTML_ERROR_MARKERS)
    )


def _is_truncated(code: str) -> bool:
    """Return True if code appears to be cut off mid-generation.

    Detects:
    - Last non-empty line ends with incomplete compound statement (no body)
    - Unbalanced parentheses/brackets/braces
    - Last non-empty line is a bare keyword or partial expression
    """
    lines = [l for l in code.splitlines() if l.strip()]
    if not lines:
        return False

    last = lines[-1].rstrip()

    # Ends with colon → block header with no body below it
    if last.endswith(":"):
        return True

    # Ends with a backslash continuation
    if last.endswith("\\"):
        return True

    # Ends with comma or open bracket/paren (mid-argument list)
    if last.endswith(",") or last.endswith("(") or last.endswith("[") or last.endswith("{"):
        return True

    # Unbalanced brackets across entire code
    if code.count("(") != code.count(")"):
        return True
    if code.count("[") != code.count("]"):
        return True
    if code.count("{") != code.count("}"):
        return True

    # No main guard at all (incomplete script — less reliable, but log-worthy)
    # We only flag this as truncation if code is suspiciously short
    if 'if __name__' not in code and len(code) < 500:
        return True

    return False


class ExperimentRunner:
    """Generates and executes research experiments."""

    def __init__(self, llm: LLMRouter, experiment_dir: Path):
        self.llm = llm
        self.experiment_dir = Path(experiment_dir)

    def _code_prompt(self, problem: str, hypotheses: str, context: str = "") -> str:
        return f"""Write a self-contained Python script to test these research hypotheses.

RESEARCH PROBLEM:
{problem[:600]}

HYPOTHESES TO TEST:
{hypotheses[:800]}

CONTEXT:
{context[:2000] if context else "(none)"}

STRICT REQUIREMENTS:
1. ONLY use these pre-installed libraries: stdlib, numpy, matplotlib, scipy
   — no pip install, no external downloads, no other third-party packages
2. Print clear labeled results for each hypothesis tested
3. For plots: use matplotlib.use('Agg') then savefig() — NEVER plt.show()
4. Print a CONCLUSIONS section at the end
5. Max runtime: 2 minutes — use efficient algorithms (segmented sieve, vectorised numpy)
6. Handle all edge cases — no unhandled exceptions
7. CRITICAL: The script MUST be complete and syntactically valid Python. Every function, class,
   and if-block must have a full body. Do not stop mid-function. If you are running long, simplify
   earlier sections — but always finish the script with the CONCLUSIONS print and a proper ending.
8. Be CONCISE: Avoid verbose comments and unnecessary complexity. Focus on the core logic.

OUTPUT FORMAT:
You MUST wrap the complete Python script between exactly two {CODE_TAG} markers:
{CODE_TAG}
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
# ... rest of your code ...
print("CONCLUSIONS: ...")
{CODE_TAG}
The {CODE_TAG} markers must appear on their own line.
Do NOT output anything before the first {CODE_TAG} or after the last {CODE_TAG}.

IMPORTANT: Generate the COMPLETE script in one response. Do not truncate or stop mid-code."""

    def _fix_prompt(self, code: str, error_output: str, problem: str) -> str:
        is_timeout = "[TIMEOUT]" in error_output
        timeout_rule = (
            "\n- TIMEOUT: The script ran too long. Drastically simplify: reduce N (e.g. primes up to 10^5 not 10^6), "
            "use faster algorithms (segmented sieve, vectorised numpy), remove nested loops over large arrays. "
            "Ensure total runtime is well under 4 minutes."
            if is_timeout else ""
        )
        return f"""Fix this failing Python script so it runs without errors.

RESEARCH PROBLEM (do NOT change domain — only fix the code):
{problem[:400]}

FAILING CODE:
{CODE_TAG}
{code}
{CODE_TAG}

ERROR OUTPUT:
{error_output}

RULES:
- Fix ONLY the errors shown — do not change what is being researched
- All imports must be at the top
- No plt.show() — use savefig() instead
- Script must be fully self-contained
- Use sys.stdout.reconfigure(encoding='utf-8', errors='replace') right after imports to avoid encoding errors{timeout_rule}

OUTPUT FORMAT — wrap the complete corrected script between exactly two {CODE_TAG} markers:
{CODE_TAG}
# fixed code here
{CODE_TAG}
The {CODE_TAG} markers must appear on their own line.
Do NOT output anything before the first {CODE_TAG} or after the last {CODE_TAG}."""

    def generate_code(self, problem: str, hypotheses: str, context: str = "") -> str:
        """Generate experiment code, with policy-block detection + truncation check + Poe fallback."""
        code_prompt = self._code_prompt(problem, hypotheses, context)
        raw = self.llm.generate_code(code_prompt)

        if _is_failed_code(raw):
            console.print("[yellow][*] Code gen failed — retrying with same model...[/yellow]")
            raw = self.llm.generate_code(code_prompt)

        if _is_failed_code(raw):
            console.print("[yellow][*] Retry also failed — falling back to Gemini-3.1-Pro[/yellow]")
            raw = self.llm.reformulate(code_prompt)

        code = _extract_tagged_code(raw)

        # If still truncated after Poe fallback, try one more time with Gemini
        if _is_truncated(code):
            console.print("[yellow][!] Code appears truncated — retrying with Gemini-3.1-Pro...[/yellow]")
            retry_raw = self.llm.reformulate(code_prompt)
            retry_code = _extract_tagged_code(retry_raw)
            if not _is_failed_code(retry_code) and not _is_truncated(retry_code):
                code = retry_code
                console.print("[green][+][/green] Full code received on retry")
            else:
                console.print("[yellow][!] Retry also truncated — will attempt fix on error[/yellow]")

        if _is_failed_code(code):
            console.print("[red][!] Could not generate valid code[/red]")
            return "# No code generated\nprint('Code generation failed')"

        return code

    def fix_code(self, code: str, error_output: str, problem: str) -> str:
        """Ask Gemini-3.1-Pro to fix failing experiment code."""
        console.print("[yellow][*] Asking Gemini-3.1-Pro to fix the code...[/yellow]")
        fix_prompt = self._fix_prompt(code, error_output, problem)
        raw = self.llm.reformulate(fix_prompt)
        fixed = _extract_tagged_code(raw)
        if _is_failed_code(fixed):
            console.print("[red][!] Fix attempt returned invalid code[/red]")
            return code  # Return original, don't make it worse
        if _is_truncated(fixed):
            console.print("[yellow][!] Fixed code truncated — retrying fix...[/yellow]")
            raw2 = self.llm.reformulate(fix_prompt)
            fixed2 = _extract_tagged_code(raw2)
            if not _is_failed_code(fixed2) and not _is_truncated(fixed2):
                fixed = fixed2
        console.print("[green][+][/green] Fixed code received")
        return fixed

    def run_code(self, code: str, timeout: int = 300) -> tuple[str, bool]:
        """Execute Python code and capture output."""
        import ast

        # Syntax-check before running — catch !@#$ tags and syntax errors early
        try:
            ast.parse(code)
        except SyntaxError as e:
            err = f"--- STDERR ---\nSyntaxError (pre-execution check): {e}\n\nCode preview:\n{code[:300]}"
            console.print(f"[red][!] Syntax error before execution: {e}[/red]")
            return err, False

        console.print("[cyan][*] Executing experiment code...[/cyan]")

        self.experiment_dir.mkdir(parents=True, exist_ok=True)
        temp_file = self.experiment_dir / "_experiment_temp.py"
        temp_file.write_text(code, encoding="utf-8")

        # Force UTF-8 on Windows to avoid 'charmap' codec errors from Unicode in print statements
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}

        try:
            result = subprocess.run(
                ["python", temp_file.name],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                cwd=str(self.experiment_dir.resolve()),
                env=env,
            )

            output = result.stdout
            if result.stderr:
                output += f"\n--- STDERR ---\n{result.stderr}"

            success = result.returncode == 0
            console.print(
                "[green][+][/green] Experiment completed"
                if success
                else "[red][!][/red] Experiment failed"
            )
            return output, success

        except subprocess.TimeoutExpired:
            return f"[TIMEOUT] Execution exceeded {timeout}s", False
        except Exception as e:
            return f"[ERROR] {e}", False
        finally:
            if temp_file.exists():
                temp_file.unlink()

    def run_full_experiment(
        self,
        problem: str,
        hypotheses: str,
        context: str = "",
        timeout: int = 300,
        max_retries: int = 1,
    ) -> tuple[str, str, bool]:
        """Generate, run, and auto-fix experiment code on failure.

        On first failure, sends the error + code to Gemini-3.1-Pro for a fix.
        Returns (final_code, output, success).
        """
        code = self.generate_code(problem, hypotheses, context)
        output, success = self.run_code(code, timeout)

        if not success:
            for attempt in range(1, max_retries + 1):
                console.print(
                    f"[yellow][*] Retry {attempt}/{max_retries} — sending error to Gemini-3.1-Pro[/yellow]"
                )
                console.print(f"[dim]  Error: {output[:150].strip()}[/dim]")

                # If code is a policy block / empty, regenerate fully instead of trying to fix
                if _is_failed_code(code):
                    console.print("[yellow][*] Code was blocked/empty — regenerating from scratch...[/yellow]")
                    fixed_code = self.generate_code(problem, hypotheses, context)
                else:
                    fixed_code = self.fix_code(code, output, problem)
                fixed_output, fixed_success = self.run_code(fixed_code, timeout)

                if fixed_success:
                    console.print("[green][+][/green] Fixed code ran successfully")
                    return fixed_code, fixed_output, True

                code = fixed_code
                output = fixed_output

            console.print("[red][!] Experiment still failing after retry[/red]")

        return code, output, success
