# Proposed Testable Hypotheses

Based on the research problem, prior findings showing VADER's superiority over simple keyword summation on technical texts, and web search evidence documenting accuracy gains from domain-specific lexicon integration (ranging from 58%→69% to 88.7% in prior studies), I propose the following five hypotheses:

---

## Hypothesis 1: MAE Reduction Through Domain-Specific Lexicon Integration

**Statement:** Integrating a domain-specific technical lexicon with VADER will produce a statistically significant reduction in Mean Absolute Error (MAE) of at least 10% compared to baseline VADER when evaluated on real-world technical corpora.

**Why it's testable:** MAE is a continuous, quantifiable metric that can be directly computed from the difference between predicted sentiment scores and ground-truth annotations. The 10% threshold represents a meaningful, operationally definable improvement benchmark, and statistical significance (p < 0.05) can be assessed using paired t-tests or Wilcoxon signed-rank tests as specified in the methodology.

**Experiment:** 
1. Annotate a held-out test set of real-world technical texts (e.g., 500 Stack Overflow comments) with ground-truth sentiment scores using expert annotators.
2. Run both baseline VADER and the hybrid VADER+technical lexicon model on identical documents.
3. Compute MAE for each model and perform a paired statistical test to determine if the hybrid model's MAE is significantly lower.

---

## Hypothesis 2: Technical Negation Handling Improvements

**Statement:** The hybrid VADER model will correctly classify at least 25% more technical negation constructions (e.g., "not working," "doesn't handle the exception") than baseline VADER, due to the addition of domain-specific negation rules.

**Why it's testable:** Technical negation represents a specific, countable linguistic feature class. Classification outcomes are binary (correct/incorrect), making error rate comparison straightforward. The 25% threshold provides an empirically measurable target.

**Experiment:**
1. Curate a subset of 200 technical texts containing explicit negation constructions from GitHub PR discussions.
2. Code each construction for expected sentiment polarity (ground truth).
3. Compare baseline VADER and hybrid model classification rates on this negation subset.
4. Calculate the proportional improvement in correct classifications.

---

## Hypothesis 3: Domain-Specific Jargon Misclassification Correction

**Statement:** The hybrid model will reduce misinterpretation of domain-specific jargon terms (e.g., classifying "deprecated," "race condition," or "memory leak" as negative sentiment when they function as neutral descriptors) by at least 30% relative to baseline VADER.

**Why it's testable:** Prior findings indicate VADER struggles with technical jargon, and web search results confirm "error" may be misclassified in IT contexts. Jargon misinterpretation is countable and classifiable as a distinct error type, making error rate measurement feasible.

**Experiment:**
1. Identify a lexicon of 50 high-frequency technical jargon terms from the corpus.
2. Extract all sentences containing these terms from the annotated dataset.
3. Measure baseline VADER's misclassification rate for these sentences.
4. Measure hybrid model's misclassification rate for the same sentences.
5. Calculate the percentage reduction in jargon-related errors.

---

## Hypothesis 4: Cross-Domain Generalization (Non-Overfitting)

**Statement:** The hybrid model will maintain accuracy within 5 percentage points of baseline VADER's performance when evaluated on non-technical, general-language text (e.g., movie reviews, social media posts), demonstrating that domain-specific tuning does not cause significant overfitting.

**Why it's testable:** This directly addresses the overfitting concern in Research Question 3. Accuracy is a standard metric applicable across any labeled corpus, and the 5-percentage-point tolerance represents a pre-specified, operationally meaningful boundary for acceptable generalization.

**Experiment:**
1. Obtain a pre-labeled general-language sentiment dataset (e.g., VADER's original validation set or IMDb reviews).
2. Run both baseline VADER and hybrid model on this dataset.
3. Compare accuracy scores; if hybrid model accuracy is within 5 points of baseline, the hypothesis is supported.

---

## Hypothesis 5: Edge-Case Document Recovery Rate

**Statement:** The hybrid model will successfully reclassify at least 20% of edge-case documents that baseline VADER misclassified, where edge-cases are defined as documents containing three or more technical jargon terms or technical negation constructions.

**Why it's testable:** This aligns directly with Success Criterion 3 and operationalizes "edge-case" using document-level feature counts. The 20% threshold matches the specified success criterion, and misclassification/reclassification is binary and countable.

**Experiment:**
1. From the full annotated corpus, identify all documents classified incorrectly by baseline VADER.
2. Filter this set to documents containing ≥3 jargon terms or negation constructions (edge-cases).
3. Run hybrid model on this edge-case subset.
4. Calculate the proportion of edge-cases correctly reclassified by the hybrid model.

---

## Summary Table

| Hypothesis | Focus | Primary Metric | Target Improvement |
|------------|-------|----------------|-------------------|
| H1 | MAE Reduction | Mean Absolute Error | ≥10% reduction |
| H2 | Technical Negation | Classification accuracy | ≥25% more correct |
| H3 | Jargon Misclassification | Error rate | ≥30% reduction |
| H4 | Cross-Domain Generalization | Accuracy on non-technical texts | Within 5 points of baseline |
| H5 | Edge-Case Recovery | Reclassification rate | ≥20% of edge-cases |

These hypotheses collectively address all three research questions while building on prior findings about VADER's baseline effectiveness and documented gains from domain-specific lexicon integration in comparable studies.