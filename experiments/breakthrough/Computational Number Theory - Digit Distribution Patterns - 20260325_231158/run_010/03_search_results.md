
### Query: "Benford's law" AND "prime numbers" AND "leading digit" theoretical derivation
Here is a summary of the theoretical relationship and derivations connecting Benford's law, prime numbers, and their leading digits, based on mathematical research.

### The Core Conflict: Primes vs. Benford's Law
Benford's law (the first-digit law) states that in many naturally occurring datasets, the leading digit $d$ ($1$ through $9$) appears with a probability of $\log_{10}(1 + 1/d)$ [[1]](https://en.wikipedia.org/wiki/Benford%27s_law). Under this law, the digit 1 appears about 30.1% of the time, while 9 appears only about 4.6% of the time [[1]](https://en.wikipedia.org/wiki/Benford%27s_law). 

When mathematicians first attempted to apply Benford's law to prime numbers, they ran into a theoretical roadblock. If you look at the standard "natural density" of prime numbers (the limit of the proportion of primes up to an integer $N$ as $N \to \infty$), the set of primes with a specific leading digit does not converge to a single probability [[2]](https://t5k.org/notes/faq/BenfordsLaw.html). Instead, the ratio oscillates endlessly as $N$ grows [[2]](https://t5k.org/notes/faq/BenfordsLaw.html). Furthermore, as proven by Persi Diaconis in 1977, if you look at the asymptotic distribution of the first significant digit of primes over increasingly large intervals, it actually approaches **uniformity** (each digit 1-9 tends toward an equal 11.1% probability), meaning primes fundamentally violate the standard Benford's law [[3]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and).

### Theoretical Derivations and Solutions
Despite the failure of natural density, number theorists have successfully derived Benford's law for prime numbers by changing how "density" (the probability of picking a random integer) is mathematically defined:

**1. Logarithmic and Zeta Densities:**
In 1972, R. E. Whitney published a derivation in the *American Mathematical Monthly* proving that if one uses **logarithmic density** instead of natural density, the leading digits of prime numbers perfectly exhibit Benford's law [[4]](https://www.kaggle.com/code/paddykb/distribution-of-first-digit-of-prime-numbers). Shortly after, Enrico Bombieri proved that primes also follow Benford's law under the **Riemann Zeta density** [[4]](https://www.kaggle.com/code/paddykb/distribution-of-first-digit-of-prime-numbers). 

**2. The Cohen-Katz Generalization (1984):**
Daniel Cohen and Talbot Katz generalized these findings in their paper *"Prime Numbers and the First Digit Phenomenon."* They proved theoretically that if you apply *any* "reasonable" density matrix (one that generalizes natural density but satisfies specific intuitive properties, like scale-invariance), the leading digits of the sequence of prime numbers will always follow Benford's law: $\log_{10}(1 + 1/d)$ [[2]](https://t5k.org/notes/faq/BenfordsLaw.html)[[4]](https://www.kaggle.com/code/paddykb/distribution-of-first-digit-of-prime-numbers). 

**3. Generalized Benford's Law for Finite Intervals (2009):**
A modern theoretical derivation by B. Luque and L. Lacasa published in *The Royal Society* (2009) demonstrated that while primes approach uniformity at infinity, any finite interval of primes $[1, N]$ strictly obeys a **Generalized Benford's Law** [[3]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and). They proved that the Prime Number Theorem is directly responsible for this size-dependent pattern. As the interval $N$ grows, a size-dependent parameter $\alpha(N)$ shifts the distribution from a Benford-like logarithmic curve toward a uniform distribution [[3]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and). 

***

### Sources

1. **PrimePages FAQ: "Does Benford's law apply to prime numbers?"** 
   Discusses the oscillation of natural density and the Cohen-Katz (1984) derivation showing that under reasonable alternative densities, primes follow Benford's law. ([Link](https://t5k.org/notes/faq/BenfordsLaw.html)) [[2]](https://t5k.org/notes/faq/BenfordsLaw.html)
2. **The Royal Society: "The first-digit frequencies of prime numbers and Riemann zeta zeros" (2009)** 
   Proves that the leading digits of primes in a finite interval follow a Generalized Benford's Law, driven by the Prime Number Theorem, and asymptotically approach uniformity. ([Link](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)) [[3]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)
3. **Wikipedia: "Benford's law"** 
   Provides the foundational definition of the first-digit law, the $\log_{10}(1 + 1/d)$ formula, and its scale-invariant theoretical derivations. ([Link](https://en.wikipedia.org/wiki/Benford%27s_law)) [[1]](https://en.wikipedia.org/wiki/Benford%27s_law)
4. **Kaggle / American Mathematical Monthly (Whitney, 1972): "Distribution of first digit of prime numbers"** 
   Details the historical derivations by R.E. Whitney and Bombieri proving that primes follow Benford's law under logarithmic and Riemann Zeta densities. ([Link](https://www.kaggle.com/code/paddykb/distribution-of-first-digit-of-prime-numbers)) [[4]](https://www.kaggle.com/code/paddykb/distribution-of-first-digit-of-prime-numbers)
5. **The Prime Glossary: "Benford's law"** 
   Summarizes the theoretical work of Theodore Hill on base-invariance and Cohen's proofs regarding supernatural densities applied to prime integers. ([Link](https://t5k.org/glossary/page.php?sort=BenfordsLaw)) [[5]](https://t5k.org/glossary/page.php?sort=BenfordsLaw)

---
Learn more:
1. [Benford's law - Wikipedia](https://en.wikipedia.org/wiki/Benford%27s_law)
2. [Does Benford's law apply to prime numbers? - PrimePages](https://t5k.org/notes/faq/BenfordsLaw.html)
3. [The first-digit frequencies of prime numbers and Riemann zeta zeros | Proceedings A | The Royal Society](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)
4. [Distribution of first digit of prime numbers - Kaggle](https://www.kaggle.com/code/paddykb/distribution-of-first-digit-of-prime-numbers)
5. [Benford's law - The Prime Glossary](https://t5k.org/glossary/page.php?sort=BenfordsLaw)



### Query: "coprime filtering" OR "primorial" probability distribution prime numbers
Here is a summary of the search results regarding the relationship between primorials, coprime filtering, and the probability distribution of prime numbers:

### 1. The Primality of Primorials and Primorial Twin Primes
Research by G. Lillie (2021) investigates "primorial primes," which are prime numbers of the form $p_n\# \pm 1$ (where $p_n\#$ is the primorial, or the product of all primes less than or equal to the $n$-th prime) [[1]](https://www.researchgate.net/publication/355224833_About_the_Primality_of_Primorials)[[2]](https://arxiv.org/pdf/2110.04302). 
* **Probability Distribution:** Using heuristics based on Mertens' Theorem and the Prime Number Theorem, the study shows that the probability of either $p_n\# - 1$ or $p_n\# + 1$ being prime is $O(n^{-1})$ [[1]](https://www.researchgate.net/publication/355224833_About_the_Primality_of_Primorials)[[2]](https://arxiv.org/pdf/2110.04302). 
* **Twin Primes:** The probability that *both* are prime (forming a primorial twin prime pair) is $O(n^{-2})$ [[1]](https://www.researchgate.net/publication/355224833_About_the_Primality_of_Primorials)[[2]](https://arxiv.org/pdf/2110.04302). This statistical distribution provides evidence that there are likely only three instances in total where both $p_n\# - 1$ and $p_n\# + 1$ are prime [[1]](https://www.researchgate.net/publication/355224833_About_the_Primality_of_Primorials)[[2]](https://arxiv.org/pdf/2110.04302). The paper also proves that numbers of the form $p_n\# \pm 1$ have the highest general probability of being prime compared to other integers of similar size [[1]](https://www.researchgate.net/publication/355224833_About_the_Primality_of_Primorials)[[2]](https://arxiv.org/pdf/2110.04302).

### 2. Phi, Primorials, and Poisson Distributions
A paper by Carl Pomerance titled "Phi, Primorials, and Poisson" explores the intersection of Euler's totient function ($\phi(n)$) and primorials [[3]](https://math.dartmouth.edu/~carlp/ppp7.pdf). 
* **Divisibility by Primorials:** The research looks at $pr(n)$, defined as the largest prime $p$ such that its primorial $p\#$ divides $\phi(n)$ [[3]](https://math.dartmouth.edu/~carlp/ppp7.pdf). 
* **Poisson Distribution:** Pomerance demonstrates that the normal order of $pr(n)$ is $\approx \frac{\log \log n}{\log \log \log n}$ [[3]](https://math.dartmouth.edu/~carlp/ppp7.pdf). Furthermore, on a tertiary asymptotic level, the distribution of these largest primes follows an asymptotic Poisson distribution [[3]](https://math.dartmouth.edu/~carlp/ppp7.pdf). The paper uses probabilistic reasoning to show that for any fixed prime $p$, almost every value of $\phi(n)$ is divisible by $p$ because $n$ is highly likely to be divisible by a prime $l \equiv 1 \pmod p$ [[3]](https://math.dartmouth.edu/~carlp/ppp7.pdf).

### 3. Prime Gaps and Remainder Correlations
Analysis of the Riemann Zeta function's zeros and the distribution of prime numbers reveals correlations between the remainders of consecutive primes [[4]](http://www.geocities.ws/oshanker/RiemannZeta/primedistribution.htm). 
* When primes are divided by 6 (yielding remainders of 1 or 5), there is a measurable dependence on the previous prime's remainder [[4]](http://www.geocities.ws/oshanker/RiemannZeta/primedistribution.htm). 
* In the context of prime gaps, heuristic models and numerical analyses suggest that for large numbers, the most likely gap between primes will be a primorial larger than 6 [[4]](http://www.geocities.ws/oshanker/RiemannZeta/primedistribution.htm). 

### 4. Pseudorandom Models of Prime Numbers
Mathematician Terence Tao discusses how primes can be modeled using statistical distributions (like the Poisson-Dirichlet process) [[5]](https://terrytao.wordpress.com/tag/prime-numbers/). 
* While primes are deterministic, their non-multiplicative statistics behave pseudorandomly [[5]](https://terrytao.wordpress.com/tag/prime-numbers/). 
* By using sieve methods (which inherently rely on filtering out multiples of primes, a concept tied to primorials) and replacing actual prime distributions with simplified random models (like the Shifted uniform distribution or Zeta distribution), mathematicians can predict the asymptotic values of various prime statistics and justify difficult conjectures [[5]](https://terrytao.wordpress.com/tag/prime-numbers/).

### Sources
* [[4]](http://www.geocities.ws/oshanker/RiemannZeta/primedistribution.htm) [Distribution of Prime Numbers - Geocities](http://www.geocities.ws/oshanker/RiemannZeta/primedistribution.htm)
* [[3]](https://math.dartmouth.edu/~carlp/ppp7.pdf) [Phi, Primorials, and Poisson - Carl Pomerance, Dartmouth](https://math.dartmouth.edu/~carlp/ppp7.pdf)
* [[1]](https://www.researchgate.net/publication/355224833_About_the_Primality_of_Primorials) [About the Primality of Primorials - ResearchGate](https://www.researchgate.net/publication/355224833_About_the_Primality_of_Primorials)
* [[2]](https://arxiv.org/pdf/2110.04302) [About the Primality of Primorials - arXiv:2110.04302](https://arxiv.org/pdf/2110.04302)
* [[5]](https://terrytao.wordpress.com/tag/prime-numbers/) [Prime Numbers | What's new - Terence Tao](https://terrytao.wordpress.com/tag/prime-numbers/)

---
Learn more:
1. [(PDF) About the Primality of Primorials - ResearchGate](https://www.researchgate.net/publication/355224833_About_the_Primality_of_Primorials)
2. [arXiv:2110.04302v1 \[math.NT\] 10 Oct 2021](https://arxiv.org/pdf/2110.04302)
3. [Phi, Primorials, and Poisson - Mathematics](https://math.dartmouth.edu/~carlp/ppp7.pdf)
4. [Distribution of Prime Numbers](http://www.geocities.ws/oshanker/RiemannZeta/primedistribution.htm)
5. [prime numbers | What's new - Terence Tao](https://terrytao.wordpress.com/tag/prime-numbers/)



### Query: "Base-210" prime number distribution uniform vs Benford model correction
Here is a summary of the search results regarding the distribution of prime numbers, Base-210 (Mod 210) wheel factorization, and the correction between uniform distribution and Benford's Law:

### 1. Prime Number "Memory" and Mod 210 Wheel Factorization
A recent massive-scale data analysis of the first 37 billion primes verified the Lemke Oliver & Soundararajan discovery that prime numbers have "memory" (they actively avoid repeating their last digits). To compute this efficiently, the author used a **Mod 210 (Base-210)** wheel factorization. Because 210 is the product of the first four primes ($2 \times 3 \times 5 \times 7$), working in Base-210 instantly filters out 77% of non-prime numbers. While the overall distribution of ending digits is strictly uniform (25% for 1, 3, 7, and 9 in base-10), the *transitions* between them are highly non-uniform. Commenters frequently questioned if this bias was related to Benford's Law [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/).

### 2. Primes Follow a "Generalized" Benford's Law (GBL)
According to a study published by The Royal Society, prime numbers do not strictly follow the standard Benford's Law (which predicts a heavy bias toward the leading digit 1). Instead, as proven by Diaconis in 1977, the first digits of primes are asymptotically **uniformly distributed**. However, researchers Luque and Lacasa discovered that finite sequences of primes follow a *Generalized Benford's Law (GBL)*. This model acts as a mathematical correction: it includes a size-dependent exponent that smoothly converges to a uniform distribution as the sequence approaches infinity [[2]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and).

### 3. The Transition from Benford to Uniformity
A detailed breakdown of Luque and Lacasa's work explains how this correction model functions. Because the average distance between primes increases as numbers get larger (Prime Number Theorem), finite datasets of primes exhibit a Benford-like logarithmic bias. The GBL model corrects for the size of the dataset ($N$). As $N$ grows, the curve flattens out, and the probabilities of leading digits being 1 through 9 equalize, perfectly bridging the gap between Benford's logarithmic model and absolute uniformity [[3]](https://blog.christianperone.com/2009/05/prime-numbers-and-the-benfords-law/).

### 4. Mathematical Proofs against Strict Benford Compliance
Discussions on Mathematics Stack Exchange confirm that applying the Prime Number Theorem to the intervals between $d \times 10^k$ and $(d+1) \times 10^k$ proves that the ratio of primes starting with different digits tends toward 1 as $k$ increases. Therefore, while a standard Benford model applies to many naturally occurring scale-invariant datasets, prime numbers require a corrective framework (like GBL) because their ultimate distribution is uniform [[4]](https://math.stackexchange.com/questions/267164/the-prime-numbers-do-not-satisfies-benfords-law).

### 5. Base-210 (Primorial) and Distribution Assumptions
In broader mathematical discussions, Base-210 is frequently cited because it is a primorial ($p_4\#$). Using Base-210 simplifies the probabilistic distribution of primes by eliminating multiples of 2, 3, 5, and 7. When analyzing random number distributions in these highly composite bases, statisticians note that while uniform distributions are a common theoretical assumption for primes at infinity, real-world finite bounds almost always exhibit Benford-like leading digit biases that must be corrected for accurate probability modeling [[5]](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number)[[6]](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well). 

***

**Sources:**
* [[5]](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number) Quora: Probability of primes and Base-210 distributions [[5]](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number)
* [[7]](https://www.ck12.org/flexi/cbse-math/prime-factorization/what-are-the-prime-factors-of-210/) Reddit (r/dataisbeautiful): *Do Prime Numbers have "memory"?* (Mod 210 Wheel Factorization) [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)
* [[8]](https://numbermatics.com/n/210/) Mathematics Stack Exchange: *The prime numbers do not satisfy Benford's law* [[4]](https://math.stackexchange.com/questions/267164/the-prime-numbers-do-not-satisfies-benfords-law)
* [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/) The Royal Society: *The first-digit frequencies of prime numbers and Riemann zeta zeros* [[2]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)
* [[9]](https://www.cuemath.com/numbers/factors-of-210/) Terra Incognita: *Prime Numbers and the Benford's Law* [[3]](https://blog.christianperone.com/2009/05/prime-numbers-and-the-benfords-law/)

---
Learn more:
1. [\[OC\] Do Prime Numbers have "memory"? I analyzed the first 37 Billion primes (up to 1 Trillion) to visualize the bias in their last digits : r/dataisbeautiful - Reddit](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)
2. [The first-digit frequencies of prime numbers and Riemann zeta zeros | Proceedings A | The Royal Society](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)
3. [Prime Numbers and the Benford's Law | Terra Incognita](https://blog.christianperone.com/2009/05/prime-numbers-and-the-benfords-law/)
4. [The prime numbers do not satisfies Benford's law - Mathematics Stack Exchange](https://math.stackexchange.com/questions/267164/the-prime-numbers-do-not-satisfies-benfords-law)
5. [If a two-digit number is chosen at random, what is the probability that the number chosen is not a prime number? - Quora](https://www.quora.com/If-a-two-digit-number-is-chosen-at-random-what-is-the-probability-that-the-number-chosen-is-not-a-prime-number)
6. [Why do humans use base-ten counting systems? Do other animals use base-two (binary)? Is this difference just cultural or biological/evolutionary as well? - Quora](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well)
7. [What are the prime factors of 210? - Steps | CK-12 Foundation](https://www.ck12.org/flexi/cbse-math/prime-factorization/what-are-the-prime-factors-of-210/)
8. [Number 210 - Curious Math Facts and Interesting Properties - Numbermatics](https://numbermatics.com/n/210/)
9. [Factors of 210 - Cuemath](https://www.cuemath.com/numbers/factors-of-210/)


