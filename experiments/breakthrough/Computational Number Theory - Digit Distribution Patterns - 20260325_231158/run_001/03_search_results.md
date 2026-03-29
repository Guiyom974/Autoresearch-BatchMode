
### Query: "prime numbers" "digit transition probabilities" OR "sequential digit dependencies" Markov
Here is a summary of the top search results regarding the intersection of prime numbers, digit transitions/dependencies, and Markov chains. 

### 1. Markov Chain of Prime Gaps
**Summary:** This 2022 paper by Merliza F. Libao models the sequence of prime gaps (the difference between consecutive prime numbers) as a discrete-time Markov chain. By treating the appearance of primes as a stochastic process, the author demonstrates that the Markov chain of prime gaps is irreducible, aperiodic, and positive recurrent. Ultimately, the paper proves that the sequence of prime gaps is ergodic, meaning it possesses a stationary (ergodic) distribution over time [[1]](https://www.researchgate.net/publication/366066509_Markov_Chain_of_Prime_Gaps).
**Source:** *NeuroQuantology / ResearchGate* [[1]](https://www.researchgate.net/publication/366066509_Markov_Chain_of_Prime_Gaps)

### 2. Distribution of Integers with Digit Restrictions via Markov Chains
**Summary:** This 2025 paper explores the distribution of integers with specific digit restrictions (such as missing digits) in arithmetic progressions. The authors use Markov chains to derive necessary and sufficient conditions for these restricted sets to be uniformly distributed. The study explicitly connects to breakthrough work on the sum-of-digits function for primes and the existence of infinitely many primes with missing digits, using Markov transition matrices instead of traditional Fourier analysis to map sequential digit dependencies [[2]](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3E6DB0E337432A1D01D622A038553E61/S0143385725102563a.pdf/distribution-of-integers-with-digit-restrictions-via-markov-chains.pdf).
**Source:** *Cambridge University Press* [[2]](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3E6DB0E337432A1D01D622A038553E61/S0143385725102563a.pdf/distribution-of-integers-with-digit-restrictions-via-markov-chains.pdf)

### 3. Markov Chains and Primes: How Randomness Shapes Patterns
**Summary:** This article discusses the philosophical and mathematical interplay between prime numbers and Markov chains. It highlights how prime numbers underpin the hashing algorithms and modular arithmetic used to generate the pseudo-random sequences that simulate Markov behavior. Primes help ensure uniform mixing and long-term balance in state transition probabilities, turning stochastic motion into sequences with predictable steady-state distributions [[3]](https://idealfiberglass.com/markov-chains-and-primes-how-randomness-shapes-patterns/).
**Source:** *Ideal Fiberglass* [[3]](https://idealfiberglass.com/markov-chains-and-primes-how-randomness-shapes-patterns/)

### 4. Prime Numbers Treated as a Markov Chain
**Summary:** This is a foundational technical report by V.R.R. Uppuluri from the Oak Ridge National Laboratory. It explores the treatment of prime numbers and their distributions through the lens of probability, measure theory, and Markov chains. The report investigates whether the sequence of primes (and related sets like Mersenne numbers) can be modeled using ergodic theory and Markovian state transitions [[4]](https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/PB180746.xhtml).
**Source:** *National Technical Reports Library (NTIS)* [[4]](https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/PB180746.xhtml)

### 5. Primes Made from Sequential Digits
**Summary:** While not strictly a Markov paper, this mathematical discussion explores "consecutive digit primes"—prime numbers composed of sequentially increasing digits (e.g., 23, 67, 89, 23456789) with specific transition rules (like returning to 1 after a 9). The discussion highlights the asymptotic density of such numbers and references historical literature (like J.S. Madachy's work) on the finite or infinite nature of primes governed by strict sequential digit dependencies [[5]](https://math.stackexchange.com/questions/903762/primes-made-from-sequential-digits).
**Source:** *Mathematics Stack Exchange* [[5]](https://math.stackexchange.com/questions/903762/primes-made-from-sequential-digits)

---
Learn more:
1. [(PDF) Markov Chain of Prime Gaps - ResearchGate](https://www.researchgate.net/publication/366066509_Markov_Chain_of_Prime_Gaps)
2. [Distribution of integers with digit restrictions via Markov chains - Cambridge University Press & Assessment](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3E6DB0E337432A1D01D622A038553E61/S0143385725102563a.pdf/distribution-of-integers-with-digit-restrictions-via-markov-chains.pdf)
3. [Markov Chains and Primes: How Randomness Shapes Patterns](https://idealfiberglass.com/markov-chains-and-primes-how-randomness-shapes-patterns/)
4. [Prime Numbers Treated as a Markov Chain. - National Technical Reports Library - NTIS](https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/PB180746.xhtml)
5. [number theory - Primes made from sequential digits - Mathematics Stack Exchange](https://math.stackexchange.com/questions/903762/primes-made-from-sequential-digits)



### Query: "digit distribution" "prime numbers" "base-2" OR "base-16" OR "arbitrary base" bias
Here is a summary of the findings regarding the digit distribution and biases of prime numbers across different number bases:

### 1. Prime Numbers and Generalized Benford's Law
In many naturally occurring datasets, the leading digits follow **Benford's Law**, which dictates a strong bias toward smaller digits (e.g., '1' appears as the first digit about 30% of the time in base-10) [[1]](https://en.wikipedia.org/wiki/Benford%27s_law). However, prime numbers behave differently. Primes in a finite interval follow a *Generalized Benford's Law* (GBL) [[1]](https://en.wikipedia.org/wiki/Benford%27s_law). This means that while there is a slight bias toward smaller leading digits in smaller finite ranges, this bias is size-dependent. As the range of prime numbers approaches infinity, their first-digit distribution smoothly approaches absolute uniformity (where all valid starting digits become equally likely) [[2]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and). 

### 2. Digit Bias in Arbitrary Bases (Base-2, Base-16, etc.)
The mathematical framework for leading-digit distributions applies to any arbitrary base $b$ [[3]](https://www.gresham.ac.uk/watch-now/benfords-very-strange-law). The expected probability of a first digit $d$ in a Benford-compliant sequence in base $b$ is given by $\log_b(1 + 1/d)$ [[3]](https://www.gresham.ac.uk/watch-now/benfords-very-strange-law). 
* **Base-16 and others:** Researchers analyzing various mathematical sequences (like L-functions or the $3x+1$ problem) in base-16 have observed how leading digits conform to these base-specific logarithmic distributions [[4]](https://web.williams.edu/Mathematics/sjmiller/public_html/BrownClasses/197/benford/Benford_AVKontorovichSJMIller_Final06b_aa.pdf). 
* **Persistent Base Biases:** A recent study analyzing multi-digit correlations across integer bases from base-2 to base-1000 found that while most bases converge to the expected logarithmic distributions, roughly 8.4% of bases exhibit "persistent correlations" where the digit distributions never fully converge, maintaining a permanent statistical bias [[5]](https://arxiv.org/pdf/2603.18243).

### 3. Chebyshev's Bias and Last-Digit Patterns
When discussing "bias" in prime numbers, mathematicians often refer to **Chebyshev's Bias** [[6]](https://www.quora.com/Do-prime-numbers-form-a-pattern-in-different-bases). While the *first* digits of primes approach uniformity, the *last* digits (which dictate the congruence class of the prime) exhibit known biases [[6]](https://www.quora.com/Do-prime-numbers-form-a-pattern-in-different-bases). For example, in base-10, primes (greater than 5) must end in 1, 3, 7, or 9 [[6]](https://www.quora.com/Do-prime-numbers-form-a-pattern-in-different-bases). Chebyshev's Bias describes the phenomenon where primes are not perfectly evenly distributed among these allowed ending digits (or modulo classes) in finite samples, often favoring congruence classes that are non-quadratic residues [[6]](https://www.quora.com/Do-prime-numbers-form-a-pattern-in-different-bases). This type of modular bias exists regardless of whether the primes are represented in base-10, base-2, or base-16.

### Sources
* ** [[7]](https://tomrocksmaths.com/wp-content/uploads/2024/06/prime-numbers-essay.docx) Wikipedia:** [Benford's Law - Distributions known to disobey Benford's law](https://en.wikipedia.org/wiki/Benford%27s_law) [[1]](https://en.wikipedia.org/wiki/Benford%27s_law)
* ** [[6]](https://www.quora.com/Do-prime-numbers-form-a-pattern-in-different-bases) The Royal Society:** [The first-digit frequencies of prime numbers and Riemann zeta zeros](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and) [[2]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)
* ** [[1]](https://en.wikipedia.org/wiki/Benford%27s_law) Quora:** [Do prime numbers form a pattern in different bases?](https://www.quora.com/Do-prime-numbers-form-a-pattern-in-different-bases) [[6]](https://www.quora.com/Do-prime-numbers-form-a-pattern-in-different-bases)
* ** [[3]](https://www.gresham.ac.uk/watch-now/benfords-very-strange-law) arXiv:** [Why Eight Percent of Benford Sequences Never Converge](https://arxiv.org/pdf/2603.18243) [[5]](https://arxiv.org/pdf/2603.18243)
* ** [[2]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and) Williams College / S.J. Miller et al.:** [Benford's Law, Values of L-Functions and the 3x+1 Problem](https://web.williams.edu/Mathematics/sjmiller/public_html/BrownClasses/197/benford/Benford_AVKontorovichSJMIller_Final06b_aa.pdf) [[4]](https://web.williams.edu/Mathematics/sjmiller/public_html/BrownClasses/197/benford/Benford_AVKontorovichSJMIller_Final06b_aa.pdf)

---
Learn more:
1. [Benford's law - Wikipedia](https://en.wikipedia.org/wiki/Benford%27s_law)
2. [The first-digit frequencies of prime numbers and Riemann zeta zeros | Proceedings A | The Royal Society](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)
3. [Benford's Very Strange Law | Gresham College](https://www.gresham.ac.uk/watch-now/benfords-very-strange-law)
4. [BENFORD'S LAW, VALUES OF L-FUNCTIONS AND THE 3x + 1 PROBLEM](https://web.williams.edu/Mathematics/sjmiller/public_html/BrownClasses/197/benford/Benford_AVKontorovichSJMIller_Final06b_aa.pdf)
5. [Why Eight Percent of Benford Sequences Never Converge - arXiv](https://arxiv.org/pdf/2603.18243)
6. [Do prime numbers form a pattern in different bases? - Quora](https://www.quora.com/Do-prime-numbers-form-a-pattern-in-different-bases)
7. [https://tomrocksmaths.com/wp-content/uploads/2024/06/prime-numbers-essay.docx](https://tomrocksmaths.com/wp-content/uploads/2024/06/prime-numbers-essay.docx)



### Query: "computational number theory" prime digit sequence "localized biases" non-uniform
Here are the search results and a summary of the findings related to your query on prime digit sequences, localized biases, and non-uniformity in computational number theory.

### Summary of Findings
The search terms intersect two distinct but related areas in mathematics and cryptography:
1. **Unexpected Biases in Prime Digits**: In 2016, mathematicians Robert Lemke Oliver and Kannan Soundararajan discovered a profound, non-uniform bias in the final digits of consecutive prime numbers [[1]](https://pmc.ncbi.nlm.nih.gov/articles/PMC4978288/)[[2]](https://arxiv.org/abs/1603.03720). While primes overall are equally distributed among permissible ending digits (1, 3, 7, 9 in base 10), *consecutive* primes strongly avoid repeating the same last digit. For example, a prime ending in 1 is much less likely to be followed by another prime ending in 1 than by a prime ending in 3, 7, or 9 [[1]](https://pmc.ncbi.nlm.nih.gov/articles/PMC4978288/)[[3]](https://www.researchgate.net/publication/305699784_Explaining_biases_in_last_digit_distributions_of_consecutive_primes). This phenomenon is explained using the Hardy-Littlewood conjectures and represents a major recent discovery in computational and analytic number theory [[1]](https://pmc.ncbi.nlm.nih.gov/articles/PMC4978288/)[[2]](https://arxiv.org/abs/1603.03720).
2. **Localized Biases in Cryptography**: The exact phrase "localized biases" alongside "computational number theory" frequently appears in cryptographic engineering literature [[4]](http://ndl.ethernet.edu.et/bitstream/123456789/32093/1/Cryptographic%20Engineering.pdf). In this context, it refers to non-uniformity in hardware-generated random bit streams. Cryptographers use techniques like the von Neumann corrector to remove these localized biases (e.g., filtering out consecutive identical bits) to create uniformly distributed sequences for secure cryptographic applications [[4]](http://ndl.ethernet.edu.et/bitstream/123456789/32093/1/Cryptographic%20Engineering.pdf).

---

### Search Results

**1. Unexpected biases in the distribution of consecutive primes (PNAS / NIH)**
*   **Summary**: This landmark paper by Lemke Oliver and Soundararajan details how the distribution of pairs of consecutive primes among reduced residue classes is "surprisingly erratic" and non-uniform. They formulate a precise conjecture based on the Hardy-Littlewood conjectures to explain why certain prime digit patterns experience significant biases.
*   **Source**: [PMC - NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC4978288/) [[1]](https://pmc.ncbi.nlm.nih.gov/articles/PMC4978288/)

**2. [1603.03720] Unexpected biases in the distribution of consecutive primes (arXiv)**
*   **Summary**: The pre-print repository version of the Lemke Oliver and Soundararajan paper. It highlights that while the sequence of primes is well distributed overall, the transition between consecutive primes exhibits heavy biases, which they verified against massive numerical data sets.
*   **Source**: [arXiv](https://arxiv.org/abs/1603.03720) [[2]](https://arxiv.org/abs/1603.03720)

**3. Explaining biases in last digit distributions of consecutive primes**
*   **Summary**: A presentation/paper discussing the computational discovery that in the first $10^8$ pairs of consecutive primes, only about 4.6 million end with the sequence {1,1}, whereas over 7.4 million end with {1,3}. It explores elementary theory and computational methods to account for this sizable, non-uniform bias.
*   **Source**: [ResearchGate](https://www.researchgate.net/publication/305699784_Explaining_biases_in_last_digit_distributions_of_consecutive_primes) [[3]](https://www.researchgate.net/publication/305699784_Explaining_biases_in_last_digit_distributions_of_consecutive_primes)

**4. How to explain this prime gap bias around last digits?**
*   **Summary**: A MathOverflow discussion analyzing experimental computational results up to the 3,500,000th prime. Mathematicians discuss how cumulative prime gaps after primes with a fixed last digit exhibit biases, linking the experimental data back to the Lemke Oliver and Soundararajan findings.
*   **Source**: [MathOverflow](https://mathoverflow.net/questions/357379/how-to-explain-this-prime-gap-bias-around-last-digits) [[5]](https://mathoverflow.net/questions/357379/how-to-explain-this-prime-gap-bias-around-last-digits)

**5. Cryptographic Engineering (Textbook)**
*   **Summary**: This textbook bridges computational number theory and electrical engineering. It explicitly discusses "localized biases" in the context of random bit streams generated for cryptography. It explains how raw sequences often have non-uniform probabilities and require algorithmic correctors (like the von Neumann corrector) to achieve true randomness. 
*   **Source**: [National Academic Digital Library of Ethiopia](http://ndl.ethernet.edu.et/bitstream/123456789/32093/1/Cryptographic%20Engineering.pdf) [[4]](http://ndl.ethernet.edu.et/bitstream/123456789/32093/1/Cryptographic%20Engineering.pdf)

---
Learn more:
1. [Unexpected biases in the distribution of consecutive primes - PMC - NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC4978288/)
2. [\[1603.03720\] Unexpected biases in the distribution of consecutive primes - arXiv](https://arxiv.org/abs/1603.03720)
3. [(PDF) Explaining biases in last digit distributions of consecutive primes - ResearchGate](https://www.researchgate.net/publication/305699784_Explaining_biases_in_last_digit_distributions_of_consecutive_primes)
4. [Cryptographic Engineering.pdf - National Academic Digital Library of Ethiopia](http://ndl.ethernet.edu.et/bitstream/123456789/32093/1/Cryptographic%20Engineering.pdf)
5. [How to explain this prime gap bias around last digits? - MathOverflow](https://mathoverflow.net/questions/357379/how-to-explain-this-prime-gap-bias-around-last-digits)


