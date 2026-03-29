

Below is a set of **5 testable hypotheses** that address the overarching research problem that emerges from the search summaries:

> **Research problem (inferred):** *How do systematic literature‑review methods compare with narrative (non‑systematic) approaches in terms of (a) the ability to surface research gaps, (b) the reproducibility of the search process, (c) the time required to produce the review, (d) the subsequent citation impact of the reviewed work, and (e) the methodological quality of the primary studies that are included?*

Each hypothesis is stated, followed by a short justification of why it can be tested, and a concrete experimental design that could generate the needed data.

---

## Hypothesis 1  
**Statement:** *Systematic reviews identify a greater number of distinct research gaps than narrative reviews.*  

**Why it is testable**  
- *Operationalisation*: A “research gap” can be coded as any explicit sentence that (i) states a lack of evidence, (ii) highlights an unresolved question, or (iii) proposes a future direction. Counting these statements yields a numeric outcome variable.  
- *Data availability*: Published systematic and narrative review articles are publicly accessible (e.g., PubMed, Scopus, Web of Science), so a large sample can be collected.  

**Experiment**  
1. **Sample**: Gather a stratified random sample of 100 systematic reviews (e.g., those that declare PRISMA compliance) and 100 narrative reviews from the same biomedical sub‑field (e.g., cardiovascular disease) published between 2015‑2023.  
2. **Coding**: Two independent raters, blind to the review type, will extract and count the number of explicit gap statements using a pre‑tested coding manual (inter‑rater reliability target ≥ 0.80 κ).  
3. **Analysis**: Compare the two distributions with a Mann‑Whitney *U* test (non‑normal count data) and report the effect size (rank‑biserial correlation).  

---

## Hypothesis 2  
**Statement:** *Reviews that include a higher proportion of recent literature (≥ 80 % of citations ≤ 5 years old) receive higher citation counts for the original article.*  

**Why it is testable**  
- *Operationalisation*: “Proportion of recent citations” is calculable from the reference list of each review; “citation count” is a standard bibliometric metric (e.g., total citations in Scopus/Google Scholar up to 5 years after publication).  
- *Falsifiability*: If the proportion of recent citations does **not** predict citations, the null hypothesis is retained.  

**Experiment**  
1. **Sample**: Retrieve 150 review articles (mix of systematic and narrative) across three disciplines (medicine, engineering, social sciences).  
2. **Data extraction**: For each article, compute the fraction of references published ≤ 5 years before the review’s publication date. Also retrieve the article’s 5‑year citation count.  
3. **Statistical model**: Fit a negative‑binomial (or Poisson) regression of citation count on the proportion of recent citations, controlling for journal impact factor, year of publication, and discipline.  

---

## Hypothesis 3  
**Statement:** *Using a PRISMA‑compliant search protocol yields more reproducible results than an ad‑hoc search.*  

**Why it is testable**  
- *Operationalisation*: Reproducibility can be quantified by the degree of overlap between independent search results (e.g., Jaccard similarity index) and by the consistency of the final included study list.  
- *Falsifiability*: If two teams using the same protocol produce identical study lists, the hypothesis is supported; any major divergence falsifies it.  

**Experiment**  
1. **Design**: Recruit 6 master’s‑level researchers (two teams of three). Each team receives the same clinical question (e.g., “Effect of vitamin D supplementation on fracture risk in older adults”).  
2. **Intervention**: Team A follows a full PRISMA checklist (databases, search strings, inclusion/exclusion criteria, PRISMA flow diagram). Team B conducts a “usual” literature search (free‑hand Boolean strings, no protocol).  
3. **Outcome measurement**: Both teams return their final included articles. Compute Jaccard similarity (intersection/union) and a Kappa statistic for each included study. Compare the two protocols with a Wilcoxon signed‑rank test.  

---

## Hypothesis 4  
**Statement:** *Systematic reviews that incorporate a formal risk‑of‑bias/quality appraisal of primary studies produce higher‑quality (i.e., more rigorously designed) subsequent primary research in that topic area.*  

**Why it is testable**  
- *Operationalisation*: “Quality appraisal” can be coded as present/absent (or a numeric score from tools like Cochrane RoB). “Quality of subsequent primary research” can be measured by the methodological rigor score of the next wave of RCTs or cohort studies (e.g., using the Cochrane Risk‑of‑Bias tool or the STROBE checklist).  
- *Falsifiability*: If subsequent studies are not more rigorous after a systematic review, the hypothesis is refuted.  

**Experiment**  
1. **Selection**: Identify 30 systematic reviews published 2010‑2015 that either performed a risk‑of‑bias assessment (n = 15) or did not (n = 15).  
2. **Follow‑up**: For each review, locate the next 5 primary studies that cited it and were published within 3 years. Code each primary study’s methodological quality.  
3. **Analysis**: Use a mixed‑effects linear model with review type (systematic + quality appraisal vs. systematic – quality appraisal) as a fixed effect and topic as a random effect to test for a difference in mean quality scores.  

---

## Hypothesis 5  
**Statement:** *Conducting a systematic review reduces the time required to identify actionable future research directions compared with a narrative review.*  

**Why it is testable**  
- *Operationalisation*: “Time to identify future directions” can be measured as the number of days from the start of the literature search to the moment the review authors first list a concrete research recommendation.  
- *Falsifiability*: If the times are statistically indistinguishable, the null hypothesis cannot be rejected.  

**Experiment**  
1. **Participants**: Recruit 20 early‑career researchers (PhD students or post‑docs) with no prior systematic‑review experience.  
2. **Task**: Assign each participant two identical clinical questions. One question must be answered with a PRISMA‑guided systematic review (including a flow diagram) and the other with a conventional narrative review. The order is counter‑balanced.  
3. **Measurement**: Log the exact timestamps for (a) start of database searching, (b) completion of full‑text screening, and (c) first explicit statement of a future‑research recommendation. Calculate the interval for each type.  
4. **Statistical test**: Perform a paired‑samples *t*‑test (or Wilcoxon if distributions are non‑normal) on the time‑to‑recommendation variable across the two conditions.  

---

### Quick Reference Table

| # | Hypothesis (H) | Independent Variable (IV) | Dependent Variable (DV) | Typical Analysis |
|---|----------------|---------------------------|--------------------------|-------------------|
| 1 | Systematic → more gaps | Review type (systematic vs. narrative) | Number of explicit gap statements | Mann‑Whitney U |
| 2 | Recent‑citation proportion → higher citations | % of citations ≤ 5 years old | 5‑year citation count | Negative‑binomial regression |
| 3 | PRISMA protocol → higher reproducibility | Search protocol (PRISMA vs. ad‑hoc) | Jaccard similarity, Kappa | Wilcoxon signed‑rank |
| 4 | Quality appraisal → higher subsequent study quality | Presence/absence of risk‑of‑bias assessment | Methodological quality score of next studies | Mixed‑effects linear model |
| 5 | Systematic faster to pinpoint future directions | Review type (systematic vs. narrative) | Time (days) to first research recommendation | Paired‑samples t‑test / Wilcoxon |

These hypotheses are **specific, measurable, and falsifiable**, making them directly amenable to empirical testing using published literature, bibliometric databases, or controlled user experiments.