# Research Problem: Chebyshev Bias at Higher Primorials — Corrected & Extended

## Background
The previous experiment identified a statistically significant "excess" of primes in residue
class a=5 mod 210 (p=0.003). However, gcd(5, 210)=5 ≠ 1, meaning this class is NOT coprime
to 210 — the only prime in it is 5 itself. The finding was a code artifact from failing to
filter non-coprime residue classes.

This run corrects the filter and performs a rigorous, theoretically-grounded investigation of
**genuine Chebyshev bias** among the φ(210)=48 coprime residue classes modulo 210 and beyond.

## Objective
Verify and quantify the Rubinstein-Sarnak prediction for Chebyshev's bias at mod 210 and 2310:
non-residue quadratic residue classes should win prime races more than 50% of the time.
Find which specific coprime classes lead, measure the bias magnitude, and check whether the
magnitude scales with log(log(x)) as theory predicts.

## Research Questions

1. **Coprime Class Audit**: Among all φ(210)=48 coprime residue classes mod 210, which are
   quadratic residues (QR) and which are quadratic non-residues (NR)? Do the NR classes hold
   more primes as predicted by Chebyshev?

2. **Bias Magnitude & Scaling**: For the two extreme classes (most and fewest primes mod 210),
   how does the normalized difference (π(x;210,a_NR) − π(x;210,a_R)) / (x/log x) evolve as
   x grows from 10^6 to 10^9? Does it scale as C·log(log(x)) as Rubinstein-Sarnak predicts?

3. **Cross-Primorial Consistency**: Does the same qualitative Chebyshev structure appear at
   P₅=2310 (φ=480 coprime classes)? Are the winning classes consistent with their quadratic
   residue status in both moduli simultaneously?

4. **Logarithmic Density of Leaders**: For the top-3 competing coprime classes mod 210, compute
   the logarithmic density δ(a) = lim_{x→∞} (1/log x) ∑_{p≤x, π(p;q,a)>π(p;q,b)} 1/p.
   Does the NR class leader density exceed 0.5 as Chebyshev's bias predicts?

5. **Dirichlet Character Contribution**: For mod 210, identify which Dirichlet characters χ
   modulo 210 are real (χ² = χ₀). These are the ones responsible for Chebyshev bias. For each
   coprime residue class, compute the character sum ∑_χ real χ(a) and verify it predicts the
   observed bias direction.

## Methodology

1. **Corrected Sieve**: Implement a segmented Sieve of Eratosthenes. For each prime p, compute
   r = p mod q. Include only if gcd(r, q) == 1 (coprime filter). Verify: class a=5 mod 210
   should contain ONLY the prime 5 itself.

2. **Quadratic Residue Classification**: For each coprime residue a mod 210, determine whether
   a is a QR mod 210 using the Jacobi symbol (product of Legendre symbols mod 2, 3, 5, 7).
   Label classes as QR or NR.

3. **Statistical Test**: Apply a Chi-squared goodness-of-fit test to compare observed prime
   counts per coprime class against the expected 1/φ(q) uniform distribution. Report p-value
   and identify the most over- and under-represented coprime classes.

4. **Race Tracking**: Track cumulative counts π(x; 210, a) for the top-3 and bottom-3 coprime
   classes at intervals x = 10^k for k=5..9. Plot normalized lead δ(x,a,b) = (π(x;q,a) −
   π(x;q,b)) / √(x/log x) over x.

5. **L-Function Cross-Check**: Compute the real Dirichlet characters mod 210 analytically
   (there are 2^3 = 8 real characters, from the factorisation 210 = 2·3·5·7). For each
   coprime class a, evaluate ∑_{χ real, χ≠χ₀} χ(a). Theory predicts this sum is negative for
   QR classes (they lose) and positive for NR classes (they win).

## Success Criteria

1. **Artifact Confirmed**: Explicitly show that a=5 mod 210 contains ≤1 prime (the prime 5
   itself) and produces no statistically meaningful count signal.

2. **Bias Confirmed**: At least one pair of coprime classes (NR vs QR mod 210) shows a
   statistically significant race lead (NR winning >50% of the time by logarithmic density)
   consistent with the Chebyshev prediction.

3. **Scaling Verified**: The normalized bias (π_NR − π_QR)/√(x/log x) grows with log(log(x))
   over at least 3 orders of magnitude of x.

4. **Cross-Primorial**: The same NR→QR ordering is reproduced at mod 2310, confirming the
   structure is intrinsic to prime distribution, not a mod-210-specific artifact.

5. **Character Sum Match**: The sign of the Dirichlet character sum for each class correctly
   predicts the observed bias direction for ≥90% of coprime classes mod 210.

## Prior Knowledge to Incorporate
- Rubinstein-Sarnak (1994): proved logarithmic density exists for prime races assuming GRH +
  Grand Simplicity Hypothesis; non-residues win with density > 0.5
- Dirichlet's theorem: primes equidistribute among coprime residue classes asymptotically
- Chebyshev bias magnitude: O(log log x) correction to the equidistribution, not O(1)
- Devin (2017): proved Chebyshev bias distributions exist WITHOUT assuming GRH (weaker bounds)

## Constraints
- All code in Python, stdlib + numpy + matplotlib only
- No downloading data — all primes generated locally
- Must explicitly verify coprimality filter before any statistical test
- Runtime ≤ 3 minutes (use segmented sieve for memory efficiency)
- Experiments must clearly distinguish: (a) theoretical prediction, (b) observed result,
  (c) whether they agree
