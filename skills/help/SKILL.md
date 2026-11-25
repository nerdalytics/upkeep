---
name: help
description: "Map of the upkeep plugin. It says which of the plugin's skills fits which situation, the order they are used in, what they need installed, how they are tailored to a project, and where they write their reports. Use when the user asks what the upkeep plugin can do, which of its skills to use, or where one of its reports went."
license: MIT
---

# upkeep

Answer the user's question from this map. If they ask what the plugin does, give the table and the usual order. If they ask which skill to use, name one and say why.

## Skills

Each skill runs when the user describes the situation, or by name as `/upkeep:<skill>`.

| Skill | Use it when | What the user gets |
|---|---|---|
| `audit` | They want to know how maintainable a repository is | A gap report with measured hotspots, duplication, complexity and coupling |
| `tech-debt-triage` | They have findings and need to decide what to fix first | A scored, ordered debt backlog |
| `review` | They want one diff or pull request reviewed for structure and design | A review report with a verdict and findings by severity |
| `gates` | They want CI to stop the codebase from getting worse | Lint and coverage thresholds, architecture rules, and a baseline check for legacy code |
| `legacy-safe-change` | They need to edit code that has no tests | The change, protected by characterization tests written first |
| `strangler-migration` | They want to replace a legacy system piece by piece | A validated migration plan, then one slice moved at a time |
| `architecture-decision-records` | A significant technical decision was made or reversed | An ADR in the project's own convention |
| `init` | The project is new to the plugin, or its toolchain or documentation layout changed | The two project skills described below |

## Usual order

The skills hand work to each other.

1. `audit` measures the repository.
2. `tech-debt-triage` ranks what the audit and the reviews found.
3. `legacy-safe-change` works off the ranked items that need an edit in place. `strangler-migration` handles the ones where the code should be replaced.
4. `gates` keeps new problems out while the team fixes the old ones.
5. `review` runs on each change. Problems it finds on lines that the change did not touch go back to `tech-debt-triage`.
6. `architecture-decision-records` records the decisions made along the way, such as retiring a legacy component.

Any skill also works alone. A user who only wants a pull request reviewed needs only `review`.

## Project skills

The skills above hold the method. What differs between projects is in two skills that `init` writes into the project's own skill folder.

| Project skill | Holds |
|---|---|
| `maintainability-checks` | The commands that test, lint and measure the project, and how its CI runs them |
| `maintainability-records` | Where the project keeps decision records, reports, debt items, migration plans and team standards, and which of them are committed |

Each skill loads the project skills it needs through `init`, so the user does not have to run `init` first. `init` compares each project skill with the files it was generated from and generates it again after those files changed, for example after a change of framework or toolchain. The user's answers are kept in the skill's "Decisions" section.

## Where the reports go

`maintainability-records` in the project says where each report goes. If the user asks where a report went, read that skill and answer from it.

Three kinds of output are lasting technical artifacts of the repository, so the skills expect them to be committed:

- Decision records, in the place where the project keeps them.
- The CI checks and architecture tests from `gates`, with their baseline file.
- The tests that `legacy-safe-change` adds.

Whether the two project skills are committed is the project's choice. `init` reports whether git ignores them.

## What must be installed

- `git`, for every skill that reads history or diffs.
- Python 3.9 or later, for the audit scripts. They use only the standard library.
- The linters, coverage tools and architecture test tools of the repository's own toolchain. The skills use what `maintainability-checks` lists and report what they could not measure.

The plugin is written for macOS, Linux, and Windows under WSL.
