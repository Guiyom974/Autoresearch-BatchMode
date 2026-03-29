Below are **five testable hypotheses** that directly follow from the research problem and the prior findings.  
Each hypothesis is stated in a way that can be operationalised, the variables are measurable, and the experiment needed to evaluate it is concrete.

---

## Hypothesis 1 – Transformers vs. the VADER‑lexicon meta‑classifier  

**Statement**  
*Fine‑tuned, domain‑specific Transformer models (e.g., CodeBERT on software‑engineering text, FinBERT on financial text) will achieve a statistically significant lower MAE than the VADER‑lexicon meta‑classifier ensemble on the same real‑world technical corpora.*

**Why it is testable**  
*Both the MAE of the meta‑classifier and the MAE of each Transformer can be computed on the same held‑out test set.  Because MAE is a continuous metric, we can apply a paired statistical test (e.g., Wilcoxon signed‑rank or paired‑t) to determine whether the observed difference is unlikely to be due to chance.*

**Experiment**  
1. **Corpora** – Use two domain‑specific datasets: (a) a curated set of Stack Overflow Q&A & GitHub commit messages (software‑engineering domain) and (b) a set of earnings‑call transcripts / analyst reports (financial domain).  
2. **Models** –  
   * **Meta‑classifier** – the existing VADER + technical‑lexicon ensemble (already trained).  
   * **Fine‑tuned Transformers** – fine‑tune CodeBERT on the software‑engineering split and fine‑tune FinBERT on the finance split (both limited to the GPU budget; if necessary, cap training steps or batch size).  
   * **Zero‑shot baseline** – a general BERT model evaluated without fine‑tuning for an additional reference point.  
3. **Evaluation** – Compute MAE for each model on a **balanced, held‑out test set** (≈ 20 % of each corpus).  
4. **Statistical test** – Perform a **paired Wilcoxon signed‑rank test** (non‑parametric) and, if residuals are normal, a **paired t‑test** as a robustness check; set α = 0.05 and correct for multiple comparisons (Bonferroni or FDR) across the two domains.

---

## Hypothesis 2 – A small core of features drives the meta‑classifier  

**Statement**  
*The VADER compound score together with ≤ 3 custom technical‑lexicon polarity scores will account for **> 70 %** of the total SHAP‑based explanation of the meta‑classifier’s predictions, while syntactic markers and the remaining lexicon entries contribute < 5 % each.*

**Why it is testable**  
*SHAP (SHapley Additive exPlanations) yields a per‑sample contribution for every input feature. By aggregating absolute SHAP values across the test set we can quantify each feature’s share of the overall explanation. The proportions are numeric and can be compared against pre‑specified thresholds.*

**Experiment**  
1. **Train** the meta‑classifier on the same technical corpora used in Hypothesis 1.  
2. **Compute SHAP values** for each test sample using a model‑agnostic explainer (e.g., TreeExplainer if the meta‑classifier is a tree‑based stacker, or KernelExplainer otherwise).  
3. **Aggregate** absolute SHAP values per feature across all test samples; normalise to percentages.  
4. **Identify** the smallest set of features whose cumulative SHAP contribution reaches the 70 % threshold.  
5. **Validate** the result with **permutation importance** (average drop in MAE when a feature is randomly shuffled) to confirm that the low‑impact features indeed have negligible influence.

---

## Hypothesis 3 – Ablation of low‑impact features improves MAE  

**Statement**  
*Removing the bottom 30 % of features (ranked by SHAP importance) from the meta‑classifier will **reduce** its MAE and yield a statistically significant improvement (p < 0.05) over the full‑feature ensemble.*

**Why it is testable**  
*We can define a clear ablation protocol: (i) rank features by SHAP importance, (ii) drop those below a cutoff, (iii) retrain the meta‑classifier on the same training folds, (iv) compare MAE on the same test folds using a paired test.*

**Experiment**  
1. **Ranking** – Use the SHAP ranking from Hypothesis 2.  
2. **Ablation steps** – Create three ablated ensembles:  
   * **Abl‑25%** – remove lowest 25 % of features.  
   * **Abl‑30%** – remove lowest 30 % (the primary hypothesis).  
   * **Abl‑50%** – remove lowest 50 % as a sanity check.  
3. **Retraining** – For each ablation level, re‑fit the stacking model on the **same training folds** (to keep the data split identical).  
4. **Evaluation** – Compute MAE on the held‑out test set for each ablated version.  
5. **Statistical testing** – Apply **paired t‑tests** (or Wilcoxon if normality fails) between the full ensemble and each ablated version; adjust α for multiple comparisons.

---

## Hypothesis 4 – Refined meta‑classifier outperforms the original VADER baseline  

**Statement**  
*The ablated (refined) meta‑classifier will achieve a **statistically significant lower MAE** than the original rule‑based VADER model on at least one of the two technical domains.*

**Why it is testable**  
*The original VADER model can be run directly on the test corpora to obtain its MAE. The refined meta‑classifier (the best‑performing ablated version from Hypothesis 3) can then be compared to VADER using the same statistical tests.*

**Experiment**  
1. **Baseline** – Run the original VADER (no additional training) on the same test splits used in Hypothesis 1.  
2. **Refined ensemble** – Use the best‑performing ablation (e.g., Abl‑30% if it shows the lowest MAE).  
3. **Comparison** – Compute MAE for both on each domain.  
4. **Power analysis** – Before the experiment, conduct a power analysis (target power = 0.80) to ensure the sample size is sufficient to detect a clinically meaningful MAE reduction (e.g., 0.01‑0.02).  
5. **Significance** – Apply a **paired Wilcoxon signed‑rank test** (two‑sided) with α = 0.05; report effect size (e.g., Cohen’s d).

---

## Hypothesis 5 – Domain‑specific performance divergence between Transformers and the meta‑classifier  

**Statement**  
*The relative advantage of Transformer models over the meta‑classifier will be **domain‑dependent**: FinBERT will significantly outperform the refined meta‑classifier on financial text, whereas CodeBERT will not show a statistically significant advantage over the refined meta‑classifier on software‑engineering text.*

**Why it is testable**  
*We can directly compare the MAE of the refined meta‑classifier (from Hypothesis 3) with each fine‑tuned Transformer on each domain. The interaction between model type and domain can be formalised as a **two‑way ANOVA** (or a non‑parametric analogue) to test the interaction effect.*

**Experiment**  
1. **Models** – Fine‑tuned FinBERT (finance) and fine‑tuned CodeBERT (software‑engineering) plus the refined meta‑classifier (best ablation).  
2. **Test sets** – Same held‑out financial and software‑engineering corpora.  
3. **Evaluation matrix** – MAE for each model‑domain pair (3 × 2 table).  
4. **Statistical analysis** – Run a **two‑way repeated‑measures ANOVA** (or Friedman test if assumptions are violated) with *model* and *domain* as factors.  
   * If the interaction term is significant (p < 0.05), perform **post‑hoc pairwise comparisons** (e.g., Wilcoxon with Bonferroni correction) to confirm the pattern described in the hypothesis.  

---

### How these hypotheses build on prior findings  

| Prior Finding | How the Hypothesis Extends It |
|---------------|--------------------------------|
| *Hybrid VADER + lexicon did **not** improve MAE (redundancy suspected).* | **H2** quantifies redundancy via SHAP; **H3** directly tests whether removing redundant features restores a gain. |
| *Meta‑classifier ensemble achieved lower MAE than components on synthetic data, but the gain was **not significant** on real data.* | **H4** asks whether a refined (ablated) ensemble can finally surpass the original VADER baseline with statistical significance. |
| *No statistical significance was observed for the modest MAE reduction on real corpora.* | **H1** introduces a stronger competitor (domain‑specific Transformers) to see if the ensemble can still compete; **H5** explores whether any advantage is domain‑specific. |

---

### Quick Reference for Experiment Design  

| Hypothesis | Primary Metric | Independent Variables | Statistical Test | Required Sample Size (per domain) |
|------------|----------------|-----------------------|------------------|-----------------------------------|
| **H1** | MAE | Model type (meta‑classifier vs. fine‑tuned Transformer) | Paired Wilcoxon / t‑test (α = 0.05, Bonferroni) | Power analysis: ~200–300 test instances (detect ΔMAE ≈ 0.015) |
| **H2** | SHAP proportion | Feature set | Descriptive (cumulative %); permutation importance as validation | Full test set (≥ 200 samples) |
| **H3** | MAE (before vs. after ablation) | Ablation level (25 %, 30 %, 50 %) | Paired t‑test / Wilcoxon (α = 0.05) | Same as H1 |
| **H4** | MAE (refined ensemble vs. VADER) | Model (refined ensemble vs. VADER) | Paired Wilcoxon (α = 0.05) | Power‑driven sample size (see H4) |
| **H5** | MAE (model × domain) | Model × Domain interaction | Two‑way repeated‑measures ANOVA / Friedman (α = 0.05) + post‑hoc | At least 150 instances per domain (to detect moderate interaction) |

These hypotheses are **actionable**, **measurable**, and **directly address the three research questions** while respecting the computational, domain‑specificity, and label‑scarcity constraints outlined in the problem statement.