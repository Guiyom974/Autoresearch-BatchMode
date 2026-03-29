

# Testable Hypotheses for GPU-Accelerated LDAB Model Evaluation

Based on the research problem and search context, I propose the following five testable hypotheses:

---

## Hypothesis 1: GPU-Accelerated Parallel Processing Achieves ≥5x Speedup Over CPU-Memoized Baseline

### 1. Statement
GPU-accelerated segmented sieving combined with custom kernel-based leading digit extraction will achieve at least a 5x (500%) reduction in execution time compared to the optimized CPU-memoized implementation for sample sizes ≥10⁶ in high primorial bases (≥2310).

### 2. Why It's Testable
This hypothesis is directly measurable through controlled benchmarking experiments. Speedup ratio is an objective metric derived from execution time comparisons between the GPU pipeline and the established CPU baseline, requiring only standardized timing methodology and identical input parameters.

### 3. Experiment Design
- **Independent Variable:** Processing architecture (GPU vs. CPU-memoized)
- **Dependent Variable:** Execution time in seconds
- **Constants:** Sample sizes (10⁶, 10⁷, 10⁸, 10⁹), primorial bases (2310, 30030, 510510), algorithmic parameters
- **Procedure:**
  1. Implement GPU pipeline using CUDA/Numba with CUDASieve-style segmented sieving
  2. Benchmark GPU implementation across all sample sizes and primorial bases
  3. Run identical workloads on CPU-memoized baseline
  4. Calculate speedup ratios: Speedup = T_CPU / T_GPU
- **Success Threshold:** Speedup ≥ 5.0 for all sample sizes ≥10⁶

---

## Hypothesis 2: Batched Segmented Sieving Prevents VRAM Saturation While Maintaining Throughput ≥10 GB/s

### 1. Statement
Chunk-based batched processing, where sieving arrays are segmented into chunks that fit within available VRAM (≤16GB), will prevent memory exhaustion while achieving sustained throughput comparable to CUDASieve benchmarks (~15 GB/s) when processing up to 10⁹ bounds.

### 2. Why It's Testable
VRAM usage and throughput (GB/s) are directly measurable using CUDA memory profiling tools (nvidia-smi, nvprof). The hypothesis tests whether a critical trade-off—batched processing for memory safety versus throughput loss—can be resolved.

### 3. Experiment Design
- **Independent Variables:** Chunk size (varying from 1GB to 16GB VRAM allocation), batch count
- **Dependent Variables:** Peak VRAM usage (GB), sustained throughput (GB/s), execution success rate
- **Constants:** Target bound (10⁹), primorial base, GPU hardware specification
- **Procedure:**
  1. Implement adaptive chunking algorithm with dynamic batch sizing
  2. Monitor VRAM consumption per batch using CUDA memory APIs
  3. Measure aggregate throughput across all batches
  4. Record any out-of-memory (OOM) failures
- **Success Threshold:** Peak VRAM < 16GB, sustained throughput ≥ 10 GB/s, 0% OOM failure rate

---

## Hypothesis 3: LDAB Model KL Divergence Remains Stable (≤0.19) Across Extended Primorial Bases

### 1. Statement
When computational bottlenecks are resolved via GPU parallelization, the LDAB model's Kullback-Leibler divergence will remain stable at approximately 0.19 or lower when extended from base 2310 to larger primorial bases (30030 and 510510) at sample sizes up to 10⁹.

### 2. Why It's Testable
KL divergence is a mathematically defined metric with established confidence intervals. Statistical stability can be tested using confidence interval analysis across multiple runs and base configurations, with significance testing against the 0.19 threshold.

### 3. Experiment Design
- **Independent Variable:** Primorial base (2310, 30030, 510510)
- **Dependent Variable:** KL divergence (D_KL) between empirical and theoretical LDAB distributions
- **Constants:** Sample size (10⁹), significance level (α = 0.05)
- **Procedure:**
  1. Generate prime sequences up to 10⁹ for each primorial base using GPU pipeline
  2. Extract leading digits in each base using parallel kernel
  3. Compute empirical frequency distributions
  4. Calculate theoretical LDAB distributions for each base
  5. Compute D_KL with bootstrapped 95% confidence intervals
- **Success Threshold:** D_KL ≤ 0.19 with 95% CI for all bases

---

## Hypothesis 4: Custom Leading-Digit Extraction Kernels Outperform General-Purpose GPU Base Conversion

### 1. Statement
A specialized GPU kernel that computes leading digits directly via modular arithmetic (rather than full base conversion followed by digit extraction) will demonstrate superior performance, reducing kernel execution time by ≥40% compared to naive two-step approaches.

### 2. Why It's Testable
Kernel execution time is directly measurable through CUDA profiling tools (Nsight, nvprof). The comparison isolates the algorithmic optimization from hardware effects by using identical GPU hardware and workload parameters.

### 3. Experiment Design
- **Independent Variable:** Kernel implementation (specialized vs. two-step)
- **Dependent Variables:** Kernel execution time (ms), instructions per warp, memory transactions
- **Constants:** Input size (10⁸ primes), primorial base, GPU hardware
- **Procedure:**
  1. Implement naive approach: full base conversion → digit extraction (two kernels)
  2. Implement specialized approach: direct leading-digit via modular arithmetic (single kernel)
  3. Profile both kernels using Nsight Compute
  4. Compare kernel execution times and compute speedup percentage
- **Success Threshold:** Specialized kernel ≥40% faster execution time

---

## Hypothesis 5: GPU Parallel Floating-Point Operations Preserve KL Divergence Precision Within ±0.01

### 1. Statement
Parallel floating-point computations in the GPU kernel, when executed with IEEE 754 single-precision and log-density adjustments, will produce KL divergence values within ±0.01 of the CPU double-precision reference implementation, ensuring precision meets the scientific output requirements.

### 2. Why It's Testable
Precision comparison is achievable by running identical workloads on CPU (double-precision) and GPU (single-precision) and computing the absolute difference in KL divergence outputs. This is a deterministic comparison with quantifiable error bounds.

### 3. Experiment Design
- **Independent Variable:** Floating-point precision mode (CPU double-precision vs. GPU single-precision)
- **Dependent Variable:** KL divergence difference |D_KL(GPU) - D_KL(CPU)|
- **Constants:** Sample size, primorial base, random seed (for reproducibility)
- **Procedure:**
  1. Compute reference KL divergence on CPU using double-precision (64-bit)
  2. Execute identical pipeline on GPU using single-precision (32-bit)
  3. Aggregate GPU results and compute KL divergence
  4. Calculate absolute error: ε = |D_KL(GPU) - D_KL(CPU)|
  5. Repeat across 10 independent runs for variance estimation
- **Success Threshold:** Mean |ε| ≤ 0.01 with standard deviation ≤ 0.005

---

## Summary Table

| Hypothesis | Core Claim | Key Metric | Success Threshold |
|------------|------------|------------|-------------------|
| H1 | GPU achieves ≥5x speedup | Speedup ratio | ≥ 5.0 |
| H2 | Batching prevents VRAM saturation | Peak VRAM, throughput | <16GB, ≥10 GB/s |
| H3 | KL divergence remains stable | D_KL | ≤ 0.19 |
| H4 | Custom kernels outperform naive | Kernel execution time | ≥40% faster |
| H5 | FP precision is preserved | |Δ_D_KL| | ≤ 0.01 |

These hypotheses collectively address the three research questions and provide a comprehensive evaluation framework for determining both computational feasibility and scientific validity of the GPU-accelerated LDAB model evaluation approach.