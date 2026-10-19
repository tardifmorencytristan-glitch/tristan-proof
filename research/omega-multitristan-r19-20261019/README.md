# Omega Multi-Tristan R19 — Minimal Witnesses for Synthetic Pareto Fronts

**Marker:** OMEGA-MULTITRISTAN-R19-EXACT-FINITE-20261019-V1  
**Status:** EXACT_FINITE_SYNTHETIC_VERIFIED / NOT PHYSICS-VALIDATED / NOT PEER REVIEWED

*Résumé français.* Dans une expérience synthétique finie avec trois problèmes, deux échelles, deux directions et quatre sous-ensembles d'objectifs, 48 fronts de Pareto sont calculés. Parmi 249 candidats admissibles, seulement 37 signatures d'appartenance sont différentes. Dix observations parmi les 48 suffisent pour conserver exactement ces 37 classes, et neuf sont insuffisantes. Deux candidats suffisent à couvrir tous les 48 fronts; aucun candidat seul ne les couvre.

## 1. Reproducible scope

This is a **finite combinatorial benchmark**, not a general optimization theorem, new physical law, or claim of scientific priority. All results below concern the frozen test fixture reproduced by the companion pure-Python file `r19_public_reproduce.py`.

- Candidate indices: the 289 ordered integer coordinate pairs `(x,y) in [-8,8]^2`, indexed in lexicographic order.
- Feasible candidates: `x*x+y*y <= 80`, giving 249 candidates.
- Problems P0/P1/P2: targets `(4,-4)`, `(-4,4)`, `(2,2)`; coupling parameters `(2,1,1)`; coupling signs `(1,-1,1)`; residual offsets `(0,4,-4)`.
- Direction D0: preserve the signed coordinates. D1: apply absolute value separately to both coordinates.
- Scale S0: preserve transformed coordinates. S1: replace each transformed integer `a` by `2*(a//2)` (and likewise `b`).
- For transformed coordinates `(a,b)` and problem `p`, minimize the three objectives:

```text
fit      = (a-tx)^2 + (b-ty)^2 + coupling[p]*(a-sign[p]*b)^2
size     = a^2 + b^2
residual = (a+b-offset[p])^2 + (p+1)*(a-b)^2
```

Four objective index subsets `J01`, `J02`, `J12`, `J012` are evaluated separately. This defines 3 x 2 x 2 x 4 = 48 Pareto fronts. Non-dominance uses weak inequality in all selected objectives and strict inequality in at least one.

## 2. Two mathematical questions — not one

**Problem A, coverage:** Choose the fewest candidates whose union of Pareto-front memberships covers all 48 contexts. The exact minimum is **two**. No single candidate belongs to all 48 contexts; candidate 144 belongs to 44. The five pairs covering all fronts are:

```text
(112,144)  (129,144)  (144,146)  (144,163)  (144,180)
```

**Problem B, discrimination:** Each candidate has a 48-bit signature indicating whether it belongs to each front. Among the 249 feasible candidates, only **37 distinct signatures** occur. Find the smallest subset of the 48 questions preserving all 37 equivalence classes. The exact minimum is **ten questions**; this does not distinguish candidates already identical under all 48 observations.

One optimal witness is:

```text
P0/S1/D1/J02
P1/S0/D0/J01
P1/S0/D0/J012
P1/S0/D1/J02
P1/S0/D1/J12
P1/S1/D0/J01
P1/S1/D0/J12
P1/S1/D1/J01
P2/S1/D0/J02
P2/S1/D1/J02
```

## 3. Finite optimality certificate

1. Among the 37 distinct full signatures there are 666 unordered pairs to separate.
2. Four questions are individually indispensable: `P1/S0/D0/J01`, `P1/S0/D1/J12`, `P1/S1/D0/J01`, and `P1/S1/D0/J12`. For each, there is a pair of full signatures differing only in that question.
3. The 48 question-columns collapse to 31 distinct answer patterns over those 37 signatures. Four are forced; 27 other types remain.
4. Any separating family of at most nine questions can be extended to nine while including the four forced columns. Duplicate column types cannot add a distinction. Thus it suffices to check the 27 choose 5 = **80,730** five-type completions. Every one fails to distinguish at least one original pair.
5. The displayed ten-question witness separates all 666 pairs. Therefore the minimum is exactly ten.

The full 48-front artifact has SHA-256:

`12bf5ebe0e1be9ea15b3057f9e111db50a94af714668f67d04c027cffeb7cdff`

The published reproducer regenerates the 48 fronts from first principles and verifies this digest, the 37 classes, the 80,730 excluded nine-question combinations, the ten-question witness, and all five two-candidate covers.

## 4. Independent verification and boundaries

Three separate authorized machines computed the bounded R19 check: vectorized/integer-optimization construction, exact combination enumeration, and an independent set-based verification. A further standalone Python reproducer ran successfully on all three. Their internal evidence was exchanged on an existing authenticated private network by content-addressed SHA-256 readback.

These are computation and reproducibility results only. They imply **no physical measurement**, no universal algorithmic advantage, no novel mathematical method, no peer review, no patent determination, and no right to disclose unrelated private archives.

Only this standalone synthetic description and its self-contained reproduction code are intended for public display. Private peer addresses, local paths, credentials, unreleased manuscripts, and private evidence receipts are excluded. The reproduction code does not access a network or execute remotely.

**AI disclosure:** AI assistance was used in drafting and coding this synthetic benchmark. Executions and independent cross-checks were performed on authorized user-owned machines.

## 5. Prior art

The mathematical method is an instance of the established *minimum test set / test collection* problem, not an assertion of discovering that problem:

- Moret and Shapiro, *On Minimizing a Set of Tests*, SIAM, https://doi.org/10.1137/0906067
- Gutin, Muciaccia and Yeo, *(Non-)existence of Polynomial Kernels for the Test Cover Problem*, https://arxiv.org/abs/1204.4368

Related prior bounded study: [Omega Web R17 research note](https://github.com/tardifmorencytristan-glitch/tristan-proof/blob/07249359dbdd2b8af2d4a065f6a8a72e665dae94/research/omega-web-r17-bounded-validation-20261019.md).

**Reproduce:** `python r19_public_reproduce.py` (Python standard library only). A successful run prints `EXACT_FINITE_SYNTHETIC_PASS`. Rerunning this test does not authorize any real-world application or external publication.