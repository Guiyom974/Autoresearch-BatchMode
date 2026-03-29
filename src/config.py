"""Configuration management for AutoResearch."""

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

console = Console()

# Load .env file
env_file = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_file)

# Cloud API — any OpenAI-compatible endpoint (Poe, OpenRouter, custom)
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY") or os.getenv("POE_API_KEY")  # POE_API_KEY kept for backward compat
CLOUD_BASE_URL = os.getenv("CLOUD_BASE_URL", "https://api.poe.com/v1")

# Local Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

# Model names (with defaults, can be overridden via .env)
CLOUD_MODEL_WEBSEARCH = os.getenv("CLOUD_MODEL_WEBSEARCH") or os.getenv("POE_MODEL_WEBSEARCH", "Web-Search")
CLOUD_MODEL_RESEARCH = os.getenv("CLOUD_MODEL_RESEARCH") or os.getenv("POE_MODEL_RESEARCH", "Gemini-3.1-Flash-Lite")
CLOUD_MODEL_REFORMULATE = os.getenv("CLOUD_MODEL_REFORMULATE") or os.getenv("POE_MODEL_REFORMULATE", "Gemini-3.1-Pro")

# Model used by the context-assessment (past-run filtering) step — must be an Ollama model
CONTEXT_ASSESSMENT_MODEL = os.getenv("CONTEXT_ASSESSMENT_MODEL", "llama3.2:latest")


def validate_env() -> None:
    """Validate required environment variables."""
    if not CLOUD_API_KEY:
        console.print(
            "[red][!] CLOUD_API_KEY not found in .env[/red]\n"
            "1. Copy .env.example to .env\n"
            "2. Set CLOUD_API_KEY to your API key\n"
            "3. Set CLOUD_BASE_URL to your provider's endpoint\n"
            "   Poe:        https://api.poe.com/v1        (key from https://poe.com/api_key)\n"
            "   OpenRouter: https://openrouter.ai/api/v1  (key from https://openrouter.ai/keys)\n"
            "4. Run launch.bat again"
        )
        sys.exit(1)

    # Check for placeholder value
    if CLOUD_API_KEY.strip() in ("your_api_key_here", "your_key_here", "sk_...", "sk-or-..."):
        console.print(
            "[red][!] CLOUD_API_KEY still has placeholder value in .env[/red]\n"
            "Edit .env and replace with your real API key."
        )
        sys.exit(1)

    # Test API key with a real call
    import openai
    console.print(f"[cyan][*] Validating API key against {CLOUD_BASE_URL}...[/cyan]")
    try:
        client = openai.OpenAI(api_key=CLOUD_API_KEY.strip(), base_url=CLOUD_BASE_URL)
        client.models.list()
        console.print("[green][+][/green] API key is valid")
    except openai.AuthenticationError:
        console.print(
            "[red][!] Invalid API key[/red]\n"
            "Your key was rejected. Please check:\n"
            "  1. CLOUD_API_KEY is correct in .env\n"
            "  2. CLOUD_BASE_URL matches your provider\n"
            "  3. No quotes or spaces around the key"
        )
        sys.exit(1)
    except Exception:
        console.print("[yellow][!] Could not validate API key (network issue?), continuing...[/yellow]")


def list_ollama_models() -> list[str]:
    """Get list of available Ollama models."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            console.print(
                "[yellow][!] Ollama not running or no models installed[/yellow]\n"
                "Install Ollama from https://ollama.ai and pull a model:\n"
                "  ollama pull llama3.2 (or any other model)\n"
                "  ollama serve"
            )
            return []

        lines = result.stdout.strip().split("\n")[1:]  # Skip header
        models = [line.split()[0] for line in lines if line.strip()]
        return models
    except FileNotFoundError:
        console.print(
            "[yellow][!] Ollama CLI not found[/yellow]\n"
            "Install from https://ollama.ai"
        )
        return []
    except subprocess.TimeoutExpired:
        console.print("[yellow][!] Ollama command timed out[/yellow]")
        return []


def select_model(task_name: str, allow_backend_choice: bool = True, default_cloud: str = "") -> tuple[str, str]:
    """Returns (backend, model_name). backend is 'cloud' or 'ollama'"""
    if allow_backend_choice:
        while True:
            backend = input(f"\nSelect backend for {task_name} (1. Cloud API, 2. Ollama): ").strip()
            if backend in ["1", "cloud", "Cloud"]:
                choice_backend = "cloud"
                break
            elif backend in ["2", "ollama", "Ollama"]:
                choice_backend = "ollama"
                break
            else:
                console.print("[red]Invalid choice. Enter 1 (Cloud API) or 2 (Ollama)[/red]")
    else:
        choice_backend = "cloud"

    if choice_backend == "cloud":
        default_str = f" [{default_cloud}]" if default_cloud else ""
        examples = "  e.g. gpt-4o, claude-sonnet-4-5, gemini-pro, Web-Search"
        while True:
            model = input(f"Enter model name for {task_name}{default_str}: ").strip()
            if not model and default_cloud:
                model = default_cloud
                break
            elif not model:
                console.print(f"[red]Model name required.[/red]\n{examples}")
                continue
            # Catch the common mistake of entering a menu number instead of a model name
            elif model.isdigit():
                console.print(
                    f"[red][!] '{model}' looks like a menu number, not a model name.[/red]\n"
                    f"{examples}"
                )
                continue
            else:
                break
        console.print(f"[green][+][/green] Selected cloud model: {model}")
        return ("cloud", model)
    else:
        models = list_ollama_models()
        if models:
            console.print("\n[cyan]Available Ollama models:[/cyan]")
            for i, m in enumerate(models, 1):
                console.print(f"  {i:2d}. {m}")
            console.print(f"  {len(models) + 1:2d}. Enter custom model name")

            while True:
                try:
                    choice_str = input(f"Select model (1-{len(models) + 1}): ").strip()
                    if not choice_str: continue
                    choice = int(choice_str)
                    if 1 <= choice <= len(models):
                        selected = models[choice - 1]
                        console.print(f"[green][+][/green] Selected Ollama model: {selected}")
                        return ("ollama", selected)
                    elif choice == len(models) + 1:
                        model = input("Enter model name: ").strip()
                        if model:
                            console.print(f"[green][+][/green] Selected Ollama model: {model}")
                            return ("ollama", model)
                except ValueError:
                    console.print("[red]Please enter a valid number[/red]")
        else:
            console.print("[yellow]No models found. Install with: ollama pull llama3.2[/yellow]")
            model = input("Enter Ollama model name (e.g., llama3.2, mistral): ").strip()
            while not model:
                console.print("[red]Model name required[/red]")
                model = input("Enter Ollama model name (e.g., llama3.2, mistral): ").strip()
            console.print(f"[green][+][/green] Selected Ollama model: {model}")
            return ("ollama", model)


def get_session_config(ollama_model: str = None) -> dict:
    """Get session configuration."""
    console.print("\n[bold cyan]--- Model Configuration ---[/bold cyan]")

    # 1. Web Search (always cloud — Ollama has no internet access)
    web_backend, web_model = select_model("Web Search", allow_backend_choice=False, default_cloud=CLOUD_MODEL_WEBSEARCH)

    # 2. Hypothesis Formulation
    reason_backend, reason_model = select_model("Hypothesis Formulation")

    # 3. Code Design
    code_backend, code_model = select_model("Code Design")

    # 4. Evaluation
    eval_backend, eval_model = select_model("Evaluation")

    return {
        "cloud_api_key": CLOUD_API_KEY,
        "cloud_base_url": CLOUD_BASE_URL,
        "ollama_base_url": OLLAMA_BASE_URL,
        "context_assessment_model": CONTEXT_ASSESSMENT_MODEL,
        "websearch_backend": web_backend,
        "websearch_model": web_model,
        "reasoning_backend": reason_backend,
        "reasoning_model": reason_model,
        "codegen_backend": code_backend,
        "codegen_model": code_model,
        "eval_backend": eval_backend,
        "eval_model": eval_model,
        "cloud_model_reformulate": CLOUD_MODEL_REFORMULATE,
    }
