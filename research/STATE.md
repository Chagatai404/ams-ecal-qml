# AMS ECAL QML — Current Research State

_Last human review: 2026-09-20_

## Central research question

Can multiscale and multifractal representations of AMS-02 ECAL showers expose physically meaningful differences between electromagnetic showers and proton-induced hadronic showers, and can those representations improve classical or quantum particle classification?

## Immediate research question

**RQ-001**

> Do electron/positron and proton showers exhibit measurably different effective multifractal structure in AMS ECAL after controlling for primary energy and incidence geometry?

## Current hypothesis

**H-001 — E0**

Electromagnetic and proton-induced showers produce different scale-dependent spatial energy distributions in AMS ECAL, measurable through quantities such as generalized dimensions \(D_q\), partition-function scaling \(\tau(q)\), multifractal spectra \(f(\alpha)\), and/or lacunarity.

This is currently a hypothesis, not an established AMS result.

## Null / competing explanation

Observed differences in estimated multifractal quantities may be explained by:

- primary-energy differences,
- incidence-angle differences,
- finite ECAL granularity,
- thresholds or noise,
- patch/preprocessing choices,
- longitudinal leakage,
- ordinary shower-width/depth differences rather than independent multiscale information.

## Current evidence level

**E0 — idea / literature-motivated hypothesis**

Related calorimeter literature supports studying fractal or multiscale shower observables, but the AMS-specific hypothesis has not yet been demonstrated in this repository.

## Current development state

Completed foundation notebooks:

- `00_ecal_calorimetry_and_geometry.ipynb`
- `01_tracker_state_and_projection.ipynb`
- `02_readout_orientation_and_cell_mapping.ipynb`
- `03_canonical_event_model.ipynb`
- `04_ecal_geometry_fidelity.ipynb`

The next research notebook should be hypothesis-driven rather than another generic implementation block.

Candidate next notebook:

```text
notebooks/05_shower_multifractal_characterization.ipynb
```

Reusable estimators should live in source code, e.g.:

```text
src/ams_ecal/multifractal.py
```

with tests in:

```text
tests/test_multifractal.py
```

## Immediate learning dependencies

Before interpreting multifractal results, the researcher should be able to explain and reconstruct:

1. scaling laws and log-log slopes;
2. box-counting dimension;
3. probability measures on a spatial partition;
4. Rényi entropy / generalized dimensions;
5. partition function \(Z_q(\epsilon)\);
6. \(\tau(q)\) and \(D_q\);
7. the \(q \to 1\) information-dimension limit;
8. multifractal spectrum \(f(\alpha)\);
9. lacunarity;
10. finite-size / finite-resolution bias.

## Planned first experiment

**EXP-001 — controlled FastMC multifractal baseline**

Goal:

Estimate simple multiscale observables for electron and proton shower samples while controlling primary energy and geometry.

Minimum outputs:

- \(D_0\)
- \(D_1\)
- \(D_2\)
- selected \(Z_q(\epsilon)\) curves
- lacunarity
- scale-fit diagnostics
- uncertainty / estimator stability
- electron-versus-proton distributions stratified by energy

Do not begin neural-architecture optimization until the observables themselves are validated.

## QML status

QML remains in scope, but it is downstream of the physics characterization.

Current intended sequence:

```text
multifractal hypothesis
→ validate observables
→ classical statistical/ML baselines
→ test information added beyond conventional shower variables
→ QML/QCNN comparison on a justified representation
```

No quantum advantage is assumed.

## Candidate later hypotheses

- Multifractal observables contain particle-ID information conditional on conventional shower variables.
- A geometry-aware GNN plus multiscale branch improves robustness/generalization.
- A QCNN-style hierarchy is a useful inductive bias for scale-dependent shower structure.
- A compact multifractal representation provides a principled low-dimensional input for VQC or quantum-kernel experiments.

These remain candidate ideas until separately promoted to hypotheses.

## Established project conventions

- AMS-specific detector values should default to official AMS sources unless a peer-reviewed AMS source explicitly supersedes them.
- Software design should keep detector/model constants configurable so updated values can be substituted without redesign.
- Reusable physics/numerical logic belongs in tested source code rather than notebook-only cells.
- Learning and comprehension are part of the research workflow, not a separate afterthought.

## Open scientific questions

- Is the AMS ECAL scale range large enough for stable multifractal estimation?
- Which \(q\) values are numerically meaningful at AMS granularity?
- How much do \(D_q\) estimates depend on energy?
- How should alternating X/Y views be incorporated into scale partitions?
- Should scaling be measured globally, per view, per depth window, or all three?
- How large is finite-resolution bias?
- Do multifractal observables add information beyond shower width, depth, and energy concentration?
- What is the correct fair baseline for a later quantum model?

## Next human decision

Approve the mathematical definition and estimator design for the first multifractal observables before implementation.
