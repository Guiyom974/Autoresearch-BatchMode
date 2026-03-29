# LinkedIn Post Draft

---

To every researcher, data scientist, and engineer who has ever stared at a blank notebook wondering where to start: what if the first 80% of the scientific loop could run itself overnight?

A few weeks ago I started extending Andrej Karpathy's autoresearch project [link0] — a proof-of-concept that chains LLM calls into a rudimentary research loop. The original idea is elegant but minimal: one pass, one hypothesis, one evaluation, stop. I found myself asking a different question. What happens if you don't stop?

The fork I am releasing today [link1] makes three additions that I believe change what autonomous research actually means in practice:

1. **Iterative breakthrough mode.** The agent does not terminate after a single experiment. It evaluates its own output, reformulates the research problem using what it just learned, and re-enters the loop. It repeats this until it detects a genuine breakthrough — defined by four hard criteria: novelty, statistical evidence, scientific impact, and publishability score ≥ 7/10. The full reasoning chain is exported as a self-contained HTML report with a Mermaid diagram tracing every iteration.

2. **Hybrid cloud / local model stack.** Web search goes through a cloud API (Poe [link2] or OpenRouter [link3]) because Ollama has no internet access. But hypothesis formulation, code generation, and evaluation route to local models via Ollama — keeping sensitive research private and inference costs near zero. The model configuration is fully user-defined: swap any model at any prompt without touching the code.

3. **Batch mode.** Point the tool at a folder of problem files and it runs the full research loop on each one sequentially, with a shared model config. This is the feature I am most excited about for #AI4Good applications: a research team with limited compute can queue fifty domain-specific problems and return the next morning to fifty structured experiment reports.

The reason I think this matters beyond the technical novelty is about access. Serious literature review and hypothesis generation today require either expensive cloud credits or privileged access to frontier APIs. This stack runs the heavy lifting locally, on consumer hardware, for free after the initial model pulls. That changes who can do autonomous research — not just well-funded labs, but NGOs working on climate models, public health researchers in emerging markets, small university teams without GPU clusters.

Is this going to replace human scientists? No. But it will make the starting line of any investigation far cheaper to reach. What's your view on where the ceiling for autonomous research agents actually sits?

---

*Links in comments:*
- link0: https://github.com/karpathy/autoresearch
- link1: https://github.com/Guiyom974/Autoresearch-BatchMode
- link2: https://poe.com/api_key
- link3: https://openrouter.ai/keys

#generativeai #ai4good #data4good #openresearch #llm #autonomousai
