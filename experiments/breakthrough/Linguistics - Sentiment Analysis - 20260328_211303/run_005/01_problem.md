# Research Problem: Linguistics - Sentiment Analysis

## Objective
To benchmark the VADER-technical lexicon meta-classifier ensemble against modern, domain-specific Transformer architectures (e.g., CodeBERT, FinBERT) and perform a deep feature-contribution analysis. Given that previous iterations showed the ensemble's performance gains over traditional baselines lacked statistical significance, this phase aims to determine if the feature-engineered ensemble approach remains viable compared to contextual embeddings, and to identify whether feature redundancy is suppressing significant performance gains.

## Research Questions
1. How does the predictive accuracy (MAE) of the VADER-lexicon meta-classifier compare to zero-shot and fine-tuned Transformer models tailored for technical discourse?
2. Which specific features (e.g., VADER compound scores, custom lexicon polarities, syntactic markers) drive the meta-classifier's decision boundary, and is there evidence of feature redundancy?
3. Can the removal of redundant or low-impact features from the ensemble yield a statistically significant improvement over baseline models?

## Methodology
1. **Model Expansion**: Implement baseline Transformer models specialized for technical language (e.g., CodeBERT for software engineering, FinBERT for finance) to serve as modern benchmarks.
2. **Feature Importance Analysis**: Apply explainability techniques (e.g., SHAP values, permutation feature importance) to the existing meta-classifier to quantify the exact contribution of VADER outputs versus custom technical lexicon signals.
3. **Ablation Study**: Systematically remove lowest-contributing features from the meta-classifier to reduce noise and test for improved statistical significance in performance differences.
4. **Rigorous Statistical Testing**: Utilize power-analysis to ensure adequate sample sizes, and apply non-parametric tests (e.g., Wilcoxon signed-rank test) alongside paired t-tests to compare the optimized ensemble against both VADER and Transformer baselines.

## Success Criteria
1. A definitive benchmarking report comparing the optimized meta-classifier against Transformer models with statistically rigorous p-values.
2. An isolated list of high-impact technical lexicon features that positively contribute to sentiment detection in technical contexts.
3. A statistically significant performance delta (p < 0.05) between the refined meta-classifier and the original VADER baseline, or conclusive evidence that feature-engineered meta-classifiers are entirely superseded by Transformers in this domain.

## Constraints
1. **Computational Overhead**: Transformer model inference and fine-tuning must be constrained to available GPU limits, potentially requiring sample-size capping during the benchmarking phase.
2. **Domain Specificity**: The evaluation must strictly utilize datasets from specific technical domains (e.g., software development forums, financial earnings calls) rather than general-purpose reviews.
3. **Label Scarcity**: Ground-truth sentiment labels in highly technical domains are subjective and sparse, requiring careful curation of the evaluation corpora.