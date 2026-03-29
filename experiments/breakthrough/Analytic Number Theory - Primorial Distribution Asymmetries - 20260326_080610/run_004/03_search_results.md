
### Query: GPU accelerated parallel prime sieving algorithms CUDA performance
Here is a summary of 5 notable GPU-accelerated parallel prime sieving algorithms and their CUDA performance based on recent search results:

### 1. CUDASieve (Segmented Sieve & Bucket Algorithm)
**Overview:** CUDASieve is a high-performance C++/CUDA implementation of the segmented Sieve of Eratosthenes. It incorporates Tomás Oliveira e Silva's Bucket algorithm, which is highly effective for handling large primes in global memory without duplicating the dataset across blocks [[1]](https://github.com/curtisseizert/CUDASieve).
**Performance:** On an NVIDIA GTX 1080, it can generate a list of 189.9 million sieving primes (up to 4 billion) in just 50 milliseconds. This translates to a processing speed of about 15.2 GB of primes per second, effectively saturating the PCIe 3.0 x16 bandwidth limit [[1]](https://github.com/curtisseizert/CUDASieve).

### 2. DAWS (Dual-Wheel Adaptive Wave Sieve)
**Overview:** Introduced in early 2026, DAWS is a hybrid GPU–CPU framework designed to overcome traditional memory bandwidth bottlenecks at massive scales. Instead of treating the GPU merely as a "prime generator," it uses the GPU for constant-cost "structural elimination" while candidate density is high [[2]](https://forums.developer.nvidia.com/t/a-new-gpu-accelerated-prime-sieve-using-constant-cost-structural-elimination-to-overcome-memory-bandwidth-limits-at-massive-scales/357200). 
**Performance:** It features an "Adaptive Cutoff Control" that dynamically shifts the remaining sparse workload (phase-jump traversal) to the CPU once the prime candidate density collapses. It also utilizes a zero-copy strategy with delta-varint encoding to compress surviving primes on the GPU, approaching the theoretical minimum for host-device data transfer overhead [[2]](https://forums.developer.nvidia.com/t/a-new-gpu-accelerated-prime-sieve-using-constant-cost-structural-elimination-to-overcome-memory-bandwidth-limits-at-massive-scales/357200).

### 3. bbuhrow's CUDA Sieve of Eratosthenes
**Overview:** This implementation focuses on heavy parallelization by segmenting the sieve interval. Each thread block is assigned a sub-interval, and within each block, 256 threads simultaneously sieve 8192 bytes of shared memory [[3]](https://sites.google.com/site/bbuhrow/home/cuda-sieve-of-eratosthenes). 
**Performance:** The algorithm avoids race conditions by using byte writes instead of read-modify-write operations. Optimizations include a "mod 6" wheel, hand-unrolled inner loops, and small-prime bit-packing. It is capable of sieving the range from 0 to 1 billion in just 38 milliseconds on an older M2050 Tesla card [[3]](https://sites.google.com/site/bbuhrow/home/cuda-sieve-of-eratosthenes).

### 4. N/6 Bit Sieve Methodology
**Overview:** A recent (2026) hybrid CUDA/OpenMP approach focused on extreme memory optimization. 
**Performance:** By utilizing an "N/6 Bit" methodology, this algorithm drastically minimizes the memory footprint required on the GPU. This allows the sieve to process massive ranges that would normally exceed standard GPU VRAM limits, making it highly scalable for modern and upcoming GPU architectures [[4]](https://www.reddit.com/r/CUDA/comments/1qfxhwq/research_on_n6_bit_sieve_methodology_for/).

### 5. Multi-GPU Segmented Sieve
**Overview:** This approach maximizes both parallelism and locality of reference by breaking the sieve into isolated chunks. Because the chunks are small enough to fit into cache and are completely independent, tens of thousands of them can be processed concurrently across multiple GPUs [[5]](https://www.youtube.com/watch?v=AVcIVLBWRPk).
**Performance:** By using a bit-array to mark composites and isolating the chunks, the algorithm scales significantly better than CPU-only code, allowing for massive throughput when computing the $N$th prime [[5]](https://www.youtube.com/watch?v=AVcIVLBWRPk). 

**Sources:**
* [[3]](https://sites.google.com/site/bbuhrow/home/cuda-sieve-of-eratosthenes) CUDA Sieve of Eratosthenes - bbuhrow [[3]](https://sites.google.com/site/bbuhrow/home/cuda-sieve-of-eratosthenes)
* [[6]](https://github.com/daddel80/PrimeNumber-Calculation-Performance) NVIDIA Developer Forums: DAWS Framework [[2]](https://forums.developer.nvidia.com/t/a-new-gpu-accelerated-prime-sieve-using-constant-cost-structural-elimination-to-overcome-memory-bandwidth-limits-at-massive-scales/357200)
* [[2]](https://forums.developer.nvidia.com/t/a-new-gpu-accelerated-prime-sieve-using-constant-cost-structural-elimination-to-overcome-memory-bandwidth-limits-at-massive-scales/357200) GitHub: curtisseizert/CUDASieve [[1]](https://github.com/curtisseizert/CUDASieve)
* [[1]](https://github.com/curtisseizert/CUDASieve) YouTube: CUDA Multi-GPU Segmented Sieve [[5]](https://www.youtube.com/watch?v=AVcIVLBWRPk)
* [[5]](https://www.youtube.com/watch?v=AVcIVLBWRPk) Reddit: Research on N/6 Bit Sieve Methodology [[4]](https://www.reddit.com/r/CUDA/comments/1qfxhwq/research_on_n6_bit_sieve_methodology_for/)

---
Learn more:
1. [curtisseizert/CUDASieve: A GPU accelerated implementation of the sieve of Eratosthenes - GitHub](https://github.com/curtisseizert/CUDASieve)
2. [A new GPU-accelerated prime sieve using constant-cost structural elimination to overcome memory bandwidth limits at massive scales - CUDA Programming and Performance - NVIDIA Developer Forums](https://forums.developer.nvidia.com/t/a-new-gpu-accelerated-prime-sieve-using-constant-cost-structural-elimination-to-overcome-memory-bandwidth-limits-at-massive-scales/357200)
3. [CUDA Sieve of Eratosthenes - bbuhrow](https://sites.google.com/site/bbuhrow/home/cuda-sieve-of-eratosthenes)
4. [Research on N/6 Bit Sieve Methodology for High-Performance Prime Generation (CUDA/OMP - Reddit](https://www.reddit.com/r/CUDA/comments/1qfxhwq/research_on_n6_bit_sieve_methodology_for/)
5. [CUDA Multi-GPU Segmented Sieve of Eratosthenes to find the Nth prime - YouTube](https://www.youtube.com/watch?v=AVcIVLBWRPk)
6. [daddel80/PrimeNumber-Calculation-Performance: Comparing efficiency of prime number algorithms, including the Sieve of Eratosthenes and Trial Division, with different optimization techniques such as multiprocessing and GPU computing (CUDA). - GitHub](https://github.com/daddel80/PrimeNumber-Calculation-Performance)



### Query: large scale arbitrary precision base conversion GPU primorial radix
Here is a summary of the search results related to large-scale arbitrary precision base conversion, GPU implementations, and radix systems. Note that while there is extensive research on GPU-accelerated arbitrary precision arithmetic and radix algorithms, literature specifically combining all these exact terms (like "primorial radix" for GPU base conversion) is highly specialized or not explicitly indexed in the top results. 

Here are the top 5 related results summarized:

### 1. Efficient GPU Implementation of Multiple-Precision Arithmetic
**Source:** [The Science and Information (SAI) Organization](https://thesai.org/Downloads/Volume11No9/Paper_1-Efficient_GPU_Implementation_of_Multiple_Precision.pdf) [[1]](https://thesai.org/Downloads/Volume11No9/Paper_1-Efficient_GPU_Implementation_of_Multiple_Precision.pdf)
*   **Summary:** This paper discusses the use of the Residue Number System (RNS) for efficient multiple-precision integer arithmetic on GPUs using CUDA [[1]](https://thesai.org/Downloads/Volume11No9/Paper_1-Efficient_GPU_Implementation_of_Multiple_Precision.pdf). RNS allows calculations on digits of a multiple-precision number to be performed in an element-wise fashion without communication overhead between them, making it ideal for massively parallel GPU architectures [[1]](https://thesai.org/Downloads/Volume11No9/Paper_1-Efficient_GPU_Implementation_of_Multiple_Precision.pdf). The authors present algorithms that use radix complement RNS arithmetic to handle negative numbers, effectively avoiding branch divergence among threads and outperforming multi-core CPU implementations [[1]](https://thesai.org/Downloads/Volume11No9/Paper_1-Efficient_GPU_Implementation_of_Multiple_Precision.pdf).

### 2. RadiK: Scalable and Optimized GPU-Parallel Radix Top-K Selection
**Source:** [arXiv (2025)](https://arxiv.org/html/2501.14336v1) [[2]](https://arxiv.org/html/2501.14336v1)
*   **Summary:** While focused on selection algorithms rather than pure base conversion, this paper highlights the challenges and optimizations of implementing Radix-based algorithms on GPUs [[2]](https://arxiv.org/html/2501.14336v1). It discusses how standard radix operations (like parallel prefix scans over histograms) face challenges with global memory access and variable-length arrays [[2]](https://arxiv.org/html/2501.14336v1). The research demonstrates how to optimize radix-based data processing to leverage the Single-Instruction Multiple-Thread (SIMT) architecture of modern GPUs [[2]](https://arxiv.org/html/2501.14336v1).

### 3. Converting Between Arbitrary Real-Valued Base Systems
**Source:** [Math Stack Exchange](https://math.stackexchange.com/questions/4592617/converting-between-arbitrary-real-valued-base-systems) [[3]](https://math.stackexchange.com/questions/4592617/converting-between-arbitrary-real-valued-base-systems)
*   **Summary:** This discussion explores the theoretical mathematics behind converting numbers into arbitrary, non-integer, and real-valued bases (such as base $\pi$, $e$, or $\sqrt{2}$) [[3]](https://math.stackexchange.com/questions/4592617/converting-between-arbitrary-real-valued-base-systems). It notes that standard integer base conversion algorithms (which rely on fractional remainders) do not generalize easily to arbitrary real numbers [[3]](https://math.stackexchange.com/questions/4592617/converting-between-arbitrary-real-valued-base-systems). The thread highlights the mathematical complexity of calculating digits up to an arbitrary precision when the radix is not a standard integer [[3]](https://math.stackexchange.com/questions/4592617/converting-between-arbitrary-real-valued-base-systems).

### 4. Base Conversions from Base 2 through 100 Using Radix Points
**Source:** [Wolfram Demonstrations Project](https://demonstrations.wolfram.com/BaseConversionsFromBase2Through100UsingRadixPoints/) [[4]](https://demonstrations.wolfram.com/BaseConversionsFromBase2Through100UsingRadixPoints/)
*   **Summary:** This demonstration outlines the standard algorithmic approach for converting numbers with fractional parts (using radix points) across a wide scale of integer bases (up to base 100) [[4]](https://demonstrations.wolfram.com/BaseConversionsFromBase2Through100UsingRadixPoints/). It separates the process into integer division for the whole number and iterative multiplication by the target radix for the fractional part, calculating out to a specified arbitrary precision [[4]](https://demonstrations.wolfram.com/BaseConversionsFromBase2Through100UsingRadixPoints/). 

### 5. Tricks for Radix Conversion by Hand
**Source:** [Applied Mathematics Consulting / John D. Cook](https://www.johndcook.com/blog/2025/01/23/radix-conversion/) [[5]](https://www.johndcook.com/blog/2025/01/23/radix-conversion/)
*   **Summary:** This article reviews mathematical shortcuts for radix conversion, heavily referencing Donald Knuth's *The Art of Computer Programming* [[5]](https://www.johndcook.com/blog/2025/01/23/radix-conversion/). It explains the "grouping" trick for converting between bases that are powers of each other (e.g., base 2 to base 8) and algebraic tricks for converting between bases with a difference of 2 (like base 8 and base 10) [[5]](https://www.johndcook.com/blog/2025/01/23/radix-conversion/). While intended for hand calculations, these mathematical grouping principles are foundational for optimizing large-scale machine conversions [[5]](https://www.johndcook.com/blog/2025/01/23/radix-conversion/).

---
Learn more:
1. [Efficient GPU Implementation of Multiple-Precision Addition based on Residue Arithmetic - The Science and Information (SAI) Organization](https://thesai.org/Downloads/Volume11No9/Paper_1-Efficient_GPU_Implementation_of_Multiple_Precision.pdf)
2. [RadiK: Scalable and Optimized GPU-Parallel Radix Top-K Selection - arXiv](https://arxiv.org/html/2501.14336v1)
3. [Converting between arbitrary real-valued base systems - Math Stack Exchange](https://math.stackexchange.com/questions/4592617/converting-between-arbitrary-real-valued-base-systems)
4. [Base Conversions from Base 2 through 100 Using Radix Points | Wolfram Demonstrations Project](https://demonstrations.wolfram.com/BaseConversionsFromBase2Through100UsingRadixPoints/)
5. [Tricks for radix conversion by hand - Applied Mathematics Consulting](https://www.johndcook.com/blog/2025/01/23/radix-conversion/)



### Query: Logarithmic-Density-Adjusted Benford model computational number theory GPU
Based on the search results, there is no single established paper, model, or framework that combines a **"Logarithmic-Density-Adjusted Benford model"**, **"computational number theory"**, and **"GPU"** acceleration into one unified topic. Instead, these terms appear across distinct areas of computer science and mathematics literature:

1. **Benford's Law and Logarithmic Density**: Benford's Law (the law of anomalous numbers) is inherently based on logarithmic probability distributions. Various statistical packages and models (such as `P5-statistics-benford`) are used to calculate deviations from Benford's Law for fraud detection and data analysis [[1]](https://www.freebsdsoftware.org/math/). "Logarithmic-density-adjusted" likely refers to a specific statistical weighting or normalization technique applied to Benford's distribution, but it does not appear as a standard, widely recognized standalone model in the top search results.
2. **Computational Number Theory**: This field involves algorithms for solving number-theoretic problems (like integer factorization, primality testing, and Diophantine equations). Libraries like `Lidia` are used for these exact mathematical calculations [[1]](https://www.freebsdsoftware.org/math/). 
3. **GPU Acceleration**: GPUs are frequently used to accelerate computationally heavy tasks, including large-scale graph processing, neural networks (like the "Neural GPU" model for algorithmic learning), and cryptographic algorithms within computational number theory [[2]](https://genes.bibli.fr/index.php?lvl=rss_see&id=24)[[3]](https://huggingface.co/datasets/ought/raft/commit/dceab293fb1f6b02e687a33ac276d5b41fffebb5.diff?file=data%2Ftai_safety_research%2Ftest_unlabeled.csv). 

**Summary of Findings:**
While GPUs are heavily utilized to accelerate algorithms in computational number theory [[2]](https://genes.bibli.fr/index.php?lvl=rss_see&id=24), and Benford's Law is a common statistical tool [[1]](https://www.freebsdsoftware.org/math/), a specific "Logarithmic-Density-Adjusted Benford model" implemented on GPUs for computational number theory does not appear in the current academic or open-source literature [[2]](https://genes.bibli.fr/index.php?lvl=rss_see&id=24)[[4]](https://gist.github.com/ankeshanand/3f3519bddc9b050b6916). It is possible that this specific combination of terms refers to a highly niche, unpublished, or proprietary research project. 

**Sources:**
*   [[2]](https://genes.bibli.fr/index.php?lvl=rss_see&id=24) *17th Chaotic Modeling and Simulation International Conference* (Mentions GPU acceleration and Computational Number Theory)
*   [[4]](https://gist.github.com/ankeshanand/3f3519bddc9b050b6916) *GitHub Gists / Research Topics* (Aggregated research tags including Computational Number Theory and GPUs)
*   [[1]](https://www.freebsdsoftware.org/math/) *FreeBSD Software Math Ports* (Lists computational number theory libraries and Benford's Law statistical modules)
*   [[3]](https://huggingface.co/datasets/ought/raft/commit/dceab293fb1f6b02e687a33ac276d5b41fffebb5.diff?file=data%2Ftai_safety_research%2Ftest_unlabeled.csv) *HuggingFace RAFT Datasets* (Mentions the "Neural GPU" and computational number theory tasks)

---
Learn more:
1. [math - Freebsd software](https://www.freebsdsoftware.org/math/)
2. [17th Chaotic Modeling and Simulation International Conference - Catalogue en ligne](https://genes.bibli.fr/index.php?lvl=rss_see&id=24)
3. [https://huggingface.co/datasets/ought/raft/commit/dceab293fb1f6b02e687a33ac276d5b41fffebb5.diff?file=data%2Ftai\_safety\_research%2Ftest\_unlabeled.csv](https://huggingface.co/datasets/ought/raft/commit/dceab293fb1f6b02e687a33ac276d5b41fffebb5.diff?file=data%2Ftai_safety_research%2Ftest_unlabeled.csv)
4. [communities - Github-Gist](https://gist.github.com/ankeshanand/3f3519bddc9b050b6916)


