# Research records

This directory contains lightweight, human-approved project state and scientific decision records. It is not a replacement for notebooks, source code, results, or the researcher's Obsidian knowledge vault.

`STATE.md` is the shared current-state summary for the human researcher, Claude, Codex, and specialist agents.

`CHAOS_FRACTALS_QML.md` preserves the broader conceptual thread connecting:

- stochastic particle cascades;
- fractal / multifractal shower structure;
- chaos theory and its limits in this context;
- multiscale classical ML;
- QCNN / quantum feature-map hypotheses;
- separate future quantum-chaos / reservoir-computing ideas.

Agents working on any of those topics should read that framing document before proposing scientific conclusions.

## Where information belongs

```text
Obsidian
├── learning sessions
├── concepts
├── derivations
├── literature notes
├── quizbook
└── personal synthesis

Git repository
├── research/STATE.md                    current accepted state
├── research/CHAOS_FRACTALS_QML.md      conceptual research framing
├── research/questions/                  formal research questions
├── research/hypotheses/                 hypotheses under test
├── research/experiments/                experiment contracts / records
├── research/decisions/                  accepted research decisions
├── notebooks/                           scientific exploration / validation
├── src/                                 reusable implementation
├── tests/                               numerical/software contracts
└── configs/                             explicit model/configuration values
```

The project should grow these folders only when real records exist; do not create bureaucracy merely to fill a structure.

## Daily research workflow

### 0. Synchronize

Before substantial work:

1. read `RESEARCH_PROTOCOL.md`;
2. read `research/STATE.md`;
3. when the task involves chaos, fractals, multifractals, multiscale learning, QCNNs, Hamiltonian embedding, or quantum reservoirs, read `research/CHAOS_FRACTALS_QML.md`;
4. inspect recent Git changes;
5. correct `STATE.md` if code/research has moved ahead of it.

The state file must describe the repository that actually exists.

### 1. Choose today's mode

State one primary question and choose the working mode:

- learning;
- literature;
- derivation;
- experiment design;
- coding;
- analysis;
- review.

Avoid mixing all modes at once.

### 2. Learning mode — Obsidian first

For concepts that affect scientific decisions:

1. create/open a Tutor Session in Obsidian;
2. use the Scientific Research OS `tutor` skill;
3. probe prerequisite understanding;
4. build a dependency map;
5. use legitimate sources;
6. teach one node at a time;
7. quiz/reconstruct before treating the concept as learned.

Permanent concept/derivation notes are promoted only after the human can explain the idea in their own words.

### 3. Scientific gate before code

Before implementing a scientific method, establish:

- scientific purpose;
- assumptions;
- mathematical definition;
- physical/statistical meaning;
- units/domain;
- limiting behavior;
- validation plan;
- authoritative sources.

If these are unresolved, implementation waits.

### 4. Parallel Claude / Codex work

Default division of labor:

```text
Claude                          Codex
------                          -----
tutoring                        implementation boundary
literature                      APIs / architecture
derivations                     tests
hypothesis formation            reproducibility
physics interpretation          numerical edge cases
```

Use separate worktrees/branches for substantial writes.

Both agents report back to the human researcher. They do not auto-merge or decide research conclusions.

### 5. Experiment design

Before seeing results, record:

- research question;
- H1 / H0 or competing explanations;
- observable prediction;
- variables and controls;
- confounders;
- metrics;
- uncertainty/statistical plan;
- seeds/configuration;
- reproduction command;
- invalidation criteria.

Use the Scientific Research OS `form-hypothesis` and `design-experiment` skills when appropriate.

### 6. Implementation

Reusable scientific logic belongs in `src/ams_ecal/` with tests in `tests/`.

Jupyter notebooks should call tested code and serve as:

- research narratives;
- sanity-check environments;
- visualization/analysis records;
- scientific validation documents.

A notebook should not be the only implementation of reusable logic.

### 7. Attack the result

Before accepting an important conclusion, use independent review where useful:

- `physics-reviewer`;
- `statistics-reviewer`;
- `source-verifier`;
- `reproducibility-auditor`;
- `adversarial-reviewer`.

The reviewer should not be the same context that authored the result when independence matters.

### 8. Close the session

Every serious session should end with:

```text
I learned:
...

The evidence says:
...

I still do not know:
...

Decisions made:
...

Next action:
...
```

Only human-accepted conclusions update `research/STATE.md`.

## Current project cadence

The current engineering and learning tracks intentionally run in parallel:

```text
FastMC engineering                 Learning/research preparation
------------------                 -----------------------------
Block 6 stochastic events          stochastic processes/statistics
Block 7 detector response          fractal/multifractal foundations
Block 8 validated datasets         estimator design / finite-size bias
                 \                 /
                  \               /
                   controlled multifractal experiments
                                  ↓
                        classical multiscale ML
                                  ↓
                     justified QML/QCNN studies
```

The broader chaos-theory roadmap remains a parallel learning track and should not be forced into the AMS physics interpretation.

## Research record structure

As concrete records appear, use:

```text
research/
├── STATE.md
├── CHAOS_FRACTALS_QML.md
├── questions/
├── hypotheses/
├── experiments/
└── decisions/
```

Do not create empty placeholder records.

## Guiding rule

**Understanding lives in Obsidian. Evidence lives in Git. The human researcher decides what becomes knowledge or conclusion.**
