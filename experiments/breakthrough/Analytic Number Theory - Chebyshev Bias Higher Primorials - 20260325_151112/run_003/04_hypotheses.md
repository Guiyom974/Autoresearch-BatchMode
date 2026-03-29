Based on the provided research problem and the context of the Rubinstein-Sarnak framework for Chebyshev's bias, here are three testable hypotheses. These hypotheses focus on the specific comparison between the principal quadratic residue ($a=1$) and a chosen quadratic non-residue ($a=11$) modulo 210.

### Hypothesis 1: The Dominance of the QNR Class
**Statement:** The quadratic non-residue (QNR) class $a=11$ will lead the principal quadratic residue (QR) class $a=1$ for the vast majority of the range $[2, 10^6]$, specifically exhibiting a "logarithmic density" of lead time significantly greater than 0.5.

*   **Why it’s testable:** This is a direct application of the Rubinstein-Sarnak theory, which posits that non-residues are "favored" in these races due to the analytic properties of the corresponding Dirichlet L-functions. By tracking the running count of the lead, you can calculate the exact proportion of integers $x \le 10^6$ where $\Delta(x) > 0$.
*   **Experimental Test:** Run the optimized sieve up to $10^6$. Maintain a counter $C_{QNR}$ that increments every time $\pi(x; 210, 11) > \pi(x; 210, 1)$. Divide this counter by $10^6$ to determine the proportion. If the result is significantly $> 0.5$, the hypothesis is supported.

### Hypothesis 2: The Frequency of Lead Changes ("Axis Crossings")
**Statement:** The lead will switch hands between the two classes fewer than 20 times within the range $[2, 10^6]$, indicating that the Chebyshev bias creates a "sticky" lead rather than frequent oscillations.

*   **Why it’s testable:** While prime races can oscillate, the Rubinstein-Sarnak framework suggests that once a bias establishes itself, it tends to persist for long intervals. Counting the number of times the sign of $\Delta(x)$ changes (i.e., when $\pi(x; 210, 11) - \pi(x; 210, 1)$ changes sign) is a discrete, quantifiable event.
*   **Experimental Test:** During the sieve iteration, store the sign of $\Delta(x)$. Every time the sign changes from positive to negative or vice versa, increment a "crossing" counter. If the final count is low (e.g., $< 20$), it demonstrates that the bias is robust and stable over this specific interval.

### Hypothesis 3: The Asymmetry of Maximum Divergence
**Statement:** The maximum magnitude of the difference $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ will be positive, and the absolute magnitude of this positive peak will exceed the absolute magnitude of any negative trough within the range $[2, 10^6]$.

*   **Why it’s testable:** This hypothesis tests the *strength* of the bias. If the QNR class is truly favored, not only should it lead more often (Hypothesis 1), but the "distance" by which it leads should be greater than the "distance" by which the QR class occasionally takes the lead.
*   **Experimental Test:** Track the running value of $\Delta(x)$ throughout the execution. Store the global maximum ($\Delta_{max}$) and the global minimum ($\Delta_{min}$). At the end of the experiment, compare $|\Delta_{max}|$ vs $|\Delta_{min}|$. If $\Delta_{max} > |\Delta_{min}|$, it provides evidence that the bias is not only frequent but also significantly stronger in the direction of the QNR.