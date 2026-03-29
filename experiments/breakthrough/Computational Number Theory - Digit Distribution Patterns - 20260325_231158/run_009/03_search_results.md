
### Query: "Benford's law" "prime numbers" primorial base distribution
Here is a summary of the search results regarding the relationship between Benford's law, prime numbers, and the primorial base distribution:

### 1. The Mantissa Distribution of the Primorial Numbers
**Source:** *Acta Arithmetica / ResearchGate* (Massé & Schneider) [[1]](https://www.researchgate.net/publication/266594298_The_mantissa_distribution_of_the_primorial_numbers)
This paper specifically investigates the primorial numbers ($P_n$), which are defined as the product of the first $n$ prime numbers. The authors prove that the sequence of mantissas of primorial numbers is distributed according to Benford's law in any numeration base $b$. They establish this by demonstrating that the values of the first Chebyshev function evaluated at prime numbers are uniformly distributed modulo 1. The paper also provides estimates for the rate of convergence to this distribution.

### 2. Intermediate Prime Factors in Specified Subsets
**Source:** *Nathan McNew et al.* [[2]](https://www.nathanmcnew.com/intermediateprimes.pdf)
This research highlights a fundamental contrast in number theory regarding Benford's law. While the standard sequence of natural numbers and the sequence of prime numbers (in their usual order) **fail** to obey Benford's law under natural asymptotic density, the $n$th primorial sequence strictly obeys it in every base $g \ge 2$. Furthermore, the paper explores how specific prime factors of numbers (such as the $k$-th largest prime factor) also conform to Benford's distribution.

### 3. Distribution of Leading Digits of Numbers
**Source:** *Yukio Ohkubo & Oto Strauch / ResearchGate* [[3]](https://www.researchgate.net/publication/312567082_Distribution_of_Leading_Digits_of_Numbers)
This paper applies the theory of distribution functions of integer sequences to find the relative densities of first digits for sequences that do not traditionally satisfy Benford's law (like the sequence of primes). While standard primes do not follow the law, the authors show that the first digits of prime powers asymptotically converge to a generalized Benford distribution. They also corroborate that the mantissas of primorial numbers follow the standard Benford's law.

### 4. Dirichlet, Sierpiński, and Benford
**Source:** *Paul Pollack* [[4]](https://pollack.uga.edu/DSB.pdf)
Pollack's paper provides a fascinating caveat to the rule that prime numbers do not follow Benford's law. While primes fail the test under *natural* asymptotic density, they **do** obey Benford's law in any base $g$ if one measures their proportion using *Dirichlet density* (or logarithmic density). The paper also shows that prime numbers can obey Benford's law in multiple multiplicatively independent bases simultaneously under this density measure. 

### 5. Why Eight Percent of Benford Sequences Never Converge
**Source:** *arXiv (March 2026)* [[5]](https://arxiv.org/pdf/2603.18243)
While this recent preprint focuses more broadly on multi-digit correlations and convergence rates of Benford sequences $b^n$, it references the foundational mathematics of the "first digit phenomenon" in prime numbers. It categorizes integer bases into convergent and persistent regimes using conditional mutual information, noting that about 8.4% of bases exhibit persistent digit correlations that deviate from perfect equidistribution, which has implications for how sequences (like prime-derived sequences) behave in different bases.

---
Learn more:
1. [The mantissa distribution of the primorial numbers - ResearchGate](https://www.researchgate.net/publication/266594298_The_mantissa_distribution_of_the_primorial_numbers)
2. [INTERMEDIATE PRIME FACTORS IN SPECIFIED SUBSETS 1. Introduction Given a positive integer n, we let p m(n) denote the mth smalles - Nathan McNew](https://www.nathanmcnew.com/intermediateprimes.pdf)
3. [(PDF) Distribution of Leading Digits of Numbers - ResearchGate](https://www.researchgate.net/publication/312567082_Distribution_of_Leading_Digits_of_Numbers)
4. [DIRICHLET, SIERPI´NSKI, AND BENFORD 1. Introduction This note centers around the following charming theorem published by Sierpi - Paul Pollack](https://pollack.uga.edu/DSB.pdf)
5. [Why Eight Percent of Benford Sequences Never Converge - arXiv](https://arxiv.org/pdf/2603.18243)



### Query: "Kullback-Leibler divergence" "Chi-squared" "goodness-of-fit" "Benford's law"
Here is a summary of the search results regarding the use of Kullback-Leibler divergence and Chi-squared tests for evaluating goodness-of-fit to Benford's Law:

### Summary

When analyzing datasets to see if they conform to **Benford's Law** (which predicts the frequency distribution of leading digits in many real-life numerical datasets), researchers and data scientists need mathematical ways to measure the "goodness-of-fit" between the observed data and the expected Benford distribution. Two of the most prominent methods used for this are the **Chi-squared test** and **Kullback-Leibler (KL) divergence**.

1. **Chi-Squared Goodness-of-Fit Test**: This is a traditional statistical test used to determine if there is a significant difference between the expected frequencies (Benford's probabilities) and the observed frequencies in a dataset [[1]](https://blog.caseystella.com/pyspark-openpayments-analysis-part-5.html)[[2]](https://dokumen.pub/benfords-law-theory-and-applications-1nbsped-9780691147611.html). It is widely used in forensic accounting and network security to flag anomalies, though it can sometimes be overly sensitive when applied to massive datasets [[3]](https://www.researchgate.net/publication/349593474_Data_validity_and_statistical_conformity_with_Benford's_Law)[[4]](https://www.mdpi.com/2227-7390/12/15/2299).
2. **Kullback-Leibler (KL) Divergence**: Rooted in information theory, KL divergence (or relative entropy) measures the amount of information lost when the expected Benford distribution is used to approximate the observed data [[1]](https://blog.caseystella.com/pyspark-openpayments-analysis-part-5.html)[[4]](https://www.mdpi.com/2227-7390/12/15/2299). Unlike the Chi-squared test, KL divergence is asymmetric and is highly sensitive to slight, subtle differences between distributions, making it an excellent metric for ranking anomalies or detecting malicious network flows [[4]](https://www.mdpi.com/2227-7390/12/15/2299)[[5]](https://www.scribd.com/document/662278815/Kullback-Leibler-divergence). 

Several studies and practical applications (such as analyzing financial payments or network traffic metadata) compute both metrics side-by-side. The Chi-squared test provides a formal statistical p-value for conformity, while KL divergence provides a continuous ranking metric to sort entities by how strangely they deviate from Benford's Law [[1]](https://blog.caseystella.com/pyspark-openpayments-analysis-part-5.html)[[3]](https://www.researchgate.net/publication/349593474_Data_validity_and_statistical_conformity_with_Benford's_Law).

### Sources

*   ** [[1]](https://blog.caseystella.com/pyspark-openpayments-analysis-part-5.html) Casey Stella's Blog**: *Data Science and Hadoop: Part 5, Benford's Law Analysis*. Discusses ranking financial payment data anomalies by computing both the Kullback-Leibler divergence and Chi-squared goodness-of-fit tests against Benford's Law. ([Link](https://blog.caseystella.com/pyspark-openpayments-analysis-part-5.html))
*   ** [[3]](https://www.researchgate.net/publication/349593474_Data_validity_and_statistical_conformity_with_Benford's_Law) ResearchGate**: *Data validity and statistical conformity with Benford's Law*. Explores using distance metrics, including KL divergence and the Chi-squared statistic, to detect data fraud and anomalies in financial statements and network flows. ([Link](https://www.researchgate.net/publication/349593474_Data_validity_and_statistical_conformity_with_Benford's_Law))
*   ** [[4]](https://www.mdpi.com/2227-7390/12/15/2299) MDPI**: *Unveiling Malicious Network Flows Using Benford's Law*. Details how KL divergence and Chi-squared tests are used to quantify deviations from Benford's Law in network traffic metadata to identify cyber-attacks. ([Link](https://www.mdpi.com/2227-7390/12/15/2299))
*   ** [[5]](https://www.scribd.com/document/662278815/Kullback-Leibler-divergence) Scribd**: *Kullback-Leibler Divergence Overview*. A theoretical overview of KL divergence, noting its application in goodness-of-fit testing alongside the Chi-squared statistic. ([Link](https://www.scribd.com/document/662278815/Kullback-Leibler-divergence))
*   ** [[2]](https://dokumen.pub/benfords-law-theory-and-applications-1nbsped-9780691147611.html) Dokumen.pub**: *Benford's Law: Theory and Applications*. A textbook excerpt that mathematically defines both the Chi-squared goodness-of-fit test and Kullback-Leibler divergence specifically in the context of testing distributions against Benford's Law. ([Link](https://dokumen.pub/benfords-law-theory-and-applications-1nbsped-9780691147611.html))

---
Learn more:
1. [Data Science and Hadoop: Part 5, Benford's Law Analysis ← - Blog - Casey Stella](https://blog.caseystella.com/pyspark-openpayments-analysis-part-5.html)
2. [Benford's Law: Theory and Applications \[1 ed.\] 9780691147611 - DOKUMEN.PUB](https://dokumen.pub/benfords-law-theory-and-applications-1nbsped-9780691147611.html)
3. [Data validity and statistical conformity with Benford's Law | Request PDF - ResearchGate](https://www.researchgate.net/publication/349593474_Data_validity_and_statistical_conformity_with_Benford's_Law)
4. [Unveiling Malicious Network Flows Using Benford's Law - MDPI](https://www.mdpi.com/2227-7390/12/15/2299)
5. [Kullback-Leibler Divergence Overview | PDF | Statistical Theory | Mathematics - Scribd](https://www.scribd.com/document/662278815/Kullback-Leibler-divergence)



### Query: "Base-210" OR "primorial number system" leading digit extraction primes
Here is a summary of the search results regarding "Base-210", the "primorial number system", and their relationship with primes and leading digits:

### 1. The Primorial Number System (Mixed Radix)
The **primorial number system** (or primoradic system) is a mixed-radix numeral system where the place values are based on the sequence of primorials (products of successive primes: 2, 6, 30, 210, 2310, etc.) [[1]](https://voodooguru23.blogspot.com/2021/02/primorial-number-system.html)[[2]](https://oeis.org/wiki/Primorial_numeral_system). In this system, the $i$-th position has a radix equal to the $i$-th prime number, meaning the digits allowed at the place value $p_{i}\#$ range from $0$ to $p_{i+1}-1$ [[2]](https://oeis.org/wiki/Primorial_numeral_system). Because the bases grow quickly, separators like colons are often used to distinguish digits for numbers exceeding $2100$ (which is $10 \times 210$) [[2]](https://oeis.org/wiki/Primorial_numeral_system). 

### 2. Base-210 and Radix Economy
**Base-210** is a specific fixed-radix system (or a specific tier in the primorial system) derived from the fourth primorial ($2 \times 3 \times 5 \times 7 = 210$) [[1]](https://voodooguru23.blogspot.com/2021/02/primorial-number-system.html)[[3]](https://static1.squarespace.com/static/642c4773648f260aef50bc21/t/66413b4dfdf62d2d23319a79/1715551064808/History-of-binaryAndLeibnizMedallion_book.pdf). 
*   **Fractions and Divisibility:** Using a primorial base like 210 is highly efficient for representing fractions. In Base-210, any fraction with a denominator made up of the prime factors 2, 3, 5, or 7 will terminate rather than repeat [[4]](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well). 
*   **Prime Localization:** Primorial bases are excellent for localizing prime numbers. In Base-210, any prime number greater than 7 must end in a digit that is coprime to 210. Out of the 210 possible ending digits, only 48 are coprime to 210, heavily restricting where primes can appear and acting as a built-in "wheel sieve" [[2]](https://oeis.org/wiki/Primorial_numeral_system).

### 3. Leading Digits and Reversible Primes
The choice of a primorial base heavily impacts the extraction of primes and the study of **reversible primes** (primes that remain prime when their digits are reversed) [[5]](https://www.primepuzzles.net/conjectures/conj_054.htm).
*   In a composite base like Base-10, if a prime's leading digit shares a factor with the base (e.g., 2, 4, 5, 6, 8), its reversal will end in that digit, making the reversed number composite. Thus, a large fraction of leading digits are "disallowed" for reversible primes [[5]](https://www.primepuzzles.net/conjectures/conj_054.htm).
*   In highly composite primorial bases like Base-30, Base-210, or Base-2310, the number of disallowed leading digits increases progressively. Consequently, the frequency of reversible primes drops significantly in Base-210 compared to smaller or prime bases [[5]](https://www.primepuzzles.net/conjectures/conj_054.htm).

### 4. Record-Scale Prime Generation (UP2 Method)
Recent computational frameworks, such as the **Universal-Primorial Prime Construction (UP2 Method)**, utilize exponential primorial bases to generate and test extremely large prime candidates [[6]](https://www.researchgate.net/publication/398722276_Universal-Primorial_Prime_Construction_UP_2_Method_A_Primorial-Base_Framework_for_Record-Scale_Prime_Generation_with_a_Universal-Constants_Seed). By embedding a wheel sieve directly into the exponential growth mechanism of a primorial base, the system structurally eliminates divisibility by all small primes up to a certain cutoff (e.g., all primes $\le 97$). This preserves computational tractability at record-scale digit lengths and allows for deterministic prime generation [[6]](https://www.researchgate.net/publication/398722276_Universal-Primorial_Prime_Construction_UP_2_Method_A_Primorial-Base_Framework_for_Record-Scale_Prime_Generation_with_a_Universal-Constants_Seed).

### Sources
*   [[3]](https://static1.squarespace.com/static/642c4773648f260aef50bc21/t/66413b4dfdf62d2d23319a79/1715551064808/History-of-binaryAndLeibnizMedallion_book.pdf) *History of Binary and Other Nondecimal Numeration* (Squarespace PDF)
*   [[1]](https://voodooguru23.blogspot.com/2021/02/primorial-number-system.html) *Primorial Number System* (Mathematical Meanderings)
*   [[6]](https://www.researchgate.net/publication/398722276_Universal-Primorial_Prime_Construction_UP_2_Method_A_Primorial-Base_Framework_for_Record-Scale_Prime_Generation_with_a_Universal-Constants_Seed) *Universal-Primorial Prime Construction (UP2 Method)* (ResearchGate)
*   [[2]](https://oeis.org/wiki/Primorial_numeral_system) *Primorial numeral system* (OEIS Wiki)
*   [[5]](https://www.primepuzzles.net/conjectures/conj_054.htm) *Conjecture 54: Reversible primes conjecture* (PrimePuzzles)
*   [[4]](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well) *Why do humans use base-ten counting systems?* (Quora)

---
Learn more:
1. [Primorial Number System - Mathematical Meanderings](https://voodooguru23.blogspot.com/2021/02/primorial-number-system.html)
2. [Primorial numeral system - OeisWiki](https://oeis.org/wiki/Primorial_numeral_system)
3. [History of Binary and Other Nondecimal Numeration - Squarespace](https://static1.squarespace.com/static/642c4773648f260aef50bc21/t/66413b4dfdf62d2d23319a79/1715551064808/History-of-binaryAndLeibnizMedallion_book.pdf)
4. [Why do humans use base-ten counting systems? Do other animals use base-two (binary)? Is this difference just cultural or biological/evolutionary as well? - Quora](https://www.quora.com/Why-do-humans-use-base-ten-counting-systems-Do-other-animals-use-base-two-binary-Is-this-difference-just-cultural-or-biological-evolutionary-as-well)
5. [Conjecture 54. Reversible primes conjeture](https://www.primepuzzles.net/conjectures/conj_054.htm)
6. [(PDF) Universal-Primorial Prime Construction (UP 2 Method): A Primorial-Base Framework for Record-Scale Prime Generation with a Universal-Constants Seed - ResearchGate](https://www.researchgate.net/publication/398722276_Universal-Primorial_Prime_Construction_UP_2_Method_A_Primorial-Base_Framework_for_Record-Scale_Prime_Generation_with_a_Universal-Constants_Seed)


