# Generate `maintainability-records`

This prompt belongs to the init skill. Follow it when `maintainability-records` is missing or out of date. The result is a skill that tells any agent where this project keeps each kind of maintainability document, in which form, and whether it is committed.

## 1. Find the home of each kind of document

Search the repository, its instruction files for agents and contributors, and the skills in the repository's own skill folders. For each kind in the list, look for an existing home.

- decision records, such as ADRs
- audit and assessment reports
- review reports
- the technical-debt backlog
- migration plans
- migration inventories, which list the routes and components of the system being replaced
- team standards, which are the documents that state how this team writes, structures, tests and reviews code

Record for each one the location, the file naming and numbering, the template or the format of two existing examples, the status vocabulary if it has one, and whether the existing files are tracked by git. With fewer than two examples, describe what exists and say how many there were.

## 2. Find out who owns it

Another skill or framework may already own a kind of document. A spec-driven workflow often writes its own decision records, and an issue tracker is often the backlog. Look for the folders and skills of such a workflow, for tracker links in the documentation, and for the hosting service of the git remote.

When another skill owns a kind of document, the entry names that skill and says that the work is handed to it. When a tracker is the backlog, the entry names the tracker and the command that creates an item in it, if a command line tool for it is installed.

## 3. Ask the user for what the repository does not show

The open questions are the location and the commit status of each kind of document that has no home. Ask them in one round, and give a recommended answer with each. Do not ask about owners, team standards or status vocabulary. Write "none found" for those.

Base the recommendation for committing on one rule. A file is committed when it is a lasting technical record, someone keeps it current, and it is the authoritative record of what it describes. A decision record and a migration plan in progress meet the rule. An audit report, a review report and a route inventory are snapshots that can be produced again, so recommend a location that git ignores or that the user names. Debt items are committed only when the repository is the backlog's home. When you found no tracker, recommend the repository as the home.

When a location is not to be committed and git does not ignore it, say so in the skill and in the report. Leave ignore files unchanged, because that edit is the user's to make.

Record each answer in "Decisions" with its date.

## 4. Write the skill

Write `maintainability-records/SKILL.md` under the rules in the init skill. Use this structure, with one table row per kind of document in the list except team standards. `{project}` is the name in the project's manifest, or the repository's folder name. The last two sections follow the format in the init skill.

```markdown
---
name: maintainability-records
description: "Where {project} keeps decision records, audit and review reports, debt items, migration plans and team standards, and which of them are committed. Read it before you write or look for one of these documents in this repository."
---

# Maintainability records for {project}

| Document | Location and naming | Format | Committed | Owner |
|---|---|---|---|---|
| Decision records | `{path}/NNNN-title.md` | `{template or example file}` | yes | {skill, team or person} |
| Audit reports | `{path}` | free | no | |
| Debt backlog | {tracker, with the command that creates an item} | | | |

## Team standards

{The documents that state the team's rules, one per line with what each covers. "none found" if there are none.}

## Handed to other skills

{Each kind of document that another skill or framework owns, and the name of that skill.}

## Decisions

## Evidence
```

List in "Evidence" the folder of each document home that exists, next to the files the statements rely on.
