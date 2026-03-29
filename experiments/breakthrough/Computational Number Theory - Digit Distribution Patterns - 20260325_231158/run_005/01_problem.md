# Research Problem: Prefix N-Gram Biases and Leading Digit Distributions of Primes in High-Order Primorial Bases 

## Objective
Following the experimental finding that lower-order primorial bases (e.g., Base-30) yielded only modest KL divergence and were surprisingly outperformed by power-of-two bases (e.g., Base-32) in general positional n-gram bias, this research pivots to a highly targeted structural analysis. The objective is to investigate whether extending to **higher-order primorial bases (Base-210 and Base-2310)** reveals pronounced structural biases specifically in the **leading digits (prefixes)** of prime numbers. Because primorial bases severely restrict valid terminal digits for primes, we hypothesize that this terminal constraint induces measurable, non-uniform compensatory distributions in the prefixes. Furthermore, we will shift from KL divergence to more robust statistical measures (Mutual Information and Chi-Squared tests) to better quantify significance given finite prime sample sizes.

## Research Questions
1. **High-Order Prefix Bias:** Do the leading digits (prefixes of length 1 to 3) of prime numbers represented in Base-210 and Base-2310 exhibit statistically significant deviations from uniform distributions when evaluated using Chi-Squared tests?
2. **Terminal-Prefix Dependency:** Does the severe constraint on allowable terminal digits in Base-210 and Base-2310 induce a measurable dependency (quantifiable via Mutual Information) between the leading and trailing digits of prime numbers?
3. **Primorial Scaling Effect:** How does the magnitude of prefix n-gram bias scale as the primorial base increases from Base-30 to Base-210 to Base-2310? 

## Methodology
1. **Prime Generation & Base Conversion:** Generate a significantly larger dataset of prime numbers (e.g., primes up to 10-50 million) to ensure sufficient statistical power for the expanded alphabet of high-order bases. Convert these primes into Base-210 and Base-2310 representations.
2. **Targeted Prefix Extraction:** Isolate the leading $k$ digits ($k \in \{1, 2, 3\}$) for all primes in the dataset. Ignore internal positional n-grams to minimize noise and focus strictly on the structural boundary of the numbers.
3. **Statistical Testing:** 
   * Apply **Chi-Squared Goodness-of-Fit tests** to compare the observed prefix distributions against the expected uniform distributions for the valid leading digits.
   * Calculate the **Mutual Information (MI)** between the prefix digit and the terminal digit to test for long-range positional dependencies.
4. **Baseline Comparison:** Compare the MI and Chi-Squared statistics of Base-210/2310 against power-of-two baseline bases (e.g., Base-256) to verify if any observed effect is uniquely primorial.

## Success Criteria
* Successful implementation of Base-210 and Base-2310 conversion algorithms for large prime datasets.
* Computation of Chi-Squared p-values and Mutual Information scores for leading digits across the specified bases.
* Identification of a statistically significant (p < 0.01) divergence or dependency in the leading digits of high-order primorial bases that exceeds the baseline noise observed in equivalent non-primorial bases.

## Constraints
* **Sparsity in High Bases:** Base-2310 has a large alphabet size. Evaluating 2-grams or 3-grams in this base requires an exponentially larger dataset of primes to avoid sparse matrix issues and invalid Chi-Squared approximations.
* **Algorithmic Efficiency:** Base conversion and string/array manipulation for millions of primes into non-standard high bases must be computationally optimized to run within standard memory limits.
* **Domain Adherence:** The study must strictly isolate base-dependent digit sequence patterns and avoid drifting into standard analytical number theory regarding prime gaps or distribution functions.