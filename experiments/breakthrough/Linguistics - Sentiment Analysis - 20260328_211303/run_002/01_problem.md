# Research Problem: Linguistics - Sentiment Analysis

## Objective
Develop and evaluate a hybrid sentiment analysis model that integrates VADER's rule-based heuristics with a domain-specific technical lexicon to improve sentiment detection accuracy in real-world technical corpora.

## Research Questions
1. How much does integrating a domain-specific technical lexicon into VADER's existing framework reduce Mean Absolute Error (MAE) compared to the baseline VADER model?
2. Which specific technical linguistic features (e.g., domain-specific jargon, context-dependent modifiers, or technical negations) are best captured by the hybrid approach that baseline VADER misses?
3. Does the hybrid model maintain baseline accuracy when applied to non-technical language, or does the domain-specific tuning cause overfitting?

## Methodology
1. **Data Collection:** Curate a dataset of real-world technical texts (e.g., Stack Overflow comments, GitHub pull request discussions, or engineering reports) annotated with ground-truth sentiment scores.
2. **Lexicon Development:** Construct a custom technical lexicon containing domain-specific terms and their corresponding sentiment weights, established through domain expert annotation or corpus-based statistical extraction.
3. **Model Integration:** Modify VADER's scoring algorithm to ingest the custom technical lexicon, allowing it to override or supplement default sentiment scores while retaining VADER's structural heuristics (e.g., punctuation emphasis, degree modifiers).
4. **Statistical Evaluation:** Evaluate the hybrid model against baseline VADER using MAE, RMSE, and Accuracy. Apply paired t-tests and Wilcoxon signed-rank tests to assess the statistical significance of any performance improvements.

## Success Criteria
1. The hybrid model achieves a statistically significant reduction in MAE (p < 0.05) compared to baseline VADER on the real-world technical dataset.
2. The hybrid model achieves an overall accuracy exceeding the 62.00% benchmark established by VADER in the previous synthetic tests.
3. The hybrid model successfully classifies at least 20% of the edge-case documents that baseline VADER misclassified due to technical jargon.

## Constraints
1. The analysis must utilize real-world technical corpora rather than synthetic data, limiting the volume of perfectly annotated ground-truth text available.
2. The hybrid model must remain entirely lexicon- and rule-based (avoiding large language models or deep learning architectures like BERT) to preserve the computational efficiency and transparency of the original VADER approach.