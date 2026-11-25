# Review of {PR title or branch}

**Verdict:** approve, approve-with-nits, or request-changes
**Scope:** {number of files and modules touched, and the hotspots among them or none}

## Findings

| # | Severity | File:Line | Rule | Suggested action |
|---|----------|-----------|------|------------------|
| 1 | blocker  | src/...:42 | changed behavior has no test | add a test that fails without the change |

## What was checked
- [ ] Ownership and module boundaries
- [ ] Justification for new cross-module dependencies
- [ ] Duplication against canonical locations
- [ ] Speculative abstraction (YAGNI)
- [ ] Tests that fail without the production change
- [ ] The team standards
- [ ] The hotspot rules, if the diff touches a hotspot

## Debt spin-offs that do not block this PR
- {problem on an untouched line}. Candidate item for tech-debt-triage. Evidence: file:line
