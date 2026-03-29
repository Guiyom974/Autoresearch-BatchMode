
### Query: "Chebyshev bias" "Random Matrix Theory" variance discrepancy "L-function zeros"
Here is a summary of the search results connecting the concepts of Chebyshev's bias, Random Matrix Theory (RMT), variance/discrepancy, and L-function zeros, based on the retrieved academic papers:

### Summary of Findings

The intersection of **Chebyshev's bias**, **Random Matrix Theory (RMT)**, and the distribution of **L-function zeros** is a rich area of analytic number theory that seeks to explain asymmetries in the distribution of primes and the statistical behavior of L-functions. 

1. **Chebyshev's Bias and the Rubinstein-Sarnak Machinery** 
   Chebyshev's bias refers to the phenomenon where primes in certain arithmetic progressions (e.g., quadratic non-residues) appear more frequently than others (e.g., quadratic residues) [[1]](https://arxiv.org/pdf/2001.05428). The foundational framework to study this bias was established by Rubinstein and Sarnak, who linked the limiting distributions of these prime discrepancies to the non-trivial zeros of Dirichlet L-functions [[1]](https://arxiv.org/pdf/2001.05428)[[2]](https://arxiv.org/pdf/1111.3896). Recent research extends this to the Chebotarev density theorem, establishing bounds on the generic fluctuations (variance/discrepancy) of error terms and analyzing asymmetries using representation theory and probabilistic techniques [[1]](https://arxiv.org/pdf/2001.05428).

2. **Random Matrix Theory and L-Function Zeros**
   Random Matrix Theory is heavily utilized to predict the statistical distribution of low-lying zeros in families of L-functions [[2]](https://arxiv.org/pdf/1111.3896)[[3]](https://arxiv.org/pdf/2408.12723). While the "main terms" of these distributions universally align with unitary, symplectic, or orthogonal symmetries, RMT models (such as the L-function Ratios Conjecture) are crucial for capturing the highly complex "lower-order terms" and error terms in their full arithmetic detail [[2]](https://arxiv.org/pdf/1111.3896)[[4]](https://msp.org/ant/2015/9-1/ant-v9-n1-s.pdf). 

3. **Murmurations and Explicit Formulas**
   Recent breakthroughs have used RMT to study "murmurations"—oscillatory patterns in the partial sums of Dirichlet coefficients [[3]](https://arxiv.org/pdf/2408.12723). By using explicit formulas that relate L-function zeros to these partial sums, researchers can input precise zero-distribution estimates derived from RMT (specifically ratios conjectures) to observe and prove murmuration phenomena across various families of L-functions, such as elliptic curves and Dirichlet characters [[3]](https://arxiv.org/pdf/2408.12723).

4. **Variance, Discrepancy, and Rescaling**
   When calculating statistics like the 1-level density of zeros, researchers often apply a global rescaling to the L-function zeros [[2]](https://arxiv.org/pdf/1111.3896)[[4]](https://msp.org/ant/2015/9-1/ant-v9-n1-s.pdf). By studying the variance and higher moments of primes in progressions, mathematicians can circumvent certain linear independence assumptions (like the Grand Riemann Hypothesis or linear independence of zeros) to establish lower bounds on discrepancies [[5]](https://msp.org/ant/2025/19-3/ant-v19-n3-p.pdf).

### Sources

*   ** [[2]](https://arxiv.org/pdf/1111.3896)** *1-Level Density of Dirichlet L-functions* (arXiv:1111.3896). Discusses the 1-level density, the Ratios Conjecture, and the use of RMT to predict lower-order terms of L-function zeros. 
*   ** [[1]](https://arxiv.org/pdf/2001.05428)** *Fine distribution properties of Frobenius elements* (arXiv:2001.05428). Explores Chebyshev's bias philosophy, fluctuations of error terms in the Chebotarev density theorem, and the Rubinstein-Sarnak machinery. 
*   ** [[3]](https://arxiv.org/pdf/2408.12723)** *Murmurations from Random Matrix Theory* (arXiv:2408.12723). Introduces a method for studying murmurations using RMT, ratios conjectures, and explicit formulas relating L-function zeros to Dirichlet coefficients. 
*   ** [[5]](https://msp.org/ant/2025/19-3/ant-v19-n3-p.pdf)** *Algebra & Number Theory vol. 19, no. 3 (2025)*. Mentions linear combinations of L-function zeros, moments of primes in progressions, and RMT. 
*   ** [[4]](https://msp.org/ant/2015/9-1/ant-v9-n1-s.pdf)** *Algebra & Number Theory vol. 9, no. 1 (2015)*. Discusses how RMT models capture lower-order terms for families of L-functions and the global rescaling of L-function zeros.

---
Learn more:
1. [arXiv:2001.05428v2 \[math.NT\] 24 Mar 2022](https://arxiv.org/pdf/2001.05428)
2. [arXiv:1111.3896v3 \[math.NT\] 2 Apr 2014](https://arxiv.org/pdf/1111.3896)
3. [arXiv:2408.12723v3 \[math.NT\] 21 Apr 2025](https://arxiv.org/pdf/2408.12723)
4. [Algebra & Number Theory vol. 9 (2015), no. 1 - MSP](https://msp.org/ant/2015/9-1/ant-v9-n1-s.pdf)
5. [Algebra & Number Theory vol. 19 (2025), no. 3 - MSP](https://msp.org/ant/2025/19-3/ant-v19-n3-p.pdf)



### Query: "prime number race" modulo 210 empirical variance "finite-scale corrections"
Here is a summary of the research regarding the "prime number race" (Shanks–Rényi prime number race), focusing on empirical variance, finite-scale corrections, and specific moduli like 210.

### Summary of Findings

**1. The Shanks–Rényi Prime Number Race and Chebyshev's Bias**
The "prime number race" refers to the comparative study of the number of primes in different arithmetic progressions modulo $q$. Let $\pi(x; q, a)$ denote the number of primes up to $x$ that are congruent to $a \pmod q$. In 1853, Chebyshev noticed a bias: primes congruent to non-squares modulo $q$ tend to appear more frequently than those congruent to squares. Rubinstein and Sarnak later formalized this by defining the logarithmic density $\delta(q; a, b)$, which represents the "probability" that $\pi(x; q, a) > \pi(x; q, b)$ [[1]](http://www-lmpa.univ-littoral.fr/~ldevin/MultidimensionalRace.pdf)[[2]](https://arxiv.org/abs/0912.4908).

**2. Empirical Variance and Finite-Scale Corrections**
To understand the inequities in these races, researchers study the variance $V(q; a, b)$ of the distribution of primes in these residue classes. Originally, this variance was defined as an infinite sum over all nontrivial zeros of Dirichlet $L$-functions. However, breakthrough work by Daniel Fiorilli and Greg Martin established an asymptotic formula that allows this variance to be evaluated exactly as a **finite expression** [[2]](https://arxiv.org/abs/0912.4908). This finite-scale evaluation makes it possible to precisely calculate and compare the densities $\delta(q; a, b)$ as $a$ and $b$ vary, revealing "fine-scale differences" and finite-scale corrections that dictate which races are more biased based on the arithmetic properties of the residue classes [[2]](https://arxiv.org/abs/0912.4908)[[3]](https://personal.math.ubc.ca/~gerg/papers/downloads/ISRPNRAFD.pdf).

**3. Modulo 210 and "Unfair" Races**
When applying these finite-scale corrections to specific moduli, certain moduli exhibit extreme biases. Modulo 210 is specifically highlighted in Fiorilli and Martin's work when cataloging the "most unfair prime number races." Because $210$ is a primorial ($2 \times 3 \times 5 \times 7$), it has many prime factors, which heavily influences the algebraic structure of its residue classes and amplifies the variance differences. The empirical variance calculations allow researchers to rank these highly biased (unfair) races, with modulo 210 featuring prominently in the top 120 most unfair two-way prime number races [[3]](https://personal.math.ubc.ca/~gerg/papers/downloads/ISRPNRAFD.pdf).

**4. Function Field Analogues**
Recent research has extended these finite-scale variance formulas and density calculations to function fields (polynomials over finite fields). Studies show that the exact rate at which the density converges to $1/2$ as the degree of the modulus grows mirrors the number field setting, though with unique exceptions where the Linear Independence (LI) hypothesis fails [[4]](https://www.researchgate.net/publication/355237664_Inequities_in_the_Shanks-Renyi_prime_number_race_over_function_fields)[[5]](https://arxiv.org/abs/2110.06669).

### Sources

*   ** [[6]](https://msp.org/ant/2025/19-4/ant-v19-n4-p.pdf)** Devin, L. (2020). *Limiting properties of the distribution of primes in an arbitrarily large number of residue classes*. [Link](http://www-lmpa.univ-littoral.fr/~ldevin/MultidimensionalRace.pdf)
*   ** [[3]](https://personal.math.ubc.ca/~gerg/papers/downloads/ISRPNRAFD.pdf)** Fiorilli, D., & Martin, G. (2013). *Inequities in the Shanks-Renyi Prime Number Race: An asymptotic formula for the densities*. Journal für die reine und angewandte Mathematik. [arXiv:0912.4908](https://arxiv.org/abs/0912.4908)
*   ** [[1]](http://www-lmpa.univ-littoral.fr/~ldevin/MultidimensionalRace.pdf)** Martin, G., & Fiorilli, D. *Inequities in the Shanks–Rényi prime number race: An asymptotic formula for the variance...* (Drafts/Preprints detailing fine-scale differences and modulo 210). [UBC Preprint](https://personal.math.ubc.ca/~gerg/papers/downloads/ISRPNRAFD.pdf)
*   ** [[7]](https://ir.cwi.nl/pub/14502/14502D.pdf)** Sedrati, Y. (2021). *Inequities in the Shanks-Renyi prime number race over function fields*. [arXiv:2110.06669](https://arxiv.org/abs/2110.06669)
*   ** [[8]](https://www.ems-ph.org/journals/newsletter/pdf/2019-03-111.pdf)** Akbary, A. *Limiting distributions of the classical error terms of prime number theory*. [Link](https://www.cs.uleth.ca/~akbary/limitingdistributionFINALQJM.pdf)

---
Learn more:
1. [limiting properties of the distribution of primes in an arbitrarily large number of residue classes - LMPA](http://www-lmpa.univ-littoral.fr/~ldevin/MultidimensionalRace.pdf)
2. [\[0912.4908\] Inequities in the Shanks-Renyi Prime Number Race: An asymptotic formula for the densities - arXiv](https://arxiv.org/abs/0912.4908)
3. [Inequities in the Shanks–Rényi prime number race: An asymptotic ...](https://personal.math.ubc.ca/~gerg/papers/downloads/ISRPNRAFD.pdf)
4. [Inequities in the Shanks-Renyi prime number race over function fields - ResearchGate](https://www.researchgate.net/publication/355237664_Inequities_in_the_Shanks-Renyi_prime_number_race_over_function_fields)
5. [\[2110.06669\] Inequities in the Shanks-Renyi prime number race over function fields - arXiv](https://arxiv.org/abs/2110.06669)
6. [Algebra & Number Theory vol. 19 (2025), no. 4 - MSP](https://msp.org/ant/2025/19-4/ant-v19-n4-p.pdf)
7. [Average prime-pair counting formula - Centrum Wiskunde & Informatica](https://ir.cwi.nl/pub/14502/14502D.pdf)
8. [OF THE EUROPEAN MATHEMATICAL SOCIETY - EMS Press](https://www.ems-ph.org/journals/newsletter/pdf/2019-03-111.pdf)



### Query: exact computation "Dirichlet L-function zeros" RMT approximation breakdown prime bias
Here is a summary of the search results regarding the exact computation of Dirichlet L-function zeros, their relationship to prime bias (such as Chebyshev's bias), and the limitations or breakdowns of approximations like Random Matrix Theory (RMT):

### 1. Exact Computation of Zeros and Chebyshev's Bias
Research by Rubinstein and Sarnak, as well as Bays and Hudson, heavily relies on the exact computation of the non-trivial zeros of Dirichlet $L$-functions to rigorously quantify "Chebyshev's bias" [[1]](https://www.researchgate.net/publication/220576941_Zeroes_of_Dirichlet_L-functions_and_irregularities_in_the_distribution_of_primes)[[2]](https://www.math.uwaterloo.ca/~mrubinst/publications/163.pdf). Chebyshev originally observed that primes congruent to 3 (mod 4) tend to outnumber those congruent to 1 (mod 4). By assuming the Generalized Riemann Hypothesis (GRH) and the Grand Simplicity Hypothesis (GSH—which posits that the imaginary parts of the zeros are linearly independent over the rationals), Rubinstein and Sarnak computed the exact logarithmic densities of these biases [[2]](https://www.math.uwaterloo.ca/~mrubinst/publications/163.pdf). For example, they found that the bias for primes of the form $4n+3$ over $4n+1$ occurs exactly $99.59\%$ of the time on a logarithmic scale [[2]](https://www.math.uwaterloo.ca/~mrubinst/publications/163.pdf).

### 2. The Role of Low-Lying Zeros
The exact location of the first non-trivial zero of a Dirichlet $L$-function (near the real axis) dictates the severity of the prime bias [[3]](https://www.researchgate.net/publication/249897242_Zeros_of_Dirichlet_L-functions_near_the_Real_Axis_and_Chebyshev's_Bias). For instance, the $L$-function for the modulus $q=163$ has an exceptionally low-lying first zero (imaginary part $\approx 0.2029$), which drastically affects the distribution and creates massive "quasi-periods" in the prime counting functions [[2]](https://www.math.uwaterloo.ca/~mrubinst/publications/163.pdf)[[3]](https://www.researchgate.net/publication/249897242_Zeros_of_Dirichlet_L-functions_near_the_Real_Axis_and_Chebyshev's_Bias). Because of these massive periods, empirical prime counting up to standard computational limits fails to reflect the true theoretical bias, meaning exact zero computation is the *only* way to accurately determine the bias [[2]](https://www.math.uwaterloo.ca/~mrubinst/publications/163.pdf).

### 3. Breakdown of Approximations and RMT
While Random Matrix Theory (RMT) and asymptotic formulas are highly successful at predicting the statistical distribution of high-lying zeros of $L$-functions, they can break down or lack precision when applied to low-lying zeros or specific, small-modulus exact computations. In the context of prime bias, simple asymptotic approximations (like using just the first term of the explicit formula) are poor predictors because the exact linear combinations of the lowest zeros dictate the sign changes in the prime counting differences [[2]](https://www.math.uwaterloo.ca/~mrubinst/publications/163.pdf). To achieve high accuracy for the bias, researchers must compute thousands of zeros exactly rather than relying on statistical RMT models [[2]](https://www.math.uwaterloo.ca/~mrubinst/publications/163.pdf). 

### 4. Algorithmic Advances in Exact Computation
Recent computational advancements have drastically improved the ability to calculate these values. Algorithms utilizing the approximate functional equation and asymptotically fast computations of the incomplete gamma function have reduced the bit complexity of computing Dirichlet $L$-functions to $p^{3/2+o(1)}$ (where $p$ is the bit accuracy) [[4]](https://arxiv.org/abs/2110.10583). This allows for the rapid, high-precision isolation of zeros necessary to resolve the exact regions where prime biases flip (axis-crossing regions), such as the Skewes-type numbers where $\pi(x; 4,1) > \pi(x; 4,3)$ [[1]](https://www.researchgate.net/publication/220576941_Zeroes_of_Dirichlet_L-functions_and_irregularities_in_the_distribution_of_primes)[[4]](https://arxiv.org/abs/2110.10583).

### 5. Consecutive Prime Biases
Beyond standard Chebyshev bias, exact computations of prime distributions have been used to study biases between *consecutive* primes (e.g., the Lemke Oliver-Soundararajan phenomenon) [[5]](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/). While RMT and the Hardy-Littlewood prime tuples conjecture provide a heuristic framework for these consecutive biases, exact computations are required to map out the secondary terms and the exact scale at which these asymptotic approximations break down or smooth out over specific intervals [[5]](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/).

**Sources:**
*   [[1]](https://www.researchgate.net/publication/220576941_Zeroes_of_Dirichlet_L-functions_and_irregularities_in_the_distribution_of_primes) Bays & Hudson: *Zeroes of Dirichlet L-functions and irregularities in the distribution of primes*
*   [[2]](https://www.math.uwaterloo.ca/~mrubinst/publications/163.pdf) Rubinstein & Sarnak: *Zeros of Dirichlet L-functions near the Real Axis and Chebyshev's Bias* 
*   [[3]](https://www.researchgate.net/publication/249897242_Zeros_of_Dirichlet_L-functions_near_the_Real_Axis_and_Chebyshev's_Bias) Alderson et al.: *Integral Moments of Quadratic Dirichlet L-functions: A Computational Perspective*
*   [[4]](https://arxiv.org/abs/2110.10583) arXiv:2110.10583: *Rapid computation of special values of Dirichlet L-functions*
*   [[5]](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/) Terence Tao: *Biases between consecutive primes*

---
Learn more:
1. [Zeroes of Dirichlet $L$-functions and irregularities in the distribution of primes](https://www.researchgate.net/publication/220576941_Zeroes_of_Dirichlet_L-functions_and_irregularities_in_the_distribution_of_primes)
2. [Zeros of Dirichlet L-functions near the Real Axis and Chebyshev's Bias](https://www.math.uwaterloo.ca/~mrubinst/publications/163.pdf)
3. [Zeros of Dirichlet L-functions near the Real Axis and Chebyshev's Bias - ResearchGate](https://www.researchgate.net/publication/249897242_Zeros_of_Dirichlet_L-functions_near_the_Real_Axis_and_Chebyshev's_Bias)
4. [\[2110.10583\] Rapid computation of special values of Dirichlet $L$-functions - arXiv](https://arxiv.org/abs/2110.10583)
5. [Biases between consecutive primes | What's new - Terence Tao - WordPress.com](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/)


