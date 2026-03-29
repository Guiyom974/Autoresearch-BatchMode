# Research Problem: Statistical Validation and Goodness-of-Fit Analysis of the Primorial-Adjusted Benford Model in Base-210

## Objective
To rigorously compute and evaluate the statistical goodness-of-fit of the newly derived primorial-adjusted Benford model against the empirical leading digit distributions of primes in Base-210. Building upon successful prime generation and coprime digit extraction phases, this iteration focuses on executing the complete statistical pipeline—specifically Kullback-Leibler (KL) divergence and Chi-squared tests—to quantitatively determine whether the primorial adjustment fully resolves the deviations observed in naive Benford and uniform models.

## Research Questions
1. **KL Divergence Comparison:** How does the Kullback-Leibler divergence of the empirical Base-210 leading digit distribution compare when measured against the Primorial-Adjusted Benford model versus the Naive Benford model?
2. **Goodness-of-Fit:** Does the Primorial-Adjusted model yield a statistically significant improvement in goodness-of-fit (via Chi-squared testing) compared to a purely uniform distribution across the 48 coprime digits of Base-210?
3. **Distribution Consistency:** Do the empirical probabilities of the 187,936 analyzed leading digits perfectly align with the expected theoretical probabilities of the 48 valid coprime digits once sample size artifacts are accounted for?

## Methodology
1. **Data Generation & Filtering:** Generate a robust dataset of primes up to $10^7$ (or higher). Strictly filter the dataset to only include primes $p > 210$ to ensure proper leading digit representation.
2. **Base-210 Extraction:** Convert the filtered primes to Base-210 and extract the leading significant digit. 
3. **Coprime Verification:** Verify that the extracted leading digits fall exclusively within the set of the 48 integers coprime to 210 (e.g., 1, 11, 13, 17, ..., 209).
4. **Statistical Testing:** 
   - Construct three theoretical probability distributions for the 48 coprime digits: Naive Benford, Primorial-Adjusted Benford, and Uniform.
   - Compute the empirical probability distribution from the generated primes.
   - Calculate the Kullback-Leibler (KL) divergence and Chi-squared statistics to compare the empirical distribution against all three theoretical models.

## Success Criteria
1. **Complete Statistical Output:** Successful, error-free computation of KL divergence and Chi-squared metrics comparing the empirical data to all three theoretical models.
2. **Quantitative Resolution:** A definitive quantitative ranking of the three models based on their divergence from the empirical prime data, proving or disproving the superiority of the Primorial-Adjusted model.
3. **Data Integrity Verification:** Explicit confirmation that the analyzed subset of primes strictly satisfies $p > 210$ and maps accurately onto the 48 expected coprime digits.

## Constraints
1. **Domain Strictness:** The analysis must remain strictly focused on leading digit distributions of primes in numerical bases, specifically Base-210.
2. **Coprime Exclusivity:** Probability models and statistical tests must only evaluate the 48 coprime digits; non-coprime digits must be structurally excluded from the null models. 
3. **Methodological Rigor:** The KL divergence calculation must strictly adhere to standard information-theoretic definitions, comparing equivalent support sets.