---
name: init
description: "Generates or refreshes the two skills that tailor the upkeep plugin to one project. `maintainability-checks` holds the commands that measure this project, and `maintainability-records` holds where this project keeps reports, debt items, plans and decisions. Use when another upkeep skill needs one of them, when one is missing or out of date, or after the project's toolchain, CI or documentation layout changed."
license: MIT
---

# Init

The other skills of this plugin hold the method, which is the same in every project. Everything that differs between projects is in two skills that live in the project itself. This skill generates them, checks whether they still match the project, and generates them again when they do not.

| Project skill | Holds | Generation prompt |
|---|---|---|
| `maintainability-checks` | The commands that run this project's tests, coverage, lint, complexity, duplication and architecture checks, the CI entry point, and the paths to exclude | `references/generate-checks.md` |
| `maintainability-records` | Where this project keeps decision records, reports, debt items, migration plans and team standards, in which format, and what gets committed | `references/generate-records.md` |

A calling skill names the project skills it needs. Handle only those. When the user runs this skill directly, handle both.

## Workflow

Progress:
- [ ] Step 1. Find the project skill. Search the repository, hidden folders included, for `maintainability-checks/SKILL.md` or `maintainability-records/SKILL.md`. Only a file inside the repository counts. A skill of the same name from the user's home or from a plugin does not. Handle each project skill separately through the steps below. If the file does not exist, go to Step 4.
- [ ] Step 2. Check that it is current. Its "Evidence" section lists the files and folders it relies on, each with a content hash, and the commit it was generated at. Compute the hashes again with `git hash-object <file>` for a file and `ls -A <folder> | git hash-object --stdin` for a folder. These commands read the working tree, so they also see files that git does not track and changes that are not committed. Then run `git diff --name-status --diff-filter=ADR <commit>..HEAD`, which lists every tracked file that was added, deleted or renamed since. That is how a new toolchain, pipeline or document folder shows up. The skill is current when every hash matches and the second command lists no manifest, tool configuration, pipeline, instruction or standards file. Run this check on every use, also in the session that generated the skill. If the skill is current, read it, follow it, and return to the calling skill.
- [ ] Step 3. If it is not current, read each file whose hash differs and compare it with what the skill states. When the change touches nothing that the skill states, such as a dependency version bump, write the new hashes and the current `HEAD` into "Evidence" and treat the skill as current. Otherwise go to Step 4 and tell the user what changed.
- [ ] Step 4. Generate. Read the generation prompt from the table and follow it. If you replace an existing skill, read its "Decisions" section first. A decision of the user holds until the user changes it or the thing it refers to no longer exists. Ask again only in the second case.
- [ ] Step 5. Write the skill as `<name>/SKILL.md`, placed the way this project places the agent skills it already has. Find those skills first and look at how each one is stored. When they are in one folder, write there. When the same skill exists in several folders, see whether the others are links to one folder or separate copies, and do the same for the new skill. When the existing skills follow no single pattern, ask the user where the two project skills go and record the answer in "Decisions". When the project has no skills, use the folder from which the agent you are running in reads project skills, and name it in the report. Write only inside the repository. Take every folder name from what you find in this repository.
- [ ] Step 6. Report the paths you wrote, what changed since the last generation, and what you could not determine. Run `git check-ignore -v <path>` on each file you wrote, and report whether git ignores it and by which rule. Whether the project skills are tracked is the project's choice, so state the fact and recommend nothing. Leave ignore files unchanged, and commit only when the user asks.
- [ ] Step 7. Make sure the agent you are running in can load both project skills by name. Check the list of available skills. If a skill is missing from it, find out what is still needed, such as a link that you were not permitted to create or a reload of the skills. Do it yourself where you can. Where only the user can do it, end the report with that action as a required step, and give it as one command line, with the commands chained, so that one paste runs them all. In Claude Code, put `!` in front, which runs the line from the prompt. Say that the other upkeep skills still work without it, because they find the files by searching.

A skill you wrote in this session may not be in the list of available skills until the next session. Read its file directly.

## Rules for a generated skill

- The frontmatter has `name` and a `description` that tells an agent what the skill holds and when to read it.
- State only what you read in a file or saw in the output of a command you ran. Write "none found" for a gap. Do not recommend a tool that the project does not use.
- The skill is complete without this plugin. Another agent in the same repository may read it with no plugin installed, so do not refer to plugin paths.
- Keep supporting scripts that the project needs next to the `SKILL.md`, each with a test, and name both in the skill.
- Leave out anything that holds only on this machine, such as a wrapper that this machine needs to start a tool. Put it in the report.
- Write dates as `YYYY-MM-DD`.
- End with these two sections. Write `none` under "Decisions" when you asked nothing. List under "Evidence" every file that a statement in the skill relies on, and leave out lock files.

```markdown
## Decisions

Answers the user gave. Regeneration keeps them.

- {question}: {answer} ({date})

## Evidence

Generated at commit `{full hash of HEAD}`.

The statements above rely on these files and folders. A changed hash means this skill may be out of date.

| Path | Hash |
|---|---|
| `{file}` | `{output of git hash-object}` |
| `{folder}/` | `{output of ls -A piped to git hash-object --stdin}` |
```

## Gotchas

- An "Evidence" section without hashes comes from an older version of this skill. Treat it as not current.
- A repository with no commits has no commit to record. Write `none` as the commit and skip the `git diff` command. The hashes still work.
- The hashes cover only the listed paths. A new file that git does not track, such as an ignored instruction file, shows up in neither command. When the calling skill meets a command from `maintainability-checks` that no longer runs, or a location from `maintainability-records` that no longer exists, treat the skill as not current.
- Regenerate the whole skill. Patching single lines of a skill that describes a replaced toolchain leaves statements about the old one behind.
