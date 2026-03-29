# Research Problem: Positional N-Gram Biases and Prefix Distributions of Primes in Primorial and High-Order Bases

## Objective
Following the methodological failure of the inter-prime gap analysis (which yielded infinite KL divergence due to undefined composite gap analogs) and the successful preliminary findings regarding prefix n-grams (where Base-32 showed a >10x higher KL divergence than Base-8), this research pivots to exclusively analyze internal positional digit patterns of primes. The objective is to computationally investigate the prefix, suffix, and internal n-gram digit sequences of prime numbers compared to composites. Specifically, the study will determine whether the observed increase in prefix n-gram bias scales linearly with base magnitude, or if structurally significant bases (such as primorial bases like Base-6 and Base-30) exhibit stronger positional sequence biases than power-of-two bases.

## Research Questions
1. **Magnitude vs. Structure:** Is the higher KL divergence observed in Base-32 prefix n-grams a strictly magnitude-driven phenomenon (larger base equals higher divergence), or do primorial bases (e.g., Base-6, Base-30) produce statistically distinct structural biases in prime prefixes compared to adjacent power-of-two bases?
2. **Positional Decay of Bias:** Does the KL divergence between prime and composite digit sequences decay as the n-gram window moves from the prefix (most significant digits) to the internal segments of the number across different bases?
3. **Suffix Distribution Constraints:** Beyond trivial divisibility rules, how do the suffix n-grams (least significant digits) of primes in highly composite bases (like Base-30) statistically diverge from the baseline composite distribution?

## Methodology
1. **Data Generation:** Generate prime numbers and a representative sample of composite numbers up to $N = 1,000,000$.
2. **Base Conversion:** Convert both sets of numbers into a targeted selection of bases: lower power-of-two (Base-8), higher power-of-two (Base-32), and primorial bases (Base-6, Base-30).
3. **Positional N-Gram Extraction:** For each number, extract strictly defined positional n-grams (e.g., $n=2$):
   - *Prefix n-grams:* The first $n$ most significant digits.
   - *Internal n-grams:* Sliding window of $n$ digits excluding the first and last digits.
   - *Suffix n-grams:* The last $n$ least significant digits.
4. **Statistical Comparison:** Compute the Kullback-Leibler (KL) divergence between the prime n-gram probability distributions and the composite n-gram probability distributions for each base and position.
5. **Validation:** Ensure smoothing (e.g., Laplace smoothing) is applied to all distributions prior to KL divergence calculation to prevent zero-frequency bins from yielding infinite values.

## Success Criteria
- Generation of finite, mathematically valid KL divergence metrics for all positional n-grams across all tested bases, successfully avoiding the zero-distribution errors of the previous iteration.
- A definitive statistical comparison showing whether Base-30 (primorial) yields a higher prefix/suffix KL divergence than Base-32 (power-of-two).
- A clear mapping of how digit pattern bias decays or intensifies depending on the structural position (prefix vs. internal) within the prime string.

## Constraints
- **Methodological Strictness:** Absolutely no gap-based analysis ($p_{n+1} - p_n$) is to be used in this iteration, as composite gaps lack a meaningful comparative definition.
- **Domain Confinement:** Analysis must remain strictly focused on the digit sequences and distributions of primes; no external cryptographic or unrelated number theory topics may be introduced.
- **Triviality Avoidance:** Suffix analyses must mathematically account for and isolate trivial non-prime endings (e.g., even digits in Base-10) so that the KL divergence reflects non-obvious sequencing biases rather than basic divisibility rules.