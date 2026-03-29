

Below are four testable hypotheses that directly address the three research questions and the success criteria outlined in the problem statement. Each hypothesis includes a clear statement, an explanation of why it is testable, and a specific experiment designed to evaluate it.

---

### **Hypothesis 1: Memory Stability via Dynamic Chunk Allocation**
**Statement:**  
The dynamic chunk-sizing algorithm, which queries available VRAM and scales processing batches automatically, will enable the GPU-accelerated LDAB pipeline to execute uninterrupted up to \( N = 10^{12} \) on a standard 24 GB GPU without encountering Out‑of‑Memory (OOM) errors.

**Why it’s testable:**  
We can directly monitor VRAM usage during execution and record whether the process completes successfully or fails with an OOM error. By varying the bound \( N \) from \( 10^9 \) to \( 10^{12} \) and measuring peak VRAM consumption, we can verify that the algorithm keeps usage below the 24 GB limit.

**Experiment:**  
1. **Hardware & Software Setup:**  
   - GPU: NVIDIA RTX 3090 (24 GB) or equivalent.  
   - CUDA environment with memory‑allocation callbacks to track peak usage.  
   - Implement the dynamic chunk‑allocation routine that adjusts batch size based on `cudaMemGetInfo`.  
2. **Test Matrix:**  
   - Execute the full LDAB pipeline for primorial bases up to \( P_{10} = 6,469,693,230 \) at \( N = 10^9, 10^{10}, 10^{11}, 10^{12} \).  
   - For each \( N \), record:  
     - Peak VRAM allocated (bytes).  
     - Number of successful chunk completions.  
     - Occurrence of OOM faults.  
3. **Success Metric:**  
   - Zero OOM errors across all \( N \) values, with peak VRAM ≤ 24 GB.  
   - Validate that the number of chunks processed matches the expected count based on the dynamic sizing algorithm.

---

### **Hypothesis 2: End‑to‑End Throughput Gain on GPU**
**Statement:**  
The fully integrated GPU LDAB pipeline will achieve at least a **10× speedup** over a highly optimized multi‑core CPU baseline when processing bounds \( N \ge 10^9 \), measured by wall‑clock time from start of prime sieving to final KL‑divergence output.

**Why it’s testable:**  
Throughput is quantifiable via elapsed time. By benchmarking both GPU and CPU implementations under identical logical workloads, we can compute the speedup ratio and compare it to the 10× threshold.

**Experiment:**  
1. **Baseline (CPU):**  
   - Multi‑core CPU implementation (e.g., using OpenMP on an 8‑core AMD Ryzen 9 5950X).  
   - Optimized prime sieving (segmented Eratosthenes) and base‑conversion.  
   - Process the same primorial sets and compute KL‑divergence.  
2. **GPU Pipeline:**  
   - Same logical steps but executed on GPU with vectorized kernels.  
   - Use CUDA events to measure kernel execution time, including data transfers.  
3. **Measurement Protocol:**  
   - Run each benchmark at logarithmic intervals: \( N = 10^8, 10^9, 10^{10}, 10^{11}, 10^{12} \).  
   - Record total wall‑clock time for the entire pipeline (sieving → base conversion → digit extraction → KL‑divergence).  
   - Compute speedup = \( \frac{\text{CPU time}}{\text{GPU time}} \).  
4. **Success Metric:**  
   - For all \( N \ge 10^9 \), speedup ≥ 10×.  
   - Report average speedup and standard deviation across runs.

---

### **Hypothesis 3: Numerical Accuracy Preservation in KL‑Divergence**
**Statement:**  
The KL‑divergence values produced by the GPU pipeline will match those from the CPU baseline **within a strict floating‑point tolerance of \( 1 \times 10^{-8} \)** for all tested bounds, ensuring that vectorized GPU arithmetic does not introduce systematic bias.

**Why it’s testable:**  
KL‑divergence is a scalar metric that can be computed on both platforms and compared directly. The tolerance is a concrete, measurable threshold.

**Experiment:**  
1. **Data Generation:**  
   - Generate leading‑digit frequency tables for each primorial base using the CPU pipeline.  
   - Store the resulting arrays as reference.  
2. **GPU Execution:**  
   - Run the GPU pipeline under identical parameters.  
   - Capture the resulting leading‑digit frequencies and compute KL‑divergence on the GPU (using a reduction kernel).  
3. **Comparison:**  
   - Compute \( \Delta = |D_{\text{CPU}} - D_{\text{GPU}}| \) for each base and \( N \).  
   - Verify \( \Delta \le 1 \times 10^{-8} \).  
4. **Success Metric:**  
   - 100 % of tests pass the tolerance.  
   - Additionally, perform a paired t‑test across multiple runs to confirm no statistically significant drift.

---

### **Hypothesis 4: Minimal Host‑Device Transfer Overhead**
**Statement:**  
For \( N = 10^{12} \), the cumulative time spent transferring data between host (CPU) and device (GPU) will be **less than 5 % of the total GPU computation time**, ensuring that chunking overhead does not erode the vectorization speedup.

**Why it’s testable:**  
CUDA provides precise timing mechanisms (e.g., `cudaEvent_t`) that separate kernel execution time from memcpy time. By annotating transfers and kernels, we can quantify their respective contributions.

**Experiment:**  
1. **Instrumentation:**  
   - Wrap all `cudaMemcpy` calls with start/stop events.  
   - Sum the elapsed times for H2D and D2H transfers.  
   - Capture kernel execution times (including memory copies) separately.  
2. **Workload:**  
   - Process the largest test case: \( N = 10^{12} \) with the highest primorial base \( P_{10} \).  
   - Use the dynamic chunking scheme; record per‑chunk transfer and compute times.  
3. **Analysis:**  
   - Compute ratio: \( \frac{\text{Transfer time}}{\text{Kernel time}} \).  
   - Success threshold: ratio < 0.05.  
4. **Success Metric:**  
   - Confirm that transfer overhead remains below 5 % across at least three independent runs.  
   - If the threshold is exceeded, investigate whether async streaming or prefetching can reduce the ratio.

---

### **Alignment with Research Questions & Success Criteria**

| Hypothesis | Addresses Research Question | Links to Success Criterion |
|------------|----------------------------|----------------------------|
| 1 – Memory Stability | Q1: Memory Stability at Scale | “Execution at Scale” (no VRAM faults) |
| 2 – Throughput | Q2: End‑to‑End Throughput | “Performance Gains” (≥10× speedup) |
| 3 – Accuracy | Q3: Precision & Accuracy Preservation | “Data Integrity” (KL‑divergence tolerance) |
| 4 – Transfer Overhead | Implicit in Q2 (chunking must not negate speedup) | “Constraints” (minimize data transfer impact) |

---

### **Summary of Testable Hypotheses**

1. **Dynamic chunk allocation will sustain VRAM ≤ 24 GB up to \( N = 10^{12} \).**  
2. **GPU pipeline will achieve ≥ 10× speedup over multi‑core CPU for \( N \ge 10^9 \).**  
3. **KL‑divergence outputs from GPU and CPU will agree within \( 1 \times 10^{-8} \).**  
4. **Host‑device transfer time will be < 5 % of total GPU compute time at \( N = 10^{12} \).**

Each hypothesis is concrete, measurable, and directly tied to the project’s objectives, allowing the research team to validate the LDAB model’s scalability, performance, and numerical integrity on modern GPU hardware.