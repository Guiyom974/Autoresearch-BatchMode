"""LLM client management for cloud API and Ollama."""

import os
import re
import sys
from typing import Optional

import httpx
import openai
from rich.console import Console

console = Console()

# Ollama context window — set large enough to handle long past-context injections
_OLLAMA_NUM_CTX = 131_072


def _handle_api_error(e: openai.APIError, service: str = "Cloud API") -> str:
    """Handle API errors with clear messages. Exits on auth errors."""
    if isinstance(e, openai.AuthenticationError):
        console.print(
            f"[red][!] {service} authentication failed[/red]\n"
            "Your API key is invalid or expired.\n"
            "  → Update CLOUD_API_KEY in .env\n"
            "  → Verify CLOUD_BASE_URL matches your provider"
        )
        sys.exit(1)
    return f"API error: {e}"


class LLMRouter:
    """Routes requests to the configured cloud API or Ollama based on task type."""

    def __init__(self, config: dict):
        """Initialize LLM router with session config.

        Args:
            config: Dict with keys:
                - cloud_api_key
                - cloud_base_url
                - cloud_model_websearch
                - cloud_model_research
                - cloud_model_reformulate
                - ollama_base_url
        """
        self.config = config
        self.cloud_client = openai.OpenAI(
            api_key=config["cloud_api_key"],
            base_url=config["cloud_base_url"],
            timeout=120.0,  # cloud API — 2 min is generous
            max_retries=0,  # we handle retries ourselves; don't double-wait on failures
        )
        self.ollama_client = openai.OpenAI(
            api_key="ollama",  # Ollama doesn't require a real API key
            base_url=config["ollama_base_url"],
            timeout=httpx.Timeout(None),  # no timeout — local models can take arbitrarily long
            max_retries=0,
        )

    def generate_search_queries(self, problem: str) -> list[str]:
        """Generate focused web search queries using the web search model.

        Keeps query generation in the same model/backend as search itself.
        Returns a list of query strings (up to 3).
        """
        model = self.config["websearch_model"]
        console.print(f"[cyan][*] Generating search queries with {model} (cloud)...[/cyan]")

        prompt = (
            f"Generate exactly 3 web search queries to find academic and technical information "
            f"about the following research problem. Each query should target a different angle.\n\n"
            f"RESEARCH PROBLEM:\n{problem[:600]}\n\n"
            f"OUTPUT FORMAT — write exactly 3 lines, each line is one complete search query:\n"
            f"query one here\n"
            f"query two here\n"
            f"query three here\n\n"
            f"Do not number them, do not use bullets, do not add any other text."
        )
        try:
            response = self.cloud_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            raw = response.choices[0].message.content

            # Parse: strip bullets/numbers FIRST, then filter noise
            queries = []
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                # Strip leading bullets, numbers, symbols first
                q = re.sub(r'^[\d\.\-\*\)\s]+', '', line).strip()
                if not q:
                    continue
                # Skip markdown headers, horizontal rules, section labels (after bullet strip)
                if q.startswith("#") or q.startswith("---") or q.startswith("==="):
                    continue
                # Skip lines that look like labels/prefixes (e.g. "Query 1:", "Search query:")
                if re.match(r'^(query|search|q|result)\s*\d*\s*:', q, re.IGNORECASE):
                    q = re.sub(r'^[^:]+:\s*', '', q).strip()
                # Skip very short fragments or multi-line blobs
                if len(q) > 15 and "\n" not in q:
                    queries.append(q)

            queries = queries[:3]  # cap at 3

            # Pad with fallback queries if model returned fewer than 3
            if not queries:
                queries = [problem[:120]]
            fallback_suffixes = ["recent research findings", "computational methods analysis", "statistical patterns study"]
            while len(queries) < 3:
                queries.append(f"{problem[:80]} {fallback_suffixes[len(queries) - 1]}")

            console.print(f"[green][+][/green] Generated {len(queries)} search queries")
            return queries
        except openai.APIError as e:
            _handle_api_error(e)
            return [problem[:120], f"{problem[:80]} recent research", f"{problem[:80]} computational methods"]

    def web_search(self, query: str, max_results: int = 5) -> str:
        """Perform web search via the cloud API.

        Note: The web_search extra_body flag is supported by Poe's Web-Search model.
        For other providers, the model will respond without live search unless it has
        built-in browsing capabilities (e.g. Perplexity on OpenRouter).

        Args:
            query: Search query
            max_results: Max results to return (hint to model)

        Returns:
            Formatted markdown string with search results
        """
        console.print(f"[cyan][*] Web search:[/cyan] {query[:80]}...")

        try:
            response = self.cloud_client.chat.completions.create(
                model=self.config["websearch_model"],
                messages=[
                    {
                        "role": "user",
                        "content": f"Search for and summarize (max {max_results} results): {query}\n\nProvide results as markdown with sources.",
                    }
                ],
                extra_body={"web_search": True},
                temperature=0.3,
            )
            result = response.choices[0].message.content
            console.print("[green][+][/green] Web search completed")
            return result
        except openai.APIError as e:
            if "500" in str(e) or "Internal Server Error" in str(e):
                console.print(f"[yellow][!] Model {self.config['websearch_model']} might not support web_search flag. Retrying without it...[/yellow]")
                try:
                    response = self.cloud_client.chat.completions.create(
                        model=self.config["websearch_model"],
                        messages=[
                            {
                                "role": "user",
                                "content": f"Search for and summarize (max {max_results} results): {query}\n\nProvide results as markdown with sources.",
                            }
                        ],
                        temperature=0.3,
                    )
                    result = response.choices[0].message.content
                    console.print("[green][+][/green] Web search completed (fallback mode)")
                    return result
                except openai.APIError as fallback_e:
                    return _handle_api_error(fallback_e) or f"Failed to search: {fallback_e}"
            return _handle_api_error(e) or f"Failed to search: {e}"

    def reason(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Generate reasoning via the configured backend.

        Args:
            prompt: User prompt
            model: Override model (default: reasoning_model from config)
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        model = model or self.config["reasoning_model"]
        backend = self.config["reasoning_backend"]
        console.print(f"[cyan][*] Reasoning with {model} ({backend})...[/cyan]")

        client = self.cloud_client if backend == "cloud" else self.ollama_client
        extra = {"options": {"num_ctx": _OLLAMA_NUM_CTX}} if backend != "cloud" else {}

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                extra_body=extra,
            )
            result = response.choices[0].message.content
            console.print("[green][+][/green] Reasoning completed")
            return result
        except openai.APIError as e:
            return _handle_api_error(e) or f"Failed to reason: {e}"

    def reformulate(self, prompt: str) -> str:
        """Reformulate problem using the configured reformulation model.

        Args:
            prompt: Problem reformulation prompt

        Returns:
            Reformulated problem statement
        """
        model = self.config["cloud_model_reformulate"]
        console.print(f"[cyan][*] Reformulating problem with {model}...[/cyan]")

        try:
            response = self.cloud_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )
            result = response.choices[0].message.content
            console.print("[green][+][/green] Problem reformulated")
            return result
        except openai.APIError as e:
            return _handle_api_error(e) or f"Failed to reformulate: {e}"

    def generate_code(
        self,
        prompt: str,
        temperature: float = 0.5,
    ) -> str:
        """Generate experiment code via configured backend.

        Args:
            prompt: Code generation prompt
            temperature: Sampling temperature

        Returns:
            Generated Python code (raw — caller extracts tags)
        """
        model = self.config["codegen_model"]
        backend = self.config["codegen_backend"]
        console.print(f"[cyan][*] Generating code with {model} ({backend})...[/cyan]")

        client = self.cloud_client if backend == "cloud" else self.ollama_client
        extra = {"options": {"num_ctx": _OLLAMA_NUM_CTX}} if backend != "cloud" else {}

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                extra_body=extra,
            )
            choice = response.choices[0]
            # finish_reason="length" means the API cut the response short — not a complete script
            if choice.finish_reason == "length":
                console.print(f"[yellow][!] {model} hit output limit (finish_reason=length) — flagging for retry[/yellow]")
                return "# TRUNCATED by API output limit"
            console.print("[green][+][/green] Code generated")
            return choice.message.content  # raw — caller extracts tags
        except openai.APIError as e:
            console.print(f"[red][!] Code generation error: {e}[/red]")
            return f"# Failed to generate code: {e}"

    def evaluate(
        self,
        output: str,
        problem: str,
        temperature: float = 0.3,
    ) -> dict:
        """Evaluate experiment results.

        Uses !@#$ tags to reliably delimit the JSON block.
        """
        import json, re

        prompt = f"""You are a senior scientific reviewer assessing whether experimental results constitute a genuine research breakthrough.

PROBLEM (first 300 chars):
{problem[:300]}

EXPERIMENT OUTPUT (first 1000 chars):
{output[:1000]}

BREAKTHROUGH CRITERIA — set breakthrough_achieved=true ONLY if ALL of the following hold:
1. NOVELTY: The finding is not a reproduction of a known result, and was not already established in prior literature.
2. EVIDENCE: Numerical results are statistically significant, reproducible, and not artifacts of the experiment setup (e.g. boundary effects, code bugs, truncation).
3. SCIENTIFIC IMPACT: The finding deepens understanding of a fundamental problem, challenges an existing model, or opens a new research direction that was not obvious before.
4. PUBLISHABILITY: The result would be accepted as the main contribution of an article in a peer-reviewed journal or a credible preprint (arXiv level), OR could serve as the central insight of a LinkedIn post shared by domain experts.

DO NOT set breakthrough_achieved=true for:
- Experiments that failed to run (syntax errors, file errors, timeouts)
- Confirmations that an artifact or bug was corrected
- Engineering optimizations (speed, memory) without a scientific finding
- Incremental parameter tuning with marginal improvement
- Reproducing already-known distributions or patterns without new insight

publishability_score: rate 0-10 where 0=failed experiment, 3=interesting pattern to explore, 6=solid finding worth a conference poster, 8=worthy of a journal article, 10=major result.

Return ONLY a JSON object between !@#$ markers:

!@#$
{{
  "summary": "one-sentence summary of the main scientific finding (not the code status)",
  "breakthrough_achieved": false,
  "confidence": 0.5,
  "publishability_score": 0,
  "next_directions": ["direction 1", "direction 2", "direction 3"]
}}
!@#$

Fill in the JSON above with your evaluation. Output ONLY the !@#$ block — no other text."""

        def _try_parse(raw: str) -> dict | None:
            """Try every strategy to extract a valid evaluation dict from raw text."""
            candidates = []

            # Strategy 1: !@#$...!@#$ tags — take LAST block
            tag_matches = re.findall(r'!@#\$(.*?)!@#\$', raw, re.DOTALL)
            if tag_matches:
                candidates.append(tag_matches[-1].strip())

            # Strategy 2: ```json...``` block — take last
            json_blocks = re.findall(r'```json\s*(.*?)```', raw, re.DOTALL)
            if json_blocks:
                candidates.append(json_blocks[-1].strip())

            # Strategy 3: ``` block — take last
            code_blocks = re.findall(r'```\s*(.*?)```', raw, re.DOTALL)
            if code_blocks:
                candidates.append(code_blocks[-1].strip())

            # Strategy 4: first { ... } in the raw text
            brace_match = re.search(r'\{[^{}]*\}', raw, re.DOTALL)
            if brace_match:
                candidates.append(brace_match.group(0))

            # Strategy 5: whole raw text
            candidates.append(raw.strip())

            for candidate in candidates:
                try:
                    data = json.loads(candidate)
                    # Normalise keys
                    return {
                        "summary": str(data.get("summary", "")),
                        "breakthrough_achieved": bool(data.get("breakthrough_achieved", False)),
                        "confidence": float(data.get("confidence", 0.5)),
                        "publishability_score": float(data.get("publishability_score", 0.0)),
                        "next_directions": list(data.get("next_directions", [])),
                    }
                except (json.JSONDecodeError, TypeError, ValueError):
                    continue
            return None

        def _default(raw: str = "") -> dict:
            return {
                "summary": raw[:200] if raw else "Evaluation unavailable",
                "breakthrough_achieved": False,
                "confidence": 0.0,
                "publishability_score": 0.0,
                "next_directions": [],
            }

        model = self.config["eval_model"]
        backend = self.config["eval_backend"]
        console.print(f"[cyan][*] Evaluating results with {model} ({backend})...[/cyan]")

        client = self.cloud_client if backend == "cloud" else self.ollama_client
        extra = {"options": {"num_ctx": _OLLAMA_NUM_CTX}} if backend != "cloud" else {}
        raw_output = None
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                extra_body=extra,
            )
            raw_output = resp.choices[0].message.content
        except openai.APIError as e:
            console.print(f"[red][!] Evaluation error: {e}[/red]")

        if raw_output:
            result = _try_parse(raw_output)
            if result:
                console.print("[green][+][/green] Evaluation completed")
                return result
            console.print("[yellow][!] JSON parse failed[/yellow]")

        console.print("[red][!] Evaluation failed[/red]")
        return _default(raw_output or "")

    def generate_next_problem(self, original_problem: str, evaluation: dict) -> str:
        """Generate the next-level problem.md using the evaluation model.

        Called after a breakthrough to push the research frontier forward.

        Args:
            original_problem: The problem.md that led to the breakthrough
            evaluation: The breakthrough evaluation dict (summary, next_directions, confidence)

        Returns:
            New problem.md content in the same markdown format
        """
        model = self.config["eval_model"]
        backend = self.config["eval_backend"]
        console.print(f"[cyan][*] Generating next problem with {model} ({backend})...[/cyan]")

        summary = evaluation.get("summary", "No summary available")
        confidence = evaluation.get("confidence", 0.0)
        next_dirs = evaluation.get("next_directions", [])
        next_dirs_text = "\n".join(f"- {d}" for d in next_dirs) if next_dirs else "- (none specified)"

        prompt = f"""A research breakthrough has been achieved. Your task is to write the next-level research problem that pushes the investigation further.

ORIGINAL PROBLEM:
{original_problem}

BREAKTHROUGH SUMMARY:
{summary}

CONFIDENCE: {confidence:.0%}

SUGGESTED NEXT DIRECTIONS:
{next_dirs_text}

TASK:
Write a new problem.md that advances the research frontier based on this breakthrough.
The new problem must:
1. Stay in the same research domain — do NOT change the subject
2. Build directly on the breakthrough finding — assume it is confirmed
3. Target the most promising next direction from the list above
4. Be more specific and deeper than the original problem
5. Use exactly this markdown structure:

# Research Problem: <title>

## Objective
<clear one-paragraph research objective>

## Research Questions
1. <specific question 1>
2. <specific question 2>
3. <specific question 3>

## Methodology
<computational approach — tools, algorithms, datasets>

## Success Criteria
<what constitutes a breakthrough at this next level>

## Constraints
- All experiments in Python (stdlib, numpy, matplotlib, scipy only)
- No external data downloads
- Experiments must complete within 2 minutes

Output ONLY the problem.md content. No preamble, no explanation."""

        client = self.cloud_client if backend == "cloud" else self.ollama_client
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            result = response.choices[0].message.content.strip()
            console.print("[green][+][/green] Next problem generated")
            return result
        except openai.APIError as e:
            console.print(f"[red][!] Failed to generate next problem: {e}[/red]")
            return ""
