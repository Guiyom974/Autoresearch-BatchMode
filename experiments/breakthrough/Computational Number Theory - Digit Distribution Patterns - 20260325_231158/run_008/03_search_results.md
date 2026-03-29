
### Query: "Benford's law" "prime numbers" "primorial base" OR "base-210" leading digit distribution
Based on the search results, the intersection of **Benford's Law**, **prime numbers**, and **primorial bases (like base-210)** reveals fascinating patterns about how primes are distributed and represented. 

Here is a summary of the findings:

### 1. Benford's Law and Prime Numbers
Benford's Law dictates that in many naturally occurring collections of numbers, the leading digit is likely to be small (e.g., "1" appears as the leading digit about 30% of the time). Prime numbers, when looked at over large, exponentially growing ranges, generally conform to Benford's Law for their leading digits [[1]](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number)[[2]](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well). Because the density of primes decreases as numbers get larger (as described by the Prime Number Theorem), the logarithmic scale of Benford's Law naturally applies to their distribution [[1]](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number).

### 2. The Role of Base-210 (Primorial Base)
Base-210 is a "primorial" base, meaning it is the product of the first consecutive prime numbers ($2 \times 3 \times 5 \times 7 = 210$). 
* **Wheel Factorization:** Base-210 is heavily used in computational number theory and prime sieving. By working in modulo 210, mathematicians and programmers can instantly filter out multiples of 2, 3, 5, and 7, which eliminates about 77% of all integers from being potential primes [[3]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). 
* **Trailing vs. Leading Digits:** In a primorial base like 210, the *last* digit of any prime number (greater than 7) must be a number that is coprime to 210. While primorial bases strictly govern the behavior of *trailing* digits, the *leading* digits of primes in base-210 will still follow a generalized Benford's Law distribution, favoring smaller leading digits [[1]](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number)[[3]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/).

### 3. Prime "Memory" and Digit Bias
A recent massive data analysis of the first 37 billion primes (up to 1 trillion) visualized the "bias" in prime digits [[3]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). The analysis verified the famous Lemke Oliver & Soundararajan discovery that primes "hate" repeating their last digits (e.g., a prime ending in 1 is less likely to be followed by another prime ending in 1) [[3]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). 
* To compute this efficiently, researchers use custom binary bitmap databases based on **Mod 210 Wheel Factorization** [[3]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). 
* When discussing these distributions and the gaps between primes, data scientists frequently point to **Benford's Law**, noting that prime gaps follow a negative slope with a log-scale distribution, which mirrors the logarithmic logic of Benford's Law [[3]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/).

### 4. Base Dependence of Benford's Law
The base you choose fundamentally changes how Benford's Law manifests. For example, in binary (base-2), Benford's Law is rendered moot for leading digits because every non-zero number must start with a "1" [[2]](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well). However, in larger bases like base-10 or base-210, the logarithmic distribution of leading digits remains a prominent feature of prime number datasets [[2]](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well).

***

### Sources
* ** [[1]](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number) Quora:** *If a two-digit number is chosen at random, what is the probability that the number chosen is not a prime number?* (Discussions on prime distribution and Benford's Law).
* ** [[2]](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well) Quora:** *Why do humans use base-ten counting systems?* (Discussions on Benford's Law, binary immunity, and primorial base expansions).
* ** [[3]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/) Reddit (r/dataisbeautiful):** *[OC] Do Prime Numbers have "memory"? I analyzed the first 37 Billion primes...* (Analysis of prime digit bias using Mod 210 Wheel Factorization and connections to Benford's Law).
* ** [[1]](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number) Quora:** *Probability and Base 210 prime possibilities.*

---
Learn more:
1. [If a two-digit number is chosen at random, what is the probability that the number chosen is not a prime number? - Quora](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number)
2. [Why do humans use base-ten counting systems? Do other animals use base-two (binary)? Is this difference just cultural or biological/evolutionary as well? - Quora](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well)
3. [\[OC\] Do Prime Numbers have "memory"? I analyzed the first 37 Billion primes (up to 1 Trillion) to visualize the bias in their last digits : r/dataisbeautiful - Reddit](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)



### Query: "goodness-of-fit" "Benford's law" adjusted null model prime number distribution statistical testing
Here is a summary of the search results regarding the use of goodness-of-fit statistical testing, adjusted null models, and Benford's Law, particularly in the context of prime number distributions:

### Summary of Findings

**1. Generalized Benford's Law and Prime Numbers**
While standard Benford's Law applies to many naturally occurring datasets spanning multiple orders of magnitude, the distribution of the first digits of prime numbers does not perfectly align with the traditional model. Instead, research shows that prime numbers (and non-trivial Riemann zeta zeros) are better described by a **Generalized Benford's Law (GBL)** [[1]](https://www.researchgate.net/publication/362199448_Testing_for_Benford's_Law_in_very_small_samples_Simulation_study_and_a_new_test_proposal/download)[[2]](https://statistics.calpoly.edu/shiny). Statistical applications and simulators often use GBL as the "adjusted null model" when performing goodness-of-fit tests on prime number sequences to accurately assess conformity [[2]](https://statistics.calpoly.edu/shiny).

**2. Goodness-of-Fit Testing for Benford's Law**
To determine if a dataset conforms to Benford's Law (or an adjusted null model like GBL), researchers utilize various non-parametric goodness-of-fit tests. Common statistical tests include:
*   **Chi-Square Test:** Frequently used to compare observed first-digit frequencies against expected Benford probabilities [[3]](https://rosettacode.org/wiki/Benford%27s_law)[[4]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0169632).
*   **Kolmogorov-Smirnov (KS) & Modified Kuiper Tests:** The Kuiper test is a modified KS goodness-of-fit test that accounts for the ordinality and circularity of leading digits. Researchers often apply correction factors (like Stephens' correction) to adjust the test statistics and critical values for more robust null hypothesis testing [[4]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0169632).
*   **Small Sample Adjustments:** Standard asymptotic tests often fail or lose reliability with very small sample sizes. Recent literature proposes new test statistics and approximations to the null distribution (e.g., via Monte Carlo simulations or wild bootstrap procedures) to create modified goodness-of-fit procedures with better inferential properties [[1]](https://www.researchgate.net/publication/362199448_Testing_for_Benford's_Law_in_very_small_samples_Simulation_study_and_a_new_test_proposal/download)[[5]](https://www.researchgate.net/publication/349462123_On_Characterizations_and_Tests_of_Benford's_Law).

**3. Applications in Anomaly Detection**
Because humans are generally poor at fabricating numbers that conform to Benford's distribution, these goodness-of-fit tests are heavily utilized in forensic statistics. By establishing Benford's Law (or an adjusted distribution) as the null model, statistically significant deviations can flag potential data manipulation, fraud, or strategic misreporting in fields ranging from international finance to customs declarations [[4]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0169632)[[5]](https://www.researchgate.net/publication/349462123_On_Characterizations_and_Tests_of_Benford's_Law).

### Sources

*   ** [[1]](https://www.researchgate.net/publication/362199448_Testing_for_Benford's_Law_in_very_small_samples_Simulation_study_and_a_new_test_proposal/download)** *Testing for Benford's Law in very small samples: Simulation study and a new test proposal* (ResearchGate, 2022). Discusses approximations to the distribution of test statistics and the Generalized Benford law for prime numbers. 
*   ** [[2]](https://statistics.calpoly.edu/shiny)** *Shiny - Statistics Department - Cal Poly*. An interactive statistical tool that applies goodness-of-fit tests to various datasets, explicitly noting that prime number sequences are tested against the Generalized Benford's Law (GBL). 
*   ** [[5]](https://www.researchgate.net/publication/349462123_On_Characterizations_and_Tests_of_Benford's_Law)** *On Characterizations and Tests of Benford's Law* (ResearchGate, 2021). Explores new tests of conformance, sum-invariance characterizations, and modified goodness-of-fit procedures. 
*   ** [[3]](https://rosettacode.org/wiki/Benford%27s_law)** *Benford's law - Rosetta Code*. Provides programmatic implementations of Benford's Law, including chi-square goodness-of-fit testing and prime number datasets. 
*   ** [[4]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0169632)** *Do Countries Consistently Engage in Misinforming the International Community...? Evidence Using Benford's Law* (PLOS One). Details the use of the modified Kuiper test, adjusted test statistics, and null hypothesis testing for detecting data manipulation.

---
Learn more:
1. [(PDF) Testing for Benford's Law in very small samples: Simulation study and a new test proposal - ResearchGate](https://www.researchgate.net/publication/362199448_Testing_for_Benford's_Law_in_very_small_samples_Simulation_study_and_a_new_test_proposal/download)
2. [Shiny - Statistics Department - Cal Poly, San Luis Obispo](https://statistics.calpoly.edu/shiny)
3. [Benford's law - Rosetta Code](https://rosettacode.org/wiki/Benford%27s_law)
4. [Do Countries Consistently Engage in Misinforming the International Community about Their Efforts to Combat Money Laundering? Evidence Using Benford's Law | PLOS One](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0169632)
5. [(PDF) On Characterizations and Tests of Benford's Law - ResearchGate](https://www.researchgate.net/publication/349462123_On_Characterizations_and_Tests_of_Benford's_Law)



### Query: empirical distribution leading digits primes coprime "base-210" OR "primorial"
Here is a summary of the search results regarding the empirical distribution of leading digits, primes, coprime conditions, and primorials (such as base-210):

### 1. Benford Behavior and Distribution in Residue Classes of Large Prime Factors
**Source:** *Canadian Mathematical Bulletin* / Paul Pollack [[1]](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/benford-behavior-and-distribution-in-residue-classes-of-large-prime-factors/77F6DAF48EA54EF008AC5B8BE19C60B1), [[2]](https://pollack.uga.edu/smoothbenford.pdf)
**Summary:** This paper investigates the leading digit distribution of the $k$-th largest prime factor of $n$, as well as the sum of all prime factors of $n$. The author proves that these leading digits are distributed according to Benford's Law (where smaller digits are more likely to appear as leading digits). The paper specifically notes that while the sequence of primes itself does not naturally form a Benford distribution without logarithmic scaling, the "primorial" function $f(n) = \prod_{k=1}^n p_k$ (the product of the first $n$ primes) *does* strictly obey Benford's law in every base.

### 2. Dirichlet, Sierpiński, and Benford
**Source:** *Paul Pollack (UGA)* [[3]](https://pollack.uga.edu/DSB.pdf)
**Summary:** This mathematical note explores the distribution of leading digits of prime numbers. It provides a Dirichlet-style proof of Sierpiński's theorem, which states that for any valid leading digit sequence $A$ and ending digit sequence $B$ (where $B$ is coprime to the base $g$), there are infinitely many primes starting with $A$ and ending with $B$. It discusses how arithmetic functions and prime densities align with Benford's Law when evaluated using logarithmic or Dirichlet densities.

### 3. The Laws of the Minor Prime Factors
**Source:** *Preprints.org (2025)* [[4]](https://www.preprints.org/frontend/manuscript/4a959743e9080bbc197e8df44c80b6ef/download_pub)
**Summary:** This paper examines the Newcomb-Benford Law (NBL) in the context of prime numbers and their factorization. It highlights that while the standard sequence of primes is not naturally Benford, applying a logarithmic or zeta density reveals that primes do comply with the NBL. The paper also explores generalized NBL distributions by constraining intervals of primes using primorials (e.g., $p_{\pi(N)}\#$) to account for the varying density of primes across different scales.

### 4. Reversible Primes Conjecture and Primorial Bases
**Source:** *PrimePuzzles.net* [[5]](https://www.primepuzzles.net/conjectures/conj_054.htm)
**Summary:** This discussion focuses on "reversible primes" (primes that remain prime when their digits are reversed) and how the base of the number system affects their frequency. In a composite base, a prime cannot end in a digit that shares a common factor with the base; therefore, its reversal cannot *begin* with that digit. The text explicitly mentions primorial bases like base 30, **base 210** ($2 \times 3 \times 5 \times 7$), and base 2310. Because these bases are highly composite (primorials), a massive fraction of potential leading/ending digits are not coprime to the base, heavily restricting the empirical distribution of valid leading digits for reversible primes compared to prime bases.

### 5. Probability and Distribution of Primes in Base-210
**Source:** *Quora* [[6]](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number)
**Summary:** In a discussion about the probability of randomly selecting primes, users highlight the constraints of highly composite bases like **base-210**. In base-210, any prime (greater than 7) must end in a digit that is coprime to 210. The thread also touches upon how the distribution of leading digits of naturally occurring numbers typically follows Benford's Law, meaning digits like 1 are significantly more common than 8 or 9, which skews empirical probability distributions when analyzing prime leading digits in arbitrary bases.

---
Learn more:
1. [Benford behavior and distribution in residue classes of large prime factors | Canadian Mathematical Bulletin - Cambridge University Press & Assessment](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/benford-behavior-and-distribution-in-residue-classes-of-large-prime-factors/77F6DAF48EA54EF008AC5B8BE19C60B1)
2. [Benford behavior and distribution in residue classes of large prime factors - Paul Pollack](https://pollack.uga.edu/smoothbenford.pdf)
3. [DIRICHLET, SIERPI´NSKI, AND BENFORD 1. Introduction This note centers around the following charming theorem published by Sierpi - Paul Pollack](https://pollack.uga.edu/DSB.pdf)
4. [The Laws of the Minor Prime Factors - Preprints.org](https://www.preprints.org/frontend/manuscript/4a959743e9080bbc197e8df44c80b6ef/download_pub)
5. [Conjecture 54. Reversible primes conjeture](https://www.primepuzzles.net/conjectures/conj_054.htm)
6. [If a two-digit number is chosen at random, what is the probability that the number chosen is not a prime number? - Quora](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number)


