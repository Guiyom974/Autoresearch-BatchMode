# Proposed Testable Hypotheses for VADER Meta-Classifier Validation

Based on the prior findings showing that a meta-classifier ensemble achieved MAE 0.1388 on synthetic data (run_003), and that direct lexicon injection failed to improve performance (run_002), I propose the following hypotheses to guide the real-world validation phase:

---

## Hypothesis 1: Performance Degradation Hypothesis

**Statement:** The meta-classifier will maintain statistically significant superiority over baseline VADER and direct lexicon injection on real-world technical corpora, but will exhibit a measurable performance degradation (higher MAE) compared to synthetic data performance.

**Why it's testable:** This hypothesis directly addresses Research Question 1 by comparing MAE values across conditions (synthetic vs. real-world) and methods (meta-classifier vs. baselines). MAE is a continuous, quantifiable metric that can be statistically compared.

**Experiment:**
1. Acquire a real-world dataset (e.g., Stack Overflow comments with human-annotated sentiment)
2. Generate sentiment scores using: (a) baseline VADER, (b) direct technical lexicon injection, (c) the trained meta-classifier (zero-shot transfer)
3. Calculate MAE for each method on the real-world corpus
4. Conduct a paired t-test comparing meta-classifier MAE to baseline MAE values
5. Calculate the MAE difference (real-world MAE − synthetic MAE of 0.1388) and test whether this degradation is statistically significant using a one-sample t-test against zero

**Expected outcome:** If supported, this hypothesis confirms generalizability while quantifying the domain shift cost.

---

## Hypothesis 2: Linguistic Edge Case Attenuation Hypothesis

**Statement:** The meta-classifier will exhibit systematically higher error rates on real-world sentences containing technical sarcasm, domain-specific idioms, or code mixed with natural language compared to sentences with straightforward technical vocabulary.

**Why it's testable:** This hypothesis addresses Research Question 3 by predicting that specific linguistic structures will drive residual errors. Error rates can be computed across annotated linguistic categories, and differences can be tested for statistical significance.

**Experiment:**
1. Annotate the misclassified sentences (top 10% by absolute error) with linguistic feature labels: (a) technical sarcasm/irony, (b) domain-specific idioms (e.g., "it's not a bug, it's a feature"), (c) mixed code and natural language, (d) elongated Intensifiers (e.g., "sooooo"), (e) negations with technical terms
2. Calculate per-category error rates and compare to baseline error rates using chi-square tests or Fisher's exact tests
3. Perform qualitative analysis to identify dominant failure patterns

**Expected outcome:** A categorized taxonomy of edge cases that systematically bypass the meta-classifier, providing actionable insights for future lexicon refinement.

---

## Hypothesis 3: Method Gap Attenuation Hypothesis

**Statement:** The performance advantage of the meta-classifier over direct lexicon injection will be smaller on real-world corpora than the advantage observed on synthetic data, indicating reduced transferability of the ensemble's learned weighting scheme.

**Why it's testable:** This hypothesis tests whether the meta-classifier's sophisticated weighting mechanism, trained on synthetic data, transfers effectively. The "gap" is a measurable difference that can be statistically compared across datasets.

**Experiment:**
1. Calculate the MAE difference (Δ) between direct injection and meta-classifier on synthetic data (from prior work)
2. Calculate the same Δ on real-world data
3. Use a two-sample t-test or bootstrap confidence interval comparison to test whether Δ_real-world < Δ_synthetic

**Expected outcome:** If supported, this suggests the meta-classifier's optimal weights are partially synthetic-data-specific and may require domain adaptation strategies (without violating constraints on modifying the base lexicon).

---

## Hypothesis 4: Corpus Complexity Interaction Hypothesis

**Statement:** The meta-classifier's MAE will positively correlate with the syntactic complexity (measured by average sentence length, number of clauses, or dependency tree depth) of real-world technical sentences, while baseline VADER will show no significant correlation.

**Why it's testable:** This hypothesis proposes an interaction effect between text complexity and method choice. Complexity metrics can be computed automatically (e.g., using spaCy), and correlation coefficients can be compared across methods using Steiger's test for dependent correlations.

**Experiment:**
1. Compute syntactic complexity metrics for each sentence in the real-world corpus (e.g., number of tokens, parse tree depth, clause count)
2. Split the corpus into complexity quartiles
3. Calculate MAE for meta-classifier and baseline VADER within each quartile
4. Compute Pearson/Spearman correlations between complexity and MAE for each method
5. Test whether the correlation is significantly stronger for the meta-classifier

**Expected outcome:** If supported, this identifies syntactic complexity as a boundary condition for the meta-classifier's advantage, explaining where zero-shot transfer fails.

---

## Hypothesis 5: Error Asymmetry Hypothesis

**Statement:** On real-world technical corpora, the meta-classifier will exhibit directional prediction bias (systematic under- or over-prediction of sentiment valence) that differs from baseline VADER's bias profile, with the meta-classifier showing reduced bias magnitude due to its ensemble averaging.

**Why it's testable:** This hypothesis examines systematic error patterns rather than random noise. Prediction bias can be quantified as mean signed error (MSE, where positive = over-prediction), and bias magnitudes can be compared across methods.

**Experiment:**
1. Calculate signed prediction errors (predicted − actual sentiment) for each sentence
2. Compute mean signed error and 95% confidence intervals for meta-classifier and baseline VADER
3. Conduct a one-sample t-test on signed errors to test whether bias differs from zero
4. Use a paired t-test to compare bias magnitudes between methods

**Expected outcome:** If supported, this identifies systematic directional errors that could be corrected via bias adjustment without retraining.

---

## Summary Table

| Hypothesis | Independent Variable(s) | Dependent Variable | Comparison Point |
|------------|------------------------|-------------------|------------------|
| H1 | Corpus type (synthetic vs. real-world) | MAE | Within meta-classifier |
| H2 | Presence of linguistic edge cases | Error rate | Within real-world corpus |
| H3 | Dataset (synthetic vs. real-world) | Δ (injection MAE − meta MAE) | Across datasets |
| H4 | Syntactic complexity | MAE | Meta-classifier vs. VADER |
| H5 | Method (meta vs. baseline) | Mean signed error | Across methods |

These hypotheses collectively address all three research questions while building directly on the prior findings that established the meta-classifier's synthetic performance (run_003) and the failure of direct injection (run_002).