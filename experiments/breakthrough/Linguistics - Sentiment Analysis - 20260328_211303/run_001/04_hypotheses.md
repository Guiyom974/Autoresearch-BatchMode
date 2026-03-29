# Testable Hypotheses for VADER vs Custom Keyword-Summation Sentiment Analysis

## Hypothesis 1: VADER Underperforms Custom Keyword-Summation on Technical Language

**Statement**: Custom keyword-summation tailored to technical vocabulary will produce sentiment scores with significantly lower error rates compared to VADER when evaluated against human-annotated ground truth for technical documents.

**Why it's testable**: 
- Ground truth can be established through expert human annotation of technical text samples
- Error rates (mean absolute error, misclassification rates) are directly measurable quantities
- Statistical significance can be assessed using paired t-tests or Wilcoxon signed-rank tests

**Experiment**:
1. Generate synthetic technical documents (software documentation, API descriptions, research abstracts) with known sentiment labels
2. Apply both VADER and custom keyword-summation to each document
3. Compare each method's output against ground truth
4. Calculate error metrics and p-values to determine if the difference is significant (p < 0.01)

---

## Hypothesis 2: Sentiment Score Distributions in Technical Language Deviate from VADER's Assumed Distribution

**Statement**: The statistical distribution of sentiment scores produced by VADER on technical documents will deviate significantly from both (a) the distribution assumed by VADER's lexicon weighting and (b) the empirical distribution of human-assigned sentiment scores.

**Why it's testable**:
- Distribution comparison is quantifiable using KL divergence, Chi-square tests, or Kolmogorov-Smirnov tests
- Prior findings (LDAB model success) demonstrate that distribution analysis can reveal model misfit
- Distributions are directly computable from score outputs

**Experiment**:
1. Generate 10^5 technical text samples using controlled vocabulary sets
2. Compute VADER compound scores and human-annotated sentiment scores
3. Fit distributions (e.g., Beta, Gaussian, Uniform) to each score set
4. Apply KL divergence and Chi-square tests to quantify divergence
5. Use p < 0.01 threshold to determine significance

---

## Hypothesis 3: Optimal Keyword-Summation Complexity Follows an Inverted-U Relationship

**Statement**: Custom keyword-summation accuracy follows a non-linear relationship with lexicon complexity—too few keywords (underfitting) and too many generic keywords (overfitting) both degrade performance, with an optimal complexity point in between.

**Why it's testable**:
- Based on prior finding that simpler Benford models outperformed over-corrected primorial models
- Lexicon complexity can be parameterized (e.g., keyword count, specificity thresholds)
- Performance curves can be empirically generated and analyzed

**Experiment**:
1. Create a parameterizable keyword-summation model with adjustable lexicon size
2. Test across a range of complexity levels (100 to 10,000 keywords)
3. Plot accuracy/error vs. complexity curve
4. Identify optimal complexity point and test whether performance degrades significantly on either side

---

## Hypothesis 4: VADER and Custom Keyword-Summation Exhibit Complementary Strengths Across Technical Sub-Domains

**Statement**: VADER performs better on technical documents containing informal elements (comments, reviews) while custom keyword-summation excels on purely technical nomenclature (specifications, documentation), indicating neither method universally dominates.

**Why it's testable**:
- Sub-domain categories are discrete and independently sampleable
- Performance differential is measurable within each sub-domain
- Interaction effects can be detected via two-way ANOVA or similar

**Experiment**:
1. Categorize technical documents into sub-domains (e.g., formal docs, informal comments, API references)
2. Apply both methods and measure performance within each category
3. Calculate interaction terms to determine if method × sub-domain effects are significant

---

## Hypothesis 5: A Hybrid VADER-Keyword Model Achieves Superior Scalability-Accuracy Tradeoff

**Statement**: Combining VADER's efficiency with domain-specific keyword adjustments will achieve comparable accuracy to pure custom keyword-summation while maintaining computational performance suitable for 10^5 document analysis within 2 minutes.

**Why it's testable**:
- Computational time is directly measurable using standard timing functions
- Accuracy comparison is quantifiable via established metrics
- Tradeoff analysis can be visualized and tested for significance

**Experiment**:
1. Implement three approaches: VADER only, keyword-summation only, hybrid VADER+keywords
2. Measure accuracy (against ground truth) and computation time for each
3. Test whether hybrid achieves statistically non-inferior accuracy (equivalence testing) with significantly faster runtime than pure keyword-summation
4. Validate across multiple independent runs for consistency (Success Criterion 3)

---

## Alignment with Prior Findings

| Hypothesis | Prior Finding Leveraged |
|------------|------------------------|
| H1 | VADER struggles with jargon not in dictionary (web search); custom models correct domain-specific biases |
| H2 | LDAB model dramatically improved fit (0.511 → 0.000034 KL divergence) by addressing distribution misfit |
| H3 | Simpler Benford (α=0) outperformed over-corrected primorial model; warns against excessive complexity |
| H4 | Different tools excel in different contexts (web search comparison findings) |
| H5 | LDAB success shows nuanced adjustments work; computational constraints require efficiency consideration |