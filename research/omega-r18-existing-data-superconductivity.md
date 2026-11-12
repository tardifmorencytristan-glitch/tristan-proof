# Ω-MULTI-TRISTAN R18: existing experimental data, independent finite verification

**Status: reproducible finite data analysis, not a claim of new physics.** Date: 2026-10-19.

## Source and attribution

Hamidieh, K. (2018), *Superconductivty Data*, UCI Machine Learning Repository, dataset DOI [10.24432/C53P47](https://doi.org/10.24432/C53P47), under CC BY 4.0. The associated paper is [10.1016/j.commatsci.2018.07.052](https://doi.org/10.1016/j.commatsci.2018.07.052). This dataset contains historical records of **21,263 known superconductors**, 81 numeric descriptors, and the material formula in an accompanying file. It **does not** include non-superconductor examples and is insufficient to prove a new material is superconducting.

Official ZIP SHA-256: `87f4490d73390ff94ee01dbf0d7d32abc80b22f2c803d471765cfc46a9f6371e` (8,300,005 bytes).
Identical bytes retrieved on two independent devices via HTTPS; a third received the digest-matched archive over authenticated private transport after encountering a TLS certificate problem (no TLS verification bypass).

## Verified finite Pareto experiment

- 21,263 rows, **15,542 distinct material-formula strings**; the difference is 5,721 excess rows beyond unique formulas. This matters when making train/test splits.
- 48 Pareto fronts spanning 3 populations (all, <=4 elements, >=5 elements), 2 exploratory temperature directions (maximize/minimize), 2 atomic-mass descriptors and 4 objective subsets.
- A selected 3-objective high-`Tc` front had 4 entries. Its size was compared descriptively with 64 deterministic temperature permutations (mean 15.765625); the permutation control alone does not support a novel physical interpretation.
- Canonical front JSON SHA-256: `ed24b8acbfeaee683670aa028f7e906529f62807df5bf3d0867ebf9b34707f05`.
- One machine reproduced the source computation; an independent implementation verified nondominance and dominance coverage for **all 48** fronts, including **680,172** excluded candidate-context memberships.
- The criteria `number_of_elements` and mean atomic mass are **proxies** for composition complexity and mass, not price or practical manufacturability.

## Group-locked predictive comparison

For each formula `f`, the split is `int(sha256("TRISTAN_R18_20261019|"+f)[:12],16)%10`; buckets 0-1 are test, 2-3 validation, and 4-9 training. Duplicate formulas never appear on opposite sides of the split.

- Train: 12,563 rows; validation: 4,380; test: **4,320**, representing 3,081 distinct formula strings.
- Baseline constant prediction: MAE 29.083 K, RMSE 34.084 K.
- Standardized ridge on 81 supplied features: MAE **13.561 K**, RMSE **17.763 K**.
- Standardized ridge on 81 supplied features plus their signed `log1p(abs(x))` transforms (162 features): MAE **12.765 K**, RMSE **16.875 K**.
- Fixed regularization grid `{10,100,1000}`, selected by validation RMSE; both methods selected 10. The test set was held out.
- Observed MAE improvement: **0.796 K**, or approximately **5.87% relative to the raw-feature ridge**; composition-cluster bootstrap 95% interval **[0.586, 0.974] K** using 300 resamples.
- Independent numerical verification with augmented least-squares (`numpy.linalg.lstsq`) reproduced both models' test metrics. This independently checks the linear algebra, but is **not** another prospective validation dataset.

**Interpretation:** nonlinear feature engineering improved a linear predictor in this single historical dataset and fixed split. It does **not** validate fractal, mycelial, tensor or hypercomplex physical fields. Published studies include much stronger models on other data/splits; cross-study headline errors are not directly comparable. For context: [Jung et al. (2024)](https://doi.org/10.1021/acs.jcim.4c01137), [Hamidieh (2018)](https://arxiv.org/abs/1803.10260).

## Reproduction

Download the original source archive from UCI; the data are **not republished** here.

```bash
python research/r18/r18_pareto.py --archive superconductivity.zip --preregister research/r18/R18_PREREGISTER.json --output repro
python research/r18/r18_predictive.py --archive superconductivity.zip --output repro
```

Python 3 and NumPy are required for the predictive script; the Pareto script uses only Python's standard library.

## Boundary conditions and next falsification

1. Replicate on the independently curated NIMS SuperCon release (e.g. DOI [10.48505/nims.4487](https://doi.org/10.48505/nims.4487)) with source/pressure/time stratification and composition de-duplication.
2. Compare to nonlinear reference models, repeated formula-group holdouts and out-of-distribution material-family splits.
3. Separately operationalize the proposed theory's measurable variables. A feature transformation is not evidence that the physical concepts represented by a theory exist.
4. Keep all unsanitized private manuscripts, code, machine data and credentials out of public distribution.

The experiment and scripts may inform further **private** scientific exploration. No physical discovery, synthesis feasibility, production deployment, public Web ingress, permanent auto-publisher or autonomous Git merge is claimed.

Decision gates: `VERIFIED_FINITE_DATA_ANALYSIS`, `PUBLIC_SANITIZED_RESEARCH_NOTE`; `HOLD` for new physical claims and automated deployment.
