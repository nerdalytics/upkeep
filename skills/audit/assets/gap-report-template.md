# Maintainability gap report for {repo or scope}

**Date:** {date}
**Scope:** {modules and languages, and the excluded generated and vendored paths}
**History window:** {for example the last 6 months, and whether the clone is shallow}

## Summary

{One paragraph with the overall state, the two or three gaps that matter most, and the trend if history exists.}

## Findings

{The table and the blocks in the format of the `findings` skill. The level is the priority hint: high, medium or low. "Evidence" holds the current state, which is the measured value and the command that produced it. Each block has these three added fields.}

- **Sub-characteristic:** {the ISO 25010 sub-characteristic}
- **Target:** {the target the team defined, or "none defined"}
- **Gap:** {what falls short of the target}

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
