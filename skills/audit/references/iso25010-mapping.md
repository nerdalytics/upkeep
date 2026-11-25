# ISO/IEC 25010 maintainability mapping

Load this file when you map audit findings to a shared quality vocabulary. ISO/IEC 25010 divides maintainability into five sub-characteristics. Each one maps to measurable indicators. Pick indicators that the repo's tooling can produce. The project skill `maintainability-checks` lists that tooling.

| Sub-characteristic | What it means | Indicators | How to measure |
|--------------------|---------------|------------|----------------|
| Modularity | Components are independent, and changes stay local | dependency cycles, fan-in and fan-out, layer violations | the project's dependency or architecture tool, and `scripts/hotspots.py` for churn concentration |
| Reusability | Parts can be used elsewhere | duplicated blocks, generic or context-bound interfaces | `scripts/dupblocks.py`, and a review of public interfaces |
| Analysability | Issues can be diagnosed | log and monitoring coverage on critical paths, quality of error context | inspection of logging at boundaries, and incident postmortems |
| Modifiability | Changes can be made without regressions | complexity per function, hotspots by churn and size, coupling | the project's complexity tool, and `scripts/hotspots.py` |
| Testability | Behavior can be verified | coverage on changed lines, tests for hotspots, available seams | the project's coverage tool, and the ratio of test code to source code per module |

## Composite scores and their limits

- **Maintainability Index (MI).** It combines Halstead volume, cyclomatic complexity, lines of code and comment ratio. Each tool has its own scale and bands, so the same code scores differently in different tools. Use one tool consistently and report its trend over time. Never compare absolute MI values across tools, and never treat one tool's bands as universal.
- **Technical Debt Ratio (TDR).** It is the estimated remediation cost divided by the development cost, as SQALE-based tools such as SonarQube compute it. The remediation-cost model is the tool's assumption and not a measurement. Quote the tool and its rating scheme, and track the trend.
- **SIG model.** It is a commercial benchmark that translates ISO characteristics into system properties and calibrates them against an industry database. It gives useful context when the team has a subscription. Local tooling cannot reproduce it.

## Reporting rule

Every mapping row in the gap report names the indicator, the command or tool that produced it, and the observed value. When no measurable indicator is available for a sub-characteristic, report it as "not measured". Never estimate it.
