import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats as stats

def main():
    print("Testing Hypotheses: Systematic vs. Narrative Literature Reviews\n")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Sample sizes
    n_sr = 150  # Systematic Reviews
    n_nr = 150  # Narrative Reviews
    
    # Simulate Data
    # H1: Number of distinct research gaps identified
    # Systematic reviews are hypothesized to identify more gaps.
    gaps_sr = np.random.poisson(lam=5.5, size=n_sr)
    gaps_nr = np.random.poisson(lam=3.2, size=n_nr)
    
    # H2: Reproducibility of the search process (score 0-100)
    # Systematic reviews should have higher reproducibility.
    repro_sr = np.clip(np.random.normal(loc=85, scale=10, size=n_sr), 0, 100)
    repro_nr = np.clip(np.random.normal(loc=45, scale=15, size=n_nr), 0, 100)
    
    # H3: Time required to produce the review (months)
    # Systematic reviews take longer.
    time_sr = np.random.normal(loc=12.5, scale=3.0, size=n_sr)
    time_nr = np.random.normal(loc=6.0, scale=2.5, size=n_nr)
    
    # H4: Subsequent citation impact (citations per year)
    # Systematic reviews might have higher citation impact.
    cites_sr = np.random.lognormal(mean=3.0, sigma=0.8, size=n_sr)
    cites_nr = np.random.lognormal(mean=2.2, sigma=0.8, size=n_nr)
    
    # H5: Methodological quality of included studies (score 0-10)
    # Systematic reviews might filter for higher quality.
    qual_sr = np.clip(np.random.normal(loc=7.8, scale=1.2, size=n_sr), 0, 10)
    qual_nr = np.clip(np.random.normal(loc=6.5, scale=1.5, size=n_nr), 0, 10)
    
    # Testing Hypothesis 1
    print("--- Hypothesis 1: Research Gaps Identified ---")
    print("H1: Systematic reviews identify a greater number of distinct research gaps.")
    t_stat1, p_val1 = stats.ttest_ind(gaps_sr, gaps_nr, equal_var=False)
    print(f"SR Mean: {np.mean(gaps_sr):.2f}, NR Mean: {np.mean(gaps_nr):.2f}")
    print(f"T-statistic: {t_stat1:.4f}, P-value: {p_val1:.4e}\n")
    
    # Testing Hypothesis 2
    print("--- Hypothesis 2: Reproducibility ---")
    print("H2: Systematic reviews have higher reproducibility scores.")
    t_stat2, p_val2 = stats.ttest_ind(repro_sr, repro_nr, equal_var=False)
    print(f"SR Mean: {np.mean(repro_sr):.2f}, NR Mean: {np.mean(repro_nr):.2f}")
    print(f"T-statistic: {t_stat2:.4f}, P-value: {p_val2:.4e}\n")
    
    # Testing Hypothesis 3
    print("--- Hypothesis 3: Time Required ---")
    print("H3: Systematic reviews require more time to produce.")
    t_stat3, p_val3 = stats.ttest_ind(time_sr, time_nr, equal_var=False)
    print(f"SR Mean: {np.mean(time_sr):.2f} months, NR Mean: {np.mean(time_nr):.2f} months")
    print(f"T-statistic: {t_stat3:.4f}, P-value: {p_val3:.4e}\n")
    
    # Testing Hypothesis 4
    print("--- Hypothesis 4: Citation Impact ---")
    print("H4: Systematic reviews have a higher subsequent citation impact.")
    # Using Mann-Whitney U test due to lognormal distribution
    u_stat4, p_val4 = stats.mannwhitneyu(cites_sr, cites_nr, alternative='two-sided')
    print(f"SR Median: {np.median(cites_sr):.2f}, NR Median: {np.median(cites_nr):.2f}")
    print(f"U-statistic: {u_stat4:.4f}, P-value: {p_val4:.4e}\n")
    
    # Testing Hypothesis 5
    print("--- Hypothesis 5: Methodological Quality ---")
    print("H5: Systematic reviews include primary studies of higher methodological quality.")
    t_stat5, p_val5 = stats.ttest_ind(qual_sr, qual_nr, equal_var=False)
    print(f"SR Mean: {np.mean(qual_sr):.2f}, NR Mean: {np.mean(qual_nr):.2f}")
    print(f"T-statistic: {t_stat5:.4f}, P-value: {p_val5:.4e}\n")
    
    # Plotting results
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Systematic (SR) vs Narrative (NR) Reviews', fontsize=16)
    
    data_pairs = [
        (gaps_sr, gaps_nr, 'Research Gaps', axes[0,0]),
        (repro_sr, repro_nr, 'Reproducibility Score', axes[0,1]),
        (time_sr, time_nr, 'Time Required (Months)', axes[0,2]),
        (cites_sr, cites_nr, 'Citations per Year (Log Scale)', axes[1,0]),
        (qual_sr, qual_nr, 'Methodological Quality', axes[1,1])
    ]
    
    for sr_data, nr_data, title, ax in data_pairs:
        ax.boxplot([sr_data, nr_data], labels=['SR', 'NR'])
        ax.set_title(title)
        if 'Citations' in title:
            ax.set_yscale('log')
            
    axes[1,2].axis('off') # Hide empty subplot
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('review_comparison_results.png')
    print("Plots saved to 'review_comparison_results.png'.\n")
    
    print("CONCLUSIONS:")
    print("Based on the simulated data analysis:")
    print("1. Systematic reviews identify significantly more research gaps than narrative reviews.")
    print("2. The reproducibility of the search process is vastly superior in systematic reviews.")
    print("3. Systematic reviews require significantly more time to conduct and publish.")
    print("4. Systematic reviews achieve a higher citation impact over time.")
    print("5. The methodological quality of included studies is higher in systematic reviews, likely due to strict inclusion/exclusion criteria.")
    print("Overall, while systematic reviews are more resource-intensive (time), they provide superior methodological rigor, reproducibility, and impact.")

if __name__ == "__main__":
    main()