# Prioritization rubric

Load this file when you score or validate debt items. Each score has a definition, so that two people who score the same finding get similar results.

## Layer classification

| Layer | Where it is | Examples | Kind of fix |
|-------|-------------|----------|-------------|
| code | files and modules | duplication, complexity, missing tests, code smells | refactoring, characterization tests |
| architecture | between modules, services and teams | dependency cycles, tight coupling, undocumented contracts, layer violations | fitness functions and a structural change, often through strangler-migration |
| organizational | people and process | knowledge held by one person, missing ownership, stalled migrations, team boundaries that do not match the system | documentation, rotation, assigning an owner, finishing or reverting the migration |

A finding that spans layers becomes one item per layer, and the items link to each other.

## Scoring scales

Each scale runs from 1 to 3.

**Impact** is what the debt costs while it stays.
- 3: It causes or directly enables incidents, security exposure, or repeated delivery delays.
- 2: It measurably slows changes in the affected area. Evidence is churn, review friction, or estimate overruns.
- 1: It is cosmetic or local friction with no measured delivery cost.

**Blast radius** is how much of the system the debt touches.
- 3: Many downstream modules or services depend on it. The dependency graph or a caller search shows wide fan-in.
- 2: One module or a small cluster depends on it.
- 1: It is a single file with no external dependents.

**Fix cost** is the estimated effort. Mark it as an estimate.
- 3: Several weeks, more than one team, or a migration.
- 2: Days of work for one team.
- 1: Hours of work, and the change is contained.

## Priority

`priority = impact × blast_radius`, from 1 to 9. Fix cost breaks ties. At equal priority, schedule the cheaper item first, because early results keep the team willing to spend time on debt. An item with fix cost 3 and priority 6 or higher gets a spike before the team schedules it.

## Context tag (optional)

The tag places the debt in Fowler's quadrant. One axis is deliberate or inadvertent, the other is prudent or reckless. It helps a retrospective tell a trade-off that the team chose under a deadline from a mistake that nobody saw. Do not use it for scoring.

## Validation checklist

Check every item against this list before it enters the backlog.
- [ ] The item has a layer, and findings that span layers are split.
- [ ] The item has evidence, which is a file path, a command output, an incident link, or a named contract gap.
- [ ] Each score matches its definition and has a one-line justification.
- [ ] A caller or dependency check supports the blast radius.
- [ ] The fix cost is marked as an estimate, and an item with fix cost 3 and priority 6 or higher has a spike step.
- [ ] The proposed action matches the layer's kind of fix.
