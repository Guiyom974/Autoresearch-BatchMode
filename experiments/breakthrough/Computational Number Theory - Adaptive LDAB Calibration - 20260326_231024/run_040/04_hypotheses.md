Below are five testable hypotheses that address the research problem’s core questions about rigorous error bounds, precision thresholds, and the source of the previously observed lack of numerical advantage. Each hypothesis builds directly on the prior overflow-detection findings (e.g., that overflow first appears at \(k \approx 132\) and that low‑\(k\) regimes are numerically stable but may still suffer subtle precision effects) and focuses on the low‑\(k\) regime (\(k = 5, 6, 7\)) required by the current scope.

---

### Hypothesis 1  
**Statement:** For the primorial index \(k = 5\) (base \(2310\)), the truncation error of the high‑order LDAB asymptotic expansion can be bounded rigorously by a closed‑form expression that decays exponentially with the series depth, and the bound is tighter than \(10^{-12}\) when at least five terms are retained.

**Why it’s testable:**  
- The bound can be derived analytically from the remainder term of the asymptotic series (e.g., using Lagrange remainder or known estimates for the logarithmic gamma expansion).  
- The bound can then be validated numerically by comparing the theoretical bound with the actual error computed against a high‑precision reference value.

**Experiment to test it:**  
1. Derive the theoretical error bound for the high‑order expansion at \(k = 5\) as a function of the truncation depth \(n\) (e.g., \(R_n \le C \cdot \rho^n\) for some \(\rho < 1\)).  
2. Using MPFR with 512‑bit precision, compute the exact LDAB density for \(k = 5\) (ground truth) and evaluate the high‑order expansion for depths \(n = 1, 2, \dots, 10\).  
3. Compute the absolute error for each \(n\) and overlay the theoretical bound. Verify that the bound holds for all \(n\) and that it is indeed below \(10^{-12}\) for \(n \ge 5\).  
4. (Optional) Attempt a formal proof of the bound using induction on \(n\) or known asymptotic estimates.

---

### Hypothesis 2  
**Statement:** For \(k = 6\) and \(k = 7\), the high‑order LDAB expansion yields a **>10‑fold reduction in relative error** compared to the guarded log‑gamma approximation **when the prime cutoff parameter exceeds a threshold \(T_k\) and when at least 256‑bit arithmetic precision is used**. Below this precision or cutoff, the advantage may disappear due to round‑off noise.

**Why it’s testable:**  
- The hypothesis makes a quantitative prediction about error ratios that can be measured directly by computing both approximations at high precision and comparing their relative errors against a trusted reference.  
- The dependence on precision and cutoff can be explored systematically via a grid search.

**Experiment to test it:**  
1. Implement both the guarded log‑gamma and the high‑order expansion in MPFR, supporting 256‑bit, 512‑bit, and 1024‑bit precisions.  
2. For each \(k = 6, 7\), generate a dense grid of prime cutoff values (e.g., 50 points uniformly spaced from 0.1 to 0.95 of the primorial).  
3. For each grid point, compute the exact LDAB density at 1024‑bit precision to serve as ground truth.  
4. Evaluate both approximations at each precision level and compute the relative error \(| \text{approx} - \text{truth} | / |\text{truth}|\).  
5. For each precision, compute the error ratio \(E_{\text{log‑gamma}} / E_{\text{high‑order}}\). Identify the cutoff range where this ratio exceeds 10.  
6. Determine whether the ratio drops below 10 when using 128‑bit precision (if feasible) to confirm the precision threshold.

---

### Hypothesis 3  
**Statement:** For \(k = 5, 6, 7\) and precision \(\ge 512\) bits, the residual error of the high‑order expansion is **dominated by truncation error** rather than floating‑point round‑off. Consequently, the error decreases approximately geometrically with each additional term (e.g., by a factor of 10 per term) and does not exhibit erratic fluctuations.

**Why it’s testable:**  
- If round‑off dominates, adding more terms beyond a certain point will cause the error to plateau or even increase. If truncation dominates, the error will continue to fall predictably.  
- This can be diagnosed by analyzing the error trend as a function of truncation depth.

**Experiment to test it:**  
1. For each \(k = 5, 6, 7\), fix a prime cutoff in the region where the high‑order expansion is expected to be most accurate (e.g., near the median of the cutoff range).  
2. Compute the high‑order expansion at truncation depths \(n = 1, 2, \dots, 20\) using 512‑bit, 1024‑bit, and 2048‑bit precisions.  
3. Plot \(\log_{10}(|E_n|)\) versus \(n\) for each precision.  
4. Fit a linear segment to the descending portion of the curve; a constant slope indicates geometric decay (truncation dominance).  
5. If the curve flattens or rises at high \(n\) for 512‑bit but continues declining at 1024‑bit, that confirms round‑off is limiting the lower precision.  
6. Quantify the “effective number of terms” beyond which no further gains are possible at each precision.

---

### Hypothesis 4  
**Statement:** There exists a **crossover point** in the prime cutoff parameter where the high‑order expansion transitions from being less accurate to being **more accurate** than the guarded log‑gamma approximation. This crossover occurs at a cutoff where the argument of the gamma function is roughly of order \(10^6\) (or equivalently, where the leading Stirling term’s relative contribution matches the first correction term), and the phenomenon is reproducible across \(k = 5, 6, 7\).

**Why it’s testable:**  
- The crossover can be located empirically by scanning the cutoff space, and the predicted magnitude can be checked against asymptotic reasoning (e.g., when the next term in Stirling’s series becomes comparable to the main term).  
- If the observed crossover aligns with the theoretical prediction, it provides insight into why previous experiments (which may have used different cutoffs) failed to see an advantage.

**Experiment to test it:**  
1. For each \(k = 5, 6, 7\), perform a fine grid search over cutoffs (e.g., 200 points from 0.05 to 0.95 of the primorial) at 512‑bit precision.  
2. Record the relative error of both methods at each point.  
3. Identify the cutoff(s) where the error of the high‑order expansion first falls below that of the guarded log‑gamma (crossover).  
4. Compute the corresponding argument \(x\) of the gamma function (which is a function of the cutoff and primorial).  
5. Using Stirling’s expansion, estimate the magnitude of \(x\) at which the first correction term equals, say, 1% of the leading term. Compare this estimate to the observed crossover values.  
6. Check if the crossover \(x\) scales consistently with \(k\) (e.g., proportionally to the primorial).

---

### Hypothesis 5  
**Statement:** A **ground‑truth computed at 1024‑bit precision is sufficient** to measure the relative error of the high‑order expansion for \(k = 7\) without significant contamination from round‑off, whereas a 512‑bit ground truth would underestimate the true error by more than **10%** due to accumulated round‑off in the reference computation.

**Why it’s testable:**  
- The hypothesis makes a quantitative prediction about the sensitivity of error measurement to the precision of the reference. By comparing error estimates obtained against references of different precisions, we can directly assess the bias.

**Experiment to test it:**  
1. Compute the exact LDAB density for \(k = 7\) using three independent ground‑truth calculations: at 512‑bit, 1024‑bit, and 2048‑bit precision (all using MPFR).  
2. Evaluate the high‑order expansion (with a fixed depth, e.g., 5 terms) at 512‑bit precision.  
3. Compute the relative error of this expansion against each of the three ground‑truth values.  
4. Compare the three error estimates. If the error computed against the 512‑bit ground truth differs from the 2048‑bit reference by >10%, the hypothesis is supported.  
5. As a control, repeat the experiment with the guarded log‑gamma approximation to see if the precision sensitivity is similar or different.  
6. Determine the minimum reference precision needed to achieve an error estimate that is stable to within 1% across successive precision doublings.

---

### How These Hypotheses Build on Prior Findings  

- The prior overflow‑detection studies established that **numerical overflow is not a concern for \(k \le 7\)** (the overflow threshold lies at \(k \approx 132\)). This frees us to focus on **precision and truncation effects** rather than overflow handling.  
- The observation that “conditional overflow detection eliminates timeouts for low thresholds but not for high thresholds” suggests that **high cutoff values** are numerically delicate. Hypothesis 4 directly targets the cutoff regime where the high‑order method may finally outpace the baseline.  
- Since prior work noted that “lack of overflow at low \(k\) does not guarantee stability,” Hypotheses 2 and 5 investigate whether subtle precision limits could have masked the high‑order method’s advantage in earlier benchmarks.  
- The prior identification of an **overflow threshold at \(k \approx 132\)** provides a sanity‑check anchor: any error‑bound derived in Hypothesis 1 should be consistent with the known safe operating range (i.e., no overflow for \(k \le 7\)).  

Together, these hypotheses form a coherent research plan: **derive provable error bounds, map the precision and cutoff thresholds where the high‑order method truly excels, and validate that the chosen ground‑truth precision is adequate**—thereby conclusively determining whether the high‑order LDAB expansions offer a quantifiable benefit and, if so, under exactly which conditions.