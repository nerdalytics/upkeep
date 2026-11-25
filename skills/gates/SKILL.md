---
name: gates
description: "Adds automated maintainability checks to a repository's CI. They are thresholds for complexity, duplication and coverage, architecture rules for layering, dependency direction and cycles, and a baseline check that blocks only new violations in legacy code. Use when the user asks for quality gates, lint or coverage thresholds, architecture tests, a ratchet, or a way to stop a codebase from getting worse."
license: MIT
---

# Maintainability gates

Turn maintainability rules into checks that fail CI. There are two types of gate. Metric thresholds cover complexity, duplication and coverage. Architecture fitness functions cover layering, dependency direction and cycles. A rule counts as a gate only when CI enforces it.

## Workflow

Progress:
- [ ] Step 1. Load the project skill `maintainability-checks` through this plugin's init skill, `upkeep:init`. It returns at once when it is current, and generates it when not. It lists the project's tools, their configuration files and the CI entry point.
- [ ] Step 2. For each gate the user wants, extend the configuration of the tool that `maintainability-checks` lists for that measure. Where it lists none, propose one tool that fits the project's toolchain, and add it only after the user has approved it. When you are not permitted to install the tool, leave its declaration in the project's files and hand the install to the user: give it as one command line, with the commands chained, so that one paste runs them all. In Claude Code, put `!` in front, which runs the line from the prompt. Add a second tool for a measure that already has one only when the user asks for it.
- [ ] Step 3. For architecture rules, read `references/fitness-functions.md` and implement them in the test suite.
- [ ] Step 4. If the repo already has violations, read `references/ratchet-policy.md` and freeze a baseline. Write the baseline check in the language and the place of the project's existing checks, so that the gate adds no new runtime to the project. `${CLAUDE_SKILL_DIR}/scripts/ratchet_baseline.py` is an example of the behavior to reproduce. Copy it only when the project's checks already run Python.
- [ ] Step 5. Run the validation loop below. Report success only after you have seen the gate fail and then pass.
- [ ] Step 6. Run the init skill again for `maintainability-checks`, so that it lists the new gate.

## Threshold policy

- Thresholds are parameters that each repo calibrates. Starting points for a new codebase are complexity in the low teens per function, a duplication percentage in the low single digits, and high coverage on changed lines. Never adopt numbers from blog posts as policy.
- In a repo with existing violations, never block on absolute values. Fail only on violations that are not in a committed baseline.
- All thresholds are in one committed config file that CI reads. Never hardcode numbers in the pipeline definition, where they drift from local runs.

## Validation loop

Follow these steps exactly.

1. Add the gate.
2. Seed a violation, for example a circular import between two modules.
3. Run the pipeline locally. It must fail with a readable message that names the rule and the file.
4. Remove the seed.
5. Run the pipeline again. It must pass.
6. Report the gate as working only after you have seen both results.

## Gotchas

- A coverage gate with an absolute threshold fails on day one in a legacy repo, and the team disables it within a week. Use a baseline. See `references/ratchet-policy.md`.
- Many tools exit with 0 on a warning. Set the rule's severity so that a violation changes the exit code, or the gate never fails. The seeded violation in the validation loop shows which case you have.
- People bypass any local check that `--no-verify` can skip. Run every pre-commit hook in CI as well.
- Fitness functions belong in the test suite or in the job that already runs on every build. Nobody runs a separate script.
- A gate without an owner gets removed the first time it blocks a release. Name the owning team in the config.
