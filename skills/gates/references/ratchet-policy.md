# Baseline policy

Load this file when the repo already has violations, as in legacy code, an inherited codebase, or any gate that would fail on day one. In such a repo, a team disables a gate with absolute thresholds within a week. A baseline check blocks new violations while the team pays down the existing ones on purpose.

## Policy

1. **Freeze a baseline.** Snapshot today's violations into a committed JSON file. The team named in the gate config owns the baseline.
2. **Block only additions.** CI fails when a violation appears that is not in the baseline. Existing violations pass.
3. **Shrink the baseline and never grow it.** When violations are fixed, take a new snapshot so that the baseline gets smaller. Adding entries to a baseline needs the same review as any policy change. Never add entries only to make CI green.
4. **Track the trend.** The baseline count is a debt metric, so report it over time. A growing baseline means that people are bypassing the check.

## The example script

`scripts/ratchet_baseline.py` in this skill is an example of a baseline check. Reproduce its behavior in the language of the project's own checks. Copy the script itself into the repo only when those checks already run Python, because CI cannot reach this skill's directory.

```bash
python3 scripts/ratchet_baseline.py snapshot violations.json -o maintainability-baseline.json
python3 scripts/ratchet_baseline.py check violations.json --baseline maintainability-baseline.json
```

`check` exits with 0 when no new violation appeared, with 1 when new violations exist, and with 2 on an input error. It prints each new violation with its rule and file, and it reports violations in the baseline that no longer occur. Commit the baseline next to the gate config. A check written for the project keeps these properties.

## Violations format

The example script reads one format, a JSON array of objects. `rule` and `file` are required strings. `symbol` is optional and defaults to empty.

```json
[{"rule": "max-complexity", "file": "src/billing/invoice.ext", "symbol": "total"}]
```

Take the tool and its command from `maintainability-checks`. Let the tool write machine-readable output, and convert that output to the array in the project's own check. Three points decide whether the gate works:

- Stop the tool's own exit code from failing the job before the baseline check runs. The baseline check decides whether the job fails.
- Give every violation a rule name. Many tools report a file they cannot parse without one, so name that case yourself.
- Run from the repo root. The script turns an absolute path into one relative to the working directory, so that the baseline matches on the next machine.

A fingerprint is `(rule, file, symbol)`. It has no line number, so an ordinary edit above a violation does not count as a new violation. The baseline stores how often each fingerprint occurs, so a second violation of the same rule in the same file fails the check.

## Gotchas

- Unstable fingerprints make every run look like new violations. Line numbers, absolute paths and timestamps are unstable. Normalize them before you take a snapshot.
- When a linter renames a rule, the check reports every old violation as fixed and every one as new. Take a new snapshot on purpose when you upgrade the tool, and say so in the commit message.
- The baseline check stops the count from growing. It does not shrink it. Pair it with funded remediation, as in tech-debt-triage, or the baseline never gets smaller.
