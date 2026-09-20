# AMS ECAL Research — Current Research State

_Last human review: 2026-09-21_

## Central research question

What physically meaningful multiscale information in electromagnetic and
proton-induced showers survives AMS-02 ECAL-like readout, how much does it add
beyond conventional calorimeter observables, and can that validated structure
later motivate useful classical or quantum inductive biases?

The accepted program order is:

```text
establish shower structure
→ test detector survival
→ quantify information content
→ classical ML benchmarks
→ QML on validated structure
```

## Immediate research question

**RQ-001**

> To what extent do electromagnetic and hadronic particle showers exhibit
> discriminative multiscale spatial structure, how much of this structure
> survives AMS-02 ECAL-like segmentation, and what information does it
> contribute to electron/positron-versus-proton classification beyond
> conventional calorimetric observables and standard ML representations?

See:

`research/questions/RQ-001_multiscale_shower_information.md`

## Current hypothesis

**H-001 — E0**

Electron/positron and proton-induced showers may produce different
scale-dependent spatial energy distributions that remain measurable after
finite detector readout.

Candidate observables include:

- generalized dimensions `D_q`;
- partition-function scaling `tau(q)`;
- multifractal-spectrum summaries where justified;
- lacunarity;
- entropy/concentration across scale;
- occupancy and energy moments under coarse-graining.

This remains a hypothesis.

The project does **not** currently claim that AMS showers are mathematical
fractals, that a stable multifractal spectrum exists, or that AMS granularity is
sufficient to resolve one.

## Null / competing explanations

Apparent multiscale differences may instead arise from:

- energy mismatch;
- incidence-angle mismatch;
- containment or boundary effects;
- ordinary shower width/depth differences;
- longitudinal leakage;
- finite segmentation;
- thresholds/noise;
- preprocessing choices;
- unstable finite-resolution estimators;
- simulator artifacts.

## Current evidence level

**E0 — literature-motivated AMS-specific research hypothesis**

Real highly granular calorimeter studies motivate fractal-sensitive shower
analysis, but the hypothesis has not yet been established for AMS-02 ECAL-like
readout in this project.

---

# Accepted publication direction — 2026-09-21

The first intended publication is now a **multiscale shower-information study**,
not a QML benchmark.

Paper 1 will ask whether scale-dependent/fractal-sensitive shower structure:

- exists robustly in detailed electron/proton transport;
- survives AMS-like segmentation;
- contains information beyond conventional shower variables;
- improves or changes classical ML behavior, especially in low-data regimes.

FastMC is a smooth phenomenological simulator and control. Because its
longitudinal/lateral parameterizations intentionally replace microscopic
branching with smooth distributions, FastMC alone cannot establish or falsify
microscopic fractal/multifractal shower structure.

The decisive simulation chain for RQ-001 is:

```text
fine-grained Geant4
→ same events projected to AMS-like 18 × 72
→ multiscale-preservation analysis
→ FastMC smooth-control comparison
→ classical information / ML study
```

QML is deliberately downstream.

Paper 2+ will test quantum architectures only after Paper 1 establishes what
multiscale structure exists, survives readout, and is useful.

See:

`research/PUBLICATION_ROADMAP.md`

---

# Conceptual research framing

The project distinguishes:

- **multiscale/fractal-sensitive shower structure:** active physics question;
- **deterministic chaos:** adjacent mathematical direction, not currently an
  AMS shower claim;
- **QML:** a later computational method that may exploit validated structure,
  not evidence that the physical structure exists.

The project must not infer deterministic chaos from branching, irregularity, or
visual complexity.

See:

`research/CHAOS_FRACTALS_QML.md`

---

# Current development state

Stage II FastMC Blocks 0–5 are complete.

The repository currently contains:

- structured AMS-02 ECAL geometry;
- tracker projection;
- alternating ECAL readout mapping;
- canonical `ECALEvent`;
- deterministic longitudinal EM gamma profile;
- deterministic lateral EM profile;
- explicit finite-depth longitudinal leakage;
- explicit finite-width lateral leakage;
- deterministic track-centered `18 × 72` lateral fractions.

Current FastMC notebooks:

- `00_ecal_calorimetry_and_geometry.ipynb`
- `01_tracker_state_and_projection.ipynb`
- `02_readout_orientation_and_cell_mapping.ipynb`
- `03_canonical_event_model.ipynb`
- `04_ecal_geometry_fidelity.ipynb`
- `05_longitudinal_em_shower.ipynb`
- `06_lateral_em_shower.ipynb`

## Next engineering target

**Block 6A — stochastic electromagnetic event generation**

The physical model is accepted.

Implementation should begin from the accepted model rather than reopening the
full fluctuation literature unless new evidence materially contradicts it.

---

# Accepted evidence and decisions — Block 6

## Mean longitudinal model

The mean longitudinal profile is a gamma distribution with:

```text
T = (alpha - 1) / beta
```

so:

```text
alpha = 1 + beta*T
```

For the AMS ECAL implementation:

```text
beta = 0.65
T(E) = ln(E / E_c) - 0.5
```

The `-0.5` offset corresponds to the electron **energy-deposition** maximum,
not the older Rossi Approximation-B electron-number maximum.

The published AMS longitudinal form is algebraically consistent with the
current implementation.

## Beta provenance

`beta = 0.65` has peer-reviewed AMS provenance.

AMS fits shower parameters on observed showers while keeping the detector-
specific scale parameter fixed at `b = 0.65`.

The project therefore keeps beta fixed in the first stochastic FastMC model.

## Origin convention

The accepted Block 6A baseline is **detector-entry referenced**.

Do not sample an explicit shower-start depth in the first model.

A first-bremsstrahlung-relative alternative may remain architecturally possible
for later Geant4 comparison, but it is not part of the baseline.

## Accepted Block 6A stochastic model

For each event:

```text
T_bar(E) = ln(E / E_c) - 0.5

s(E) =
    1 / (-2.5 + 1.25 * ln(E / E_c))

mu(E) =
    ln(T_bar(E)) - 0.5 * s(E)^2

ln(T0) ~ Normal(mu(E), s(E)^2)

alpha_event =
    1 + 0.65 * T0
```

Then:

1. integrate the gamma profile over the 18 finite readout intervals;
2. convert fractions to stochastic layer energies;
3. distribute each layer energy using the existing deterministic lateral
   profile;
4. preserve longitudinal and lateral leakage;
5. produce an `ECALEvent` with explicit RNG provenance.

### Provenance of the fluctuation width

The `ln(T)` width law is a **transferred approximation** from Grindhammer &
Peters' sampling-calorimeter parameterization.

It is not an AMS-specific fitted fluctuation law.

This is accepted because FastMC is deliberately a simple phenomenological
generator whose adequacy will later be tested against Geant4.

### Explicitly excluded from Block 6A

- fluctuating beta;
- explicit shower-start sampling;
- independent per-layer random draws;
- a two-variable `(T, alpha)` fluctuation model;
- a new stochastic lateral model;
- microscopic transport;
- attempts to uniquely decompose every latent variance source.

## Acceptance philosophy

FastMC only needs to be:

- fast;
- reproducible;
- physically defensible;
- free of obvious simulator artifacts;
- realistic enough for controlled downstream benchmarks;
- transparent about transferred approximations.

The definitive test of whether a simplification matters is later comparison
against detailed transport and, where possible, real detector/test-beam
information.

---

# Block 7 status

Detector response remains planned.

Potential effects:

- sampling / visible-energy response;
- noise;
- thresholds;
- gains;
- saturation;
- dead channels;
- calibration effects.

Because some AMS shower parameters were fitted to observed deposits, overlap
with later response modeling must be watched for possible double counting.

This is a Block 7 concern, not a Block 6A blocker.

---

# Block 8 status

FastMC dataset generation and validation remains planned.

Dataset validation must include:

- energy/geometry matching between classes;
- seed isolation;
- split integrity;
- containment/leakage checks;
- response distributions;
- absence of accidental label leakage.

---

# RQ-001 / multiscale direction

## First decisive experiment

**EXP-001 — detailed-transport multiscale preservation study**

FastMC is not the physical evidence source for RQ-001.

Minimum comparison:

1. fine-grained Geant4 shower deposits;
2. the same events projected to the canonical `18 × 72` representation;
3. FastMC as a smooth phenomenological control.

Interpretation:

- signal in fine Geant4 but not AMS projection:
  detector segmentation removes the relevant scales;
- signal in fine Geant4 and AMS projection but not FastMC:
  FastMC masks physically accessible multiscale structure;
- comparable relevant observables in projected Geant4 and FastMC:
  FastMC preserves enough structure for that tested purpose.

Ordinary agreement in mean profile, containment, or energy resolution does not
answer this question.

## Candidate multiscale observables

Only after estimator validation:

- `D_0`, `D_1`, `D_2`, selected `D_q`;
- `Z_q(epsilon)`;
- `tau(q)`;
- multifractal-spectrum summaries where scale support is adequate;
- lacunarity;
- entropy/concentration;
- occupancy/energy moments under controlled coarse-graining.

## Open questions

- Is the accessible AMS-like scale range large enough for stable estimation?
- Which `q` values are numerically meaningful?
- How should alternating X/Y views be handled?
- Should scaling be measured globally, per view, per depth range, or all three?
- How large is finite-resolution bias?
- Do multiscale observables add information beyond shower depth, width,
  containment, and energy?
- Can raw ML learn the same structure implicitly?
- Does explicit multiscale information improve low-data/sample efficiency?

---

# QML status

QML remains in scope as a later publication-level stage.

Accepted order:

```text
detailed transport
→ validate multiscale observables
→ test AMS-readout survival
→ conventional + multiscale classical analysis
→ raw classical ML controls
→ QML/QCNN on a justified representation
```

Candidate future directions:

1. compact validated multiscale inputs for VQCs or quantum kernels;
2. QCNNs as candidate hierarchical/multiscale inductive biases;
3. scale-structured Hamiltonian embeddings;
4. detector-topology-aware quantum connectivity.

No quantum advantage is assumed.

---

# Established project conventions

- AMS-specific detector facts should default to official AMS/collaboration
  sources or peer-reviewed AMS publications.
- Scientific constants and model parameters remain configurable.
- Reusable physics/numerical logic belongs in tested source code.
- Notebooks are for derivation, teaching, visualization, and validation.
- Hypothesis-sensitive literature discovery should be independent of existing
  implementation assumptions when practical.
- Cross-validation means independent reconstruction/reproduction rather than
  agreement checking.
- The human researcher is the final authority on accepted assumptions,
  hypotheses, and conclusions.
- Fractal/multifractal structure may be tested directly; deterministic chaos
  may not be claimed without a justified dynamical-system formulation.

---

# Next session — start here

1. Implement Block 6A from the already accepted stochastic model.
2. Keep beta fixed at `0.65`.
3. Keep the first implementation detector-entry referenced.
4. Use one stochastic `T0` rather than independent per-layer noise.
5. Reuse the existing longitudinal and lateral integration code.
6. Preserve RNG/configuration provenance.
7. Add tests for positivity, reproducibility, leakage, finite outputs, and
   ensemble behavior.
8. Build the Block 6 teaching/validation notebook only after reusable tested
   code exists.
9. Keep the multiscale/fractal investigation as a parallel learning/research
   track until the Geant4 detailed-transport stage.

## Next human decision

No additional longitudinal-physics decision is required before Block 6A
implementation.

The next substantial scientific decisions will concern:

- Block 6B proton phenomenology;
- Block 7 detector response;
- Geant4 detailed-transport design for RQ-001.
