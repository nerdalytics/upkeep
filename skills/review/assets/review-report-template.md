# Review of {PR title or branch}

**Verdict:** approve, approve-with-nits, or request-changes
**Scope:** {number of files and modules touched, and the hotspots among them or none}

## Findings

{The table and the blocks in the format of the `findings` skill. The level is the severity: blocker, major, minor or nit.}

## What was checked
- [ ] Ownership and module boundaries
- [ ] Justification for new cross-module dependencies
- [ ] Duplication against canonical locations
- [ ] Speculative abstraction (YAGNI)
- [ ] Tests that fail without the production change
- [ ] The team standards
- [ ] The hotspot rules, if the diff touches a hotspot

## Debt spin-offs that do not block this PR
{The table and the blocks in the format of the `findings` skill, with numbers that continue after the findings above. The level is the severity that the problem would have in a review of its own. Each one is a candidate item for tech-debt-triage.}
