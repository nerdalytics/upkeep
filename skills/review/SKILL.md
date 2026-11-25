---
name: review
description: "Reviews a diff, pull request or staged changes for maintainability. It checks module ownership, new cross-module dependencies, duplication, speculative abstraction, and whether changed behavior has tests. Use when the user asks for a review of a change with a focus on structure, design or maintainability. For a whole repository, use audit."
license: MIT
---

# Maintainability review

Review the diff, not the repository. Every finding cites `file:line` and the rule it breaks. A problem on a line that the diff did not touch is a debt spin-off and does not block this PR.

## Workflow

Progress:
- [ ] Step 1. Load the project skill `maintainability-records` through this plugin's init skill, `upkeep:init`. It returns at once when it is current, and generates it when not. Read the team standards it lists. They hold the team's decisions and override this checklist wherever the two conflict.
- [ ] Step 2. Get the diff from the PR, with `git diff --staged`, or with `git diff -M <base>...HEAD`. The base is the PR's target branch. Without a PR, it is the branch that this project merges into. Take it from `git symbolic-ref --short refs/remotes/<remote>/HEAD` for the remote that `git remote` lists, and ask the user when that gives no single answer. List the touched files and the module that owns each one.
- [ ] Step 3. Apply the checklist below to changed lines only.
- [ ] Step 4. If the diff touches a module that is flagged as a hotspot, load `references/hotspot-rules.md` and apply its extra rules.
- [ ] Step 5. Write the report from `assets/review-report-template.md` to the place `maintainability-records` gives for review reports, with the branch and the date in the file name. Then reply with the path, the verdict, and the findings table.

## Review checklist

Use judgment about emphasis. A diff that mostly renames things needs different attention than a new subsystem.

1. **Ownership.** The change is in the module that owns the responsibility. Cross-cutting logic placed in a feature module is a finding.
2. **New dependencies.** Every new import between modules needs a sentence of justification in the PR description. A dependency without one is a blocker.
3. **Duplication.** When the logic already exists elsewhere, point at the canonical location and do not accept a second copy.
4. **Speculative abstraction.** An interface, factory or config option with exactly one use is a YAGNI finding. Ask for the second concrete use case.
5. **Test coverage of changed behavior.** The diff includes a test that fails without the production change. Existing tests that still pass do not cover new behavior.
6. **Readability.** Naming and formatting follow the team standards. The diff does not reformat untouched lines, because that hides the last real author of each line in `git blame`.
7. **Boy Scout bound.** Cleanup is welcome, in a commit separate from behavior changes.

## Severity

- `blocker` is for a change that breaks a convention protecting a hotspot, lacks a test for changed behavior, or adds a cross-module dependency without justification.
- `major` is for duplication, speculative abstraction, or an ownership violation.
- `minor` is for naming, unclear intent, or a new public API without documentation.
- `nit` is for style that the linter does not catch. Never block on nits.

## Output

Use `assets/review-report-template.md`. The verdict is approve, approve-with-nits, or request-changes. List debt spin-offs in their own section so that they are not lost after the merge, and hand them to the tech-debt-triage skill.

## Gotchas

- A rename that touches 40 files is one change. Run `git diff -M` and judge what changed apart from the rename.
- Style rules do not apply to generated files such as lockfiles, migrations, `*.pb.go` and `*_pb2.py`. Check `.gitattributes` for `linguist-generated` before you flag one.
- The team standards override this checklist on any conflict. They record the team's decisions, and this skill only gives the procedure. When `maintainability-records` lists no team standards, say so in the report and apply the checklist alone.
- Never request changes on untouched lines. Open a debt item.
- Zero findings on a 500-line diff is suspicious. Check test coverage of changed behavior again before you approve.
