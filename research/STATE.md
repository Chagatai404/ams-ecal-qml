# AMS ECAL QML — Current Research State

_Last human review: 2026-09-20_

## Central research question

Can multiscale and multifractal representations of AMS-02 ECAL showers expose physically meaningful differences between electromagnetic showers and proton-induced hadronic showers, and can those representations improve classical or quantum particle classification?

## Conceptual research framing

The current research direction grew out of a broader investigation of chaos theory, fractal geometry, criticality, and quantum machine learning.

The key project distinction is:

- **Fractal / multifractal structure:** directly relevant active AMS hypothesis.
- **Deterministic chaos:** adjacent mathematical research area, not currently a claim about shower dynamics.
- **QML:** computational method that may later exploit a validated multiscale representation; not evidence that the physical hypothesis is true.

The detailed framing and long-term research tree are recorded in:

```text
research/CHAOS_FRACTALS_QML.md
```

The project must not infer chaos merely from branching, irregularity, or visual complexity.

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

**Stage II FastMC Blocks 0–5 are complete on `main`.**

The repository now contains:

- detector/calorimetry foundation;
- tracker projection and alternating ECAL readout mapping;
- canonical `ECALEvent` representation;
- geometry-fidelity validation;
- deterministic mean longitudinal electromagnetic shower model;
- deterministic mean lateral electromagnetic shower model;
- finite-depth longitudinal leakage;
- finite-width measured-coordinate lateral leakage;
- tracker-centered deterministic `18 × 72` lateral-fraction representation.

Current FastMC notebooks include:

- `00_ecal_calorimetry_and_geometry.ipynb`
- `01_tracker_state_and_projection.ipynb`
- `02_readout_orientation_and_cell_mapping.ipynb`
- `03_canonical_event_model.ipynb`
- `04_ecal_geometry_fidelity.ipynb`
- `05_longitudinal_em_shower.ipynb`
- `06_lateral_em_shower.ipynb`

The latest FastMC work was merged to `main` on 2026-09-20.

### Next engineering target

**Block 6A — stochastic electromagnetic event generation** (6B, proton phenomenology, is a separate
later design problem and must not be mixed into the first electromagnetic patch)

The immediate engineering problem is to introduce physically meaningful event-to-event shower fluctuations with reproducible random-number control while preserving the validated deterministic mean longitudinal and lateral behavior.

Before implementation, the physics of the fluctuation model must be understood and sourced.

Key Block-6 questions include:

- Which shower quantities should fluctuate event-to-event?
- Which fluctuations are correlated rather than independent?
- How should generated ensembles recover the deterministic mean models?
- What stochastic approximations are defensible for electrons/positrons?
- What phenomenological approximations, if any, are defensible for proton-event diversity without pretending to be full hadronic transport?
- Where should RNG ownership, seeds, and stochastic configuration live in the software architecture?
- Which invariants must remain true for every generated event?

Detector response/digitization remains Block 7, and validated FastMC dataset generation remains Block 8.

## Parallel learning / research track — multifractal shower structure

The multifractal direction remains active, but it does **not** replace the FastMC sequence.

The intended parallel progression is:

```text
FastMC foundation                  Multifractal learning
-----------------                  ----------------------
Block 6 stochastic events          scaling laws
Block 7 detector response          box-counting dimension
Block 8 validated datasets         D0, D1, D2
                                   Z_q(epsilon), tau(q)
                                   f(alpha)
                                   lacunarity
                                   finite-resolution bias
              \                    /
               \                  /
                controlled multifractal study
```

Do not implement specialized multifractal estimators or neural architectures merely because the hypothesis is interesting. First learn and verify the mathematics, then define and validate estimators on controlled cases.

## Broader chaos / fractal learning track

A longer learning roadmap is kept because it may later support other research directions:

```text
logistic map
→ bifurcations
→ Lyapunov exponents
→ Sharkovskii / Li–Yorke chaos
→ Hausdorff and generalized fractal dimensions
→ strange attractors
→ ergodic theory
→ spatiotemporal chaos
→ quantum chaos
```

For the immediate AMS study, the relevant subset is:

```text
scaling laws
→ fractal dimension
→ generalized dimensions
→ multifractals
→ finite-resolution estimation
→ multiscale representation learning
```

Chaos diagnostics are not a prerequisite for the first AMS multifractal experiment.

## Immediate learning dependencies

### For Block 6

Before approving the stochastic generator design, the researcher should understand:

1. expectation versus an individual random realization;
2. variance and covariance;
3. independent versus correlated fluctuations;
4. probability distributions used for positive / constrained quantities;
5. reproducible pseudorandom-number generation and seed ownership;
6. how a stochastic model should reproduce a validated deterministic mean;
7. what shower fluctuations are physically motivated by calorimeter literature.

### For the multifractal track

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

## Planned first multifractal experiment

**EXP-001 — controlled FastMC multifractal baseline**

This experiment is planned for after the event generator and dataset path are sufficiently validated to produce meaningful event populations.

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

### Candidate QML mechanisms

These are research hypotheses, not accepted design choices:

1. **Compact multifractal quantum input**
   - use validated multiscale observables as a principled low-dimensional representation for VQC / quantum-kernel experiments.

2. **QCNN as a multiscale inductive bias**
   - test whether hierarchical convolution/pooling is useful for scale-dependent shower information;
   - compare against matched classical hierarchical controls.

3. **Scale-structured Hamiltonian embedding**
   - revisit geometry-based couplings with local/intermediate/global interaction scales rather than arbitrary circuit connectivity.

4. **Quantum chaos / quantum reservoir computing**
   - maintain as a separate future direction;
   - do not mix into the initial AMS multifractal study without a clear independent research question.

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
- AI providers have no fixed project roles; the human researcher assigns the task role for each session.
- For substantial work, prefer one primary agent at a time; use another agent later for independent verification, reproduction, or review when useful.
- Multiple agents should not perform substantial writes in the same worktree at the same time.
- Hypothesis-sensitive literature discovery should be performed independently of implementation assumptions before repository reconciliation.
- Cross-validation means independent reconstruction, verification, or reproduction rather than agreement checking.
- The human researcher is the convergence point and decides what is accepted or merged.
- Fractal/multifractal structure may be tested directly; deterministic chaos may not be claimed without an explicitly defined dynamical system and valid diagnostic.

## Accepted evidence and decisions — Block 6

_Added 2026-09-20 after a learning session, an independent literature-discovery pass, and an
independent source-verification pass. Full record: Obsidian evidence map "EM Shower Fluctuations in
Sampling Calorimeters" and tutor session "AMS FastMC Block 6"._

### Externally established in the relevant regime

- The mean longitudinal profile is a gamma distribution whose maximum lies at `(a-1)/b`. Our
  `alpha = 1 + beta*T` construction is exactly this identity rearranged, so the profile peak sits at
  the predicted shower maximum by construction. Verified against PDG 2025 Eq. (34.35) and Leroy &
  Rancoita (2000) Eq. (12).
- **The shower-maximum offset convention is pinned.** For the *energy-deposition* profile,
  `C_e = -0.5` and `C_gamma = +0.5`. Both PDG 2025 Eq. (34.36) and Leroy & Rancoita Eqs. (12)-(13)
  give this. The older `C_e = -1.0`, `C_gamma = -0.5` constants belong to Rossi's Approximation B for
  the *electron-number* maximum, a different observable, and PDG regards them as superseded. Our
  `shower_max_offset_x0: -0.5` paired with an energy-deposition gamma profile matches both sources.
  **Risk to avoid:** mixing an Approximation-B offset with an energy-deposition profile would cost
  about 0.5 X_0 (~5 mm here), and the two treatments appear in the same paper.
- Longitudinal shape parameters fluctuate and are **correlated**. A Block 6 generator must reproduce
  that correlation; independent per-layer draws are physically wrong.
- The definition of shower origin is a genuine modelling degree of freedom - existing fast-simulation
  implementations differ, anchoring either at first bremsstrahlung or at calorimeter entry.
- The gamma form is documented to fail in roughly the first two radiation lengths, and that region
  was excluded when the parameterization was fitted (PDG 2025 p. 28, verbatim). AMS cites the PDG
  for the functional form itself, so the caveat attaches to the same form AMS adopted; whether AMS
  excluded that region when determining b is unknown.
- **`gamma_rate: 0.65` has peer-reviewed provenance.** M. Aguilar et al., Physics Reports 894 (2021)
  1-116, section 1.7.1: "In the AMS ECAL, we found that the scale parameter b is constant
  (b = 0.65)." Primary reconstruction source: A. Kounine, Z. Weng, W. Xu, C. Zhang, NIM A 869 (2017)
  110-117, DOI 10.1016/j.nima.2017.07.013 - exact locator not yet extracted.
- **The published AMS longitudinal form is algebraically identical to our implementation.** AMS
  Eq. (2) has exponent bT0, giving alpha = 1 + b*T0 and normalization Gamma(bT0 + 1), which is
  exactly `AMSLongitudinalGammaModel.shape_parameter`. Our construction is the published form, not
  an approximation of it.
- **AMS fits T0 per individual shower; we predict it from energy.** AMS obtains E0 and T0 from a fit
  to observed depositions per shower. That AMS treats T0 as a free per-shower parameter is direct
  evidence that T0 varies event to event, which is the Block 6 quantity; the distribution of fitted
  T0 at fixed energy is an empirical target for the stochastic model. Our predicted-T approach is a
  forward-generation choice and should not be conflated with the AMS reconstruction procedure.

### Not established — deliberately not modelled as physics

- That an explicit shower-start fluctuation is *required* for an accurate AMS-02 ECAL FastMC.
  Entry-anchored modelling demonstrably works, and AMS reconstruction succeeds without an explicit
  start variable.
- That shower-start motion is what prevents orthogonalizing the fluctuation sources. No source
  establishes this for electromagnetic calorimeter showers; **dropped from the evidence base.**

### Accepted decision — Block 6 origin convention

- The first stochastic implementation is **entry-referenced**. `shower_start_depth_x0` is **not**
  sampled.
- The architecture must nonetheless be able to represent the alternative: a longitudinal fluctuation
  model carrying an `origin_convention` of `"detector_entry"` or `"first_bremsstrahlung"`, with
  `shower_start_depth_x0: float | None` held in **internal generated-shower state**, not in the
  public `ECALEvent` schema.
- First-interaction-relative generation is activated only when justified by an AMS-specific source
  or by our own Geant4 reference simulation, without restructuring the simulator.
- **Graduation criterion (amended 2026-09-21, three tiers, passed in order).** An adversarial review
  showed the original single-ablation form was symmetric between the two candidates and could not
  discriminate them.
  1. **Internal stochastic consistency** - ensemble mean, containment, 18-layer covariance, T_0
     distribution, early-layer occupancy and longitudinal leakage reproduce the chosen reference
     parameterization. Necessary, but symmetric between candidates, so it discriminates nothing.
  2. **Identifiability stress test** - across several widely separated energies, cross-fit each
     generator against the synthetic data of the other under shared energy-scaling laws and
     determine which observables, if any, discriminate them. If none do, the ablation cannot choose,
     and that is itself the result.
  3. **Physical graduation** - an explicit start-depth degree of freedom becomes the preferred
     physical model only once an asymmetric external reference (event-level Geant4 truth, suitable
     test-beam information, or equivalent) shows it improves the *conditional structure* rather than
     merely *repartitioning variance*.

  Until a Tier 3 reference exists, entry-anchored remains the baseline and first-bremsstrahlung
  remains an architecturally supported alternative.

### ACCEPTED — Block 6A electromagnetic stochastic model (2026-09-21)

Accepted by the human researcher after four evidence passes. Implementation begins 2026-09-22.

**The model.** For each event, at fixed `beta = 0.65`:

```text
T_bar(E) = ln(E / E_c) - 0.5                       mean shower maximum, X_0
s(E)     = 1 / (-2.5 + 1.25 * ln(E / E_c))         lognormal width of ln(T0)
mu(E)    = ln(T_bar(E)) - 0.5 * s(E)^2             centering so E[T0] = T_bar(E)
ln(T0)   ~ Normal(mu(E), s(E)^2)
alpha_ev = 1 + 0.65 * T0
```

then integrate the existing gamma profile over the 18 finite depth intervals, and distribute each
stochastic layer energy with the **existing deterministic** lateral cell fractions around the
projected track.

**Explicitly excluded from 6A:** fluctuating beta; an explicit shower-start variable; a two-variable
correlated (T, alpha) model; any new lateral fluctuation model; microscopic transport; any attempt
to uniquely identify hidden physical variance components.

**Provenance of the width law — transferred approximation.** Verified verbatim in Grindhammer &
Peters, Appendix A.2.3 "Fluctuated longitudinal profiles", sampling-calorimeter variant. Three
qualifications recorded deliberately:

1. The same equation line also publishes `sigma(ln alpha_sam) = 1/(-0.82 + 0.79 ln y)` and
   `rho(ln T, ln alpha) = 0.784 - 0.023 ln y`. Fixing beta drops that second degree of freedom.
2. **Quantified consequence:** because alpha is fully determined by T0, we generate about **61% of
   the published shape-parameter spread**, near-constant in energy, with correlation forced to 1
   where the reference has rho ~ 0.51-0.62. Accepted because b = 0.65 is AMS's own detector-specific
   measurement, and therefore better evidence for this calorimeter than a generic sampling law.
   Recorded as a known deviation for later Geant4 comparison, not an unnoticed one.
3. **Origin-convention transfer:** Grindhammer anchors T at first bremsstrahlung; we anchor at
   detector entry. Entry-anchored T0 additionally contains first-interaction-depth spread, so this
   width most likely *underestimates* ours. Magnitude unknown. The F_S sampling corrections in that
   appendix apply to the means, not to sigma, so the width transfers more cleanly than the mean.

**External sanity check, AMS test beam at ~250 GeV** — a check, never a calibration target, because
the reported values include reconstruction and detector effects:

| | model | reported | difference |
|---|---|---|---|
| RMS shower maximum | 0.945 X_0 | 0.9669 X_0 | -0.022 (about 2%) |
| mean shower maximum | 9.901 X_0 | 8.851 X_0 | +1.05 |

The mean offset is in a physically expected direction: Grindhammer section 3.3 states the signal
maximum in a sampling calorimeter occurs *earlier* than in a homogeneous calorimeter of the same
effective material, because e/mip falls with depth, while our T_bar comes from the PDG
homogeneous-style relation. Recorded as a documented ~1 X_0 offset relevant to Block 7 and to
early-layer comparisons.

**Acceptance philosophy for 6A.** A mixture of stochastic gamma profiles need not reproduce the
deterministic Block-4 profile point by point. The checks that matter are reproducibility;
positivity; sensible shower diversity; correct mean scale; realistic longitudinal spread; coherent
layer-to-layer correlation; leakage remaining explicit; no simulator artifacts or label leakage;
rough consistency with known AMS/test-beam quantities; and eventual Geant4 comparison. The
identifiability and latent-variable-recovery tests explored earlier are **not** 6A blockers.

### Provisional decision — pending literature

- Sampling fluctuation belongs to **Block 7**, not Block 6: the cascade develops through the whole
  lead + fibre composite and does not know which material is instrumented, so energy deposited in
  passive lead is shower physics while reading out only the fibres is a construction choice. Still
  **provisional**, and the reason is now sharper rather than resolved: because AMS fits b to observed
  depositions, some detector behaviour is already inside Blocks 4-5, so a Block 7 sampling model
  risks double-counting it. The boundary is right in principle; the partition is not yet quantified.

## Open scientific questions

### Block 6

Settled during the 2026-09-20 learning and literature session (see Accepted evidence below):

- ~~How should stochastic events be validated against the deterministic mean model?~~ The ensemble
  average must converge to the validated deterministic profile. Blocks 4-5 become the oracle for
  Block 6 rather than being replaced by it.
- ~~Which fluctuations must be correlated across depth?~~ Longitudinal shape parameters fluctuate
  and are correlated; a generator must reproduce that. Independent per-layer draws are excluded.

Still open:

- What stochastic shower fluctuations are required for a useful FastMC baseline? Specifically, which
  distributions are defensible for the positive/constrained quantities involved.
- Which transverse fluctuations must be correlated, and with what longitudinal coupling? The
  literature reports no first-principles theory for transverse-longitudinal coupling.
- Which proton fluctuations can be modeled phenomenologically without overstating physical fidelity?
- **How much detector behaviour is already absorbed into `gamma_rate: 0.65`?** Provenance is now
  settled (see Accepted evidence). The live question is quantitative: AMS fits the individual shower
  parameters to *observed* cell depositions, so b characterizes measured shower shape rather than
  true deposition in the composite. How much a later Block 7 response model would double-count is
  unquantified. Needs the Kounine primary paper and ultimately a numerical check.
- Whether the documented failure of the gamma form in roughly the first two radiation lengths - about
  the first two readout layers here - applies to the AMS fit. `layer_energy_fractions` currently
  integrates from t = 0 through that region.

### Multifractal direction

- Is the AMS ECAL scale range large enough for stable multifractal estimation?
- Which \(q\) values are numerically meaningful at AMS granularity?
- How much do \(D_q\) estimates depend on energy?
- How should alternating X/Y views be incorporated into scale partitions?
- Should scaling be measured globally, per view, per depth window, or all three?
- How large is finite-resolution bias?
- Do multifractal observables add information beyond shower width, depth, and energy concentration?
- Can a learnable multiscale representation outperform fixed multifractal summaries without merely relearning conventional shower width/depth?
- What is the correct fair baseline for a later quantum model?

### Chaos / complex-systems direction

- Is there any mathematically justified dynamical-system formulation of shower development that would make chaos diagnostics meaningful?
- Which tools from nonlinear dynamics are useful without claiming deterministic chaos?
- Should quantum-chaotic / reservoir-computing ideas remain a separate project rather than an AMS classifier component?

## Next session — start here

1. Open an Obsidian Tutor Session:
   **“AMS FastMC Block 6 — Stochastic Shower Generation.”**
2. Assign one primary agent to run the Scientific Research OS learning workflow:
   - probe prerequisite understanding;
   - build a dependency map;
   - test current project knowledge across physics, mathematics/statistics, and software conventions;
   - teach the physics of shower-to-shower fluctuations before implementation.
3. When external literature becomes necessary, use a fresh isolated literature-scout context for the independent discovery pass so repository assumptions do not seed the search.
4. Independently verify implementation-affecting scientific claims before reconciling the literature with the existing FastMC.
5. If useful after the physical model is understood, assign a second agent to inspect or reproduce the software architecture independently, without preloading the first agent's reasoning.
6. Continue the multifractal learning track in separate Obsidian tutoring sessions without allowing it to derail the FastMC foundation.
7. Human approves the stochastic model and experiment contract.
8. Only then begin Block-6 implementation.

## Next human decision

Approve the physically justified stochastic **variables and distributions** and their software
boundary before Block 6 implementation begins. The origin convention and the ensemble-recovery
acceptance test are already decided (see Accepted evidence and decisions). What remains unapproved is
which quantities fluctuate, under which distribution families for positive/constrained quantities,
and how the correlation structure is parameterized.
