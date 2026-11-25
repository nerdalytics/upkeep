---
name: tech-debt-triage
description: "Turns maintainability findings into a prioritized technical-debt backlog. Each item is classified as code, architecture or organizational debt, cites evidence, and has scores for impact, blast radius and fix cost. Use when the user asks to prioritize or groom technical debt, plan refactoring work, or turn an audit report, review comments or incident notes into backlog items."
license: MIT
---

# Tech debt triage

Turn findings into backlog items that a team can schedule. Every item cites evidence, names its layer, and has scores tied to the rubric. Reject an item that has no evidence. This skill classifies and prioritizes. Measuring is the job of `audit`. Carrying out the fix is the job of legacy-safe-change or strangler-migration.

## Workflow

Progress:
- [ ] Step 1. Load the project skill `maintainability-records` through this plugin's init skill, `upkeep:init`. It returns at once when it is current, and generates it when not. Then collect the inputs from the places it names. These are audit gap reports, debt spin-offs from reviews, incident postmortems, and notes on stalled migrations. Findings pasted into the conversation count too.
- [ ] Step 2. Classify each finding as code, architecture, or organizational debt. Read `references/prioritization-rubric.md` for the definitions. When a finding spans layers, split it into one item per layer.
- [ ] Step 3. Score impact, blast radius, and fix cost on the rubric's scales. Take the blast radius from the dependency graph or a caller search. Do not estimate it.
- [ ] Step 4. Write each item from `assets/debt-item-template.md`. Tools filter the backlog by field name, so keep the field names exact. A backlog has one authoritative home, and `maintainability-records` names it. If it is the repository, save each item there in the naming that skill gives, and take the next id from the directory listing. If it is an issue tracker, create the items there with the command that skill gives, after the user has approved the list. Then reply with the paths or links and the ordered backlog.
- [ ] Step 5. Check every item against the rubric's validation checklist before you report the backlog. Fix or drop the items that fail.
- [ ] Step 6. Recommend capacity. The team reserves a fixed share of each sprint for debt and sets that share itself. Order the backlog by priority. At equal priority, the item with the lower fix cost comes first.

## Gotchas

- Debt spin-offs from reviews capture only code debt. Architecture debt sits between modules, as cycles, undocumented contracts, or a wrong dependency direction. Organizational debt sits with people, as knowledge held by one person or missing ownership. Look for all three layers on purpose. Otherwise the backlog covers only the debt that is easy to see.
- "This feels messy" is not evidence. An item needs a file path, a command output, an incident link, or a named contract gap.
- Refactoring does not fix organizational debt. Its fixes are documentation, pairing, rotation, or a change of ownership. If you score it like code debt, it ends up at the bottom of the backlog.
- A stalled migration is a debt item even when nobody complains about it. Half-moved code has to be maintained in two places.
- A fix cost is a guess until someone tries the change in a spike. Mark it as an estimate and revise it after the first attempt.
- Do not raise a priority to get an item scheduled. The team must be able to check each priority against the rubric.
