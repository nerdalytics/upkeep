---
name: strangler-migration
description: "Plans and carries out the step-by-step replacement of a legacy system or component behind a facade or router, the Strangler Fig pattern. It covers the inventory, thin slices, contract tests, a traffic shift with a rollback for each slice, and decommission. Use when the user wants to replace, rewrite or retire a legacy system, extract a service from a monolith, or move off a component without a big-bang cutover."
license: MIT
---

# Strangler migration

Replace a legacy system in steps, behind an indirection layer, while it keeps serving traffic. Move no code until you have validated the migration plan against the real inventory of routes and components. For everyday edits inside legacy code, use legacy-safe-change.

## Workflow

Progress:
- [ ] Step 1. Load the project skill `maintainability-records` through this plugin's init skill, `upkeep:init`. It returns at once when it is current, and generates it when not. Then take the inventory from the source of truth. Extract the real list of routes, endpoints and components from code and config, such as router definitions, gateway config and handler registrations. Save it as `inventory.md` in a folder for this component, at the place `maintainability-records` gives for migration plans. You validate the plan against it.
- [ ] Step 2. Select the first thin slice. It is low in risk, easy to understand, and useful by itself. It is one endpoint or one component, not a subsystem.
- [ ] Step 3. Characterize the behavior of that slice with the legacy-safe-change procedure, and pin its interface with contract tests.
- [ ] Step 4. Write the migration plan from `assets/migration-plan-template.md` to `plan.md` next to the inventory. The plan stays the authoritative record until decommission, so name its owner in it and update it as slices move. Follow `maintainability-records` on what is committed. You can extract the inventory from the code again, so it is a working file. Then validate the plan against the Step 1 inventory. Every route in the plan must exist in the inventory. Every inventory entry must belong to a slice or carry the mark stay-legacy. A route that is missing from the inventory fails validation, and so does an entry without a slice. Fix the plan before you execute it.
- [ ] Step 5. Add the facade or router. At first it forwards everything to legacy. The contract tests must stay green to show that behavior is unchanged.
- [ ] Step 6. Build the slice behind the facade. Shift traffic to it in steps. Define the rollback for the slice in the plan before the shift starts.
- [ ] Step 7. Repeat for the other slices in plan order. Legacy stays authoritative for everything that has not shifted.
- [ ] Step 8. When all slices have shifted and are stable, load `references/decommission-checklist.md` and retire the legacy component.

## Gotchas

- A facade with no decommission date becomes a permanent second system. Put the decommission criteria into the plan from the start.
- A shared database couples slices without anyone noticing. Decide in the plan which slice owns which data. Two services that write to one table are a distributed monolith.
- Do not cut the whole router over at once. Shift one slice, observe it, then go on. The rollback must be a routing change that needs no redeploy of the legacy system.
- Contract tests pin the interface, which is the request and response shapes and the error codes. They do not pin the implementation. If a contract test breaks during the shift, the slice is wrong and the test is right.
- Do not rename or improve the API during the migration, because that doubles the risk. Migrate first. Improve the API later as a separate change.
- Do not shift traffic until both paths have metrics and logs. Without them you cannot compare the new path with the legacy path.
