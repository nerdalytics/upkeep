# Maintainability gap report for {repo or scope}

**Date:** {date}
**Scope:** {modules and languages, and the excluded generated and vendored paths}
**History window:** {for example the last 6 months, and whether the clone is shallow}

## Summary

{One paragraph with the overall state, the two or three gaps that matter most, and the trend if history exists.}

## Findings

| # | ISO 25010 sub-characteristic | Current state (value and evidence) | Target | Gap | Priority hint |
|---|------------------------------|------------------------------------|--------|-----|---------------|
| 1 | Modifiability | {file} has {n} commits and {n} lines, from `hotspots.py` output | {target the team defined} | {what falls short} | {high, medium or low, and why} |

## Evidence appendix

List every command you ran, verbatim, with its output or a link to the saved output.

```text
$ python3 {path to this skill}/scripts/hotspots.py {repo root} --since "6 months ago"
{output}
```

## Not measured

- {sub-characteristic or indicator}: {why you could not measure it}

## Handoff

The findings go to tech-debt-triage for classification and prioritization. This report does not schedule or carry out remediation.
