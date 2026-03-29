
## Iteration 1 [ORIGINAL]
Timestamp: 2026-03-25T20:33:40.468201

# Research Problem: Digit Sequencing and Base-N Distribution Patterns in Prime Numbers

## Objective
Computationally investigate non-obvious patterns in the digit distributions and sequence structures of prime numbers across different numerical bases (e.g., Base-2, Base-10, Base-16). The goal is to discover unexpected localized biases in the digits of primes or sequential digit dependencies that deviate from a purely random uniform distribution, while avoiding well-known trivias (like Base-10 primes not ending in 2 or 5).

## Research Questions
1. **Digit Transition Probabilities:** If a prime $p$ in Base-10 contains the digit "3", what is the probability that the next adjacent digit is also a "3"? Does the transition probability matrix for the digits of prime numbers differ significantly from the expected uniform distribution for random odd numbers?
2. **Terminal Digit Dependencies:** Does the final digit of $p$ influence the distribution of the final digit of the *next* prime $p_{n+1}$? 
3. **Base-N Density Fluctuation:** When expressing primes in Base-16 (Hexadecimal), are certain hex digits over-represented in the middle digits of primes as we sample up to $x = 10^7$? 
4. **Digit Sum Biases:** Does the sum of the digits of a prime number cluster around specific expected values faster than would be expected by a normal distribution limit theorem?

## Methodology
1. **Prime Generation:** Generate a subset of primes up to $x = 10^7$ using a standard fast sieve mechanism.
2. **Digit Extraction:** Convert the prime numbers into string/array representations in multiple bases (e.g., Base-10 and Base-16) to analyze their structure.
3. **Markov Chain Analysis:** Build a 10x10 transition matrix for adjacent digits within primes to analyze transition probabilities between consecutive digits.
4. **Statistical Testing:** Use Chi-square goodness-of-fit tests to compare observed sequences and digit counts against a uniform baseline model.
5. **Visualization:** Produce histograms or heatmaps showing deviations from the expected random distribution.

## Success Criteria
1. **Significant Deviation:** Identification of at least one digit pairing or terminal dependency with statistically significant deviation ($p < 0.01$) from a uniformly populated random gap model.
2. **Reproducibility:** The codebase successfully runs end-to-end within 3 minutes and the deviation holds true over varying datasets (e.g., $10^6$ vs $10^7$).
3. **Robust Evaluation:** The LLM evaluation identifies the pattern as non-obvious and not simply an artifact of standard division rules (like primes avoiding ending in '5' in base 10).

## Constraints
1. **Tooling Limits:** All calculations must be performed locally using Python (standard libraries, `numpy`, `matplotlib`). No external APIs for calculations.
2. **Execution Time:** The data generation, sequence parsing, and statistical calculation should not exceed 2-3 minutes to prevent timeouts.
3. **Sanity Checking:** All findings must first explicitly baseline against randomly generated odd numbers or simple "not divisible by 2 or 5" sets to ensure the discovered bias is unique to prime structure and not just basic arithmetic modulo.


---

## Iteration 2 [REFORMULATED]
Timestamp: 2026-03-25T20:35:45.429316

# Research Problem: Markovian Digit Transition Probabilities in Base-2 and Base-10 Primes

## Objective
Establish a robust computational baseline to investigate Markovian transition probabilities of adjacent digits in prime numbers, focusing specifically on Base-10 and Base-2 representations. The goal is to rigorously quantify whether the sequence of digits within a prime number exhibits localized, non-trivial dependencies (e.g., predicting the next digit based on the current digit) that deviate from a purely random uniform distribution, ensuring a highly verified and systematic computational pipeline.

## Research Questions
1. **Base-10 Transition Biases:** Excluding the least significant digit (to avoid trivial divisibility rules), do the digit transition matrices $P(d_{i+1} | d_i)$ for primes exhibit statistically significant deviations from expected uniform distributions compared to composite numbers of the same magnitude?
2. **Base-2 Bit-Flipping Patterns:** In the binary representation of primes, are there unexpected localized biases in bit-sequence transitions (e.g., the probability of encountering "10" vs "11" after a "1"), and how do these scale as the magnitude of the prime increases?

## Methodology
1. **Data Generation:** Computationally generate all prime numbers up to $10^7$ using a highly verified, strictly validated sieve algorithm to ensure data integrity.
2. **Base Conversion & Truncation:** Convert the primes into Base-10 and Base-2 string representations. Truncate the final digit/bit to eliminate well-known trivial biases (e.g., Base-10 primes not ending in 2, 4, 5, 6, 8, 0; Base-2 primes always ending in 1).
3. **Transition Matrix Construction:** For each base, construct a Markov transition matrix mapping the frequency of digit $d_{i+1}$ immediately following digit $d_i$.
4. **Statistical Analysis:** Apply Chi-square goodness-of-fit tests to compare the empirical transition matrices of primes against randomly generated sequences and composite numbers.

## Success Criteria
1. Successful extraction and population of $10 \times 10$ (Base-10) and $2 \times 2$ (Base-2) empirical transition matrices without computational or parsing errors.
2. Identification of statistically significant deviations (p-value < 0.01) in specific digit transitions, or a rigorous mathematical confirmation of uniform randomness.
3. Clear visualizations (e.g., heatmaps) of the transition probability matrices.

## Constraints
1. The analysis must strictly exclude the least significant digit to prevent contamination from elementary divisibility rules.
2. The computational scope is limited to primes up to $10^7$ to ensure the analysis can be run quickly and reliably in a single execution environment.
3. The methodology must focus purely on adjacent pairwise dependencies (Markov order 1) before attempting higher-order sequential patterns.

---

## Iteration 3 [REFORMULATED]
Timestamp: 2026-03-25T20:39:46.062337

# Research Problem: High-Resolution Markovian Transition Matrices of Internal Digits in Base-2 and Base-10 Primes

## Objective
To systematically compute and statistically validate Markovian transition probabilities of adjacent internal digits in Base-10 and Base-2 prime numbers. Building upon the foundational intent of prior analyses, this iteration aims to rigorously isolate internal digit sequences from known terminal-digit biases (such as Base-10 primes never ending in even numbers or 5). The goal is to construct highly accurate, large-scale transition matrices and apply rigorous statistical testing to determine if local digit dependencies deviate from uniform randomness.

## Research Questions
1. **Transition Deviations:** What are the precise empirical transition matrices for adjacent internal digits ($d_i \rightarrow d_{i+1}$) in Base-10 ($10 \times 10$ matrix) and Base-2 ($2 \times 2$ matrix) primes up to $10^8$?
2. **Statistical Significance:** Do specific transition pairs (e.g., the likelihood of a '3' being followed by another '3' in Base-10, or '1' followed by '0' in Base-2) exhibit statistically significant deviations from a randomized control distribution when evaluated using Chi-square goodness-of-fit tests?
3. **Prime vs. Composite Baselines:** How do the transition matrices of prime numbers differ from those of composite numbers or random odd integers of the same magnitude?

## Methodology
1. **Data Generation:** Utilize an optimized sieve algorithm (e.g., Sieve of Eratosthenes) to generate all prime numbers up to a substantial threshold (e.g., $10^8$). 
2. **Data Sanitization:** Strip the terminal digit from all Base-10 and Base-2 representations to eliminate trivial divisibility artifacts. 
3. **Matrix Construction:** Iterate through the digits of each truncated prime to tally adjacent digit pairs, constructing normalized Markovian transition matrices for both Base-2 and Base-10.
4. **Statistical Testing:** Compare the observed transition frequencies against expected frequencies (derived from random odd integer distributions) using Chi-square tests to calculate $p$-values for each transition pair.

## Success Criteria
1. Successful compilation of complete, normalized transition matrices for internal digits of primes in both Base-10 and Base-2.
2. Robust statistical analysis output, including $p$-values for specific digit transitions, confirming or refuting the presence of non-trivial Markovian dependencies.
3. Clear visualization (e.g., heatmaps) of the transition matrices comparing prime sequences to composite baselines.

## Constraints
1. The analysis must strictly exclude the least significant digit (terminal digit) in Base-10 to avoid interference from fundamental divisibility rules.
2. The computational approach must be highly optimized to handle prime generation and string/digit manipulation up to $10^8$ without exceeding standard memory constraints.
3. The scope must remain strictly within Base-2 and Base-10 representations to ensure depth of statistical analysis before expanding to other bases.

---

## Iteration 4 [REFORMULATED]
Timestamp: 2026-03-25T20:42:08.328662

# Research Problem: Higher-Order (k-step) Markovian Dependencies and Sub-sequence Clustering in Internal Digits of Base-10 Primes

## Objective
To systematically compute and statistically validate higher-order ($k=2$ and $k=3$) Markovian transition probabilities of internal digit sequences in Base-10 prime numbers. Since previous attempts to construct 1st-order matrices were interrupted before yielding data, this iteration narrows the scientific focus to computationally robust, higher-order dependencies. The goal is to rigorously isolate internal digit sequences (triplets and pairs) from known terminal-digit biases and determine if long-range digit dependencies exist that would be obscured by simple adjacent-digit analysis.

## Research Questions
1. **Higher-Order Transitions:** Do sequences of three consecutive internal digits (e.g., the transition from "34" to "5") in Base-10 prime numbers exhibit statistically significant deviations from a uniform distribution expected in random odd numbers?
2. **Sub-sequence Clustering:** Are there specific internal digit pairs or triplets that appear with unexpectedly high or low frequencies in primes up to $10^8$, independent of the leading or terminal digits?
3. **Composite Baseline Comparison:** How do the $k$-step transition matrices of prime numbers differ from those of composite numbers of the same magnitude?

## Methodology
1. **Data Generation:** Computationally generate all prime numbers and a control set of randomly selected composite odd numbers up to $10^8$.
2. **Data Sanitization:** Strip the first digit and the last digit from all numbers in the dataset to strictly isolate the "internal core" digits, completely eliminating Benford's Law effects and terminal-digit biases (e.g., absence of 2, 4, 5, 6, 8, 0).
3. **Matrix Construction:** Construct 2nd-order ($100 \times 10$) and 3rd-order ($1000 \times 10$) transition probability matrices for the internal digits.
4. **Statistical Testing:** Apply Pearson's Chi-Square tests and Kullback-Leibler (KL) divergence to compare the empirical prime digit distributions against both the uniform theoretical distribution and the composite number control group.

## Success Criteria
- Successful construction of error-free 2nd and 3rd-order transition matrices for internal digits.
- Identification of at least one specific digit transition sequence where the prime distribution diverges from the composite/random distribution with a statistical significance of $p < 0.01$.
- Generation of a clear KL-divergence metric quantifying the exact information difference between prime internal digits and uniform randomness.

## Constraints
- **Domain Strictness:** The analysis must remain entirely focused on the digits of prime numbers. Do not expand into other number theory sequences (e.g., Fibonacci).
- **Exclusion of Trivia:** Leading digits and the final digit must be explicitly excluded from all transition calculations to prevent known biases from skewing the transition matrices.
- **Computational Tractability:** The algorithm must be optimized to handle matrices up to $10^8$ without memory overflow, ensuring clean execution.

---

## Iteration 5 [REFORMULATED]
Timestamp: 2026-03-25T20:44:58.817636

# Research Problem: Robust Computational Extraction and Analysis of 1st- and 2nd-Order Markovian Dependencies in Internal Digits of Base-10 Primes

## Objective
To systematically compute and statistically validate 1st-order and 2nd-order Markovian transition probabilities of internal digit sequences in Base-10 prime numbers. Since previous computational iterations failed to execute properly, this phase focuses on ensuring a scientifically rigorous, computationally stable extraction of transition matrices. The goal is to isolate internal digit sequences (pairs and triplets) from known boundary constraints (e.g., the last digit of primes) and determine if their sequential dependencies deviate from a uniform random distribution.

## Research Questions
1. **1st-Order Internal Dependencies:** What is the empirical 1st-order transition probability matrix for internal digits of Base-10 primes up to $10^8$, and does it show statistically significant deviations from a uniform distribution (excluding the final digit)?
2. **2nd-Order Internal Dependencies:** Do sequences of three internal digits (2nd-order transitions) exhibit localized clustering or avoidance patterns that cannot be explained by 1st-order probabilities?
3. **Scale Invariance:** Do the observed transition probabilities remain stable as the magnitude of the prime numbers increases across different logarithmic buckets (e.g., $10^6$ vs $10^8$)?

## Methodology
1. **Data Generation:** Generate a comprehensive dataset of all prime numbers up to a specified threshold (e.g., $10^8$) using an optimized Sieve of Eratosthenes.
2. **Data Sanitization:** Strip the first and last digits from each prime in the dataset to strictly isolate internal digits, removing trivial boundary biases (such as the inability of primes to end in 2, 4, 5, 6, 8, or 0).
3. **Matrix Computation:** Construct precise 1st-order ($10 \times 10$) and 2nd-order ($100 \times 10$) transition probability matrices based on the sanitized internal digit sequences.
4. **Statistical Testing:** Apply Chi-square goodness-of-fit tests to compare the empirical transition matrices against an expected uniform distribution matrix.
5. **Validation:** Implement robust error-handling and logging in the computational pipeline to ensure uninterrupted execution and reliable data extraction.

## Success Criteria
1. **Computational Stability:** Successful, uninterrupted execution of the digit-extraction and matrix-computation algorithms over the target prime dataset.
2. **Matrix Generation:** The successful generation of complete, empirical 1st-order and 2nd-order transition probability matrices for internal prime digits.
3. **Statistical Clarity:** A definitive statistical conclusion (via p-values) indicating whether internal digit transitions in Base-10 primes exhibit non-uniform Markovian dependencies.

## Constraints
1. **Domain Adherence:** The research must strictly remain within the analysis of digit distributions and sequence structures of prime numbers.
2. **Boundary Exclusion:** The analysis must strictly exclude the final digit of the prime numbers to prevent known trivial biases from skewing the transition matrices.
3. **Computational Efficiency:** The algorithms must be highly optimized to handle millions of primes without memory overflow or execution timeouts.

---

## Iteration 6 [REFORMULATED]
Timestamp: 2026-03-25T20:48:15.125046

# Research Problem: Algorithmic Validation and Robust Execution for Extracting Markovian Dependencies in Base-10 Prime Digits

## Objective
To successfully and rigorously compute the 1st- and 2nd-order Markovian transition probabilities for internal digit sequences of Base-10 prime numbers by developing a computationally robust and fault-tolerant algorithmic pipeline. Following previous execution failures, this iteration focuses on implementing rigorous validation, error handling, and logical logging to ensure the uninterrupted and accurate statistical extraction of digit dependencies, strictly isolating internal sequences from boundary constraints.

## Research Questions
1. **Algorithmic Robustness:** How can we structure the prime generation and digit-parsing algorithms with comprehensive error handling and logging to guarantee successful execution over large sets of primes (e.g., up to $10^7$)?
2. **Transition Probabilities:** Once a stable pipeline is established, what are the exact 1st-order (pair) and 2nd-order (triplet) Markovian transition probabilities for internal digits of Base-10 primes?
3. **Statistical Deviation:** Do the successfully extracted internal transition matrices exhibit statistically significant deviations from a uniform distribution when analyzed using chi-square tests?

## Methodology
1. **Pipeline Validation:** Develop a Python-based computational script with strict syntax validation and structural integrity checks to prevent pre-execution failures.
2. **Robust Execution Architecture:** Implement comprehensive `try-except` blocks, execution logging, and modular architecture to gracefully handle edge cases during prime generation and string manipulation.
3. **Prime Generation and Parsing:** Generate primes up to $10^7$ using a highly optimized Sieve of Eratosthenes. Convert primes to strings and strip the first and last digits to isolate internal sequences.
4. **Markovian Extraction:** Calculate the empirical frequencies of internal digit transitions ($d_i \to d_{i+1}$ and $d_i, d_{i+1} \to d_{i+2}$) and compile them into normalized transition probability matrices.
5. **Statistical Testing:** Apply Pearson's chi-square test to compare the observed transition matrices against the expected uniform distribution matrices.

## Success Criteria
1. **Execution Success:** The computational script runs to completion without syntax, runtime, or logical errors, successfully generating detailed execution logs.
2. **Data Extraction:** Complete 1st-order ($10 \times 10$) and 2nd-order ($100 \times 10$) Markovian transition matrices are successfully outputted for the internal digits of the target prime set.
3. **Statistical Output:** The experiment outputs valid p-values and chi-square statistics quantifying the deviation of internal prime digit transitions from true randomness.

## Constraints
1. **Domain Strictness:** The analysis must remain strictly focused on the digit sequences of prime numbers, avoiding any deviation into unrelated number theory or cryptography.
2. **Internal Digits Only:** The algorithm must explicitly exclude the first digit (which cannot be zero) and the last digit (which is restricted to 1, 3, 7, 9 in Base-10) to prevent trivial biases.
3. **Computational Efficiency:** The robust error-handling mechanisms must not introduce unacceptable computational overhead, allowing the analysis of primes up to $10^7$ within standard execution time limits.

---

## Iteration 7 [REFORMULATED]
Timestamp: 2026-03-25T20:54:20.111372

# Research Problem: Empirical Extraction and Statistical Analysis of 1st- and 2nd-Order Markovian Digit Transitions in Base-10 Primes

## Objective
To successfully compute and statistically analyze the 1st- and 2nd-order Markovian transition probabilities for internal digit sequences of Base-10 prime numbers. Building upon the foundational hypothesis of sequential digit dependencies, this iteration focuses on executing the mathematical extraction over a specific, large range of primes (e.g., $10^6$ to $10^8$) to rigorously test for statistically significant deviations from a uniform random distribution, avoiding edge-case biases.

## Research Questions
1. What are the exact 1st-order ($10 \times 10$) and 2nd-order ($100 \times 10$) digit transition probability matrices for the internal digits of Base-10 primes in the range $[10^6, 10^8]$?
2. When subjected to Chi-square goodness-of-fit tests, do these empirical transition matrices exhibit statistically significant deviations from the null hypothesis (which posits that internal digit transitions are uniformly distributed)?
3. Are there specific digit pairs or triplets (e.g., "3" followed by "7") that occur with anomalous frequency compared to non-prime integers in the same range?

## Methodology
1. **Prime Generation:** Utilize an efficient sieve algorithm to generate all prime numbers within the targeted range of $10^6$ to $10^8$.
2. **Data Sanitization:** For each prime, isolate the *internal* digits by stripping the most significant digit (to avoid Benford's Law biases) and the least significant digit (to avoid the well-known exclusion of even numbers and 5).
3. **Matrix Construction:** 
   - Construct a 1st-order transition matrix tracking the frequency of digit $d_{i+1}$ given $d_i$.
   - Construct a 2nd-order transition matrix tracking the frequency of digit $d_{i+2}$ given the sequence $(d_i, d_{i+1})$.
4. **Statistical Testing:** Compare the resulting matrices against a control set of composite numbers in the same range. Calculate Chi-square statistics and p-values to determine if the prime digit transitions deviate from expected uniform randomness.

## Success Criteria
1. The successful generation and population of both 1st- and 2nd-order Markovian transition matrices for the specified prime range.
2. The calculation of clear statistical metrics (Chi-square values, p-values) that quantify the deviation of prime internal digit sequences from uniform randomness.
3. Identification of at least three specific digit transitions (if any exist) that show the highest divergence from expected probabilities.

## Constraints
1. The analysis must strictly focus on Base-10 representations.
2. The first and last digits of every prime must be strictly excluded from the transition counts to prevent known trivial biases from skewing the Markovian analysis.
3. The computational approach must focus entirely on the mathematical and statistical extraction, assuming a clean, syntactically valid execution environment.

---

## Iteration 8 [REFORMULATED]
Timestamp: 2026-03-25T20:57:30.942697

# Research Problem: Validated Computational Extraction of Markovian Digit Transitions in Base-10 Primes

## Objective
To successfully execute and validate the computational pipeline for extracting 1st- and 2nd-order Markovian transition probabilities within the internal digit sequences of Base-10 prime numbers. Since previous attempts were hindered by execution pipeline failures, this iteration focuses on establishing a robust, error-free computational framework to analyze primes in the range of $10^6$ to $10^8$, ensuring rigorous testing for statistically significant deviations from uniform random distributions.

## Research Questions
1. **Pipeline Validity:** Can a robust computational script be formulated and executed without structural or syntax errors to accurately parse the internal digits of primes?
2. **1st-Order Transitions:** Once the computational pipeline is validated, do the 1st-order digit transition probabilities (e.g., the likelihood of '7' following '3') in primes significantly deviate from those in composite numbers of the same magnitude?
3. **2nd-Order Dependencies:** Do 2nd-order Markovian transitions (e.g., the sequence '1-3-7') reveal deeper localized biases in prime digit distributions?

## Methodology
1. **Computational Framework Development:** Develop a clean, strictly formatted Python script to generate primes between $10^6$ and $10^8$ using an efficient sieve algorithm. 
2. **Data Sanitization:** Ensure the execution environment and code generation process are free of extraneous characters or invalid delimiters that could disrupt execution.
3. **Markov Matrix Construction:** Construct 10x10 (1st-order) and 100x10 (2nd-order) empirical transition matrices for the internal digits of the generated primes, explicitly excluding the highly constrained final digit.
4. **Statistical Analysis:** Apply Chi-square goodness-of-fit tests to compare the empirical transition matrices against a null hypothesis of uniform random transitions.

## Success Criteria
1. **Execution Success:** The computational script runs to completion without syntax or parsing errors.
2. **Matrix Generation:** Successful generation of both 1st-order and 2nd-order transition probability matrices for the specified range of primes.
3. **Statistical Significance:** Computation of p-values for the transition matrices to determine if any observed localized biases are statistically significant.

## Constraints
1. **Domain Adherence:** The study must remain strictly focused on the digit distributions and sequential dependencies of prime numbers.
2. **Digit Constraints:** Analysis must exclude the final digit of the primes, as its distribution is trivially constrained (only 1, 3, 7, 9 are possible).
3. **Computational Efficiency:** The prime generation and matrix construction algorithms must be optimized to handle bounds up to $10^8$ within reasonable memory and time limits.

---

## Iteration 9 [REFORMULATED]
Timestamp: 2026-03-25T21:00:10.746059

# Research Problem: High-Resolution Analysis of 1st- and 2nd-Order Markovian Digit Transitions in Base-10 Primes ($10^6$ to $10^8$)

## Objective
To precisely quantify 1st- and 2nd-order Markovian transition probabilities within the internal digit sequences of Base-10 prime numbers in the range of $10^6$ to $10^8$. Moving past initial framework validation, this iteration focuses on deploying a robust, error-free computational pipeline to identify statistically significant localized biases or sequential dependencies. The primary goal is to determine if internal prime digits exhibit "memory" of preceding digits that deviates from a purely random uniform distribution, completely isolating these effects from known trivial rules.

## Research Questions
1. Do the internal 1st-order digit transition probabilities (e.g., $P(d_{i+1} | d_i)$) of primes in the $10^6$ to $10^8$ range differ with statistical significance from uniformly expected values?
2. Are there specific 2nd-order Markovian chains (e.g., $P(d_{i+2} | d_{i+1}, d_i)$) that exhibit anomalous suppression or enhancement in prime numbers compared to a control dataset of odd composite numbers of the same magnitude?
3. How does the transition probability matrix evolve as the magnitude of the primes increases across the specified range?

## Methodology
1. **Data Generation:** Utilize an optimized Sieve of Eratosthenes to generate a complete set of prime numbers strictly between $10^6$ and $10^8$. Generate a parallel control set of odd composite numbers in the same range.
2. **Digit Extraction & Truncation:** Convert the numbers to Base-10 strings. Strip the first digit (to avoid Benford's Law biases) and the final digit (to avoid trivial primality constraints like the absence of 2, 4, 5, 6, 8, 0) from all numbers.
3. **Markovian Matrix Construction:** Parse the remaining internal digit sequences to populate $10 \times 10$ matrices for 1st-order transitions and $100 \times 10$ matrices for 2nd-order transitions.
4. **Statistical Testing:** Perform Chi-square goodness-of-fit tests to compare the empirical prime transition matrices against the control matrices and a theoretical uniform distribution.

## Success Criteria
1. Uninterrupted, error-free computational extraction of the Markovian transition matrices for the specified range.
2. Generation of statistically rigorous p-values comparing the internal digit transitions of primes against the uniform and composite-number null hypotheses.
3. Identification of at least three specific digit transitions (if any exist) that show the highest divergence from expected random behavior.

## Constraints
1. The analysis must strictly ignore the trailing digit of all primes to prevent contamination from known Base-10 divisibility rules.
2. The analysis must strictly ignore the leading digit to prevent contamination from Benford's Law.
3. The computational pipeline must be structurally sound and strictly focused on data extraction without syntax interruptions.

---

## Iteration 10 [REFORMULATED]
Timestamp: 2026-03-25T21:04:50.503458

# Research Problem: Robust Statistical Extraction of 1st- and 2nd-Order Markovian Digit Transitions in Internal Base-10 Primes ($10^6$ to $10^8$)

## Objective
To successfully compute and rigorously quantify the 1st- and 2nd-order Markovian transition probabilities of internal digits within Base-10 primes in the range of $10^6$ to $10^8$. Following previous execution limitations, this iteration emphasizes a robust, error-free analytical pipeline to establish the definitive transition matrices. The primary goal is to determine if the internal digits of primes exhibit any localized "memory" or sequential dependencies that deviate from expected uniform randomness, isolating these effects from trivial boundary biases.

## Research Questions
1. **Empirical Transition Matrices:** What are the exact empirical 1st-order ($10 \times 10$) and 2nd-order ($100 \times 10$) transition probability matrices for internal digits (strictly excluding the first and last digits) of Base-10 primes between $10^6$ and $10^8$?
2. **Statistical Deviation:** Do these internal transition probabilities deviate significantly from a uniformly random distribution, and how do they compare against the transition matrices of composite numbers within the exact same numerical range?
3. **Localized Biases:** Are there specific digit pairs (e.g., "3 followed by 3") or triplets that occur with a statistically significant higher or lower frequency than predicted by standard uniform probability models?

## Methodology
1. **Data Generation:** Utilize an optimized Sieve of Eratosthenes to generate all prime numbers strictly within the $10^6$ to $10^8$ range.
2. **Data Sanitization:** Convert primes to strings and explicitly strip the most significant (first) and least significant (last) digits to eliminate well-known Base-10 boundary artifacts (e.g., primes cannot end in 0, 2, 4, 5, 6, 8).
3. **Markovian Analysis:** 
   - Tally 1st-order transitions ($P(D_i | D_{i-1})$) and 2nd-order transitions ($P(D_i | D_{i-1}, D_{i-2})$) across the sanitized internal digit sequences.
   - Compute the corresponding probability matrices.
4. **Statistical Testing:** Apply Chi-square tests of independence and calculate the Kullback-Leibler (KL) divergence to measure the distance between the observed prime digit transition distributions and a purely uniform null hypothesis.

## Success Criteria
1. Successful compilation of complete, mathematically sound 1st- and 2nd-order transition probability matrices for the specified range.
2. Generation of statistically rigorous p-values (via Chi-square analysis) determining whether internal prime digits exhibit non-random Markovian memory.
3. Clear visualization (e.g., heatmaps) of the transition matrices to highlight any identified localized biases.

## Constraints
1. The analysis must be strictly confined to Base-10 integers between $10^6$ and $10^8$.
2. The algorithm must strictly exclude the terminal digit of every prime to prevent the trivial $\{1, 3, 7, 9\}$ ending rule from skewing the transition probabilities. 
3. The computational pipeline must be scientifically verified for mathematical correctness prior to statistical extraction, ensuring no invalid data artifacts influence the matrices.

---
