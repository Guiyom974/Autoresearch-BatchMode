
### Query: "prime race" modulo 210 quadratic residue non-residue
## Quadratic Residues and Non-Residues Modulo 210

The concept of quadratic residues and non-residues is fundamental in number theory, with applications in cryptography and primality testing. When considering these properties modulo a composite number like 210, the behavior becomes more complex than modulo a prime. The "prime race" refers to the distribution of primes within arithmetic progressions, a concept related to the Chebotarev Density Theorem.

### Quadratic Residues Modulo n

An integer 'a' is a quadratic residue modulo 'n' if the congruence $x^2 \equiv a \pmod{n}$ has a solution. If no such solution exists, 'a' is a quadratic non-residue modulo 'n' [[1]](https://en.wikipedia.org/wiki/Quadratic_residue)[[2]](https://brilliant.org/wiki/quadratic-residues/). For a prime modulus 'p', there are exactly $(p-1)/2$ quadratic residues and $(p-1)/2$ quadratic non-residues among the non-zero integers [[3]](https://www.math.uci.edu/~ndonalds/math180a/7quadres.pdf)[[4]](https://gyu.people.wm.edu/Fall2016/Math412/nt-lec17-note.pdf).

### Modulo 210

The number 210 is a composite number, specifically $210 = 2 \times 3 \times 5 \times 7$. When dealing with composite moduli, the properties of quadratic residues are determined by their properties modulo the prime power factors of the modulus, combined using the Chinese Remainder Theorem [[1]](https://en.wikipedia.org/wiki/Quadratic_residue).

The distribution of quadratic residues and non-residues modulo composite numbers can be intricate. For instance, modulo 15 (which is $3 \times 5$), there are $(3-1)/2 = 1$ invertible quadratic residue modulo 3 and $(5-1)/2 = 2$ invertible quadratic residues modulo 5. This leads to $1 \times 2 = 2$ invertible quadratic residues modulo 15 [[5]](https://arminstraub.com/downloads/teaching/numbertheory-fall18/lecture20.pdf).

### Prime Race and Chebotarev Density Theorem

The "prime race" describes how primes are distributed among different congruence classes. The Chebotarev Density Theorem provides a framework for understanding this distribution. It states that the density of prime ideals that split in a certain way in a Galois extension of number fields is uniform across conjugacy classes in the Galois group [[6]](https://en.wikipedia.org/wiki/Chebotarev_density_theorem)[[7]](https://mathtube.org/lecture/video/explicit-results-about-primes-chebotarevs-density-theorem). This theorem has implications for the distribution of primes in arithmetic progressions, which is a more specific case.

While the direct connection between "prime race" and quadratic residues modulo 210 is not explicitly detailed in the provided search results, the underlying principles of number theory, such as the distribution of primes and the behavior of congruences, are relevant. The Chebotarev Density Theorem suggests that various patterns in number theory, including those related to quadratic residues, tend to be equidistributed in a statistical sense [[6]](https://en.wikipedia.org/wiki/Chebotarev_density_theorem)[[8]](https://math.stackexchange.com/questions/4643758/chebotarevs-density-theorem-equidistribution-of-prime-ideals-and-class-field).

The study of quadratic residues and non-residues modulo composite numbers, especially those with multiple small prime factors like 210, involves understanding how these properties combine from their behavior modulo each prime factor. The "prime race" concept, in a broader sense, touches upon the predictable yet complex distribution of prime numbers, which underpins many number-theoretic properties, including quadratic residuosity.

---
Learn more:
1. [Quadratic residue - Wikipedia](https://en.wikipedia.org/wiki/Quadratic_residue)
2. [Quadratic Residues | Brilliant Math & Science Wiki](https://brilliant.org/wiki/quadratic-residues/)
3. [7 Quadratic Residues - UCI Mathematics](https://www.math.uci.edu/~ndonalds/math180a/7quadres.pdf)
4. [Math 412: Number Theory Lecture 16 quadratic residues and nonresidues - Gexin Yu](https://gyu.people.wm.edu/Fall2016/Math412/nt-lec17-note.pdf)
5. [Sketch of Lecture 20 - 17 Quadratic residues - Armin Straub](https://arminstraub.com/downloads/teaching/numbertheory-fall18/lecture20.pdf)
6. [Chebotarev density theorem - Wikipedia](https://en.wikipedia.org/wiki/Chebotarev_density_theorem)
7. [Explicit results about primes in Chebotarev's density theorem - mathtube.org](https://mathtube.org/lecture/video/explicit-results-about-primes-chebotarevs-density-theorem)
8. [Chebotarev's Density Theorem, Equidistribution of Prime Ideals, and Class-Field Theory](https://math.stackexchange.com/questions/4643758/chebotarevs-density-theorem-equidistribution-of-prime-ideals-and-class-field)



### Query: "prime race" pi(x; 210, 11) vs pi(x; 210, 1)
The user is asking to compare the distribution of prime numbers in two arithmetic progressions:
*   $\pi(x; 210, 11)$: the number of primes less than or equal to $x$ that are congruent to 11 modulo 210.
*   $\pi(x; 210, 1)$: the number of primes less than or equal to $x$ that are congruent to 1 modulo 210.

This comparison falls under the topic of "prime number races," which studies how primes are distributed among different congruence classes.

Here's a summary of the relevant information:

### Prime Number Races and Chebyshev's Bias

The study of how primes are distributed among different arithmetic progressions is known as "prime number races" [[1]](https://www.math.ubc.ca/~gerg/teaching/613-Winter2011/PrimeNumberRaces.pdf)[[2]](https://arxiv.org/abs/math/0408319). A key phenomenon in this area is "Chebyshev's bias," which observes that for certain moduli, one congruence class tends to have more primes than another, even though Dirichlet's theorem on arithmetic progressions states that primes are asymptotically evenly distributed among all valid congruence classes [[3]](https://en.wikipedia.org/wiki/Chebyshev%27s_bias)[[4]](https://math101.guru/en/problems-2/chebyshevs-bias/).

*   **Dirichlet's Theorem on Arithmetic Progressions**: This theorem guarantees that for any two coprime integers $a$ and $d$, there are infinitely many primes of the form $a + nd$, where $n$ is a positive integer. It also implies that these primes are asymptotically evenly distributed among the $\phi(d)$ possible congruence classes modulo $d$ [[5]](https://kskedlaya.org/ant/chap-primes-in-ap.html)[[6]](https://math.uchicago.edu/~may/REU2012/REUPapers/LiAng.pdf). This means that, in the long run, the number of primes in each valid class should be roughly equal.

*   **Chebyshev's Bias**: Despite the asymptotic even distribution, in initial intervals, one congruence class often "leads" in the race for primes. The most famous example is the comparison between primes of the form $4k+1$ and $4k+3$, where primes of the form $4k+3$ tend to be more numerous [[3]](https://en.wikipedia.org/wiki/Chebyshev%27s_bias)[[4]](https://math101.guru/en/problems-2/chebyshevs-bias/). This bias is not fully understood and is related to the distribution of zeros of Dirichlet L-functions, often requiring assumptions like the Generalized Riemann Hypothesis for rigorous proofs [[4]](https://math101.guru/en/problems-2/chebyshevs-bias/)[[7]](https://projecteuclid.org/journals/experimental-mathematics/volume-3/issue-3/Chebyshevs-bias/em/1048515870.pdf).

### The Specific Case: $\pi(x; 210, 11)$ vs. $\pi(x; 210, 1)$

The comparison between $\pi(x; 210, 11)$ and $\pi(x; 210, 1)$ is a specific instance of a prime number race.

*   **Modulus 210**: The modulus $q=210$ is $2 \times 3 \times 5 \times 7$. The number of reduced residue classes modulo 210 is given by Euler's totient function, $\phi(210) = \phi(2)\phi(3)\phi(5)\phi(7) = (2-1)(3-1)(5-1)(7-1) = 1 \times 2 \times 4 \times 6 = 48$. This means there are 48 congruence classes modulo 210 that contain infinitely many primes [[5]](https://kskedlaya.org/ant/chap-primes-in-ap.html)[[7]](https://projecteuclid.org/journals/experimental-mathematics/volume-3/issue-3/Chebyshevs-bias/em/1048515870.pdf).

*   **Residue Classes 11 and 1**: Both 11 and 1 are coprime to 210, so both $\pi(x; 210, 11)$ and $\pi(x; 210, 1)$ represent counts of primes in valid arithmetic progressions.

*   **The "Race"**: The question of which of these two functions, $\pi(x; 210, 11)$ or $\pi(x; 210, 1)$, is larger for a given $x$ is a "prime number race" [[1]](https://www.math.ubc.ca/~gerg/teaching/613-Winter2011/PrimeNumberRaces.pdf)[[2]](https://arxiv.org/abs/math/0408319). While asymptotically they should be roughly equal, there might be initial intervals where one consistently outperforms the other. The specific behavior of this race (i.e., which class "wins" more often or for longer stretches) depends on subtle properties of the distribution of primes, often related to the Generalized Riemann Hypothesis [[7]](https://projecteuclid.org/journals/experimental-mathematics/volume-3/issue-3/Chebyshevs-bias/em/1048515870.pdf).

*   **Generalization**: The phenomenon of Chebyshev's bias can be generalized to other moduli beyond 4. For any modulus $q$, one can compare primes in different residue classes. The question of which class "wins" can be complex and may depend on whether the residue classes correspond to quadratic residues or non-residues, among other factors [[3]](https://en.wikipedia.org/wiki/Chebyshev%27s_bias)[[7]](https://projecteuclid.org/journals/experimental-mathematics/volume-3/issue-3/Chebyshevs-bias/em/1048515870.pdf).

In summary, the comparison between $\pi(x; 210, 11)$ and $\pi(x; 210, 1)$ is about which of these two arithmetic progressions contains more primes up to a certain value $x$. While Dirichlet's theorem suggests they should be roughly equal in the long run, Chebyshev's bias indicates that there can be significant and persistent differences in initial segments, making it a subject of ongoing study in number theory.

---
Learn more:
1. [Prime Number Races - UBC Math](https://www.math.ubc.ca/~gerg/teaching/613-Winter2011/PrimeNumberRaces.pdf)
2. [\[math/0408319\] Prime Number Races - arXiv](https://arxiv.org/abs/math/0408319)
3. [Chebyshev's bias - Wikipedia](https://en.wikipedia.org/wiki/Chebyshev%27s_bias)
4. [Chebyshev's Bias - THE GREAT MYSTERIES OF MATH](https://math101.guru/en/problems-2/chebyshevs-bias/)
5. [Chapter 4 Primes in arithmetic progressions - Kiran Kedlaya](https://kskedlaya.org/ant/chap-primes-in-ap.html)
6. [Dirichlet's theorem about primes in arithmetic progressions](https://math.uchicago.edu/~may/REU2012/REUPapers/LiAng.pdf)
7. [Chebyshev's Bias - Project Euclid](https://projecteuclid.org/journals/experimental-mathematics/volume-3/issue-3/Chebyshevs-bias/em/1048515870.pdf)



### Query: computational prime race modulo 210 prime number theorem bias
The "prime race" is a phenomenon observed in the distribution of prime numbers, where primes in different residue classes modulo a given number do not appear with equal frequency over certain ranges, despite the Prime Number Theorem for Arithmetic Progressions stating they are asymptotically equally distributed. This bias is often referred to as Chebyshev's bias.

Here's a summary of key points regarding computational prime race, modulo 210, and the prime number theorem bias:

*   **Chebyshev's Bias (Prime Race):** This bias suggests that primes are not uniformly distributed among residue classes. For example, there tend to be more primes of the form 4n+3 than 4n+1 up to a certain number. This phenomenon extends to other moduli and residue classes [[1]](https://www.researchgate.net/publication/322843741_Prime_Number_Races)[[2]](https://www.reddit.com/r/math/comments/l2gcer/a_nonbias_in_primes/). The "race" refers to comparing the counts of primes in different residue classes as you go further into the number line [[1]](https://www.researchgate.net/publication/322843741_Prime_Number_Races)[[3]](https://www.dms.umontreal.ca/~andrew/PDF/PrimeRace.pdf).

*   **Modulo 210:** The number 210 is significant because it's the product of the first four primes (2, 3, 5, 7). Using modulo 210 in computations, such as with the Ulam spiral, helps in analyzing the distribution of primes by filtering out multiples of these small primes, thus increasing the density of primes being examined [[4]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)[[5]](https://primorial-sieve.com/_Ulam%20spiral%20modulo%20210.pdf). The squares of primes greater than 7 modulo 210 can result in specific values like 1, 79, 109, 121, 151, or 169 [[6]](https://www.reddit.com/r/math/comments/1zbj55/what_do_you_guys_know_about_racing_prime_numbers/).

*   **Prime Number Theorem Bias:** While the Prime Number Theorem describes the overall asymptotic distribution of primes, it doesn't preclude biases in smaller scales or specific subsets of primes. For instance, primes don't end in 1, 3, 7, or 9 with perfect uniformity; there's a tendency for primes to avoid ending in the same digit as the previous prime [[7]](https://en.wikipedia.org/wiki/Prime_number_theorem)[[8]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/). This bias is also observed in the distribution of primes modulo 10, where primes ending in 3 or 7 are slightly more common than those ending in 1 or 9 [[7]](https://en.wikipedia.org/wiki/Prime_number_theorem).

*   **Computational Aspects:** Researchers use computational methods to study these biases, often involving large numbers of primes. This includes analyzing the "race" between primes in different residue classes and observing patterns in their distribution [[1]](https://www.researchgate.net/publication/322843741_Prime_Number_Races)[[9]](https://www.semanticscholar.org/paper/Extreme-biases-in-prime-number-races-with-many-Ford-Harper/4bd56da1beef45ac7301eba8fe78275318b7c592). The proofs for these biases often involve analyzing auxiliary races that are simpler than the full n-way race and employing Gaussian approximation theorems [[9]](https://www.semanticscholar.org/paper/Extreme-biases-in-prime-number-races-with-many-Ford-Harper/4bd56da1beef45ac7301eba8fe78275318b7c592)[[10]](https://arxiv.org/abs/1711.08539).

*   **"Prime Conspiracy" and Memory:** The observed biases have led some to describe a "prime conspiracy," suggesting primes have a form of "memory" where their distribution is not entirely random. For example, primes seem to "hate" repeating their last digit immediately [[4]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)[[8]](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/). This "repulsion" effect has been observed across different bases [[4]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/).

*   **Mathematical Framework:** The study of prime races and biases often relies on advanced conjectures like the Generalized Riemann Hypothesis (GRH) and the Linear Independence (LI) of logarithms of primes [[1]](https://www.researchgate.net/publication/322843741_Prime_Number_Races)[[9]](https://www.semanticscholar.org/paper/Extreme-biases-in-prime-number-races-with-many-Ford-Harper/4bd56da1beef45ac7301eba8fe78275318b7c592). The analysis frequently involves the Riemann zeta function and its related functions, as these encode information about prime distribution [[2]](https://www.reddit.com/r/math/comments/l2gcer/a_nonbias_in_primes/).

---
Learn more:
1. [Prime Number Races - ResearchGate](https://www.researchgate.net/publication/322843741_Prime_Number_Races)
2. [A (non)-Bias in Primes : r/math - Reddit](https://www.reddit.com/r/math/comments/l2gcer/a_nonbias_in_primes/)
3. [Prime Number Races - Département de mathématiques et statistique](https://www.dms.umontreal.ca/~andrew/PDF/PrimeRace.pdf)
4. [\[OC\] Do Prime Numbers have "memory"? I analyzed the first 37 Billion primes (up to 1 Trillion) to visualize the bias in their last digits : r/dataisbeautiful - Reddit](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)
5. [The Ulam spiral functions (mod 210). - Primorial-sieve.com](https://primorial-sieve.com/_Ulam%20spiral%20modulo%20210.pdf)
6. [What do you guys know about RACING Prime Numbers? : r/math - Reddit](https://www.reddit.com/r/math/comments/1zbj55/what_do_you_guys_know_about_racing_prime_numbers/)
7. [Prime number theorem - Wikipedia](https://en.wikipedia.org/wiki/Prime_number_theorem)
8. [Mathematicians Discover Prime Conspiracy - Quanta Magazine](https://www.quantamagazine.org/mathematicians-discover-prime-conspiracy-20160313/)
9. [\[PDF\] Extreme biases in prime number races with many contestants - Semantic Scholar](https://www.semanticscholar.org/paper/Extreme-biases-in-prime-number-races-with-many-Ford-Harper/4bd56da1beef45ac7301eba8fe78275318b7c592)
10. [\[1711.08539\] Extreme biases in prime number races with many contestants - arXiv.org](https://arxiv.org/abs/1711.08539)


