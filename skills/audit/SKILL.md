---
name: audit
description: "Measures how maintainable a repository is and writes a gap report. It covers churn and size hotspots, duplicated blocks, complexity and coupling, and it cites a file path or command output for every finding. Use when the user asks how maintainable, healthy or risky a codebase is, wants hotspots or duplication found, or needs a baseline before refactoring or modernization. It only measures. To rank the findings, use tech-debt-triage."
license: MIT
---

# Maintainability audit

Measure, then report. Every finding in the report cites a file path or the command output that produced it. Make no claim without a source. This skill assesses. It does not fix or prioritize. Hand the report to tech-debt-triage for prioritization.

## Workflow

Progress:
- [ ] Step 1. Load the project skills `maintainability-checks` and `maintainability-records` through this plugin's init skill, `upkeep:init`. It returns at once when they are current, and generates them when not. Then scope the audit. List the languages and the module layout, and take the generated and vendored directories to exclude from `maintainability-checks`. Confirm that the clone has full history with `git rev-parse --is-shallow-repository`, because a shallow clone distorts churn.
- [ ] Step 2. Rank hotspots with `python3 ${CLAUDE_SKILL_DIR}/scripts/hotspots.py <repo-root> --since "6 months ago"`. The scripts are in this skill's directory, not in the audited repo, so call them by full path and pass the repo root. The score is churn weighted by file size. It is a proxy and does not measure complexity.
- [ ] Step 3. Find duplicated blocks with `python3 ${CLAUDE_SKILL_DIR}/scripts/dupblocks.py <repo-root>`.
- [ ] Step 4. For complexity and coupling numbers, run the commands that `maintainability-checks` lists, and record each exact command in the report. Where it lists none for a measure, write in the report that the measure was not taken. Do not estimate.
- [ ] Step 5. Map the findings to ISO 25010 sub-characteristics with `references/iso25010-mapping.md`.
- [ ] Step 6. Write the gap report from `assets/gap-report-template.md`, with the current state, target, gap and evidence for each finding. Save it where `maintainability-records` puts audit reports, with the date in the file name, and commit it only if that skill says audit reports are committed. Then reply with the path and the summary paragraph.

## Interpretation

Measure exactly as described. Interpretation is your judgment. The scripts produce candidates, and you decide which ones matter.

- A high-churn file that is a stable, well-tested configuration table is not worth refactoring.
- Duplication in generated files or license headers is noise. Exclude those files and run the script again.
- Compare against the repo's own history when it exists. A trend tells you more than a single number.

## Gotchas

- `hotspots.py` counts commits per path. A rename splits a file's churn across its old and new paths. Check `git log --follow` on a suspicious entry before you rank it low.
- Lines of code measure size, not complexity. Never report LOC as complexity in the gap report.
- Maintainability Index scales differ between tools. The 0 to 100 bands of Visual Studio are not the bands of another tool. Report the tool and its scale, and track the trend, not a universal threshold.
- Technical Debt Ratio depends on the tool's model of remediation cost. Quote the tool's rating scheme. Do not present a percentage as an industry-wide judgment.
- Exclude generated and vendored code from every measurement, and say what you excluded.
