

Below are **four concrete, testable hypotheses** that directly address the three research questions and can be demonstrated with the small‑scale GPU/CPU comparison you are planning.  
Each hypothesis is written as a clear, falsifiable statement, followed by a short justification of why it can be tested and the concrete experiment you would run to evaluate it.

---

## 1.  Chunked GPU processing with CUDA streams will keep peak VRAM usage under the 8 GB consumer‑grade limit for all primorial‑base conversions up to a bound of \(10^{7}\).

**Why it is testable**  
* The hypothesis makes a quantitative claim about **peak VRAM consumption** that can be measured with NVIDIA profiling tools (e.g., `nvidia-smi`, `nvprof`, or NSight Compute).  
* The claim can be disproved simply by observing any single run that exceeds 8 GB.  

**Experiment**  
1. **Implement the chunked pipeline** using the “depth‑first” memory‑pool strategy described in the search results: allocate a reusable device buffer, split the prime array into chunks of a fixed size (e.g., 1 M elements), and enqueue each chunk into its own CUDA stream.  
2. **Profile the run** for the three initial primorial bases \(p_{2}\# , p_{3}\# , p_{4}\#\) at the maximum bound \(N = 10^{7}\). Record the **maximum VRAM used** (including device arrays for the sieve, the base‑conversion workspace, and any temporary buffers).  
3. **Repeat** the measurement for a range of chunk sizes (10 k, 50 k, 100 k, 500 k, 1 M) to verify that the hypothesis holds across plausible configuration choices.  

*Pass criterion:* Every measurement shows **≤ 8 GB** of VRAM consumption.

---

## 2.  The LDAB leading‑digit distributions and KL‑divergence metrics produced by the memory‑optimized GPU pipeline will be statistically identical to those from the validated CPU implementation at a bound of \(10^{7}\).

**Why it is testable**  
* “Statistically identical” can be formalised with a standard test for distributional equality (e.g., a two‑sample Kolmogorov‑Smirnov test or a χ² test) and by comparing the numerical KL‑divergence values within a tiny tolerance (≈ 10⁻¹²).  
* The hypothesis is falsifiable: any non‑zero difference that exceeds the chosen tolerance disproves it.  

**Experiment**  
1. **Run the GPU pipeline** on the three primorial bases up to \(N = 10^{7}\) and collect the **leading‑digit frequency vectors** (for digits 1–9) and the resulting **KL‑divergence** \(D_{KL}(P_{\text{GPU}}\|Q)\) where \(Q\) is the theoretical LDAB distribution.  
2. **Run the CPU baseline** (the same algorithm executed on a CPU with arbitrary‑precision integers) and collect the identical statistics.  
3. **Statistical testing**:  
   * Perform a **two‑sample KS test** on the 9‑dimensional frequency vectors (or a χ² goodness‑of‑fit test).  
   * Compute the absolute difference \(\Delta = |D_{KL}^{\text{GPU}} - D_{KL}^{\text{CPU}}|\).  
4. **Decision rule**: Accept the hypothesis if the KS test *p‑value* > 0.05 **and** \(\Delta < 10^{-12}\).  

*Pass criterion:* Both conditions satisfied for each primorial base.

---

## 3.  The memory‑optimized GPU pipeline will achieve a runtime speedup of **at least 3×** relative to the CPU baseline when evaluating the LDAB model at a bound of \(10^{7}\).

**Why it is testable**  
* Speedup is a direct ratio of two measurable wall‑clock times.  
* The hypothesis can be disproved by a single run where the ratio falls below 3.  

**Experiment**  
1. **Benchmark the CPU baseline**: time the LDAB evaluation on the same three primorial bases (use a single‑threaded or optimally‑vectorized CPU implementation).  
2. **Benchmark the GPU pipeline**: time the entire pipeline (H2D transfer, kernel execution, D2H transfer) for the identical workload.  
3. **Calculate speedup**: \(\text{Speedup} = \frac{T_{\text{CPU}}}{T_{\text{GPU}}}\).  
4. **Replicate** the timing at least **10 times** for each platform to obtain a distribution of speedup values, then compute mean and 95 % confidence interval.  

*Pass criterion:* The **lower bound of the 95 % CI** of the speedup is ≥ 3.

---

## 4.  Overlapping host‑to‑device (H2D) and device‑to‑host (D2H) transfers with CUDA streams will improve overall GPU‑pipeline throughput by **> 50 %** compared with a fully sequential (non‑overlapped) execution.

**Why it is testable**  
* The claim is about the **percentage throughput gain** of overlapped versus sequential pipelines, which can be quantified by measuring end‑to‑end wall‑clock time under two controlled execution modes.  
* The hypothesis is falsifiable: if the measured gain is ≤ 50 % the hypothesis is rejected.  

**Experiment**  
1. **Implement two GPU versions**:  
   * **Sequential version**: allocate a single CUDA stream, transfer a full chunk, run the kernel, transfer result, repeat for all chunks.  
   * **Overlapped version**: use multiple streams (e.g., 4–8) and launch the next H2D while the current kernel runs (depth‑first pipeline).  
2. **Run both versions** for the same workload (primorial bases, N = 10⁷) and record the **total elapsed time** for each.  
3. **Compute gain**: \(\text{Gain} = \frac{T_{\text{seq}} - T_{\text{overlap}}}{T_{\text{seq}}} \times 100\%\).  
4. **Repeat** at least 5 times to mitigate variance; report mean gain and standard deviation.  

*Pass criterion:* The **mean gain** exceeds 50 %.

---

### How these hypotheses together address the research problem  

| Research Question | Addressed By |
|-------------------|--------------|
| **Memory‑Efficient Architecture** – can chunking keep VRAM within consumer limits? | Hypothesis 1 (VRAM ceiling) |
| **Algorithmic Integrity** – do the GPU results match CPU? | Hypothesis 2 (statistical equivalence) |
| **Small‑Scale Speedup** – is the GPU faster enough? | Hypothesis 3 (≥ 3× speedup) |
| **Pipelining Benefit** – does overlapping transfers help? | Hypothesis 4 (> 50 % throughput gain) |

All four hypotheses are **quantitative, measurable, and reproducible** under the constrained environment (consumer‑grade GPU, bound ≤ 10⁷). Running the experiments described above will provide the data needed to accept or reject each hypothesis and, consequently, give a clear go/no‑go signal for scaling the architecture to the higher primorial bounds (10⁹–10¹²) in later phases.