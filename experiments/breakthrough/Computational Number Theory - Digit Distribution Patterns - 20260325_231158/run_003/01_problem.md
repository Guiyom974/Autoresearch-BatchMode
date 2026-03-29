# Research Problem: Positional N-Gram Patterns and Inter-Prime Gap Digit Sequences in Higher Bases

## Objective
Following the null findings regarding internal continuous n-gram distributions in Base-2 (which yielded a KL divergence of 0.00 between primes and composites), this research shifts focus to structural digit patterns derived from inter-prime gaps and strict positional constraints. The objective is to computationally investigate the n-gram digit sequences of prime gaps ($p_{n+1} - p_n$) and the positional n-grams (prefixes vs. internal segments) of prime numbers in higher numerical bases (specifically Base-10 and Base-16). By increasing digit diversity and shifting from internal prime digits to the distances between primes, the goal is to uncover localized sequence biases that differ significantly from random or composite baseline distributions.

## Research Questions
1. **Inter-Prime Gap Distributions:** Do the n-gram digit sequences comprising inter-prime gaps in Base-10 and Base-16 exhibit statistically significant deviations (KL divergence > 0.01) from the gap sequences of randomly distributed odd composite numbers?
2. **Positional N-Gram Bias:** Are there localized biases in the leading (prefix) n-grams of prime numbers in higher bases compared to their internal n-grams, once normalized for Benford's Law-like leading digit distributions?
3. **Base-Dependent Structures:** Does the transition from Base-10 to Base-16 reveal new n-gram dependencies in prime gaps that were otherwise obscured by decimal representation?

## Methodology
1. **Data Generation:** Generate a robust dataset of primes up to $N = 10^7$ and calculate the corresponding inter-prime gaps. Generate a matched control dataset of composite numbers and their sequential gaps.
2. **Base Conversion & Extraction:** Convert both primes and their gaps into Base-10 and Base-16 string representations.
3. **Positional & Gap Analysis:**
   - Extract fixed-length n-grams ($n=2, 3$) specifically from the inter-prime gap values.
   - Extract localized n-grams from the specific positions within the primes (e.g., first 3 digits vs. middle 3 digits).
4. **Statistical Testing:** Compute the Kullback-Leibler (KL) divergence, Total Variation Distance, and Chi-square statistics between the prime-derived gap/positional n-grams and the composite control group.
5. **Normalization:** Apply strict controls to filter out trivial modular arithmetic constraints (e.g., Base-10 primes never ending in 2, 4, 5, 6, 8, or 0) and natural logarithmic distributions (Benford's Law) for leading digits.

## Success Criteria
1. **Statistical Significance:** Detection of a KL divergence $> 0.05$ or a stable Chi-square p-value $< 0.01$ between prime gap n-grams and composite gap n-grams in either Base-10 or Base-16.
2. **Non-Trivial Discovery:** The identified pattern or bias must persist even after normalizing for known trivial end-digit constraints and leading-digit laws.
3. **Reproducibility:** The observed deviation must scale consistently across multiple contiguous subsets of the generated prime dataset (e.g., persisting in the $10^5-10^6$ range as well as the $10^6-10^7$ range).

## Constraints
1. **Domain Adherence:** The study must strictly remain within the statistical analysis of digit sequences and Base-N representations; it must not pivot to unrelated analytic number theory domains.
2. **Computational Limits:** N-gram sizes should be restricted to $n \le 4$ to ensure statistical validity and sufficient sample density within the generated $10^7$ limit.
3. **Control Rigidity:** All discovered biases must be strictly measured against a well-defined control group (pseudo-random odd composites) to ensure the findings are unique to prime distributions.