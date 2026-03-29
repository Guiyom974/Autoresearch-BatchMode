
### Query: "prime numbers" "digit transition probabilities
Here is a summary of the search results regarding the transition probabilities of the last digits of prime numbers. This phenomenon, often referred to as "prime number memory" or "modular repulsion," was most notably brought to light by mathematicians Robert Lemke Oliver and Kannan Soundararajan in 2016.

### 1. Modular Repulsion in the Last Digits of Consecutive Primes (ResearchGate, 2026)
A recent computational analysis of the first 100,000 primes explores the "repulsion" effect in the last digits of consecutive primes. While one might expect a uniform 25% chance for a prime (greater than 5) to end in 1, 3, 7, or 9, consecutive primes are significantly less likely to share the same last digit (only about a 14–16% probability). The paper constructs transition matrices for immediate and distant transitions, revealing a "Short-Range Order" where primes exhibit a strong repulsion against repeating their trailing digit. This modular "memory" decays exponentially, returning to long-range randomness within about ten prime intervals [[1]](https://www.researchgate.net/publication/401778400_Modular_Repulsion_in_the_Last_Digits_of_Consecutive_Primes_An_Empirical_Transition_Matrix_Analysis_and_Decay_of_Bias).

### 2. Visualizing Prime Number "Memory" (Reddit `r/dataisbeautiful`, 2025)
An independent data analysis of the first 37 billion primes (up to 1 trillion) visualized the Lemke Oliver & Soundararajan discovery on a massive scale. The creator generated a heatmap of transition probabilities showing a distinct "diagonal repulsion"—meaning primes "hate" repeating their last digit immediately. The analysis also confirmed that while the overall distribution of prime endings is perfectly democratic (~25% for 1, 3, 7, and 9), the *transition* from one prime to the next is highly biased. Furthermore, this repulsion effect was confirmed to be universal across different numerical bases [[2]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/).

### 3. Biases Between Consecutive Primes (Terence Tao's Blog, 2016)
Fields Medalist Terence Tao discussed the original 2016 paper by Lemke Oliver and Soundararajan. Tao explains that the transition probabilities between residue classes of any distance (in any base) show a distinct bias. He notes that this phenomenon is superficially similar to the well-known "Chebyshev bias" (which concerns the reduction of a single prime to a small modulus) but is actually a much stronger bias arising from a completely different mathematical source, deeply connected to the prime tuples conjecture [[3]](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/).

### 4. Hacker News Discussion on the "Unnoticed Property" (2016)
A 2016 Hacker News thread discussing the original discovery highlights how unexpected this property was to the mathematics and computer science communities. Commenters pointed out that the phenomenon is easiest to understand in base 3: since all primes (except 3 itself) must end in either 1 or 2 in base 3, one might expect a 50/50 split. However, a prime ending in 1 is actually more than twice as likely to be followed by a prime ending in 2 than by another prime ending in 1. The thread emphasizes that the primes' last digits "conspire" in every base greater than 2 [[4]](https://news.ycombinator.com/item?id=11282480).

***

**Sources:**
*   [[1]](https://www.researchgate.net/publication/401778400_Modular_Repulsion_in_the_Last_Digits_of_Consecutive_Primes_An_Empirical_Transition_Matrix_Analysis_and_Decay_of_Bias) [Modular Repulsion in the Last Digits of Consecutive Primes: An Empirical Transition Matrix Analysis and Decay of Bias - ResearchGate](https://www.researchgate.net/publication/401778400_Modular_Repulsion_in_the_Last_Digits_of_Consecutive_Primes_An_Empirical_Transition_Matrix_Analysis_and_Decay_of_Bias)
*   [[2]](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/) [[OC] Do Prime Numbers have "memory"? I analyzed the first 37 Billion primes... - Reddit](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)
*   [[3]](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/) [Biases between consecutive primes | What's new - Terence Tao](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/)
*   [[4]](https://news.ycombinator.com/item?id=11282480) [A previously unnoticed property of prime numbers - Hacker News](https://news.ycombinator.com/item?id=11282480)

---
Learn more:
1. [Modular Repulsion in the Last Digits of Consecutive Primes: An Empirical Transition Matrix Analysis and Decay of Bias - ResearchGate](https://www.researchgate.net/publication/401778400_Modular_Repulsion_in_the_Last_Digits_of_Consecutive_Primes_An_Empirical_Transition_Matrix_Analysis_and_Decay_of_Bias)
2. [\[OC\] Do Prime Numbers have "memory"? I analyzed the first 37 Billion primes (up to 1 Trillion) to visualize the bias in their last digits : r/dataisbeautiful - Reddit](https://www.reddit.com/r/dataisbeautiful/comments/1palhp2/oc_do_prime_numbers_have_memory_i_analyzed_the/)
3. [Biases between consecutive primes | What's new - Terence Tao - WordPress.com](https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/)
4. [A previously unnoticed property of prime numbers - Hacker News](https://news.ycombinator.com/item?id=11282480)


