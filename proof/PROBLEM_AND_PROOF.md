# Problem and proof

How fast does the number of realizable gaussoids grow with the number of labelled variables? [Boege, dissertation, Conjecture 7.3](https://tboege.de/research/dissert.pdf#page=140)

**Theorem.** For each infinite field the logarithm of the number of principally regular symmetric-matrix conditional-independence patterns is Θ(n³). The same estimate holds over each ordered field with all principal minors positive.

Independent subset choices across quadratically many pairs encode a cubic number of bits. The Schur complement and specialization arguments have precedents in Boege’s thesis (§§4.1–4.2). The upper bound is Boege’s Proposition 4.46; the direct product-polynomial bound is the method of Rónyai, Babai and Ganapathy.

For a conditioning block equal to the identity, elimination evaluates the distinguished minor exactly as t² times a difference of two subset sums. With nonzero t, exactly one subset makes it zero. Distinct choices for any of the cross pairs therefore give distinct full patterns, regardless of uncontrolled minors. I checked the characteristic-two case using independence over the prime field, the finite-root exception set, and the explicit order-only positivity estimate for non-Archimedean fields. For the rational near-identity assertion, all nonidentically-zero minors have only finitely many exceptional parameters, so each array realizes a fixed full pattern along sufficiently small positive rationals. In the upper bound the product-evaluation matrix is triangular in nondecreasing order of support cardinality. Thus the recovered paper’s main quantitative result passes. The candidate now states the lower bound separately for each field and makes the rational choice of parameters explicit.

The [complete proof](../paper/manuscript.pdf) is accompanied by its [LaTeX source](../paper/manuscript.tex). Labels are fixed. Each field has its own count. The proof also constructs rational positive definite realizations arbitrarily near the identity for a subfamily. The proportion of patterns admitting these realizations (Question 7.5) remains open.
