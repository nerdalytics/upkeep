---
name: findings
description: "The one format for the list of findings in every report that an upkeep skill writes, and in the reply that presents the report. Load it before you write an audit report or a review report."
license: MIT
user-invocable: false
---

# Findings

A report lists its findings twice. A table gives the overview, and one block per finding gives the detail. The reply in the conversation shows only the table.

## The table

```markdown
| # | Level | Where | Finding |
|---|-------|-------|---------|
| 1 | blocker | `src/billing/invoice.ext:42` | Changed behavior has no test |
| 2 | major | `src/billing/coupons.ext:120-180` and 2 more | The discount rule exists in three places |
```

The table has these four columns and no others.

- **#** numbers the findings from 1. Order them by level, the highest first, and by path within a level.
- **Level** is one word from the scale of the calling skill, spelled as that skill spells it.
- **Where** is one location, written as `path:line` or `path:first-last`, with the path relative to the repository root. When a finding has several locations, give the first and the number of the others, as in the second row. A finding that is not about a file names its subject, such as a branch or a command.
- **Finding** is one sentence of at most 15 words. It states the problem and not the fix.

## The block

Write one block per row below the table, with the same number and the same sentence.

```markdown
### 1. Changed behavior has no test

- **Level:** blocker
- **Where:** `src/billing/invoice.ext:42`
- **Rule:** {the rule it breaks, and where that rule is stated}
- **Evidence:** {the file content or the command output that shows the problem}
- **Action:** {one concrete next step}
```

- **Where** lists every location, one per line when there are several.
- **Rule** names its source: an item of the calling skill's checklist, a team standard with its file and section, or the measure that was taken.
- **Evidence** cites a file with its lines, or a command with its output. A finding without evidence is left out of the report.
- **Action** is one step. When the fix needs a decision first, the action is that decision.

The calling skill's template may add fields to the block. They go between "Evidence" and "Action", with the names that the template gives.

## Findings that the report hands on

Some findings do not belong to the subject of the report, such as a problem on a line that a reviewed change did not touch. They get the same table and the same blocks in a section of their own. Their numbers continue after the last number of the main table, so that each number occurs once in a report.

## The reply

The reply that presents the report has the path of the report, one sentence that counts the findings per level, and the table. Leave the blocks in the report.

## No findings

Write "No findings." in place of the table, and say in one sentence what was checked.
