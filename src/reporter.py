"""HTML report generation for breakthrough mode experiments."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console

console = Console()


def generate_breakthrough_report(
    base_dir: Path,
    problem_title: str = "Research Breakthrough Report",
    output_file: Optional[Path] = None,
) -> Path:
    """Generate self-contained HTML report for breakthrough experiments.

    Args:
        base_dir: Breakthrough experiment base directory
        problem_title: Title for the report
        output_file: Output HTML file (default: base_dir/report.html)

    Returns:
        Path to generated HTML file
    """
    if output_file is None:
        output_file = base_dir / "report.html"

    console.print(f"[cyan][*] Generating breakthrough report...[/cyan]")

    # Collect run data
    runs_data = []
    for run_dir in sorted(base_dir.glob("run_*")):
        if run_dir.is_dir():
            meta_file = run_dir / "meta.json"
            if meta_file.exists():
                meta = json.loads(meta_file.read_text(encoding="utf-8", errors="replace"))
                runs_data.append({"run_dir": run_dir.name, "meta": meta})

    # Read history
    history_text = ""
    history_file = base_dir / "history" / "problem_versions.md"
    if history_file.exists():
        history_text = history_file.read_text(encoding="utf-8", errors="replace")

    # Read base meta
    base_meta = {}
    base_meta_file = base_dir / "meta.json"
    if base_meta_file.exists():
        base_meta = json.loads(base_meta_file.read_text(encoding="utf-8", errors="replace"))

    # Generate Mermaid diagram
    mermaid_diagram = _generate_mermaid_diagram(runs_data)

    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{problem_title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        body.dark-mode {{
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #f0f0f0;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        body.dark-mode .container {{
            background: #2a2a2a;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .controls {{
            padding: 20px;
            background: #f8f9fa;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #eee;
        }}

        body.dark-mode .controls {{
            background: #333;
            border-bottom-color: #555;
        }}

        .toggle-btn {{
            padding: 8px 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1em;
        }}

        .toggle-btn:hover {{
            background: #5568d3;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 50px;
        }}

        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}

        body.dark-mode .section h2 {{
            color: #a7b3ff;
            border-bottom-color: #a7b3ff;
        }}

        .section h3 {{
            color: #555;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}

        body.dark-mode .section h3 {{
            color: #ddd;
        }}

        .mermaid {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            overflow-x: auto;
        }}

        body.dark-mode .mermaid {{
            background: #333;
        }}

        .run-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 15px 0;
            border-radius: 6px;
        }}

        body.dark-mode .run-card {{
            background: #333;
            border-left-color: #a7b3ff;
        }}

        .run-title {{
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
        }}

        body.dark-mode .run-title {{
            color: #a7b3ff;
        }}

        details {{
            margin: 15px 0;
        }}

        summary {{
            cursor: pointer;
            padding: 10px;
            background: #e8eaf6;
            border-radius: 6px;
            font-weight: 600;
            user-select: none;
        }}

        body.dark-mode summary {{
            background: #444;
        }}

        summary:hover {{
            background: #d8e0f0;
        }}

        body.dark-mode summary:hover {{
            background: #555;
        }}

        .code-block {{
            background: #272822;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}

        .history {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}

        body.dark-mode .history {{
            background: #333;
        }}

        footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #eee;
            font-size: 0.9em;
        }}

        body.dark-mode footer {{
            background: #333;
            border-top-color: #555;
            color: #aaa;
        }}

        .status-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
            margin: 5px 0;
        }}

        .status-breakthrough {{
            background: #c8e6c9;
            color: #2e7d32;
        }}

        .status-completed {{
            background: #bbdefb;
            color: #1565c0;
        }}

        .status-failed {{
            background: #ffccbc;
            color: #d84315;
        }}

        body.dark-mode .status-breakthrough {{
            background: #1b5e20;
            color: #81c784;
        }}

        body.dark-mode .status-completed {{
            background: #0d47a1;
            color: #64b5f6;
        }}

        body.dark-mode .status-failed {{
            background: #bf360c;
            color: #ff7043;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}

        body.dark-mode th, body.dark-mode td {{
            border-bottom-color: #555;
        }}

        th {{
            background: #e8eaf6;
            font-weight: 600;
        }}

        body.dark-mode th {{
            background: #444;
        }}

        tr:hover {{
            background: #f5f5f5;
        }}

        body.dark-mode tr:hover {{
            background: #3a3a3a;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔬 {problem_title}</h1>
            <p>AutoResearch Breakthrough Experiment Report</p>
        </header>

        <div class="controls">
            <span>Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            <button class="toggle-btn" onclick="toggleDarkMode()">🌙 Dark Mode</button>
        </div>

        <div class="content">
            <!-- Overview Section -->
            <div class="section">
                <h2>📊 Experiment Overview</h2>
                <table>
                    <tr>
                        <th>Total Iterations</th>
                        <td>{base_meta.get('total_iterations', len(runs_data))}</td>
                    </tr>
                    <tr>
                        <th>Final Status</th>
                        <td><span class="status-badge status-{base_meta.get('final_status', 'completed')}">{base_meta.get('final_status', 'N/A').upper()}</span></td>
                    </tr>
                    <tr>
                        <th>Start Time</th>
                        <td>{base_meta.get('start_time', 'N/A')}</td>
                    </tr>
                    <tr>
                        <th>End Time</th>
                        <td>{base_meta.get('end_time', 'N/A')}</td>
                    </tr>
                </table>
            </div>

            <!-- Research Flow Diagram -->
            <div class="section">
                <h2>🔄 Research Flow</h2>
                <div class="mermaid">
{mermaid_diagram}
                </div>
            </div>

            <!-- Problem Evolution -->
            <div class="section">
                <h2>📈 Problem Evolution</h2>
                <details open>
                    <summary>View problem reformulations across iterations</summary>
                    <div class="history">
                        <pre>{_escape_html(history_text)}</pre>
                    </div>
                </details>
            </div>

            <!-- Iteration Results -->
            <div class="section">
                <h2>🔍 Detailed Results by Iteration</h2>
                {_generate_runs_html(base_dir, runs_data)}
            </div>

            <!-- Summary -->
            <div class="section">
                <h2>✨ Key Findings</h2>
                <p>This breakthrough research experiment explored the research problem through {len(runs_data)} iteration(s),
                with each iteration informing the reformulation of the problem for the next round.</p>
                <p><strong>Final Status:</strong> {base_meta.get('final_status', 'Completed').upper()}</p>
            </div>
        </div>

        <footer>
            <p>Generated by AutoResearch | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>For reproducibility, all experiment artifacts are stored locally in the experiment directory.</p>
        </footer>
    </div>

    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        mermaid.contentLoaded();

        function toggleDarkMode() {{
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        }}

        // Load saved theme preference
        if (localStorage.getItem('darkMode') === 'true') {{
            document.body.classList.add('dark-mode');
        }}
    </script>
</body>
</html>"""

    output_file.write_text(html, encoding="utf-8")
    console.print(f"[green][+][/green] Report generated: {output_file}")

    return output_file


def _generate_mermaid_diagram(runs_data: list[dict]) -> str:
    """Generate Mermaid flowchart for research iterations."""
    lines = ["graph TD"]

    for i, run in enumerate(runs_data, 1):
        status = run["meta"].get("evaluation", {}).get("breakthrough_achieved", False)
        if status:
            node_shape = f"A{i}[\"Iteration {i}\n✨ BREAKTHROUGH!\"]"
        else:
            node_shape = f"A{i}[\"Iteration {i}\"]"
        lines.append(f"  {node_shape}")

        if i < len(runs_data):
            lines.append(f"  A{i} -->|Reformulate| A{i + 1}")

    lines.append(f"  A{len(runs_data)} --> B[\"Final Report\"]")

    return "\n".join(lines)


def _generate_runs_html(base_dir: Path, runs_data: list[dict]) -> str:
    """Generate HTML for all run results."""
    html_parts = []

    for run in runs_data:
        run_dir = base_dir / run["run_dir"]
        run_num = run["run_dir"].split("_")[1]

        evaluation = run["meta"].get("evaluation", {})
        status = "BREAKTHROUGH" if evaluation.get("breakthrough_achieved") else "COMPLETED"
        status_class = "breakthrough" if evaluation.get("breakthrough_achieved") else "completed"

        html_parts.append(f"""
        <div class="run-card">
            <div class="run-title">Iteration {run_num} - {status}</div>
            <span class="status-badge status-{status_class}">{status}</span>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Confidence</td>
                    <td>{evaluation.get('confidence', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Publishability Score</td>
                    <td>{evaluation.get('publishability_score', 'N/A')}/10</td>
                </tr>
                <tr>
                    <td>Steps Completed</td>
                    <td>{run['meta'].get('steps_completed', 'N/A')}</td>
                </tr>
            </table>

            <details>
                <summary>📝 Summary</summary>
                <p>{_escape_html(evaluation.get('summary', 'No summary available'))}</p>
            </details>

            <details>
                <summary>🎯 Next Directions</summary>
                <ul>
""")
        for direction in evaluation.get("next_directions", []):
            html_parts.append(f"                    <li>{_escape_html(direction)}</li>\n")
        html_parts.append("                </ul>\n            </details>\n")

        # Show code if available
        code_file = run_dir / "03_experiment_code.py"
        if code_file.exists():
            code_content = code_file.read_text(encoding="utf-8", errors="replace")
            html_parts.append(f"""
            <details>
                <summary>💻 Generated Code</summary>
                <div class="code-block"><pre>{_escape_html(code_content[:1000])}{"..." if len(code_content) > 1000 else ""}</pre></div>
            </details>
""")

        # Show output if available
        output_file = run_dir / "04_run_output.txt"
        if output_file.exists():
            output_content = output_file.read_text(encoding="utf-8", errors="replace")
            html_parts.append(f"""
            <details>
                <summary>📋 Execution Output</summary>
                <div class="code-block"><pre>{_escape_html(output_content[:500])}{"..." if len(output_content) > 500 else ""}</pre></div>
            </details>
""")

        html_parts.append("        </div>\n")

    return "".join(html_parts)


def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
