# Research Problem: Higher-Order N-Gram Digit Sequencing and Base-N Distribution Patterns in Prime Numbers

## Objective
Following the null findings regarding single-digit transition probabilities (1-grams) in Base-10, this research shifts focus to higher-order structural patterns. The objective is to computationally investigate the frequencies and distributions of longer n-gram digit sequences (n $\ge$ 3) within prime numbers across multiple numerical bases (specifically Base-10 and Base-2). The goal is to determine whether prime structural constraints manifest as localized biases or suppressed sequences in higher-order n-grams that are undetectable at the single-transition level.

## Research Questions
1. **Higher-Order Sequence Bias:** Do the frequency distributions of digit triplets (3-grams) and quadruplets (4-grams) within the internal digits of prime numbers deviate significantly from those of composite control numbers in Base-10 and Base-2?
2. **Suppressed N-Grams:** Are there specific n-gram sequences that appear at a statistically suppressed rate deep within the digits of large primes compared to expected uniform distributions?
3. **Base-Specific Constraints:** Does Base-2, where prime structure heavily dictates bit-flipping at the lower and upper bounds, exhibit more pronounced internal n-gram biases than Base-10?

## Methodology
1. **Data Generation:** Generate a dataset of prime numbers and a precisely matched control group of composite numbers up to at least $10^7$.
2. **Preprocessing:** Strip the terminal digits (e.g., the final digit in Base-10, which must be 1, 3, 7, or 9) to strictly control for well-known terminal biases that skew the overall distribution.
3. **N-Gram Extraction:** Parse the internal digits of both primes and controls into overlapping n-grams for $n \in \{3, 4, 5\}$.
4. **Statistical Analysis:** Compute the frequency distributions of these n-grams for both sets. Use Kullback-Leibler (KL) divergence and Chi-square goodness-of-fit tests to evaluate statistical significance between the prime n-gram distributions and the control distributions.

## Success Criteria
1. Successful extraction and statistical comparison of internal n-grams (n=3, 4) for primes vs. controls in both Base-10 and Base-2.
2. Identification of a statistically significant deviation (p < 0.01) in specific higher-order n-gram frequencies, OR a rigorous empirical demonstration that internal uniformity holds strongly even at higher dimensions (n up to 5).
3. Generation of comparative heatmaps or frequency distribution plots isolating the most over- and under-represented n-grams.

## Constraints
1. **Terminal Trivialities:** All analysis must strictly exclude or normalize against the terminal digit of the numbers to prevent trailing-digit rules from polluting internal sequence data.
2. **Computational Limits:** N-gram analysis scales exponentially with base size and n-gram length; algorithms must be optimized to handle millions of primes efficiently without memory overflow.
3. **Control Group Matching:** The control numbers must be drawn from the same magnitude brackets as the primes to ensure digit-length distributions are identical between test and control sets.