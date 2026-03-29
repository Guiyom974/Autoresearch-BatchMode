

# Testable Hypotheses for Multi-GPU Distributed LDAB Scaling Research

Based on the research problem, here are five testable hypotheses addressing the core objectives of scaling efficiency, numerical accuracy, and throughput optimization.

---

## Hypothesis 1: Multi-GPU Scaling Efficiency

### 1. Hypothesis Statement

The distributed processing of 389 independent chunks across a 4x GPU configuration will achieve **≥85% linear scaling efficiency**, defined as (T₁/T₄) / 4 × 100%, where T₁ and T₄ represent wall-clock execution times for single and quad-GPU configurations, respectively.

### 2. Why It's Testable

This hypothesis is directly measurable through empirical benchmarking. The independent nature of the 389 chunks allows for clean distribution across GPUs with minimal inter-chunk dependencies. Scaling efficiency can be computed as a ratio of ideal to actual speedup, providing a quantitative metric that can be compared against the 85% threshold specified in the success criteria. The null hypothesis (H₀: efficiency < 85%) can be rejected if the measured efficiency exceeds the threshold with statistical confidence across multiple trial runs.

### 3. Experiment to Test It

- **Setup**: Execute the full N=10¹² LDAB evaluation using 1, 2, 4, and 8 GPU configurations
- **Measurements**: Record wall-clock time (T), throughput (primes/second), and per-GPU utilization for each configuration
- **Analysis**: Calculate scaling efficiency as S(n) = T₁/(n × Tₙ) × 100% for each GPU count n; plot strong scaling curve
- **Validation**: Repeat trials (n≥5) to compute mean efficiency and 95% confidence intervals; verify whether lower bound of CI exceeds 85%

---

## Hypothesis 2: Precision-Preserving Aggregation Fidelity

### 1. Hypothesis Statement

Implementing **Kahan summation** during global reduction will maintain KL divergence accuracy to **≥7 significant decimal places** compared to high-precision CPU-based verification, whereas standard atomic addition will degrade accuracy below 5 decimal places at N=10¹².

### 2. Why It's Testable

This hypothesis establishes a comparative framework between summation methods. A high-precision CPU implementation (using arbitrary-precision libraries or verified analytical values) serves as the ground truth reference. The difference in KL divergence outputs between methods can be quantified numerically, enabling direct comparison against the 7-decimal-place threshold. The experiment can isolate the effect of summation methodology by controlling for all other variables.

### 3. Experiment to Test It

- **Baseline**: Compute theoretical LDAB leading-digit distribution and resulting KL divergence analytically for N=10¹²
- **Control Group**: Run multi-GPU LDAB evaluation using standard floating-point atomicAdd for aggregation
- **Treatment Group**: Run identical evaluation using Kahan summation (and optionally Neumaier summation) for aggregation
- **Comparison**: Calculate |KL_treatment − KL_theoretical| and |KL_control − KL_theoretical|; express as decimal place agreement
- **Statistical Test**: Perform paired t-test across ≥10 independent trials to determine significance of accuracy difference

---

## Hypothesis 3: Dynamic Chunk Allocation Superiority

### 1. Hypothesis Statement

**Dynamic chunk allocation** based on real-time GPU availability and VRAM monitoring will achieve **≥20% higher throughput** than static round-robin chunk distribution across heterogeneous multi-GPU nodes, due to improved load balancing and reduced GPU idle time.

### 2. Why It's Testable

The comparison between dynamic and static allocation strategies is operationally straightforward to implement and measure. Throughput (chunks processed per second) provides a direct, objective metric for comparison. The 20% threshold represents a meaningful performance gap that can be reliably detected through replicated benchmarking trials. The hypothesis specifically addresses heterogeneous environments where static allocation would fail to adapt to varying GPU states.

### 3. Experiment to Test It

- **Simulation**: Create artificial heterogeneity by introducing computational load delays on subset of GPUs (simulating varying workloads)
- **Static Test**: Distribute 389 chunks evenly using round-robin assignment; measure total execution time and per-GPU utilization variance
- **Dynamic Test**: Implement manager-based allocation (analogous to vTensor architecture) with real-time VRAM and availability monitoring; measure same metrics
- **Metrics**: Calculate coefficient of variation (CV) in per-GPU completion times and overall throughput ratio
- **Rejection Criterion**: Reject H₀ if dynamic method shows ≥20% throughput improvement and ≥30% reduction in CV

---

## Hypothesis 4: Communication Overhead Bounds

### 1. Hypothesis Statement

For configurations with ≥4 GPUs, **inter-GPU communication overhead** during the final reduction phase will constitute **<10% of total execution time**, ensuring that network transfers do not negate the computational speedup from parallel chunk processing.

### 2. Why It's Testable

Communication time can be explicitly instrumented using CUDA events and NCCL timing primitives before and after collective operations. The 10% threshold provides a clear demarcation between acceptable and problematic communication overhead. By profiling both collective communication time and pure computation time separately, the proportion can be calculated definitively. This hypothesis is falsifiable—if communication exceeds 10%, the hypothesis is rejected regardless of throughput gains.

### 3. Experiment to Test It

- **Instrumentation**: Insert CUDA event markers around all NCCL all-reduce and MPI reduction operations
- **Timing Protocol**: Measure T_compute (chunk processing) and T_comm (reduction operations) independently for 4x and 8x configurations
- **Profiling**: Use NVTX markers and NCCL backend timing to decompose T_comm into intra-node (NVLink) and inter-node (InfiniBand/RoCE) components
- **Threshold Check**: Calculate ratio R = T_comm / (T_compute + T_comm) × 100%; verify R < 10%
- **Sensitivity Analysis**: Measure R across varying chunk sizes (e.g., 2.57B, 5B, 10B elements per chunk) to identify optimal granularity

---

## Hypothesis 5: Weak Scaling vs. Strong Scaling Efficiency Divergence

### 1. Hypothesis Statement

**Weak scaling efficiency** (maintaining constant workload per GPU while increasing GPU count) will exceed **strong scaling efficiency** (constant total workload with increasing GPU count) by **≥15 percentage points** at 8x GPU configurations, due to reduced synchronization overhead when problem size per GPU remains constant.

### 2. Why It's Testable

Both weak and strong scaling experiments are standard HPC benchmarking methodologies. By holding either total problem size (strong) or per-GPU workload (weak) constant, the scaling efficiency differential emerges naturally from the measured times. The 15 percentage point difference is detectable with reasonable trial counts and provides clear evidence of synchronization effects. This hypothesis addresses a fundamental scaling law prediction that can be empirically validated.

### 3. Experiment to Test It

- **Strong Scaling**: Fix N=10¹² total elements; distribute across 1, 2, 4, and 8 GPUs; measure Tₙ
- **Weak Scaling**: Fix per-GPU chunk count at 389/n for n GPUs (maintaining ~2.57B elements per GPU); measure Tₙ
- **Efficiency Calculation**:
  - Strong: E_strong(n) = T₁/(n × Tₙ) × 100%
  - Weak: E_weak(n) = T₁/Tₙ × 100% (ideal = 100%)
- **Comparison**: For each n≥4, calculate ΔE = E_weak(n) − E_strong(n)
- **Confirmation**: Hypothesis supported if ΔE ≥ 15% for n=8 configuration across ≥5 replicated trials

---

## Summary Table

| Hypothesis | Independent Variable | Dependent Variable | Threshold | Test Type |
|------------|---------------------|---------------------|-----------|-----------|
| H1: Scaling Efficiency | GPU count (1→4→8) | Scaling efficiency % | ≥85% | Strong scaling benchmark |
| H2: Precision Fidelity | Summation method | KL divergence accuracy (decimal places) | ≥7 places | Comparative accuracy test |
| H3: Dynamic Allocation | Allocation strategy | Throughput improvement % | ≥20% | A/B comparison with heterogeneity |
| H4: Comm. Overhead | GPU count + topology | Communication time proportion % | <10% | Profiling and timing analysis |
| H5: Weak vs Strong | Scaling paradigm | Efficiency differential % | ≥15 pp | Dual scaling benchmark |

These hypotheses collectively address the research questions while providing concrete, measurable outcomes aligned with the stated success criteria.