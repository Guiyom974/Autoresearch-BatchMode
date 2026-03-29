# AutoResearch

Autonomous AI research tool that turns a research problem into a complete experiment cycle: web search → hypothesis formulation → Python code generation → local execution → scientific evaluation → iterative refinement.

Experiments are saved to disk with full artifacts (queries, search results, hypotheses, generated code, run output, evaluation). Breakthrough mode generates a self-contained HTML report after all iterations.

---

## What it does

| Mode | Description |
|------|-------------|
| **Standard** | Single pass: search → hypothesize → code → run → evaluate |
| **Breakthrough** | Iterative: repeats the standard loop N times, reformulating the problem between each iteration using the evaluation from the previous run. Stops early on breakthrough. Generates HTML report. |
| **Batch** | Runs any mode on every problem file in a folder, sequentially, with a shared model configuration. |

---

## Requirements

- **Python 3.9+**
- **A cloud API key** — Poe, OpenRouter, or any OpenAI-compatible endpoint
- **Ollama** (optional) — needed only if you want to run hypothesis formulation, code generation, or evaluation locally instead of via the cloud API

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/autoresearch.git
cd autoresearch

# 2. Copy the config template
copy .env.example .env      # Windows
# cp .env.example .env      # Mac/Linux

# 3. Edit .env with your API key (see Configuration section below)

# 4. Run — the launcher creates the venv and installs dependencies automatically
launch.bat
```

On first run `launch.bat` creates `.venv/` and runs `pip install -r requirements.txt`. Subsequent runs activate the existing venv directly.

---

## Configuration

Edit `.env` (copied from `.env.example`). You only need to set the two required lines for your chosen provider.

### Option A — Poe

Best option if you want **live web search**. Poe's `Web-Search` model retrieves real-time results.

Get your key at: https://poe.com/api_key

```env
CLOUD_API_KEY=your_poe_key_here
CLOUD_BASE_URL=https://api.poe.com/v1
```

During model setup, enter `Web-Search` for the web search model and any Poe model name for the others (e.g. `Gemini-3.1-Flash-Lite`, `claude-sonnet-4-5`, `gpt-4o`).

### Option B — OpenRouter

Access to hundreds of models. For web search, use a model with built-in browsing (e.g. `perplexity/sonar-pro`). Other models will respond from training data only.

Get your key at: https://openrouter.ai/keys

```env
CLOUD_API_KEY=sk-or-your_openrouter_key_here
CLOUD_BASE_URL=https://openrouter.ai/api/v1
```

During model setup, enter full OpenRouter model IDs (e.g. `google/gemini-flash-1.5`, `anthropic/claude-3.5-sonnet`).

### Option C — Any OpenAI-compatible endpoint

```env
CLOUD_API_KEY=your_key_here
CLOUD_BASE_URL=https://your-endpoint.com/v1
```

### Local Ollama (optional)

If you want to run reasoning, code generation, or evaluation locally:

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3.2`
3. Start the server: `ollama serve`

No extra `.env` changes needed — Ollama defaults to `http://localhost:11434/v1`.

To use a remote Ollama instance:
```env
OLLAMA_BASE_URL=http://your-server:11434/v1
```

### Context assessment model

AutoResearch uses a small local Ollama model to screen past experiments for relevance before each run (fast name-based filtering, then content extraction). Default is `llama3.2:latest`. Override with:

```env
CONTEXT_ASSESSMENT_MODEL=llama3.2:latest
```

If Ollama is not available, this step is skipped gracefully and past context is omitted.

---

## Running

### Interactive menu

```
launch.bat
```

Presents a menu to choose Standard, Breakthrough, or Batch mode.

### Command line

```bash
# Standard mode — single research pass on problem.md
launch.bat standard

# Standard mode — custom problem file
launch.bat standard --problem "problem a/Ecology - Climate Feedback - problem.md"

# Breakthrough mode — 5 iterations
launch.bat breakthrough --iterations 5

# Breakthrough mode — custom problem, 3 iterations
launch.bat breakthrough --iterations 3 --problem my_research.md

# Batch mode — run all *problem.md files in a folder (standard)
launch.bat standard --batch "problem a/"

# Batch mode — breakthrough on all problems in a folder
launch.bat breakthrough --batch "problem a/" --iterations 3
```

---

## Model setup prompt

When you run any mode, AutoResearch asks you to configure models for four tasks:

```
Select backend for Web Search (1. Cloud API, 2. Ollama):
  → Always choose 1 (Cloud API) — Ollama has no internet access

Select backend for Hypothesis Formulation (1. Cloud API, 2. Ollama):
  → Cloud: enter model name (e.g. Gemini-3.1-Flash-Lite, gpt-4o-mini)
  → Ollama: pick from the list of installed models

Select backend for Code Design (1. Cloud API, 2. Ollama):
  → Same as above — code generation works well with strong local models

Select backend for Evaluation (1. Cloud API, 2. Ollama):
  → Evaluation requires structured JSON output — use a capable model
```

In **batch mode**, you configure models once and the same selection applies to every problem file.

You can skip the model prompts for Ollama by passing `--ollama-model`:

```bash
launch.bat standard --ollama-model llama3.2
```

---

## Writing a problem file

Create a markdown file following this structure. See `problem a/` for examples.

```markdown
# Research Problem: Domain - Topic Name

## Objective
One paragraph describing what to investigate.

## Research Questions
1. Specific testable question 1
2. Specific testable question 2
3. Specific testable question 3

## Methodology
How to approach it computationally — algorithms, tools, datasets.

## Success Criteria
What constitutes a meaningful result or breakthrough.

## Constraints
- Python only (numpy, scipy, matplotlib)
- No external data downloads
- Experiments must complete within 2 minutes
```

Name the file `Category - Topic - problem.md` (e.g. `Physics - Double Pendulum - problem.md`). This naming convention is used to label experiment output folders and the HTML report.

---

## Experiment output

Results are saved under `experiments/`:

```
experiments/
  standard/
    Physics - Double Pendulum - 20260101_120000/
      01_problem.md
      02_search_queries.md
      03_search_results.md
      04_hypotheses.md
      05_experiment_code.py
      06_run_output.txt
      07_evaluation.md
      meta.json

  breakthrough/
    Physics - Double Pendulum - 20260101_120000/
      meta.json
      history/
        problem_versions.md      ← all reformulations across iterations
      run_001/
        (same 7 files as standard)
      run_002/
        ...
      report.html                ← self-contained HTML report (dark mode, Mermaid diagram)
```

If a breakthrough is detected, `problem-new.md` is written to the working directory with a next-level problem statement generated from the breakthrough findings.

---

## Breakthrough criteria

The evaluation model sets `breakthrough_achieved = true` only when all four conditions hold:

1. **Novelty** — not a reproduction of a known result
2. **Evidence** — statistically significant, reproducible, not an artifact
3. **Scientific impact** — deepens understanding or opens a new direction
4. **Publishability** — arXiv-level quality or better

Additionally, the code enforces minimum thresholds: `confidence >= 90%` and `publishability_score >= 7/10`. The LLM flag alone is not sufficient.

---

## Architecture

```
src/
  config.py      — loads .env, model selection prompts, session config
  llm.py         — LLMRouter: routes tasks to cloud API or Ollama
  researcher.py  — research loop (standard + breakthrough), past-context builder
  experiment.py  — code generation, execution, auto-fix on failure
  tracker.py     — artifact logging (step files + meta.json)
  reporter.py    — HTML report generation with Mermaid diagram
  main.py        — CLI entry point (argparse)
```

**Task routing:**

| Task | Backend |
|------|---------|
| Web search | Cloud API only (Ollama has no internet) |
| Hypothesis formulation | Cloud or Ollama (user choice) |
| Code generation | Cloud or Ollama (user choice) |
| Evaluation | Cloud or Ollama (user choice) |
| Problem reformulation | Cloud API (reformulation model) |
| Past-context screening | Ollama only (context assessment model) |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `openai` | OpenAI SDK used for all API calls (cloud + Ollama both speak OpenAI protocol) |
| `httpx` | HTTP client (used for Ollama timeout configuration) |
| `python-dotenv` | `.env` file loading |
| `rich` | Terminal formatting, panels, colored output |
| `numpy` | Numerical computing (used in generated experiment scripts) |
| `matplotlib` | Visualization (used in generated experiment scripts) |
| `scipy` | Scientific computing (used in generated experiment scripts) |

---

## License

MIT
