# Counting realizable gaussoids over infinite fields

[![Repository verification](https://github.com/DannyExperiments/realizable-gaussoids-cubic-growth/actions/workflows/verify.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/realizable-gaussoids-cubic-growth/actions/workflows/verify.yml) [![Verifier replay](https://github.com/DannyExperiments/realizable-gaussoids-cubic-growth/actions/workflows/replay.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/realizable-gaussoids-cubic-growth/actions/workflows/replay.yml) [![PDF build](https://github.com/DannyExperiments/realizable-gaussoids-cubic-growth/actions/workflows/pdf.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/realizable-gaussoids-cubic-growth/actions/workflows/pdf.yml)

How fast does the number of realizable gaussoids grow with the number of labelled variables? The original question appears in [Boege, dissertation, Conjecture 7.3](https://tboege.de/research/dissert.pdf#page=140).

**Result.** For each infinite field the logarithm of the number of principally regular symmetric-matrix conditional-independence patterns is Θ(n³). The same estimate holds over each ordered field with all principal minors positive.

[Read the paper (PDF)](paper/manuscript.pdf) · [LaTeX source](paper/manuscript.tex) · [Proof guide](proof/PROBLEM_AND_PROOF.md) · [Reproduce the checks](REPRODUCIBILITY.md)

Independent subset choices across quadratically many pairs encode a cubic number of bits. The Schur complement and specialization arguments have precedents in Boege’s thesis (§§4.1–4.2). The upper bound is Boege’s Proposition 4.46; the direct product-polynomial bound is the method of Rónyai, Babai and Ganapathy.

Internally reviewed, not peer reviewed. [Mathematical audit](audits/public_safe_reports/MATHEMATICAL_AUDIT.md) · [Literature and priority](audits/public_safe_reports/LITERATURE_AUDIT.md) · [Citation](CITATION.cff)
