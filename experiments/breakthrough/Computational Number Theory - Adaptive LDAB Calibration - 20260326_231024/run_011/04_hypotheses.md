Based on the research problem and prior findings, we propose the following testable hypotheses. The hypotheses aim to establish the theoretical scaling of artifact-free primorial gap variances and build on previous observations that weighting methods failed and floating-point underflow was an issue for large primorials.

### Hypothesis 1: Variance Scales as Square of Mean Gap
**Statement:**  
The variance of gaps in the artifact-free extraction for primorials \(P_k\) (for \(k=3\) to \(7\)) scales asymptotically as the square of the mean gap, i.e., \(\text{Var}(\text{gap}) \sim \left( \frac{P_k}{\phi(P_k)} \right)^2\), with the ratio \(\text{Var}/\left( \frac{P_k}{\phi(P_k)} \right)^2 \to 1\) as \(k\) increases.

**Why Testable:**  
We can compute the exact variance for each primorial and compare it directly to the theoretical prediction. The mean gap is exactly \(P_k/\phi(P_k)\) when including the wrap-around gap, and the square of this value provides a benchmark.

**Experiment:**  
1. Generate the reduced residue system for each \(P_k\) (\(k=3,\ldots,7\)) using the corrected algorithmic framework.  
2. Extract all \(\phi(P_k)\) gaps (including the wrap-around gap).  
3. Compute the empirical variance \(\text{Var}_{\text{emp}}\) and the theoretical variance \(\text{Var}_{\text{th}} = (P_k/\phi(P_k))^2\).  
4. Calculate the ratio \(R_k = \text{Var}_{\text{emp}} / \text{Var}_{\text{th}}\).  
5. Analyze \(R_k\) across \(k\) to see if it converges to 1. Perform regression analysis (e.g., log-log) to confirm scaling.

### Hypothesis 2: Coefficient of Variation Tends to 1
**Statement:**  
The coefficient of variation (CV) of gaps—defined as \(\text{CV} = \sqrt{\text{Var}(\text{gap})} / \text{mean}(\text{gap})\)—tends to 1 as \(k\) increases, indicating that the gap distribution approaches a geometric/exponential distribution.

**Why Testable:**  
The CV is a dimensionless measure that can be computed directly from the data and compared to the theoretical value of 1 for a geometric distribution with large mean.

**Experiment:**  
1. For each primorial \(P_k\), compute the mean gap \(\bar{g}\) (which equals \(P_k/\phi(P_k)\)) and the standard deviation \(\sigma_g = \sqrt{\text{Var}_{\text{emp}}}\).  
2. Compute \(\text{CV}_k = \sigma_g / \bar{g}\).  
3. Plot \(\text{CV}_k\) versus \(k\) and examine convergence to 1. Use statistical tests (e.g., t-test) to assess significance of trends.

### Hypothesis 3: Variance Matches Random Subset Model
**Statement:**  
The empirical variance for the primorial gap distribution is statistically indistinguishable from the variance of gaps in a random subset of \([1, P_k]\) of size \(\phi(P_k)\), suggesting that the coprime structure does not alter variance beyond random sampling effects.

**Why Testable:**  
We can simulate random subsets of the same size and density, compute their variances, and compare the primorial variance to the simulated distribution.

**Experiment:**  
1. For each \(P_k\), generate \(N=1000\) random subsets of \([1, P_k]\) of size \(\phi(P_k)\) (without replacement).  
2. For each subset, compute the variance of gaps (including wrap-around).  
3. Obtain the mean \(\mu_{\text{rand}}\) and standard deviation \(\sigma_{\text{rand}}\) of these variances.  
4. Compute the z-score: \(z = (\text{Var}_{\text{emp}} - \mu_{\text{rand}}) / \sigma_{\text{rand}}\).  
5. If \(|z| < 2\) for all \(k\), the hypothesis is supported.

### Hypothesis 4: Wrap-Around Gap Is Not an Outlier
**Statement:**  
The wrap-around gap follows the same distribution as the other gaps, confirming that the periodic boundary handling does not introduce asymmetry.

**Why Testable:**  
We can test whether the wrap-around gap lies within the typical range of the other gaps using z-scores.

**Experiment:**  
1. For each \(P_k\), compute the non-wrap-around gaps \(g_1, \ldots, g_{\phi(P_k)-1}\) and the wrap-around gap \(g_{\text{wrap}}\).  
2. Calculate the mean \(\mu_g\) and standard deviation \(\sigma_g\) of the non-wrap-around gaps.  
3. Compute the z-score: \(z_{\text{wrap}} = (g_{\text{wrap}} - \mu_g) / \sigma_g\).  
4. If \(|z_{\text{wrap}}| < 2\) for all \(k\), the wrap-around gap is not an outlier.

These hypotheses are designed to rigorously test the theoretical predictions and ensure artifact-free results, building directly on the need to avoid prior weighting method failures and address computational precision.