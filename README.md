# AutoResearch — AI Research Automation Tool

An autonomous research assistant that combines web search, LLM reasoning, and local code generation to iteratively explore research problems.

## Features

✨ **Autonomous Research Loops**
- Read a problem statement, search the web, generate hypotheses, run experiments
- Two operating modes: **standard** (single run) and **breakthrough** (iterative with problem reformulation)

🔍 **Integrated Web Search**
- Uses Poe API with web search enabled (Gemini models)
- Provides contextual information for hypothesis formulation

🧠 **Multi-Model LLM Routing**
- **Web Search & Research**: Poe API (Gemini models with web search)
- **Code Generation & Evaluation**: Local Ollama (your choice of model)
- **Problem Reformulation**: Poe API (Gemini-3.1-Pro for high-quality reformulation)

📊 **Complete Observability**
- Every step (search, hypotheses, code, output, evaluation) saved locally
- Structured experiment folders with timestamps
- JSON metadata for each run
- Problem evolution history in breakthrough mode

🎨 **Beautiful HTML Reports**
- Self-contained reports with Mermaid diagrams showing research flow
- Dark mode support
- Collapsible sections for detailed exploration
- Works offline (all assets embedded)

## Quick Start

### 1. Setup

Clone/extract this directory, then:

```bash
# Copy .env template and add your Poe API key
copy .env.example .env
# Edit .env and set: POE_API_KEY=your_key_here
```

Get your Poe API key from: https://poe.com/api/keys

### 2. Install Ollama

Download and install Ollama from https://ollama.ai, then pull a model:

```bash
ollama pull mistral
# or try: ollama pull neural-chat, llama2, etc.
ollama serve  # Keep this running in a separate terminal
```

### 3. Run Standard Mode

```bash
launch.bat standard
```

This will:
1. Create a venv (first time only)
2. Prompt you to select an Ollama model
3. Run a single research loop on `problem.md`
4. Save all artifacts to `experiments/standard/YYYYMMDD_HHMMSS/`

### 4. Run Breakthrough Mode

```bash
launch.bat breakthrough --iterations 3
```

This will:
1. Run 3 iterations of research
2. Between iterations, reformulate the problem using Gemini-3.1-Pro
3. Stop early if a breakthrough is detected
4. Generate an HTML report at `experiments/breakthrough/YYYYMMDD_HHMMSS/report.html`

## Usage

```
launch.bat [standard|breakthrough] [options]

Standard mode:
  launch.bat standard [--problem FILE] [--ollama-model NAME]

Breakthrough mode:
  launch.bat breakthrough --iterations N [--problem FILE] [--ollama-model NAME]

Options:
  --problem FILE        Path to problem.md (default: ./problem.md)
  --ollama-model NAME   Ollama model name (default: prompt user)
  --iterations N        Number of breakthrough iterations (default: 3)
```

## How It Works

### Standard Mode Flow

```
1. Load problem.md
   ↓
2. Generate search queries (Poe/Gemini)
   ↓
3. Web search for information (Poe with web_search=True)
   ↓
4. Formulate research hypotheses (Poe/Gemini)
   ↓
5. Generate experiment code (Ollama)
   ↓
6. Execute experiment code locally
   ↓
7. Evaluate results (Ollama)
   ↓
8. Save all artifacts to disk
```

### Breakthrough Mode Flow

```
FOR each iteration:
  1. Run standard mode research loop
  2. Log problem version to history
  3. Check if breakthrough achieved → if yes, STOP
  4. Reformulate problem (Poe/Gemini-3.1-Pro)
  5. Next iteration with new problem

After all iterations:
  Generate self-contained HTML report with Mermaid diagram
```

## File Structure

```
D:\LocalProjects\Python apps\AutoResearch\
├── launch.bat                    ← Run this to start research
├── .env                          ← Your Poe API key (create from .env.example)
├── .env.example                  ← Template
├── problem.md                    ← Active research problem (edit this)
├── requirements.txt              ← Python dependencies
├── README.md                     ← This file
├── src/
│   ├── main.py                   ← CLI entry point
│   ├── config.py                 ← Configuration management
│   ├── llm.py                    ← LLM routing (Poe + Ollama)
│   ├── researcher.py             ← Research loop logic
│   ├── experiment.py             ← Code generation & execution
│   ├── tracker.py                ← Experiment tracking
│   └── reporter.py               ← HTML report generation
└── experiments/
    ├── standard/
    │   └── YYYYMMDD_HHMMSS/      ← One folder per standard run
    │       ├── meta.json          ← Run metadata
    │       ├── 01_problem.md
    │       ├── 02_search_results.md
    │       ├── 03_hypotheses.md
    │       ├── 04_experiment_code.py
    │       ├── 05_run_output.txt
    │       └── 06_evaluation.md
    └── breakthrough/
        └── YYYYMMDD_HHMMSS/
            ├── meta.json
            ├── history/
            │   └── problem_versions.md   ← All problem reformulations
            ├── run_001/
            ├── run_002/
            ├── run_003/
            └── report.html               ← Self-contained report
```

## Example: Prime Number Research

The default `problem.md` contains a research problem about prime number patterns. Try it:

```bash
launch.bat standard
```

This will search for prime pattern information, generate code to analyze primes, and report findings.

To reformulate the problem and iterate:

```bash
launch.bat breakthrough --iterations 2
```

## Configuration

### Environment Variables (.env)

```
POE_API_KEY=sk_...                              # Required: Poe API key
POE_MODEL_WEBSEARCH=Web-Search                  # Optional: override model names
POE_MODEL_RESEARCH=Gemini-3.1-Flash-Lite
POE_MODEL_REFORMULATE=Gemini-3.1-Pro
OLLAMA_BASE_URL=http://localhost:11434/v1       # Optional: override Ollama URL
```

### Model Names

Model names must exactly match available models on Poe. Check:
- https://poe.com/api/keys (after logging in)
- Or let the tool list available models on first run

For Ollama, use:
- `ollama list` to see available models
- `ollama pull <model>` to install new ones

## Troubleshooting

### Poe API Error
- Verify POE_API_KEY is set correctly in `.env`
- Check your Poe account has remaining API credits
- Ensure model names are exact (case-sensitive on Poe)

### Ollama Connection Error
```
[!] Ollama error
```
- Make sure Ollama is running: `ollama serve` in a separate terminal
- Check OLLAMA_BASE_URL in `.env` (default: http://localhost:11434/v1)

### Model Not Found
```
[!] Poe API error: Model not found
```
- Run research once to list available models
- Update model names in `.env` to match what's available
- Poe model names are case-sensitive (e.g., `Gemini-3-Pro`, not `gemini-3-pro`)

### Timeout on Execution
- Increase max execution timeout in code
- Simplify the experiment (use smaller datasets)
- Check Ollama model is responsive: `ollama list`

## For Your Own Research

### Edit problem.md

Replace the prime number problem with your own research question:

```markdown
# Research Problem: Your Title

## Objective
What are you trying to discover?

## Research Questions
1. Key question 1?
2. Key question 2?

## Methodology
How will you investigate this?

## Success Criteria
When is a breakthrough achieved?

## Constraints
What are the limits?
```

### Run Research

```bash
launch.bat standard --problem your_problem.md
launch.bat breakthrough --iterations 3 --problem your_problem.md
```

## Key Concepts

**Breakthrough**: The system considers a "breakthrough" achieved when:
- The Ollama model evaluates findings as novel (non-trivial)
- Confidence score is high
- Results are reproducible

**Problem Reformulation**: In breakthrough mode, after each iteration:
- Uses Gemini-3.1-Pro to analyze results
- Reformulates problem to explore promising directions
- Keeps all versions in history for reproducibility

**Local Observability**: Every single step is saved:
- Search queries and results
- Generated hypotheses
- Generated code
- Execution output
- Evaluation summary
- All in timestamped experiment folders

## Requirements

- Python 3.9+
- Windows (batch file) or modify `launch.bat` for other OS
- Internet connection (for Poe API calls)
- Ollama running locally (for code generation)
- Poe API key

## License

MIT

## Credits

Inspired by Andrej Karpathy's autoresearch concepts. Built as a general-purpose research automation tool.
