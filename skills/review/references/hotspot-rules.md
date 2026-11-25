# Hotspot rules

Load this file only when the diff touches a module flagged as a hotspot. A hotspot has high churn and high complexity. An `audit` report or the debt backlog usually lists it.

## Identifying a hotspot

A module is a hotspot when one of these holds:
- The newest audit report or the debt backlog lists it. `maintainability-records` says where both are.
- It changed often in recent history and contains large or deeply branching functions. Use the audit's measured ranking when one exists. Do not judge by eye.

## Extra rules for hotspot diffs

1. **Characterization first.** If the touched behavior has no test, the PR adds a characterization test before the change, as the legacy-safe-change skill describes. A missing one is a blocker.
2. **Diff budget.** Keep behavior diffs small in each hotspot module. The team sets the line budget. Split a larger change into stacked PRs.
3. **No new callers of deprecated APIs.** A new call to an API that the module header marks as deprecated needs an explicit migration note.
4. **Dependency direction.** A hotspot module does not gain new fan-in in the PR that changes its behavior. Use separate PRs.
5. **Observability.** A behavior change keeps or improves log and metric coverage on the changed path. A path without logs or metrics in a hotspot can fail without anyone noticing.

## Reviewer posture

Ask what breaks downstream if the change is wrong before you ask whether it is elegant. In a hotspot, prefer the plain, reversible change to the clever one.
