# Research Problem: Low-Bound Empirical Verification of the Modulo 210 Prime Race ($a=11$ vs $a=1$)

## Objective
To bypass the severe computational bottlenecks encountered in previous iterations by drastically restricting the maximum evaluation bound. We will evaluate the Rubinstein-Sarnak Chebyshev bias prediction for a single, targeted two-way prime race modulo 210: the quadratic non-residue (QNR) class $a=11$ against the principal quadratic residue class $a=1$. The strict objective is to measure the logarithmic density of this specific race up to a hard-capped bound of $x = 10^7$, ensuring the computation completes and yields actionable baseline data.

## Research Questions
1. Does the QNR class $a=11$ maintain a strict dominance over the principal class $a=1$ modulo 210 for all primes up to $x = 10^7$?
2. If lead changes occur within this restricted bound, at what specific values of $x$ do they manifest?
3. What is the empirical logarithmic density of the set of $x \le 10^7$ for which $\pi(x; 210, 11) > \pi(x; 210, 1)$?

## Methodology
1. **Targeted Prime Generation:** Utilize a highly optimized prime sieve strictly capped at $N = 10^7$. 
2. **Binary Class Filtering:** As primes are generated, filter and count *only* those that satisfy $p \equiv 1 \pmod{210}$ and $p \equiv 11 \pmod{210}$. Discard all other primes immediately to save memory.
3. **Cumulative Tallying:** Maintain a running tally of $\pi(x; 210, 11)$ and $\pi(x; 210, 1)$.
4. **Logarithmic Density Calculation:** At regular intervals (e.g., every $10^4$), compute the logarithmic weight $\frac{1}{x}$ to approximate the logarithmic density of the QNR lead.
5. **Lead Change Tracking:** Record the exact prime values where the lead transitions from one class to the other.

## Success Criteria
1. The experiment successfully completes without timing out or exhausting memory resources.
2. Output includes the total count of primes in both the $a=11$ and $a=1$ classes up to $10^7$.
3. Output provides a definitive list of the first $k$ lead changes (if any exist below $10^7$).
4. Output yields a calculated logarithmic density for this specific two-way race over the bounded interval.

## Constraints
1. **Hard Bound:** The maximum value for $x$ must absolutely not exceed $10^7$. 
2. **Strict Two-Class Limit:** The algorithm must only track counts for $a=1$ and $a=11$. Do not calculate or store data for the other 46 coprime residue classes.
3. **Empirical Only:** Do not attempt to compute Dirichlet L-functions, zeros, or theoretical Rubinstein-Sarnak distributions in this run; focus solely on the empirical prime counting function $\pi(x)$.