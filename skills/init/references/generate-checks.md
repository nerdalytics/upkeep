# Generate `maintainability-checks`

This prompt belongs to the init skill. Follow it when `maintainability-checks` is missing or out of date. The result is a skill that tells any agent how this project is measured, with commands that the user let you run and that you have seen run.

## 1. Explore

Read what defines the project's toolchain before you run anything:

- the build and package manifests, and the task runners or scripts they define
- the configuration of every linter, formatter, type checker, test runner and coverage tool
- the CI pipeline definitions, and the hooks that run before a commit or a push
- the contribution and agent instruction files, which often name the commands that the team uses

Take the tools from these files. A tool that no file mentions is not part of the project.

## 2. Find one command per measure

For each measure in the list, find the command that the project itself uses, preferring the one that CI runs. One command can serve several measures. When a file declares a tool and no file gives a command for it, use the tool's plain invocation and say in the skill that no file gives the command.

- tests
- test coverage
- test coverage of changed lines only
- lint and static analysis
- complexity per function or file
- duplication
- dependency and architecture rules, such as cycles, layering and forbidden imports
- any threshold, baseline or budget that an existing check compares against, and the file that sets it

## 3. Ask the user which commands to run

Run none of these commands before the user has agreed. A check can take minutes, use the network or write files, so the user decides what runs. List the commands you found, each with its measure and the file that states it, and ask in one round which of them to run now. Recommend running all of them, because a command that was not seen running may not work. Reading files and running `git` need no such question.

Run the commands the user chose, from the repository root. For each other command, record the command, the file you took it from, and "not run, by the user's choice". Record the user's answer under "Decisions", so that a later generation runs the same commands without asking again. Ask again only for a command that is new since then.

Record for each command you ran the exact command as the project states it, the exit code you saw, the form of its output, and the configuration file that controls it. A check that exits with an error because it found violations is a valid result. Record the exit code and the number of findings, not the findings. If the project has no tool for a measure, record "none found". If a command cannot run here, for example because a tool is not installed or the sandbox blocks it, record the command, the file you took it from, and the reason. Install nothing and change no configuration. Adding a missing check is the job of the `gates` skill.

Also record:

- the CI entry point, which is the pipeline file and the jobs that run the commands above
- every other place that enforces a check, such as a hook that runs before a commit or a push, or a hook of an agent, with the file that defines it
- the single command that runs every check locally, if the project has one
- source code in a language that no tool covers, which goes under "Not measured"
- the paths that hold generated, vendored or third-party code, with the file that shows it, such as an ignore file or `.gitattributes`

## 4. Write the skill

Write `maintainability-checks/SKILL.md` under the rules in the init skill. Use this structure, with one table row per measure in the list. `{project}` is the name in the project's manifest, or the repository's folder name. The last two sections follow the format in the init skill.

```markdown
---
name: maintainability-checks
description: "The commands that test, lint and measure {project}, and where the project enforces them. Read it before you measure, review or gate maintainability in this repository."
---

# Maintainability checks for {project}

{One paragraph on the stack and toolchain, as found.}

## Commands

| Measure | Command | Configured in | Seen on {date} |
|---|---|---|---|
| Tests | `{command}` | `{file}` | exit 0, {summary of the output} |
| Complexity | none found | | |

## Where checks are enforced

{The pipeline file and the jobs that run the commands, the local command that runs them all, and each hook that runs a check, with the file that defines it. Write "none found" for a place the project does not have.}

## Excluded paths

{Generated, vendored and third-party paths, each with the file that shows it.}

## Not measured

{Each measure with no tool, and each command that could not run or that the user chose not to run, with the reason.}

## Decisions

## Evidence
```
