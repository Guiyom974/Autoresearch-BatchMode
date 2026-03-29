
### Query: "prime number" digit distribution biases across different numerical
Here is a summary of the findings regarding digit distribution biases in prime numbers across different numerical bases, based on the top search results:

### 1. The "Anti-Repetition" Bias of Consecutive Primes
For a long time, mathematicians assumed that the final digits of prime numbers behaved almost entirely randomly. For example, in base 10, any prime number greater than 5 must end in 1, 3, 7, or 9. It was expected that a prime ending in 1 would have an equal (roughly 25%) chance of being followed by a prime ending in 1, 3, 7, or 9 [[1]](https://www.sciencenews.org/article/mathematicians-find-peculiar-pattern-primes)[[2]](https://brilliant.org/wiki/distribution-of-primes/). 

However, in 2016, mathematicians Robert Lemke Oliver and Kannan Soundararajan discovered a massive departure from this expected randomness: **primes "hate" to repeat their final digits** [[1]](https://www.sciencenews.org/article/mathematicians-find-peculiar-pattern-primes)[[3]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/). When looking at the first 100 million primes, a prime ending in 1 is followed by another prime ending in 1 only about 18% of the time, while it is followed by a prime ending in 3 or 7 much more frequently [[1]](https://www.sciencenews.org/article/mathematicians-find-peculiar-pattern-primes)[[4]](https://golem.ph.utexas.edu/category/2016/03/unexpected_biases_in_the_distr.html). 

### 2. The Phenomenon Persists Across Different Numerical Bases
Lemke Oliver and Soundararajan's computational experiments (which checked the first 400 billion primes) revealed that this bias is not just an artifact of our base-10 counting system [[1]](https://www.sciencenews.org/article/mathematicians-find-peculiar-pattern-primes)[[3]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/). 
* **Base 3:** In base 3, primes (other than 2) must end in either 1 or 2. The researchers found that a base-3 prime ending in 1 is more than twice as likely to be followed by a prime ending in 2 than by another prime ending in 1 [[3]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/).
* **Universal Conjecture:** The mathematicians conjectured and found numerical evidence that this anti-repetition bias holds true in *every* numerical base, though the specific frequencies vary depending on the base [[3]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/)[[4]](https://golem.ph.utexas.edu/category/2016/03/unexpected_biases_in_the_distr.html).

### 3. The Mathematical Explanation
The researchers realized that simple explanations—such as a prime ending in 3 hitting numbers ending in 7, 9, or 1 before it reaches another number ending in 3—could not account for the sheer magnitude of the bias [[1]](https://www.sciencenews.org/article/mathematicians-find-peculiar-pattern-primes)[[3]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/). 

Instead, they proved that the bias can be explained by the **Hardy–Littlewood prime *k*-tuples conjecture**, a highly sophisticated model of prime randomness developed in 1923 [[3]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/)[[5]](https://www.pnas.org/doi/10.1073/pnas.1605366113). The biases do eventually even out and approach true randomness as you go infinitely far along the number line, but they do so at a remarkably slow ("snail's pace") rate [[3]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/)[[4]](https://golem.ph.utexas.edu/category/2016/03/unexpected_biases_in_the_distr.html).

### 4. Biases in the Parity of the "Sum of Digits"
Beyond just the final digit, other base-dependent biases have been observed. A 2018 paper explored the parity (evenness or oddness) of the *sum* of a prime number's digits. Researchers found that in base 10, the sum of a prime number's digits is significantly more likely to be odd than even. This sum-of-digits bias was also tested and shown to persist across other even number bases, allowing researchers to reliably differentiate between a list of random numbers and a list of primes just by looking at their digit sums [[6]](https://arxiv.org/pdf/1812.11841).

***

### Sources
1. **Quanta Magazine:** *Mathematicians Discover Prime Conspiracy* (2016) - Details Lemke Oliver and Soundararajan's discovery of the last-digit bias across base 3, base 10, and others. [[3]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/)
2. **Science News:** *Mathematicians find a peculiar pattern in primes* (2016) - Discusses the statistical breakdown of the anti-repetition bias in the first 100 million primes. [[1]](https://www.sciencenews.org/article/mathematicians-find-peculiar-pattern-primes)
3. **PNAS:** *Unexpected biases in the distribution of consecutive primes* (2016) - The original peer-reviewed paper by Lemke Oliver and Soundararajan explaining the phenomenon using the prime *k*-tuples conjecture. [[5]](https://www.pnas.org/doi/10.1073/pnas.1605366113)
4. **The n-Category Café:** *Weirdness in the Primes* (2016) - Explains the mathematical formulas behind the discrepancy and how the bias scales as numbers approach infinity. [[4]](https://golem.ph.utexas.edu/category/2016/03/unexpected_biases_in_the_distr.html)
5. **arXiv:** *A Peculiarity in the Parity of Primes* (2018) - Research detailing a different bias regarding the odd/even parity of the sum of a prime's digits across various even bases. [[6]](https://arxiv.org/pdf/1812.11841)

---
Learn more:
1. [Mathematicians find a peculiar pattern in primes - Science News](https://www.sciencenews.org/article/mathematicians-find-peculiar-pattern-primes)
2. [Distribution of Primes | Brilliant Math & Science Wiki](https://brilliant.org/wiki/distribution-of-primes/)
3. [Mathematicians Discover Prime Conspiracy - Quanta Magazine](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/)
4. [Weirdness in the Primes | The n-Category Café](https://golem.ph.utexas.edu/category/2016/03/unexpected_biases_in_the_distr.html)
5. [Unexpected biases in the distribution of consecutive primes - PNAS](https://www.pnas.org/doi/10.1073/pnas.1605366113)
6. [A Peculiarity in the Parity of Primes - arXiv.org](https://arxiv.org/pdf/1812.11841)



### Query: # Research Problem: Digit Sequencing and Base-N Distribution Patterns in Prime N recent research findings
Here is a summary of recent research findings regarding digit sequencing and base-N distribution patterns in prime numbers. The studies range from the distribution of leading/ending digits to the behavior of primes when specific digits are omitted in various bases.

### 1. Primes with a Missing Digit in Base-N Expansions
**Research:** *Primes with a missing digit: Distribution in arithmetic progressions and an application in sieve theory* (Nath, 2023–2025) [[1]](https://umontreal.scholaris.ca/bitstreams/3387c6de-3723-4cf5-99b7-6f8c735df2d0/download)[[2]](https://www.researchgate.net/publication/375619707_Primes_with_a_missing_digit_Distribution_in_arithmetic_progressions_and_an_application_in_sieve_theory)
*   **Findings:** This research explores the Fourier structure of integers that have a missing digit in their $b$-adic (base-$b$) expansion. The author proved Bombieri–Vinogradov type theorems for primes with a missing digit in large positive integer bases. By combining the circle method with the semi-linear sieve, the study established the correct order of magnitude for the number of primes of the form $p = 1 + m^2 + n^2$ that omit a specific digit in a large odd base $b$ [[1]](https://umontreal.scholaris.ca/bitstreams/3387c6de-3723-4cf5-99b7-6f8c735df2d0/download)[[2]](https://www.researchgate.net/publication/375619707_Primes_with_a_missing_digit_Distribution_in_arithmetic_progressions_and_an_application_in_sieve_theory). 

### 2. Missing Digits and Sums of Two Prime Squares
**Research:** *Missing digits and sums of two prime squares* (Sabuncu, 2026) [[3]](https://pure.mpg.de/rest/items/item_3690994_1/component/file_3690995/content)
*   **Findings:** Building on the study of sparse sets in sieve theory, this 2026 paper applies the Hardy–Littlewood circle method to investigate integers whose base-$g$ expansion omits a fixed digit and which can be represented as the sum of two prime squares ($n = p^2 + q^2$). The research exploits the strong Fourier decay properties of the indicator function for missing-digit numbers to obtain asymptotic formulas for the weighted count of these representations [[3]](https://pure.mpg.de/rest/items/item_3690994_1/component/file_3690995/content).

### 3. Benford's Law and the Leading Digits of Prime Factors
**Research:** *Benford behavior and distribution in residue classes of large prime factors* (Canadian Mathematical Bulletin, 2023) [[4]](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/benford-behavior-and-distribution-in-residue-classes-of-large-prime-factors/77F6DAF48EA54EF008AC5B8BE19C60B1)
*   **Findings:** While it is known that the leading digits of prime numbers themselves approach a uniform distribution rather than strictly following Benford's Law, this study investigated the leading digit distribution of the $k$-th largest prime factor of an integer $n$, as well as the sum of all prime factors of $n$. The researchers found that in these specific prime-factor sequences, the leading digits *do* strongly distribute according to Benford's law. Furthermore, this Benford behavior emerges simultaneously with equidistribution in arithmetic progressions [[4]](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/benford-behavior-and-distribution-in-residue-classes-of-large-prime-factors/77F6DAF48EA54EF008AC5B8BE19C60B1).

### 4. 2D "Random Walks" Based on Prime Digit Sequencing
**Research:** *The Distribution of Prime Numbers: A Geometrical Perspective* (Fraile & Fernández, 2025) [[5]](https://blog.computationalcomplexity.org/2025/06/the-distribution-of-prime-numbers.html)
*   **Findings:** This computational study mapped the sequence of prime numbers into geometric "random walks" based on digit sequencing. In one of their models, known as the "Prime Walk" (PW), a 2D path is generated by choosing a direction based strictly on the last digit of the next prime number in base 10 (e.g., 1 = down, 3 = up, 7 = right, 9 = left). The study visualizes how the deterministic yet pseudo-random distribution of prime ending-digits creates vast, unpredictable geometric structures (termed "Jacob's Ladders") that oscillate infinitely [[5]](https://blog.computationalcomplexity.org/2025/06/the-distribution-of-prime-numbers.html).

### 5. Distribution of the Units Digit of Primes Across Multiple Bases
**Research:** *Distribution of the units digit of primes* (Ko, Chaos, Solitons & Fractals) [[6]](https://www.researchgate.net/publication/238941476_Distribution_of_the_units_digit_of_primes)
*   **Findings:** This foundational study analyzed the distribution of the units digit of consecutive primes in base 5, base 8, base 10, and base 12 using DNA sequence visualization methods. The research found that while 1-number (single digit) distributions are uniform across relatively prime endings, 2-number distributions (pairs of consecutive primes) show a distinct deficiency in repeated digits (e.g., primes ending in 11, 33, 77 in base 10). The study noted that base 8 exhibited more regularity in its prime digit distribution patterns compared to bases 10 and 12 [[6]](https://www.researchgate.net/publication/238941476_Distribution_of_the_units_digit_of_primes). 

***

**Sources:**
1. Nath, K. (2024/2025). *Primes with a missing digit: Distribution in arithmetic progressions and an application in sieve theory*. Journal of the London Mathematical Society / Université de Montréal [[1]](https://umontreal.scholaris.ca/bitstreams/3387c6de-3723-4cf5-99b7-6f8c735df2d0/download)[[2]](https://www.researchgate.net/publication/375619707_Primes_with_a_missing_digit_Distribution_in_arithmetic_progressions_and_an_application_in_sieve_theory).
2. Sabuncu, C. (2026). *Missing digits and sums of two prime squares*. Max Planck Institute [[3]](https://pure.mpg.de/rest/items/item_3690994_1/component/file_3690995/content).
3. *Benford behavior and distribution in residue classes of large prime factors*. (2023). Canadian Mathematical Bulletin, Cambridge University Press [[4]](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/benford-behavior-and-distribution-in-residue-classes-of-large-prime-factors/77F6DAF48EA54EF008AC5B8BE19C60B1).
4. Fraile, A., & Fernández, D. (2025). *The Distribution of Prime Numbers: A Geometrical Perspective*. Computational Complexity [[5]](https://blog.computationalcomplexity.org/2025/06/the-distribution-of-prime-numbers.html).
5. Ko, C.-M. (2002). *Distribution of the units digit of primes*. Chaos, Solitons and Fractals / ResearchGate [[6]](https://www.researchgate.net/publication/238941476_Distribution_of_the_units_digit_of_primes).

---
Learn more:
1. [Université de Montréal Primes with a missing digit : distribution in arithmetic progressions and sieve-theoretic applications](https://umontreal.scholaris.ca/bitstreams/3387c6de-3723-4cf5-99b7-6f8c735df2d0/download)
2. [Primes with a missing digit: Distribution in arithmetic progressions and an application in sieve theory - ResearchGate](https://www.researchgate.net/publication/375619707_Primes_with_a_missing_digit_Distribution_in_arithmetic_progressions_and_an_application_in_sieve_theory)
3. [Missing digits and sums of two prime squares - MPG.PuRe](https://pure.mpg.de/rest/items/item_3690994_1/component/file_3690995/content)
4. [Benford behavior and distribution in residue classes of large prime factors | Canadian Mathematical Bulletin - Cambridge University Press & Assessment](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/benford-behavior-and-distribution-in-residue-classes-of-large-prime-factors/77F6DAF48EA54EF008AC5B8BE19C60B1)
5. [The Distribution of Prime Numbers: A Geometrical Perspective - Computational Complexity](https://blog.computationalcomplexity.org/2025/06/the-distribution-of-prime-numbers.html)
6. [(PDF) Distribution of the units digit of primes - ResearchGate](https://www.researchgate.net/publication/238941476_Distribution_of_the_units_digit_of_primes)



### Query: # Research Problem: Digit Sequencing and Base-N Distribution Patterns in Prime N computational methods analysis
Here is a summary of research and computational methods related to digit sequencing, distribution patterns, and the generation of prime numbers, based on the search results:

### 1. Prime Numbers from Digit Permutations and Sequencing
Research into digit sequencing often explores the frequency and distribution of primes when manipulating the digits of other integers. For example, computational experiments have been conducted to determine how many permutations of the digits of consecutive positive integers yield prime numbers (even allowing for leading zeros). These problems are often tackled using brute-force computational permutation algorithms (like Python's `itertools`) combined with primality tests (like SymPy's `isprime`). Statistical analysis in these sequences shows that the distribution of primes generated through digit permutations generally aligns with expected probabilistic proportions based on the total number of digits [[1]](https://mathoverflow.net/questions/409074/prime-numbers-made-of-permutations-of-digits-of-consecutive-positive-integers).

### 2. Advanced Sequence and Decomposition Methods
Recent computational approaches have proposed generating prime numbers using sequence and decomposition methods based on co-prime properties. A study implemented in MATLAB demonstrated that new prime numbers can be efficiently generated using the formula $n = (\prod_{i=1}^{m} p_i \cdot k) + V \mod \prod_{i=1}^{m} p_i$, where a number is co-prime with a sequence of $m$ prime numbers. This method focuses on the mathematical definition that any prime number is co-prime with all other prime numbers, forming a basis for generating new prime sequences computationally [[2]](https://www.academia.edu/97930076/Generation_of_Prime_Numbers_from_Advanced_Sequence_and_Decomposition_Methods).

### 3. Elimination of Composites via Sequence Equations
Another computational method for determining prime numbers involves using specific algebraic sequences to directly compute primes by eliminating composites. A 2017 study presented a single equation capable of generating all prime numbers (except 2 and 3) alongside composite numbers not divisible by 2 or 3. By determining the periodicity of the indices of the generated composites, the researchers derived a secondary equation to filter out redundancy. This technique acts as a modern, algorithmic variation of the Sieve of Eratosthenes and has been computationally verified up to one billion, showing strict adherence to the Prime Number Theorem [[3]](https://thescipub.com/pdf/jmssp.2017.177.185.pdf).

### 4. Base Distribution and the Cramer Model
When analyzing the distribution patterns of primes, computational number theory heavily relies on the Prime Number Theorem and the Cramer model. The Cramer model suggests that prime numbers behave like a random sequence with a specific growth constraint, where each number $n$ has a probability of $1/\ln(n)$ of being prime. Computational sieving (such as the Sieve of Eratosthenes, Atkin, or Sundaram) is used to study statistical data on these distributions, including counting primes, finding large gaps between consecutive primes, and analyzing primes of specific base-N forms [[4]](http://numbers.computation.free.fr/Constants/Primes/countingPrimes.html). 

### 5. Large Prime Generation for Cryptography
In applied computational number theory, generating primes with specific bit-lengths (Base-2 distribution) is critical for cryptography (e.g., RSA). Because there is no known formula to deterministically calculate the next prime based on previous ones, computational methods rely on generating random numbers in a target range and testing them using fast probabilistic methods. This usually involves a short round of sieving followed by the Baillie–PSW or Miller–Rabin primality tests, which can efficiently verify massive primes (e.g., 1,024 to 2,048 bits) [[5]](https://en.wikipedia.org/wiki/Generation_of_primes).

***

### Sources
*   ** [[1]](https://mathoverflow.net/questions/409074/prime-numbers-made-of-permutations-of-digits-of-consecutive-positive-integers) MathOverflow:** [Prime numbers made of permutations of digits of consecutive positive integers](https://mathoverflow.net/questions/409074/prime-numbers-made-of-permutations-of-digits-of-consecutive-positive-integers)
*   ** [[5]](https://en.wikipedia.org/wiki/Generation_of_primes) Wikipedia:** [Generation of primes](https://en.wikipedia.org/wiki/Generation_of_primes)
*   ** [[2]](https://www.academia.edu/97930076/Generation_of_Prime_Numbers_from_Advanced_Sequence_and_Decomposition_Methods) Academia.edu:** [Generation of Prime Numbers from Advanced Sequence and Decomposition Methods](https://www.academia.edu/97930076/Generation_of_Prime_Numbers_from_Advanced_Sequence_and_Decomposition_Methods)
*   ** [[4]](http://numbers.computation.free.fr/Constants/Primes/countingPrimes.html) Numbers Computation:** [Counting the number of primes](http://numbers.computation.free.fr/Constants/Primes/countingPrimes.html)
*   ** [[3]](https://thescipub.com/pdf/jmssp.2017.177.185.pdf) Science Publications:** [Sequences for Determination of Prime Numbers by Elimination of Composites](https://thescipub.com/pdf/jmssp.2017.177.185.pdf)

---
Learn more:
1. [Prime numbers made of permutations of digits of consecutive positive integers](https://mathoverflow.net/questions/409074/prime-numbers-made-of-permutations-of-digits-of-consecutive-positive-integers)
2. [(PDF) Generation of Prime Numbers from Advanced Sequence and Decomposition Methods](https://www.academia.edu/97930076/Generation_of_Prime_Numbers_from_Advanced_Sequence_and_Decomposition_Methods)
3. [Sequences for Determination of Prime Numbers by Elimination of Composites - Science Publications](https://thescipub.com/pdf/jmssp.2017.177.185.pdf)
4. [Counting the number of primes](http://numbers.computation.free.fr/Constants/Primes/countingPrimes.html)
5. [Generation of primes - Wikipedia](https://en.wikipedia.org/wiki/Generation_of_primes)


