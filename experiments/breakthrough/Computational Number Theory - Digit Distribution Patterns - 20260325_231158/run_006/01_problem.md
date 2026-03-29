# Research Problem: Disentangling Benford's Law from Primorial Structural Artifacts in Base-210 Prime Digit Distributions

## Objective
Following the experimental finding that high-order primorial bases (Base-210) exhibit a statistically significant but modest deviation from uniformity (KL divergence ~0.141), largely dominated by a massive bias toward the leading digit '1' (~7.5% vs. ~0.5% expected), this research must pivot to address a critical confounding variable. The objective is to isolate and disentangle the 'leading 1' dominance effect. By systematically comparing coprime-residue-filtered digit classes, we aim to determine whether the observed leading digit anomalies are simply a manifestation of Benford's Law generalized to Base-210, or if there are genuine, intrinsic structural artifacts associated with high-order primorial bases.

## Research Questions
1. **Benford vs. Primorial Bias:** To what extent does the leading digit distribution of primes in Base-210 align with a Base-210 generalized Benford's Law distribution, and how much of the observed KL divergence (~0.141) is solely attributable to this Benford effect?
2. **Coprime Residue Uniformity:** Since Base-210 has exactly $\phi(210) = 48$ coprime residues, how does the distribution of leading digits behave when we strictly analyze and compare only these 48 valid coprime starting digits, normalizing for expected frequency?
3. **Secondary Digit Anomalies:** Once the overwhelming 'leading 1' bias is statistically isolated or removed, do any of the remaining 47 coprime residue classes show statistically significant localized biases or clustering that point to true primorial sequence dependencies?

## Methodology
1. **Data Generation:** Generate a robust dataset of primes up to a minimum of $10^8$ to ensure sufficient sample sizes across all 209 possible leading digits in Base-210.
2. **Benford Baseline Construction:** Calculate the theoretical Benford's Law distribution for leading digits in Base-210, adjusting for the specific maximum bounds of the generated prime dataset.
3. **Coprime Filtering:** Filter the leading digit analysis to isolate the 48 coprime residues of Base-210 (since a prime > 210 cannot start with a digit sharing a factor with 210 if it is a 1-digit prime in that base, though for multi-digit primes, this restriction applies strictly to the *trailing* digit. *Correction for analysis:* We will analyze both leading digits normalized against Benford, and trailing/least-significant digits filtered strictly by the 48 coprime residues).
4. **Statistical Testing:** Recompute the KL divergence, Chi-squared statistics, and Cramér's V for the leading digits against the Benford-expected baseline rather than a uniform baseline. 

## Success Criteria
1. **Attribution of Divergence:** A clear statistical breakdown quantifying the percentage of the previously observed 0.141 KL divergence that is explained by Benford's Law versus residual structural bias.
2. **Residue Profiling:** A definitive map of the transition probabilities and frequencies of the 48 coprime residues in the least significant digit, determining if primorial bases force trailing digit biases.
3. **Effect Size Isolation:** Establishment of a new, true effect size (Cramér's V) for prime digit bias in Base-210 once the 'leading 1' Benford artifact is controlled for.

## Constraints
1. **Strict Base Focus:** Analysis must remain constrained to Base-210 for this phase to fully resolve the Benford confounding variable before any scaling to Base-2310 or Base-30030 is attempted.
2. **Domain Adherence:** The study must strictly evaluate positional digit/n-gram distributions of prime numbers, avoiding drift into general number theory regarding primorial gaps unless directly tied to digit representation.
3. **Statistical Rigor:** All expected baselines must account for the logarithmic distribution of primes (Prime Number Theorem) when calculating expected uniform or Benford distributions across arbitrary bounds.