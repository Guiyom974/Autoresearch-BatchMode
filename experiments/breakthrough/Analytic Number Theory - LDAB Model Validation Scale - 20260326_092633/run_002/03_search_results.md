
### Query: "Chebyshev bias" AND ("modulo 210" OR "modulo 2310" OR "primorial") prime distribution
Here is a summary of the search results regarding **Chebyshev's bias** and its relationship with **primorials** (such as modulo 210, 2310, etc.) in the context of prime number distribution. 

### 1. Prime After Prime (Bit Player)
This article discusses the irregular distribution of primes and introduces **Chebyshev's bias**—the phenomenon where primes are not perfectly distributed among allowed residue classes (e.g., primes congruent to 3 mod 4 appear slightly more often than 1 mod 4). It connects this to the concept of "jumping champions," which are the most frequent differences between consecutive primes. The sequence of jumping champions (2, 6, 30, 210, 2310...) are exactly the **primorials** (the product of the first $n$ primes). Primorials act as favored intervals between consecutive primes because an interval of a primorial avoids divisibility by all the small primes that make up that primorial [[1]](http://bit-player.org/2016/prime-after-prime/).

### 2. Biases Between Consecutive Primes (Terence Tao's Blog)
Fields Medalist Terence Tao discusses the Lemke Oliver-Soundararajan paper on biases in the last digits of consecutive primes. He explains how the **Chebyshev bias** (a preference towards quadratic non-residues) plays a role in balancing the distribution of primes. Tao explicitly mentions how **primorials** affect prime gaps: if one looks at prime gaps near a jumping champion (a primorial close to $\log n$), it creates a bias because the jumping champion is divisible by all small primes. This biases the prime gaps to favor being divisible by such primes, interacting deeply with the distribution of consecutive primes [[2]](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/).

### 3. Prime Running Functions (Taylor & Francis)
This mathematical paper investigates "prime running races," which are analogous to the prime number races that exhibit Chebyshev's bias. The authors study the differences between the number of primes in different residue classes modulo $d$. To test their probabilistic models and predictions for small moduli, they evaluate the bias by taking $Q$ to be a **large primorial** and comparing the model's predictions against empirical estimates. This highlights the use of primorials as a highly composite bounding tool to measure the asymptotic drift and bias in prime distributions [[3]](https://www.tandfonline.com/doi/full/10.1080/10586458.2020.1786863).

### 4. Chebyshev's Bias and Generalized Riemann Hypothesis (ResearchGate)
This paper explores Chebyshev's bias across various moduli and its equivalence to the Generalized Riemann Hypothesis (GRH). The authors define specific ratios and functions to measure the bias $\delta(x, q)$ and explicitly utilize **primorial numbers** in their definitions and bounds to regularize the counting functions. Primorials are used to filter out small prime factors when analyzing the logarithmic density of the bias across different competing residue classes [[4]](https://www.researchgate.net/publication/51963532_Chebyshev's_bias_and_generalized_Riemann_hypothesis).

### 5. Sign Modules in Secure Arithmetic Circuits (IACR ePrint)
While primarily a cryptography paper, it relies heavily on the analytic number theory of prime distributions. It references **Chebyshev's bias** and the prime counting function $\pi(x; a, b)$ for primes in arithmetic progressions. The paper utilizes **primorials** (denoted as the product of the first $k$ primes) to construct bounds for modular reductions and secure arithmetic black-boxes, showing how the biased distribution of primes modulo primorials can impact the probability of finding effective sign modules in prime fields [[5]](https://eprint.iacr.org/2011/539.pdf).

***

**Sources:**
* [[1]](http://bit-player.org/2016/prime-after-prime/) *Prime After Prime* - Bit Player (http://bit-player.org/2016/prime-after-prime/)
* [[3]](https://www.tandfonline.com/doi/full/10.1080/10586458.2020.1786863) *Prime Running Functions* - Taylor & Francis (https://www.tandfonline.com/doi/full/10.1080/10586458.2020.1786863)
* [[4]](https://www.researchgate.net/publication/51963532_Chebyshev's_bias_and_generalized_Riemann_hypothesis) *Chebyshev's bias and generalized Riemann hypothesis* - ResearchGate (https://www.researchgate.net/publication/51963532)
* [[2]](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/) *Biases between consecutive primes* - Terence Tao (https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/)
* [[5]](https://eprint.iacr.org/2011/539.pdf) *Sign Modules in Secure Arithmetic Circuits* - IACR (https://eprint.iacr.org/2011/539.pdf)

---
Learn more:
1. [Prime After Prime - Bit Player](http://bit-player.org/2016/prime-after-prime/)
2. [Biases between consecutive primes | What's new - Terence Tao - WordPress.com](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/)
3. [Full article: Prime Running Functions - Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/10586458.2020.1786863)
4. [(PDF) Chebyshev's bias and generalized Riemann hypothesis - ResearchGate](https://www.researchgate.net/publication/51963532_Chebyshev's_bias_and_generalized_Riemann_hypothesis)
5. [Sign Modules in Secure Arithmetic Circuits (A Full Version)](https://eprint.iacr.org/2011/539.pdf)



### Query: statistical methods "goodness-of-fit" expected frequencies primes "residue classes"
Here is a summary of the search results discussing the intersection of statistical methods (such as goodness-of-fit and expected frequencies) with number theory concepts like primes and residue classes:

### 1. Fixed Points and Residue Classes Modulo $p$ (arXiv:1403.5548)
This paper explores the distribution of fixed points in modular arithmetic and specific residue classes modulo $p$ [[1]](https://arxiv.org/pdf/1403.5548). The authors use statistical methods to test whether the observed frequencies of certain prime properties match theoretical predictions (such as the binomial distribution) [[1]](https://arxiv.org/pdf/1403.5548). They specifically employ **chi-squared goodness-of-fit tests** to compare the expected frequencies of primes against collected data for six-digit primes, analyzing whether elements of a given order are uniformly distributed across residue classes [[1]](https://arxiv.org/pdf/1403.5548). 
**Source:** [arXiv:1403.5548 [math.NT]](https://arxiv.org/pdf/1403.5548)

### 2. Prime Generation via Polynomials (Preprints.org)
This research analyzes polynomials designed to generate prime numbers and integrates modular arithmetic to ensure the outputs meet specific **residue classes** modulo small primes [[2]](https://www.preprints.org/manuscript/202411.0123). To validate their models, the researchers generate histograms of prime frequencies and perform **goodness-of-fit tests** [[2]](https://www.preprints.org/manuscript/202411.0123). This statistical approach allows them to compare the empirical output distribution of the generated primes with established theoretical prime density models [[2]](https://www.preprints.org/manuscript/202411.0123).
**Source:** [Prime Generation via Polynomials: Analysis and Applications - Preprints.org](https://www.preprints.org/manuscript/202411.0123)

### 3. Predicting Maximal Gaps in Sets of Primes (MDPI)
This paper investigates the distribution of primes and prime $k$-tuples within specific "$H$-allowed" **residue classes** [[3]](https://www.mdpi.com/2227-7390/7/5/400). The authors calculate the **expected frequencies** and average gaps between primes in these classes [[3]](https://www.mdpi.com/2227-7390/7/5/400). To validate their empirical histograms against theoretical distributions (such as the Generalized Extreme Value distribution), they utilize the **Kolmogorov–Smirnov goodness-of-fit statistic**, noting excellent fits (statistics often less than 0.01) for their prime gap models [[3]](https://www.mdpi.com/2227-7390/7/5/400).
**Source:** [Predicting Maximal Gaps in Sets of**Summarizing Each Source**

I'm now going through each result. Result one, arXiv:1403.5548, uses chi-squared tests to compare expected prime frequencies across different residue classes. Result two, from Preprints.org, focuses on polynomial outputs and goodness-of-fit, ensuring outputs fit specific modular conditions. MDPI's paper explores prime gaps with the Kolmogorov-Smirnov test against theoretical distributions within these classes, while Waterloo’s paper discusses primes and modular forms. The final paper highlights goodness of fit regarding empirical and theoretical models.


 Primes - MDPI](https://www.mdpi.com/2227-7390/7/5/400)

### 4. Statistics of Modular Forms with Small Rationality Fields (University of Waterloo)
This working paper discusses "arithmetic statistics," which compares deterministic arithmetic quantities to random variables [[4]](https://www.math.uwaterloo.ca/~a2cowan/statspaper.pdf). The authors highlight the equidistribution of primes among congruence (residue) classes as a foundational example of this [[4]](https://www.math.uwaterloo.ca/~a2cowan/statspaper.pdf). To test their data, they utilize a statistical test that is asymptotically equivalent to **Pearson's $\chi^2$ test for goodness of fit**, allowing them to evaluate whether the observed arithmetic data (like Frobenius conjugacy classes and primes) aligns with expected probabilistic heuristics [[4]](https://www.math.uwaterloo.ca/~a2cowan/statspaper.pdf).
**Source:** [Statistics of Modular Forms - University of Waterloo](https://www.math.uwaterloo.ca/~a2cowan/statspaper.pdf)

### 5. Experimental Insights on Prime Gaps (IntechOpen)
This chapter provides an empirical analysis of prime gaps and the **residue classes** they occupy [[5]](https://www.intechopen.com/online-first/1235016). The authors note a philosophical point regarding statistical methods in number theory: while primes are deterministic and not subject to random sampling, descriptive statistical tools and **goodness-of-fit measures** are still highly valuable [[5]](https://www.intechopen.com/online-first/1235016). These methods are used to measure the degree to which empirical frequencies of prime gaps resemble theoretical or heuristic models, such as Cramér's probabilistic model [[5]](https://www.intechopen.com/online-first/1235016).
**Source:** [Perspective Chapter: Experimental Insights on Prime Gaps - IntechOpen](https://www.intechopen.com/online-first/1235016)

---
Learn more:
1. [arXiv:1403.5548v2 \[math.NT\] 13 Jul 2015](https://arxiv.org/pdf/1403.5548)
2. [Prime Generation via Polynomials: Analysis and Applications\[v1\] - Preprints.org](https://www.preprints.org/manuscript/202411.0123)
3. [Predicting Maximal Gaps in Sets of Primes - MDPI](https://www.mdpi.com/2227-7390/7/5/400)
4. [STATISTICS OF MODULAR FORMS WITH SMALL RATIONALITY FIELDS WORK IN PROGRESS - University of Waterloo](https://www.math.uwaterloo.ca/~a2cowan/statspaper.pdf)
5. [Perspective Chapter: Experimental Insights on Prime Gaps - IntechOpen](https://www.intechopen.com/online-first/1235016)



### Query: "quadratic residue" non-residue Chebyshev bias sparse distribution finite scale
Here is a summary of the search results regarding Chebyshev's bias, quadratic residues, and their distributions, based on the retrieved sources:

### 1. Chebyshev's Bias and Quadratic Non-Residues
Chebyshev's bias refers to the phenomenon where prime numbers exhibit a slight preference for certain congruence classes. Specifically, a randomly selected prime $p$ of a large magnitude $x$ is typically slightly more likely to be a **quadratic non-residue** modulo $q$ than a quadratic residue [[1]](https://ism.uqam.ca/pdf/Hutama.pdf). This bias balances out the fact that squares and higher powers of primes (which are inherently quadratic residues) also contribute to the overall distribution of prime powers [[2]](https://terrytao.wordpress.com/tag/prime-gaps/). The difference in probabilities is relatively small, typically on the order of $O(1/\sqrt{x})$ [[1]](https://ism.uqam.ca/pdf/Hutama.pdf).

### 2. Prime Number Races and Comparative Prime Number Theory
The study of this bias falls under "comparative prime number theory," which examines inequalities between the counting functions of primes in different arithmetic progressions (often called "prime number races") [[3]](https://arxiv.org/pdf/2309.08729). For example, in the modulo 4 race, primes of the form $4n + 3$ (non-residues) hold a significant lead over primes of the form $4n + 1$ (residues) for an overwhelming majority of the time, a bias first observed by Chebyshev in 1853 [[1]](https://ism.uqam.ca/pdf/Hutama.pdf)[[3]](https://arxiv.org/pdf/2309.08729). 

### 3. Limiting Distributions and Finite Scales
To rigorously study these biases, mathematicians look at normalized versions of these prime counting quantities. These are expected to have limiting logarithmic distribution functions—essentially continuous histograms or measures that record the frequencies with which the normalized quantities take values in various intervals [[3]](https://arxiv.org/pdf/2309.08729). When modeling these biases at finite scales, researchers sometimes use random walks (using Legendre symbol values as steps) to visualize the bias and extend the models to other number fields, such as Gaussian primes [[1]](https://ism.uqam.ca/pdf/Hutama.pdf). 

### 4. Extensions to Other Sets (Sums of Two Squares)
Recent research has extended the concept of Chebyshev's bias to other sparse sets of integers. For instance, studies have shown that the set of positive integers that can be written as a sum of two squares is strongly biased *towards* quadratic residues, assuming the Generalized Riemann Hypothesis (GRH) [[3]](https://arxiv.org/pdf/2309.08729). 

### Sources
*   ** [[2]](https://terrytao.wordpress.com/tag/prime-gaps/)** Terence Tao's Blog: *Prime Gaps and Chebyshev Bias* - Discusses the preference of primes towards quadratic non-residues to balance out the contribution of squares.
*   ** [[4]](https://people.math.harvard.edu/~knill/primes/papers/gaussian.pdf)** Oliver Knill (Harvard Mathematics): *Some Experiments in Number Theory* - Touches on the Chebyshev bias, Riemann hypothesis, and quadratic reciprocity in Gaussian primes.
*   ** [[1]](https://ism.uqam.ca/pdf/Hutama.pdf)** Hutama (Institut des sciences mathématiques): *Modeling Chebyshev's Bias in the Gaussian Primes as a Random Walk* - Explains the $4n+3$ vs $4n+1$ prime race and models the non-residue bias using random walks.
*   ** [[3]](https://arxiv.org/pdf/2309.08729)** arXiv:2309.08729 (Annotated Bibliography for Comparative Prime Number Theory) - Details the history of prime number races, logarithmic distributions, and biases in sparse sets like sums of two squares.
*   ** [[5]](https://shoup.net/ntb/ntb-b1.pdf)** Victor Shoup: *A Computational Introduction to Number Theory and Algebra* - Provides foundational mathematical context on finite probability distributions, the Jacobi symbol, and quadratic residues.

---
Learn more:
1. [Modeling Chebyshev's Bias in the Gaussian Primes as a Random Walk - Institut des sciences mathématiques](https://ism.uqam.ca/pdf/Hutama.pdf)
2. [prime gaps | What's new - Terence Tao](https://terrytao.wordpress.com/tag/prime-gaps/)
3. [arXiv:2309.08729v3 \[math.NT\] 11 Dec 2024](https://arxiv.org/pdf/2309.08729)
4. [SOME EXPERIMENTS IN NUMBER THEORY 1. Introduction In this medley of experiments, we pick up some number theoretical themes. Our - Harvard Mathematics Department](https://people.math.harvard.edu/~knill/primes/papers/gaussian.pdf)
5. [A Computational Introduction to Number Theory and Algebra (BETA version 1) - Victor Shoup](https://shoup.net/ntb/ntb-b1.pdf)


