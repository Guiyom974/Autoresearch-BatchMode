# Research Problem: Adaptive LDAB Calibration for Multi‑Scale Prime Bases

## Objective
Leveraging the confirmed dynamically calibrated LDAB model for base‑210, develop a **real‑time adaptive correction framework** that continuously updates the LDAB density estimate as the prime cutoff expands, and demonstrate its ability to keep the KL divergence below 10⁻⁴ across several primorial bases (210, 2310, 30030) and a streaming real‑world prime stream.

## Research Questions
1. **Variation of the optimal density factor:** How does the correction factor \(c(t)\) that multiplies the LDAB log‑density term change as a function of the current prime bound \(t\) (e.g., every 10 000th prime up to \(10^6\))?
2. **Closed‑form adaptive predictor:** Can \(c(t)\) be expressed analytically using the RMT covariance factor \(\alpha(t)\) derived from the recent zero‑spacing statistics of Dirichlet L‑functions for the relevant characters, and does this predictor match the empirically fitted factor within 5 %?
3. **Robustness across bases and streams:** Does the adaptive LDAB maintain KL < 10⁻⁴ for bases 210, 2310, 30030 when applied to (i) a static list of the first \(10^6\) primes and (ii) a simulated streaming source that appends new primes indefinitely, while updating \(c(t)\) in < 0.2 s per update?

## Methodology
1. **Prime generation:** Implement a segmented Sieve of Eratosthenes in pure Python to produce the first \(10^6\) primes and store them in a NumPy array (≈78 KB, fits in memory).  
2. **Base‑specific LDAB baseline:** For each base \(b\in\{210,2310,30030\}\) compute the leading‑digit frequencies of primes in each sliding window of size \(W=10^4\).  
3. **Adaptive correction:**  
   - Approximate the RMT covariance factor \(\alpha(t)\) from the recent pair‑correlation of zeros using the explicit formula  
     \[
     \alpha(t)\approx 1+\frac{2}{\pi}\int_{0}^{T(t)}\frac{\sin u}{u}\,du,
     \]  
     where \(T(t)\) is the zero height corresponding to the current prime bound (use the known asymptotic \(T(t)\sim \frac{\log t}{2\pi}\)).  
   - Derive the adaptive density term \(c(t)=1/\alpha(t)\).  
   - Update \(c(t)\) after each window and recompute the LDAB density as \(p_{\text{LDAB}}(d; t)=c(t)/\log_b(x_d)\) where \(x_d\) is the smallest number with leading digit \(d\) in base \(b\).  
4. **KL evaluation:** For every window compute the Kullback‑Leibler divergence between the observed leading‑digit distribution and the adaptive LDAB distribution. Also compute the static‑LDAB divergence for comparison.  
5. **Statistical analysis:** Fit the empirical \(c(t)\) to the analytic predictor using linear regression on \(\log t\) and report the residual error. Verify that the adaptive KL stays below \(10^{-4}\) for at least 95 % of windows across all bases.  
6. **Streaming test:** Simulate a stream by appending the next 100 000 primes (generated on‑the‑fly) and update \(c(t)\) after each batch of 1 000 primes, measuring update latency and KL stability.

All computations rely only on `numpy`, `scipy`, and `matplotlib`; no external data files are read or written.

## Success Criteria
- **Empirical‑analytic alignment:** The fitted function \(c_{\text{fit}}(t)\) matches the analytic predictor \(c(t)\) with a mean absolute relative error ≤ 5 % across the entire prime range.  
- **KL reduction:** The adaptive LDAB achieves a **10‑fold reduction** in KL divergence compared with the static LDAB (baseline KL ≈ 3.5 × 10⁻⁴ → adaptive KL ≤ 3.5 × 10⁻⁵) for at least 95 % of windows in each base.  
- **Real‑time capability:** Updating the correction factor after each batch of 1 000 streaming primes completes in ≤ 0.2 s on a single CPU core, and the KL divergence never exceeds 1 × 10⁻⁴ throughout the 100 000‑prime stream.  
- **Cross‑base generalization:** The same adaptive algorithm, without per‑base retuning, satisfies the KL bound for bases 210, 2310, and 30030 simultaneously.

## Constraints
- All experiments in **Python** (standard library, `numpy`, `matplotlib`, `scipy` only).  
- **No external data downloads**; all prime data are generated internally.  
- **Execution time:** The full pipeline (prime generation + all window analyses) must finish within **2 minutes** on the target hardware.  
- Results must be reproducible by running the script twice with identical random seeds (if any) and the same deterministic sieve.