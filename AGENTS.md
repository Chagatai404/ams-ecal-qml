# AGENTS.md

This repository is a human-led scientific research project.

## Start here

Before substantial work:

1. Read `RESEARCH_PROTOCOL.md`.
2. Read `research/STATE.md`.
3. Inspect the relevant source, tests, notebook, and configuration files.
4. Use installed Scientific Research OS skills when the task matches them.

## Authority

The human researcher is the final authority on:

- scientific assumptions,
- research direction,
- interpretation,
- accepting/rejecting hypotheses,
- merging agent work.

Do not silently promote hypotheses or interpretations into accepted facts.

## Default Codex role

Codex is primarily the implementation/reproducibility agent:

- implement tested scientific utilities,
- design clean APIs,
- write and run tests,
- build reproducible experiments,
- refactor notebook logic into `src/`,
- audit numerical edge cases,
- record exact commands and configurations.

Codex may explain scientific reasoning, but should not bypass the learning/research workflow by implementing a method whose assumptions are still unresolved.

## Scientific change checklist

Before implementing a new scientific method, state:

- scientific purpose,
- assumptions,
- mathematical definition,
- units/domain,
- expected limiting behavior,
- validation plan.

For a new research experiment, use the `design-experiment` skill when available.

## Branch / worktree policy

Never have Claude and Codex perform substantial writes on the same working tree at the same time.

Preferred structure:

```text
ams-ecal-qml/          # human integration worktree
ams-ecal-qml-codex/    # Codex worktree
ams-ecal-qml-claude/   # Claude worktree
```

Preferred branches:

```text
research/<topic>        # human/integration branch
agent/codex-<task>      # Codex
agent/claude-<task>     # Claude
```

Rules:

1. One agent owns one worktree/branch at a time.
2. Agents do not merge their own branches into the integration branch.
3. Commit small coherent changes.
4. Before handoff, report:
   - commits,
   - files changed,
   - tests run,
   - scientific assumptions introduced,
   - unresolved issues.
5. The human reviews diffs and chooses what to merge.
6. Agent branches may be discarded freely; accepted evidence must remain reproducible on the integration branch.

## Notebook policy

Notebooks are research records, not utility libraries.

If code is reusable:
- move it into `src/ams_ecal/`;
- add tests under `tests/`;
- call it from the notebook.

Do not bury important constants or scientific assumptions in unexplained notebook cells.

## Source policy

Important physics claims require authoritative sources.

For AMS detector facts, prefer official AMS/collaboration material and peer-reviewed AMS publications.

Do not substitute generic calorimeter values for AMS-specific values silently.

## Secrets

Do not read, print, copy, summarize, commit, or expose credentials, tokens, secrets, or unrelated `.env` values.

If a task genuinely requires a secret-backed command, request the minimum necessary human action rather than inspecting secret contents.
