# Generate `maintainability-checks`

This prompt belongs to the init skill. Follow it when `maintainability-checks` is missing or out of date. The result is a skill that tells any agent how this project is measured, with commands that you have seen run.

## 1. Explore

Read what defines the project's toolchain before you run anything:

- the build and package manifests, and the task runners or scripts they define
- the configuration of every linter, formatter, type checker, test runner and coverage tool
- the CI pipeline definitions, and the hooks that run before a commit or a push
- the contribution and agent instruction files, which often name the commands that the team uses

Take the tools from these files. A tool that no file mentions is not part of the project.

## 2. Find and run one command per measure

For each measure in the list, find the command that the project itself uses, preferring the one that CI runs. Run it from the repository root and note what you observe. One command can serve several measures. When a file declares a tool and no file gives a command for it, use the tool's plain invocation and say in the skill that no file gives the command.

- tests
- test coverage
- test coverage of changed lines only
- lint and static analysis
- complexity per function or file
- duplication
- dependency and architecture rules, such as cycles, layering and forbidden imports
- any threshold, baseline or budget that an existing check compares against, and the file that sets it

Record for each one the exact command as the project states it, the exit code you saw, the form of its output, and the configuration file that controls it. A check that exits with an error because it found violations is a valid result. Record the exit code and the number of findings, not the findings. If the project has no tool for a measure, record "none found". If a command cannot run here, for example because a tool is not installed or the sandbox blocks it, record the command, the file you took it from, and the reason. Install nothing and change no configuration. Adding a missing check is the job of the `gates` skill.

Also record:

- the CI entry point, which is the pipeline file and the jobs that run the commands above
- the single command that runs every check locally, if the project has one
- source code in a language that no tool covers, which goes under "Not measured"
- the paths that hold generated, vendored or third-party code, with the file that shows it, such as an ignore file or `.gitattributes`

## 3. Write the skill

Write `maintainability-checks/SKILL.md` under the rules in the init skill. Use this structure, with one table row per measure in the list. `{project}` is the name in the project's manifest, or the repository's folder name. The last two sections follow the format in the init skill.

```markdown
---
name: maintainability-checks
description: "The commands that test, lint and measure {project}, and how its CI runs them. Read it before you measure, review or gate maintainability in this repository."
---

# Maintainability checks for {project}

{One paragraph on the stack and toolchain, as found.}

## Commands

| Measure | Command | Configured in | Seen on {date} |
|---|---|---|---|
| Tests | `{command}` | `{file}` | exit 0, {summary of the output} |
| Complexity | none found | | |

## CI

{Pipeline file, the jobs that run the commands, and the local command that runs them all.}

## Excluded paths

{Generated, vendored and third-party paths, each with the file that shows it.}

## Not measured

{Each measure with no tool, and each command that could not run, with the reason.}

## Decisions

## Evidence
```
