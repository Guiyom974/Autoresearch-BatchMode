
### Query: "Benford's Law" prime number digit distribution non-standard bases
Here is a summary of how Benford's Law applies to the digit distribution of prime numbers, including its behavior in non-standard bases, based on the search results:

### 1. Primes and the Standard Benford's Law
Standard Benford's Law predicts that the leading digit $d$ of a number in a dataset occurs with probability $\log_b(1 + 1/d)$, where $b$ is the base. However, the sequence of prime numbers **does not** follow the standard Benford's Law in base 10 or any other integer base $b > 2$ [[1]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)[[2]](https://mathoverflow.net/questions/402905/new-experiments-involving-ramanujan-primes-benfords-law). Because the distribution of primes is governed by the Prime Number Theorem (growing asymptotically as $x/\log x$), they approximate a uniform distribution in their first digit as the interval increases [[1]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)[[2]](https://mathoverflow.net/questions/402905/new-experiments-involving-ramanujan-primes-benfords-law). In base 2, Benford's Law is trivially true for the first digit (since all positive integers start with 1), but primes fail standard Benford tests for subsequent digits [[2]](https://mathoverflow.net/questions/402905/new-experiments-involving-ramanujan-primes-benfords-law)[[3]](https://en.wikipedia.org/wiki/Benford%27s_law).

### 2. The Generalized Benford's Law (GBL) for Primes
In 2009, physicists Bartolo Luque and Lucas Lacasa discovered that while primes fail the standard law, their leading digits follow a **Generalized Benford's Law (GBL)** [[1]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)[[4]](https://blog.christianperone.com/2009/05/prime-numbers-and-the-benfords-law/). 
* The GBL introduces a size-dependent exponent $\alpha$. The probability of a leading digit $d$ becomes proportional to $(d + 1)^{1-\alpha} - d^{1-\alpha}$ [[4]](https://blog.christianperone.com/2009/05/prime-numbers-and-the-benfords-law/). 
* For a given interval $[1, N]$, there is a specific value $\alpha(N) \approx 1/(\log N - 1.1)$ that perfectly describes the first-digit distribution of primes in that interval [[4]](https://blog.christianperone.com/2009/05/prime-numbers-and-the-benfords-law/)[[5]](https://www.gresham.ac.uk/watch-now/benfords-very-strange-law). 
* As $N \to \infty$, $\alpha \to 0$, which mathematically explains why the leading digits of primes slowly drift toward a uniform distribution rather than a standard Benford distribution (where $\alpha = 1$) [[1]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and).

### 3. Behavior in Non-Standard Bases
The failure of the standard Benford's Law for prime numbers is **base-invariant** [[2]](https://mathoverflow.net/questions/402905/new-experiments-involving-ramanujan-primes-benfords-law). For any base $b > 2$, the asymptotic density of primes means there will always be an overrepresentation of numbers starting with $b-1$ compared to what standard Benford's Law predicts [[2]](https://mathoverflow.net/questions/402905/new-experiments-involving-ramanujan-primes-benfords-law). However, the Generalized Benford's Law framework discovered by Luque and Lacasa can be extended to other bases, adjusting the probability bounds and the $\alpha(N)$ parameter to match the logarithmic scaling of the chosen base $b$ [[3]](https://en.wikipedia.org/wiki/Benford%27s_law)[[4]](https://blog.christianperone.com/2009/05/prime-numbers-and-the-benfords-law/). 

### 4. Prime Factors and Exact Benford Behavior
While the sequence of prime numbers itself requires a generalized law, certain prime-related functions *do* strictly obey the standard Benford's Law across all bases. A 2022 paper by Paul Pollack and Akash Singha Roy demonstrated that the $k$-th largest prime factor of an integer $n$, as well as the sum of all prime factors of $n$, strictly follow the standard Benford's Law [[6]](https://pollack.uga.edu/smoothbenford.pdf). Crucially, Pollack proved that this Benford behavior holds true and emerges uniformly **in every base $b \ge 2$** [[6]](https://pollack.uga.edu/smoothbenford.pdf). 

***

### Sources
* ** [[4]](https://blog.christianperone.com/2009/05/prime-numbers-and-the-benfords-law/) Terra Incognita (2009):** *Prime Numbers and the Benford's Law* - Discusses Luque and Lacasa's GBL and programmatic implementations across bases.
* ** [[6]](https://pollack.uga.edu/smoothbenford.pdf) Paul Pollack (2022):** *Benford behavior and distribution in residue classes of large prime factors* - Proves that specific prime factor sequences obey standard Benford's Law in any base $b$.
* ** [[3]](https://en.wikipedia.org/wiki/Benford%27s_law) Wikipedia:** *Benford's Law* - General overview of base-invariance and triviality in base 2.
* ** [[1]](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and) Proceedings of the Royal Society A (2009):** *The first-digit frequencies of prime numbers and Riemann zeta zeros* - The original Luque & Lacasa paper proving the size-dependent GBL for primes.
* ** [[2]](https://mathoverflow.net/questions/402905/new-experiments-involving-ramanujan-primes-benfords-law) MathOverflow (2021):** *New experiments involving Ramanujan primes: Benford's law* - Mathematical breakdown of why prime asymptotic density fails standard Benford's Law for all bases $b > 2$.

---
Learn more:
1. [The first-digit frequencies of prime numbers and Riemann zeta zeros | Proceedings A | The Royal Society](https://royalsocietypublishing.org/rspa/article/465/2107/2197/82851/The-first-digit-frequencies-of-prime-numbers-and)
2. [New experiments involving Ramanujan primes: Benford's law - MathOverflow](https://mathoverflow.net/questions/402905/new-experiments-involving-ramanujan-primes-benfords-law)
3. [Benford's law - Wikipedia](https://en.wikipedia.org/wiki/Benford%27s_law)
4. [Prime Numbers and the Benford's Law | Terra Incognita](https://blog.christianperone.com/2009/05/prime-numbers-and-the-benfords-law/)
5. [Benford's Very Strange Law | Gresham College](https://www.gresham.ac.uk/watch-now/benfords-very-strange-law)
6. [Benford behavior and distribution in residue classes of large prime factors - Paul Pollack](https://pollack.uga.edu/smoothbenford.pdf)



### Query: primorial base structural artifacts prime distribution coprime residue classes
Here is a summary of the concepts surrounding primorial bases, structural artifacts, prime distribution, and coprime residue classes, based on the search results:

### 1. Primorial Numeral Systems and Structural Artifacts
A **primorial numeral system** (or primoradic system) is a mixed-radix numeral system where the place values are based on primorial numbers ($p_i\#$, the product of the first $i$ primes) [[1]](https://oeis.org/wiki/Primorial_numeral_system). In this base, integers are uniquely represented using successive prime numbers as radices [[1]](https://oeis.org/wiki/Primorial_numeral_system). Structural artifacts arise in this system because the base inherently encodes divisibility by the first $k$ primes. For example, any number ending in a zero in a primorial base is divisible by the primes making up that place value's primorial [[1]](https://oeis.org/wiki/Primorial_numeral_system). 

### 2. Coprime Residue Classes Modulo a Primorial
The study of reduced residue systems modulo a primorial ($p_k\#$) is a common approach to understanding prime distribution [[2]](https://math.stackexchange.com/questions/546425/distribution-of-a-reduced-residue-system-within-a-primorial)[[3]](https://mathoverflow.net/questions/203913/are-reduced-residue-systems-relative-primorials-an-active-area-of-research-if-n). 
* **Reduced Residue Systems:** The number of elements in a reduced residue system modulo $p_k\#$ is given by Euler's totient function, $\phi(p_k\#)$ [[2]](https://math.stackexchange.com/questions/546425/distribution-of-a-reduced-residue-system-within-a-primorial). These are the integers strictly less than $p_k\#$ that are coprime to it.
* **Isomorphism to Finite Fields:** By the Chinese Remainder Theorem, the residue class ring $\mathbb{Z}/p\#\mathbb{Z}$ is isomorphic to the product of finite fields $\mathbb{Z}/q\mathbb{Z}$ for all primes $q \le p$ [[3]](https://mathoverflow.net/questions/203913/are-reduced-residue-systems-relative-primorials-an-active-area-of-research-if-n). This means that "global" questions about residue classes modulo a primorial can often be reduced to questions about residue classes modulo individual primes [[3]](https://mathoverflow.net/questions/203913/are-reduced-residue-systems-relative-primorials-an-active-area-of-research-if-n).

### 3. Prime Distribution and Gaps
The distribution of coprime residue classes within a primorial directly impacts our understanding of prime distribution:
* **Local vs. Global Behavior:** While the global product structure of $\mathbb{Z}/p\#\mathbb{Z}$ is well understood, the "local" behavior—how these coprime residues are distributed in small subintervals (like between $p$ and $p^2$)—is highly complex [[3]](https://mathoverflow.net/questions/203913/are-reduced-residue-systems-relative-primorials-an-active-area-of-research-if-n). 
* **Uneven Distribution and the Jacobsthal Function:** The elements of reduced residue systems modulo primorials are not perfectly evenly distributed. The Jacobsthal function demonstrates that the gap between consecutive coprime elements can deviate significantly from the average gap, creating dense clusters and sparse areas of residues [[2]](https://math.stackexchange.com/questions/546425/distribution-of-a-reduced-residue-system-within-a-primorial). 
* **Connection to Major Conjectures:** If these coprime residues were distributed perfectly evenly, major unsolved problems like the Twin Prime Conjecture, De Polignac's Conjecture, and the Hardy-Littlewood $k$-tuple conjecture would be trivial to prove [[2]](https://math.stackexchange.com/questions/546425/distribution-of-a-reduced-residue-system-within-a-primorial). Recent breakthroughs in finding large gaps between primes rely heavily on finding large gaps inside the reduced residue system of a primorial [[3]](https://mathoverflow.net/questions/203913/are-reduced-residue-systems-relative-primorials-an-active-area-of-research-if-n).

### 4. Primorial-Based Primes
Researchers and amateur mathematicians often look for primes of the form $p_m\# \pm k$, where $k$ is an odd number [[4]](https://worldofnumbers.com/primorialprimes.pdf). 
* If $k$ is greater than the $m$-th prime but less than its square, $p_m\# \pm k$ can only be prime if $k$ itself is prime [[4]](https://worldofnumbers.com/primorialprimes.pdf). 
* Because primorials grow incredibly fast (a primorial can easily have over a million digits), searching for primes in these specific coprime residue classes is a targeted way to discover massive prime numbers [[4]](https://worldofnumbers.com/primorialprimes.pdf).

***

### Sources
* ** [[1]](https://oeis.org/wiki/Primorial_numeral_system)** [OEIS Wiki: Primorial numeral system](https://oeis.org/wiki/Primorial_numeral_system)
* ** [[4]](https://worldofnumbers.com/primorialprimes.pdf)** [World of Numbers: Primorial Based Primes (R. A. Bonham)](https://worldofnumbers.com/primorialprimes.pdf)
* ** [[5]](https://www.cp.eng.chula.ac.th/~athasit/2110301-04%20THEORY%20OF%20NUMBER-Distribution%20of%20Prime.pdf)** [Chulalongkorn University: Theory of Numbers - Distribution of Prime](https://www.cp.eng.chula.ac.th/~athasit/2110301-04%20THEORY%20OF%20NUMBER-Distribution%20of%20Prime.pdf)
* ** [[2]](https://math.stackexchange.com/questions/546425/distribution-of-a-reduced-residue-system-within-a-primorial)** [Mathematics Stack Exchange: Distribution of a reduced residue system within a primorial](https://math.stackexchange.com/questions/546425/distribution-of-a-reduced-residue-system-within-a-primorial)
* ** [[3]](https://mathoverflow.net/questions/203913/are-reduced-residue-systems-relative-primorials-an-active-area-of-research-if-n)** [MathOverflow: Are reduced residue systems relative primorials an active area of research?](https://mathoverflow.net/questions/203913/are-reduced-residue-systems-relative-primorials-an-active-area-of-research-if-n)

---
Learn more:
1. [Primorial numeral system - OeisWiki](https://oeis.org/wiki/Primorial_numeral_system)
2. [Distribution of a reduced residue system within a primorial - Mathematics Stack Exchange](https://math.stackexchange.com/questions/546425/distribution-of-a-reduced-residue-system-within-a-primorial)
3. [Are reduced residue systems relative primorials an active area of research? If not, why not?](https://mathoverflow.net/questions/203913/are-reduced-residue-systems-relative-primorials-an-active-area-of-research-if-n)
4. [PRIMORIAL BASED PRIMES R. A. Bonham Abstract   The product of all successive primes starting at Prime\[1\] = 2 and ending at t - World!Of Numbers](https://worldofnumbers.com/primorialprimes.pdf)
5. [distribution of prime numbers](https://www.cp.eng.chula.ac.th/~athasit/2110301-04%20THEORY%20OF%20NUMBER-Distribution%20of%20Prime.pdf)



### Query: Kullback-Leibler divergence leading digit bias confounding variables primes
Based on the search results, there does not appear to be a single prominent study that simultaneously incorporates "Kullback-Leibler divergence," "leading digit bias," "confounding variables," and "primes" into one specific framework. However, these concepts intersect across statistical analysis, fraud detection, and number theory. 

Here is a summary of how these concepts appear in the relevant literature:

### 1. Kullback-Leibler Divergence (KLD)
Kullback-Leibler divergence (or relative entropy) is a fundamental statistical method used to measure how one probability distribution diverges from a second, expected probability distribution [[1]](https://pubmed.ncbi.nlm.nih.gov/21492134/)[[2]](https://www.mdpi.com/1099-4300/24/6/838). In practical applications, such as psychometrics or signal processing, KLD is used to detect heterogeneous data or measure the fit of two distributions [[1]](https://pubmed.ncbi.nlm.nih.gov/21492134/). 

### 2. Leading Digit Bias (Benford's Law)
"Leading digit bias" is most famously described by **Benford's Law**, which dictates that in many naturally occurring, multi-magnitude datasets, the leading digit is not uniformly distributed. Instead, the number 1 appears as the leading digit about 30.1% of the time, with higher digits appearing with logarithmically decreasing frequency [[3]](https://pmc.ncbi.nlm.nih.gov/articles/PMC4331362/). 
* **Application & Confounding Variables:** Benford's Law is heavily used to detect scientific misconduct, accounting fraud, and voter fraud [[3]](https://pmc.ncbi.nlm.nih.gov/articles/PMC4331362/)[[4]](https://pmc.ncbi.nlm.nih.gov/articles/PMC10088595/). However, researchers must account for **confounding variables** or inappropriate datasets. For example, data that is normally distributed, uniformly distributed, or heavily constrained by human intervention (like consumer prices or assigned drug volumes) will naturally violate Benford's Law without it being indicative of fraud [[4]](https://pmc.ncbi.nlm.nih.gov/articles/PMC10088595/). 
* *Note: KLD is frequently used in the literature as a mathematical tool to measure the distance between an observed dataset's digit distribution and the expected Benford distribution.*

### 3. Digit Bias in Primes
While Benford's Law applies to the *leading* digits of many datasets, mathematicians have also discovered unexpected biases in the *last* digits of prime numbers. Recent work by Lemke Oliver and Soundararajan revealed an asymmetry in the distribution of the final digits of consecutive primes. For instance, a prime ending in 1 is much less likely to be followed by another prime ending in 1 than by a prime ending in 3, 7, or 9 [[5]](https://www.researchgate.net/publication/305699784_Explaining_biases_in_last_digit_distributions_of_consecutive_primes). This breaks the previous intuitive assumption that the last digits of consecutive primes would be roughly uniformly distributed among the allowed odd numbers [[5]](https://www.researchgate.net/publication/305699784_Explaining_biases_in_last_digit_distributions_of_consecutive_primes).

### Summary of Sources
* ** [[1]](https://pubmed.ncbi.nlm.nih.gov/21492134/)** Belov, D. I., & Armstrong, R. D. (2011). *Distributions of the Kullback-Leibler divergence with applications.* Discusses the statistical distribution of KLD and its use in detecting heterogeneous response data. 
* ** [[3]](https://pmc.ncbi.nlm.nih.gov/articles/PMC4331362/)** *Benford's Law: Textbook Exercises and Multiple-Choice Testbanks* (2015). Explains the logarithmic trend of leading digits and its application in detecting data tampering. 
* ** [[4]](https://pmc.ncbi.nlm.nih.gov/articles/PMC10088595/)** *Investigating and preventing scientific misconduct using Benford's Law* (2023). Details how to use digit distribution to catch fraud, noting the importance of controlling for dataset types (confounding variables) that do not naturally follow the law. 
* ** [[5]](https://www.researchgate.net/publication/305699784_Explaining_biases_in_last_digit_distributions_of_consecutive_primes)** Lichtblau, D. (2016). *Explaining biases in last digit distributions of consecutive primes.* Explores the mathematical proofs behind the unexpected asymmetry in the final digits of consecutive prime numbers. 
* ** [[2]](https://www.mdpi.com/1099-4300/24/6/838)** *A Generic Formula and Some Special Cases for the Kullback–Leibler Divergence...* (2022). Explores complex mathematical applications of KLD in information theory.

---
Learn more:
1. [Distributions of the Kullback-Leibler divergence with applications - PubMed](https://pubmed.ncbi.nlm.nih.gov/21492134/)
2. [A Generic Formula and Some Special Cases for the Kullback–Leibler Divergence between Central Multivariate Cauchy Distributions - MDPI](https://www.mdpi.com/1099-4300/24/6/838)
3. [Benford's Law: Textbook Exercises and Multiple-Choice Testbanks - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4331362/)
4. [Investigating and preventing scientific misconduct using Benford's Law - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10088595/)
5. [(PDF) Explaining biases in last digit distributions of consecutive primes - ResearchGate](https://www.researchgate.net/publication/305699784_Explaining_biases_in_last_digit_distributions_of_consecutive_primes)


