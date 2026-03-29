
### Query: "n-gram" OR "higher-order" digit sequence distribution prime numbers
Here is a summary of the top results regarding the distribution of "n-gram" or "higher-order" digit sequences and gaps in prime numbers. The intersection of these terms spans statistical mathematics, physics, and machine learning.

### 1. Statistical Distributions of Higher-Order Prime Gaps
Research into the statistical mechanics of prime numbers frequently examines **higher-order gaps** (denoted as $\delta^i P_n$). A study by Lattanzi on the statistical distributions of prime number gaps analyzes massive datasets of primes (up to 50 million). The research models the finite differences between consecutive primes (1st-order gaps) and extends this to $i$-th order gaps using binomial coefficients. The study finds that these higher-order gap distributions can be best-fitted by pseudo-Voigt or exp-exp differential distribution functions, revealing unexpected inner cluster structures linked to the nature of primes [[1]](https://en.wikipedia.org/wiki/Prime_number_theorem).

### 2. Power Laws and Last-Digit Sequence Biases (N-grams)
While Dirichlet's theorem states that primes ending in 1, 3, 7, and 9 are equally distributed asymptotically, recent statistical physics research has found non-random biases in their immediate sequences (effectively 2-grams or n-grams of prime last digits). A paper published in *Scirp* discusses how a prime ending in 1 is less likely to be followed by another prime ending in 1. For example, primes ending in 3 or 7 follow a 1 about 30% of the time, while a 9 follows a 1 only 22% of the time. These transition frequencies (digit n-grams) exhibit power-law behaviors and periodic oscillations, providing empirical support for the Hardy-Littlewood $k$-tuple conjecture before randomness takes over at infinity [[2]](https://dms.umontreal.ca/~koukoulo/documents/publications/primes.pdf).

### 3. Hidden Multiscale "Higher-Order" Order (Hyperuniformity)
A major breakthrough by Princeton University researchers (Torquato et al.) discovered that the distribution of prime numbers exhibits patterns similar to the positions of atoms in crystal-like materials. Rather than being pseudo-random, prime configurations are "hyperuniform of class II." This means they possess a hidden multiscale, higher-order structure across macroscopic length scales. The primes represent an "effectively limit-periodic point process" resulting in dense Bragg peaks, fundamentally changing how physicists and mathematicians view the higher-order spatial distribution of primes [[3]](http://thales.doa.fmph.uniba.sk/macaj/skola/teoriapoli/primes.pdf).

### 4. Machine Learning and N-gram Analysis on Prime Distribution
In computational and cryptographic research, machine learning techniques are being applied to find structural patterns in primes. Research by M. El Boujnouni explores the distribution of prime numbers using Support Vector Domain Description (SVDD). While traditional n-gram analysis is heavily used by the author for text/byte sequence classification (like spam or malware), similar supervised learning models are applied to the structural sequences of prime numbers to detect non-apparent regularities and patterns that could impact public-key cryptography (like RSA and Elliptic Curve) [[4]](https://www.reddit.com/r/science/comments/9drofi/the_seemingly_random_digits_known_as_prime/).

### 5. LLM Memorization of Prime Number Digit Sequences
In the realm of Natural Language Processing, the concept of "n-grams" applied to prime numbers appears in the study of Large Language Models (LLMs). A 2025 paper on diagnosing memorization in Chain-of-Thought reasoning notes that LLMs often rely on the pretraining frequency of specific digit n-grams rather than actual arithmetic. When models are prompted to generate or expand prime numbers, their output is heavily influenced by the local context of n-gram token frequencies seen in the training data, demonstrating how AI models statistically map the digit sequences of primes [[5]](https://www.cirm-math.fr/ProgWeebly/Renc1595/Abstracts1595.pdf).

***

**Sources:**
*   [[1]](https://en.wikipedia.org/wiki/Prime_number_theorem) Lattanzi, "Statistical Distributions of Prime Number Gaps" - *Journal of Advances in Mathematics and Computer Science* (2024). [Link](https://scispace.com/pdf/statistical-distributions-of-prime-number-gaps-267bnhwi50.pdf)
*   [[2]](https://dms.umontreal.ca/~koukoulo/documents/publications/primes.pdf) "A Power Law Governing Prime Gaps" - *Scientific Research Publishing (Scirp)*. [Link](https://www.scirp.org/journal/paperinformation?paperid=70336)
*   [[3]](http://thales.doa.fmph.uniba.sk/macaj/skola/teoriapoli/primes.pdf) "The seemingly random digits known as prime numbers are not nearly as scattershot as previously thought" - *Princeton University / r/science*. [Link](https://www.reddit.com/r/science/comments/9drofi/the_seemingly_random_digits_known_as_prime/)
*   [[4]](https://www.reddit.com/r/science/comments/9drofi/the_seemingly_random_digits_known_as_prime/) El Boujnouni, M. "A study of prime numbers distribution based on support vector domain description" - *Journal of Information and Optimization Sciences* (2021). [Link](https://www.researchgate.net/scientific-contributions/Mohamed-El-Boujnouni-2059919975)
*   [[5]](https://www.cirm-math.fr/ProgWeebly/Renc1595/Abstracts1595.pdf) "Diagnosing Memorization in Chain-of-Thought Reasoning One Token at a Time" - *arXiv:2508.02037* (2025). [Link](https://arxiv.org/html/2508.02037v1)

---
Learn more:
1. [Prime number theorem - Wikipedia](https://en.wikipedia.org/wiki/Prime_number_theorem)
2. [The Distribution of Prime Numbers](https://dms.umontreal.ca/~koukoulo/documents/publications/primes.pdf)
3. [Prime Numbers](http://thales.doa.fmph.uniba.sk/macaj/skola/teoriapoli/primes.pdf)
4. [The seemingly random digits known as prime numbers are not nearly as scattershot as previously thought. A new analysis by Princeton University researchers has uncovered patterns in primes that are similar to those found in the positions of atoms inside certain crystal-like materials : r/science - Reddit](https://www.reddit.com/r/science/comments/9drofi/the_seemingly_random_digits_known_as_prime/)
5. [Prime Numbers and Automatic Sequences : Determinism and Randomness Nombres premiers et suites automatiques : aléa - CIRM](https://www.cirm-math.fr/ProgWeebly/Renc1595/Abstracts1595.pdf)



### Query: binary representation bit sequence patterns prime numbers "base 2"
Here is a summary of the search results regarding patterns in the binary (base 2) representation of prime numbers:

### 1. Palindromic Primes and Reversible Bit Sequences
A common observation among math enthusiasts is that reversing the binary representation of certain prime numbers often yields another prime number, or the sequence is entirely palindromic [[1]](https://mathoverflow.net/questions/487843/are-there-specific-binary-patterns-characteristic-of-prime-numbers)[[2]](https://www.reddit.com/r/math/comments/578drx/i_believe_ive_found_something_very_interesting/). For example, 13 in binary is `1101`, and reversed it becomes `1011` (which is 11, also prime) [[2]](https://www.reddit.com/r/math/comments/578drx/i_believe_ive_found_something_very_interesting/). 
* **Mersenne and Fermat Primes:** Mersenne primes ($2^p - 1$) are represented in binary as a continuous string of `1`s, making them inherently palindromic [[1]](https://mathoverflow.net/questions/487843/are-there-specific-binary-patterns-characteristic-of-prime-numbers). Fermat primes ($2^{2^n} + 1$) appear as a `1` followed by a sequence of `0`s and ending in a `1`, which is also palindromic [[1]](https://mathoverflow.net/questions/487843/are-there-specific-binary-patterns-characteristic-of-prime-numbers).
* **Statistical Bias:** Mathematicians note that this "reversal" pattern is somewhat expected. Because leading zeros are discarded, every valid reversed binary number must end in a `1` [[2]](https://www.reddit.com/r/math/comments/578drx/i_believe_ive_found_something_very_interesting/). In base 2, any number ending in `1` is odd, which inherently doubles the probability of the resulting number being prime compared to a random integer [[2]](https://www.reddit.com/r/math/comments/578drx/i_believe_ive_found_something_very_interesting/).

### 2. The Ratio of Ones to Zeros
When analyzing the bit sequences of prime numbers, researchers and programmers have questioned the distribution of `1`s and `0`s. Because all primes (except 2) are odd, their binary representations must always end in `1` [[3]](https://math.stackexchange.com/questions/3043070/counting-zeros-and-ones-in-binary-representations-of-prime-numbers)[[4]](https://www.quora.com/How-do-prime-numbers-work-in-binary). Furthermore, a binary number always starts with a `1`. This guarantees at least two `1`s in the binary representation of any odd prime, creating a natural bias toward `1`s over `0`s when looking at the raw digit counts of primes up to a certain limit [[3]](https://math.stackexchange.com/questions/3043070/counting-zeros-and-ones-in-binary-representations-of-prime-numbers). 

### 3. Primality is Base-Independent
While visual bit sequence patterns (like palindromes or square-free sequences) are interesting in base 2, the fundamental property of primality is completely independent of the number base [[4]](https://www.quora.com/How-do-prime-numbers-work-in-binary)[[5]](https://web.williams.edu/Mathematics/sjmiller/public_html/105Sp10/addcomments/Hayes_ThirdBase.htm). A prime number has only two factors (1 and itself), and this mathematical truth remains constant whether the number is written in base 10, base 3, or base 2 [[4]](https://www.quora.com/How-do-prime-numbers-work-in-binary). The patterns we see in binary are largely artifacts of how powers of 2 interact with odd numbers, rather than a secret key to generating primes [[2]](https://www.reddit.com/r/math/comments/578drx/i_believe_ive_found_something_very_interesting/)[[4]](https://www.quora.com/How-do-prime-numbers-work-in-binary).

### Sources
* [[1]](https://mathoverflow.net/questions/487843/are-there-specific-binary-patterns-characteristic-of-prime-numbers) [MathOverflow: Are There Specific Binary Patterns Characteristic of Prime Numbers?](https://mathoverflow.net/questions/487843/are-there-specific-binary-patterns-characteristic-of-prime-numbers)
* [[2]](https://www.reddit.com/r/math/comments/578drx/i_believe_ive_found_something_very_interesting/) [Reddit (r/math): I believe I've found something very interesting with prime numbers...](https://www.reddit.com/r/math/comments/578drx/i_believe_ive_found_something_very_interesting/)
* [[3]](https://math.stackexchange.com/questions/3043070/counting-zeros-and-ones-in-binary-representations-of-prime-numbers) [Math StackExchange: Counting zeros and ones in binary representations of prime numbers](https://mathstackexchange.com/questions/3043070/counting-zeros-and-ones-in-binary-representations-of-prime-numbers)
* [[5]](https://web.williams.edu/Mathematics/sjmiller/public_html/105Sp10/addcomments/Hayes_ThirdBase.htm) [Brian Hayes: Third Base (Williams College Mathematics)](https://web.williams.edu/Mathematics/sjmiller/public_html/105Sp10/addcomments/Hayes_ThirdBase.htm)
* [[4]](https://www.quora.com/How-do-prime-numbers-work-in-binary) [Quora: How do prime numbers work in binary?](https://www.quora.com/How-do-prime-numbers-work-in-binary)

---
Learn more:
1. [Are There Specific Binary Patterns Characteristic of Prime Numbers? \[closed\]](https://mathoverflow.net/questions/487843/are-there-specific-binary-patterns-characteristic-of-prime-numbers)
2. [I believe I've found something very interesting with prime numbers but don't have the mathematical knowledge to provide a proof. Can someone point me in the right direction? : r/math - Reddit](https://www.reddit.com/r/math/comments/578drx/i_believe_ive_found_something_very_interesting/)
3. [Counting zeros and ones in binary representations of prime numbers](https://math.stackexchange.com/questions/3043070/counting-zeros-and-ones-in-binary-representations-of-prime-numbers)
4. [How do prime numbers work in binary? - Quora](https://www.quora.com/How-do-prime-numbers-work-in-binary)
5. [Third Base](https://web.williams.edu/Mathematics/sjmiller/public_html/105Sp10/addcomments/Hayes_ThirdBase.htm)



### Query: statistical biases digit frequencies prime numbers structural constraints
Here is a summary of the search results regarding statistical biases, digit frequencies, prime numbers, and structural constraints, based on the most relevant findings:

### 1. Prime Number "Memory" and Last-Digit Bias
A major mathematical discovery by Lemke Oliver and Soundararajan (2016) revealed a surprising statistical bias in the final digits of prime numbers [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). While primes (greater than 5) must end in 1, 3, 7, or 9, and these endings are equally distributed overall (~25% each), consecutive primes exhibit a "repulsive force" [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). 
* **The Bias:** A prime ending in a specific digit (e.g., 7) is significantly less likely to be followed by another prime ending in that same digit [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). Instead of a 25% chance of repeating, primes "hate" repeating their last digit immediately [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/).
* **Structural Constraints:** This bias is driven by the structural constraints of prime gaps. For a prime ending in 7 to be followed by another prime ending in 7, the gap between them must be a multiple of 10 (e.g., 10, 20, 30) [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). However, a shift to a different ending (e.g., 7 to 9) only requires a gap of 2 [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). Because smaller gaps between primes are statistically more common, changes in the last digit are naturally more frequent than repetitions [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/). Furthermore, the researchers found that this bias is even stronger than what gap distribution alone predicts, pointing to deeper structural constraints in number theory [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/).

### 2. Number Frequencies and Prime Factorization
Research into the psychological and linguistic frequencies of numbers shows that the frequency with which we use specific numbers is heavily influenced by their mathematical structure [[2]](https://pmc.ncbi.nlm.nih.gov/articles/PMC7618399/). 
* **Compositional Constraints:** A study on the compositional nature of number concepts found that a number's frequency in language is elevated if it has a simple decomposition into prime factors [[2]](https://pmc.ncbi.nlm.nih.gov/articles/PMC7618399/). 
* **Statistical Modeling:** When modeling number frequencies, numbers with comparable magnitudes but more complex prime factorizations have significantly lower frequencies in human usage [[2]](https://pmc.ncbi.nlm.nih.gov/articles/PMC7618399/). This demonstrates a psychological and structural bias where the simplicity of a number's prime components dictates its statistical frequency in everyday language [[2]](https://pmc.ncbi.nlm.nih.gov/articles/PMC7618399/).

### 3. Statistical Distributions of Prime Number Gaps
Recent empirical research treats prime number gaps as raw experimental data to understand the structural organization of primes [[3]](https://www.researchgate.net/publication/377853941_Statistical_Distributions_of_Prime_Number_Gaps). 
* **Gap Distributions:** By analyzing the first 37 billion primes (and gaps up to $5 \times 10^7$), researchers have found that the statistical distributions of these gaps can be best-fitted using specific mathematical functions, like the pseudo-Voigt fit function (a convolution of Lorentz and Gauss distributions) [[3]](https://www.researchgate.net/publication/377853941_Statistical_Distributions_of_Prime_Number_Gaps).
* **Inner Structures:** These statistical analyses reveal "inner structures" and clusters within prime gaps, suggesting that the seemingly random distribution of prime numbers is governed by strict, underlying phenomenological constraints [[3]](https://www.researchgate.net/publication/377853941_Statistical_Distributions_of_Prime_Number_Gaps).

### Sources
* ** [[2]](https://pmc.ncbi.nlm.nih.gov/articles/PMC7618399/)** *The compositional nature of number concepts: Insights from number frequencies* (PMC) - [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC7618399/)
* ** [[1]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)** *Do Prime Numbers have "memory"? I analyzed the first 37 Billion primes to visualize the bias in their last digits* (Reddit / r/dataisbeautiful) - [Link](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)
* ** [[3]](https://www.researchgate.net/publication/377853941_Statistical_Distributions_of_Prime_Number_Gaps)** *Statistical Distributions of Prime Number Gaps* (ResearchGate, 2024) - [Link](https://www.researchgate.net/publication/377853941_Statistical_Distributions_of_Prime_Number_Gaps)

---
Learn more:
1. [\[OC\] Do Prime Numbers have "memory"? I analyzed the first 37 Billion primes (up to 1 Trillion) to visualize the bias in their last digits : r/dataisbeautiful - Reddit](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)
2. [The compositional nature of number concepts: Insights from number frequencies - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7618399/)
3. [(PDF) Statistical Distributions of Prime Number Gaps - ResearchGate](https://www.researchgate.net/publication/377853941_Statistical_Distributions_of_Prime_Number_Gaps)


