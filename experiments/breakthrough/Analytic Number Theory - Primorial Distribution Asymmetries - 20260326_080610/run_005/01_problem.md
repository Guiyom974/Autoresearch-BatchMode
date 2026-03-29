# Research Problem: Memory-Optimized GPU Pipelines and Small-Scale Validation for LDAB Model Evaluation

## Objective
Initial attempts to implement massive-scale GPU acceleration for evaluating the Logarithmic-Density-Adjusted Benford (LDAB) model in high primorial bases encountered critical memory allocation and array-handling bottlenecks. Naive parallelization of base conversion and sieving at high bounds exceeds standard VRAM limits and causes memory-indexing faults. Therefore, before scaling to bounds of $10^9$ to $10^{12}$, this phase pivots to developing a memory-efficient, chunked GPU architecture. The objective is to design a robust data pipeline that correctly handles array allocations for primorial base conversions and to validate the computational integrity of this pipeline on small-scale bounds ($10^6$ to $10^7$) against validated CPU baselines.

## Research Questions
1. **Memory-Efficient Architecture:** How can chunked batch processing and optimized VRAM allocation strategies resolve the memory overhead and indexing faults associated with massive primorial base conversions on GPUs?
2. **Algorithmic Integrity:** Does the memory-optimized GPU pipeline yield identical leading-digit counts and KL-divergence metrics for the LDAB model as the established CPU implementation at smaller bounds ($10^7$)?
3. **Small-Scale Speedup:** Can a strictly memory-managed GPU implementation achieve a baseline performance speedup (e.g., $\ge 3\times$) over CPU-bound methods at small scales, thereby proving viability for future high-bound scaling?

## Methodology
1. **Pipeline Restructuring:** Redesign the GPU base-conversion algorithm to use batched/chunked processing, ensuring that prime arrays transferred to the device do not exceed safe memory thresholds.
2. **Memory Profiling:** Implement strict memory profiling to track VRAM usage during the parallel sieving and base conversion steps, ensuring array indices are correctly mapped within local thread blocks.
3. **Small-Scale Validation:** Run the LDAB model evaluation on prime bounds up to $10^7$ across several initial primorial bases (e.g., $p_2\#, p_3\#, p_4\#$).
4. **Comparative Analysis:** Cross-verify the GPU-generated leading digit distributions against the CPU baseline to guarantee that no precision or data is lost during the chunked GPU processing.

## Success Criteria
1. **Stability:** The GPU implementation executes flawlessly without memory allocation errors or out-of-bounds array faults.
2. **Accuracy:** The GPU pipeline produces $100\%$ identical leading digit distributions and LDAB KL-divergence results compared to the validated CPU baseline at $10^7$.
3. **Performance Viability:** The stabilized GPU implementation demonstrates at least a $3\times$ speedup over the CPU baseline at the $10^7$ bound, validating the architecture's potential for scaling.

## Constraints
1. **Scale Limitation:** Testing must be strictly capped at a maximum bound of $10^7$ until memory stability and algorithmic accuracy are definitively proven.
2. **Domain Focus:** All optimizations must strictly serve the evaluation of the LDAB model and Chebyshev's bias in primorial bases; general-purpose GPU benchmarking is out of scope. 
3. **Hardware Constraints:** The memory architecture must be designed to function within standard consumer-grade GPU VRAM limitations (e.g., 8GB - 16GB) to ensure reproducible and accessible research.