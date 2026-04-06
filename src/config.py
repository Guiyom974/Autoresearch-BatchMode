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

# API Keys and URLs
POE_API_KEY = os.getenv("POE_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

# Model names (with defaults, can be overridden via .env)
POE_MODEL_WEBSEARCH = os.getenv("POE_MODEL_WEBSEARCH", "Web-Search")  # Poe's built-in web search model
POE_MODEL_RESEARCH = os.getenv("POE_MODEL_RESEARCH", "Gemini-3.1-Flash-Lite")
POE_MODEL_REFORMULATE = os.getenv("POE_MODEL_REFORMULATE", "Gemini-3.1-Pro")


def validate_env() -> None:
    """Validate required environment variables."""
    if not POE_API_KEY:
        console.print(
            "[red][!] POE_API_KEY not found in .env[/red]\n"
            "1. Get your API key from: https://poe.com/api/keys\n"
            "2. Copy .env.example to .env\n"
            "3. Paste your key as POE_API_KEY=...\n"
            "4. Run launch.bat again"
        )
        sys.exit(1)

    # Check for placeholder value
    if POE_API_KEY.strip() in ("your_api_key_here", "your_key_here", "sk_..."):
        console.print(
            "[red][!] POE_API_KEY still has placeholder value in .env[/red]\n"
            "Edit .env and replace with your real key from: https://poe.com/api/keys"
        )
        sys.exit(1)

    # Test API key with a real call
    import openai
    console.print("[cyan][*] Validating Poe API key...[/cyan]")
    try:
        client = openai.OpenAI(api_key=POE_API_KEY.strip(), base_url="https://api.poe.com/v1")
        client.models.list()
        console.print("[green][+][/green] Poe API key is valid")
    except openai.AuthenticationError:
        console.print(
            "[red][!] Invalid Poe API key[/red]\n"
            "Your key was rejected by Poe. Please check:\n"
            "  1. Get a fresh key from: https://poe.com/api/keys\n"
            "  2. Paste it in .env as: POE_API_KEY=<key>\n"
            "  3. No quotes, no spaces around the key"
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
                "  ollama pull mistral (or any other model)\n"
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


def select_model(task_name: str, allow_backend_choice: bool = True, default_poe: str = "") -> tuple[str, str]:
    """Returns (backend, model_name). backend is 'poe' or 'ollama'"""
    if allow_backend_choice:
        while True:
            backend = input(f"\nSelect backend for {task_name} (1. Poe, 2. Ollama): ").strip()
            if backend in ["1", "poe", "Poe"]:
                choice_backend = "poe"
                break
            elif backend in ["2", "ollama", "Ollama"]:
                choice_backend = "ollama"
                break
            else:
                console.print("[red]Invalid choice. Enter 1 (Poe) or 2 (Ollama)[/red]")
    else:
        choice_backend = "poe"

    if choice_backend == "poe":
        default_str = f" [{default_poe}]" if default_poe else ""
        examples = "  e.g. gemini-3.1-pro, claude-sonnet-4.6, web-search, minimax-m2.7"
        while True:
            model = input(f"Enter Poe model name for {task_name}{default_str}: ").strip()
            if not model and default_poe:
                model = default_poe
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
        console.print(f"[green][+][/green] Selected Poe model: {model}")
        return ("poe", model)
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
            console.print("[yellow]No models found. Install with: ollama pull mistral[/yellow]")
            model = input("Enter Ollama model name (e.g., mistral, neural-chat): ").strip()
            while not model:
                console.print("[red]Model name required[/red]")
                model = input("Enter Ollama model name (e.g., mistral, neural-chat): ").strip()
            console.print(f"[green][+][/green] Selected Ollama model: {model}")
            return ("ollama", model)

def get_session_config(ollama_model: str = None) -> dict:
    """Get session configuration."""
    console.print("\n[bold cyan]--- Model Configuration ---[/bold cyan]")

    # 1. Web Search (always Poe — Ollama has no internet access)
    web_backend, web_model = select_model("Web Search", allow_backend_choice=False, default_poe="Web-Search")

    # 2. Hypothesis Formulation
    reason_backend, reason_model = select_model("Hypothesis Formulation")

    # 3. Code Design
    code_backend, code_model = select_model("Code Design")

    # 4. Evaluation
    eval_backend, eval_model = select_model("Evaluation")

    return {
        "poe_api_key": POE_API_KEY,
        "ollama_base_url": OLLAMA_BASE_URL,
        "websearch_backend": web_backend,
        "websearch_model": web_model,
        "reasoning_backend": reason_backend,
        "reasoning_model": reason_model,
        "codegen_backend": code_backend,
        "codegen_model": code_model,
        "eval_backend": eval_backend,
        "eval_model": eval_model,
        "poe_model_reformulate": POE_MODEL_REFORMULATE,
    }
