# Proposed Testable Hypotheses

Based on the research problem, prior findings that direct lexicon injection failed, and the identified need for more sophisticated integration strategies, I propose the following five hypotheses:

---

## Hypothesis 1: Ensemble Separation Will Reverse the MAE Degradation Caused by Direct Lexicon Injection

**Statement:** Independent scoring pipelines (VADER + Technical Lexicon scored separately, then combined) will produce lower MAE than the failed direct-lexicon-injection method, though may not surpass baseline VADER.

**Why It's Testable:**
- This hypothesis makes a directional prediction (MAE_injection > MAE_ensemble ≥ MAE_baseline) that can be directly measured
- The prior finding established that direct injection increased MAE, providing a clear baseline failure point
- We can construct both Pipeline B (weighted average) and Pipeline A (baseline) using identical evaluation corpora and compute MAE for each

**Experiment:**
1. Apply the previously failed direct-injection model to the synthetic technical corpus (replicating run_002 conditions)
2. Apply Pipeline B (static weighted average) with predefined weights (e.g., 0.6 VADER : 0.4 TechLex) to the same corpus
3. Compare MAE across all three using paired t-tests
4. Use the same k-fold cross-validation scheme for consistency

---

## Hypothesis 2: ML Meta-Classification Will Achieve ≥10% MAE Reduction on Negation-Heavy Subsets

**Statement:** The ML meta-classifier (Pipeline C) will significantly improve sentiment detection specifically on documents containing technical negations, achieving at least a 10% MAE reduction compared to baseline VADER on this subset.

**Why It's Testable:**
- The research problem explicitly identifies "technical negations" as a failure mode requiring reversal
- The success criteria specify a 10% MAE reduction threshold with p < 0.05
- We can isolate the negation-heavy subset using the annotation schema (documents flagged for technical negation patterns like "no signal," "not convergent," "failure to initialize")

**Experiment:**
1. Train Pipeline C using logistic regression on VADER metrics (pos, neg, neu, compound) and Technical Lexicon scores as features
2. Evaluate Pipeline C on a held-out negation-heavy test set
3. Compare MAE to baseline VADER evaluated on the same subset
4. Conduct a one-tailed paired t-test (α = 0.05) to verify significance

---

## Hypothesis 3: Learned Feature Weights Will Reveal Domain-Specific Optimal Distributions

**Statement:** The logistic/ridge regression coefficients in Pipeline C will show that the Technical Lexicon receives higher weight for jargon-heavy documents, while VADER's compound score retains higher weight for negation-heavy documents, reflecting complementary strengths.

**Why It's Testable:**
- Model coefficients are directly observable and interpretable
- We can partition the test corpus into jargon-heavy and negation-heavy subsets and examine whether coefficient magnitudes correlate with subset performance
- This builds on Hypothesis 2 by explaining *why* the ML model succeeds

**Experiment:**
1. Train Pipeline C on the full training set
2. Extract learned coefficients (β_VADER_compound, β_VADER_pos, β_TechLex_pos, etc.)
3. Evaluate Pipeline C separately on jargon-heavy vs. negation-heavy subsets
4. Analyze whether higher TechLex coefficient magnitude correlates with better performance on jargon-heavy subset (and vice versa for VADER)
5. Perform correlation analysis between feature importance and subset performance

---

## Hypothesis 4: Cross-Validation Will Demonstrate Generalization, Not Overfitting

**Statement:** Pipeline C will maintain the ≥10% MAE reduction threshold across all k folds during k-fold cross-validation, indicating the model generalizes to unseen technical documents rather than memorizing the training corpus.

**Why It's Testable:**
- This is a direct test of the success criterion requiring consistent MAE reduction across folds
- We can compute fold-specific MAE values and verify that no single fold accounts for the improvement
- Unlike Pipeline A and B, Pipeline C is susceptible to overfitting, making this hypothesis critical for validity

**Experiment:**
1. Implement 5-fold cross-validation on the full technical corpus
2. Train Pipeline C independently on each training fold, evaluate on corresponding test fold
3. Record MAE for each fold
4. Verify: (a) mean MAE across folds meets the 10% reduction threshold, and (b) no fold shows MAE increase compared to baseline
5. Report variance in MAE across folds as a measure of stability

---

## Hypothesis 5: Static Weighted Averaging Will Show Diminishing Returns for Extreme Weight Biases

**Statement:** Among predefined weight combinations for Pipeline B, intermediate weights (0.4–0.6 range for VADER) will minimize MAE, while extreme biases toward either VADER or the Technical Lexicon will degrade performance, indicating that neither source alone is sufficient.

**Why It's Testable:**
- This hypothesis generates specific, falsifiable predictions about weight distribution (U-shaped MAE curve)
- Weight combinations are experimentally manipulable
- Results would inform whether static averaging is viable or if ML is necessary

**Experiment:**
1. Define a grid of weight combinations for Pipeline B (e.g., VADER: {0.2, 0.4, 0.5, 0.6, 0.8})
2. Evaluate MAE for each weight combination on the full corpus
3. Fit a quadratic regression of MAE as a function of VADER weight
4. Test whether the quadratic term is significant (indicating U-shape)
5. Identify the optimal weight region and compare to ML-learned weights

---

## Summary Table

| Hypothesis | Independent Variable | Dependent Variable | Key Comparison |
|-----------|---------------------|---------------------|----------------|
| H1 | Integration method (injection vs. ensemble) | MAE | Pipeline B vs. Failed injection model |
| H2 | Model (Pipeline C vs. Pipeline A) | MAE on negation subset | ≥10% reduction with p < 0.05 |
| H3 | Document subset (jargon vs. negation) | Learned coefficient magnitude | Correlation analysis |
| H4 | Cross-validation fold | MAE per fold | Consistency across all folds |
| H5 | VADER weight (0.2–0.8) | MAE | Quadratic fit vs. linear |

These hypotheses build sequentially on the prior findings, address all three research questions, and remain feasible within the specified constraints (lightweight, interpretable, VADER-retaining).