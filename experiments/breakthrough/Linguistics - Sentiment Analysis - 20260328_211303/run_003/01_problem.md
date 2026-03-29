# Research Problem: Linguistics - Sentiment Analysis

## Objective
Evaluate alternative integration strategies—specifically static weighted averaging and machine-learning-based meta-classification—for combining VADER's general sentiment heuristics with a technical sentiment lexicon. This aims to correct the systematic misclassifications and valence conflicts introduced by direct rule-addition, ultimately improving sentiment detection accuracy in technical corpora.

## Research Questions
1. How does an ensemble integration strategy (scoring VADER and a standalone technical lexicon independently, then combining) affect Mean Absolute Error (MAE) compared to the baseline VADER model and the previously failed direct-lexicon-injection method?
2. Can a lightweight machine-learning meta-classifier (e.g., logistic or ridge regression) optimally weight VADER outputs against technical lexicon scores to significantly improve the handling of technical negations and context-dependent modifiers?
3. What is the optimal weight distribution between general sentiment heuristics and domain-specific lexicon scores across different sub-types of technical text (e.g., jargon-heavy vs. negation-heavy)?

## Methodology
1. **Corpus Generation & Annotation**: Generate a synthetic technical dataset (or curate an existing one) with labeled sentiment ground truths, ensuring distinct subsets that isolate technical jargon and technical negations.
2. **Model Architecture**: Develop three distinct scoring pipelines:
    * *Pipeline A (Baseline)*: Standard VADER.
    * *Pipeline B (Weighted Average)*: Independent VADER score and independent Technical Lexicon score, combined using predefined static weights.
    * *Pipeline C (ML Meta-Classifier)*: A lightweight supervised model trained to predict final sentiment using VADER metrics (pos, neg, neu, compound) and Technical Lexicon metrics as input features.
3. **Cross-Validation**: Implement k-fold cross-validation to ensure the ML integration strategy does not overfit to the specific technical corpus.
4. **Statistical Testing**: Perform paired t-tests and calculate MAE on the overall corpus and specific subsets (negations, jargon) to determine the statistical significance of performance differences between the pipelines.

## Success Criteria
1. **MAE Reduction**: The newly proposed integration strategies (Pipeline B or C) must achieve a statistically significant (p < 0.05) MAE reduction of at least 10% compared to the baseline VADER model.
2. **Negation Handling Improvement**: The models must demonstrate a statistically significant reduction in MAE specifically on the subset of documents containing technical negations, reversing the degradation observed in previous iterations.
3. **Generalization**: The ML Meta-Classifier must maintain its MAE reduction threshold across all folds during cross-validation.

## Constraints
1. The research must retain VADER as the foundational general-sentiment model; replacing it entirely with a deep-learning model (e.g., BERT) falls outside the scope of this heuristic-focused study.
2. The integration strategies must remain computationally lightweight and highly interpretable, avoiding black-box architectures that obscure the linguistic drivers of the sentiment score.
3. The technical lexicon used for the ensemble must be kept strictly separate from VADER's internal `lexicon.txt` to prevent internal valence calculation conflicts.