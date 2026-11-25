# Decommission checklist

Load this file only in the last phase, when all slices have shifted and their observation windows have passed. You cannot undo decommissioning after the code is deleted, so link evidence to every box.

## Traffic
- [ ] Logs or metrics show zero requests to the legacy component over the full observation window. Name the dashboard or query.
- [ ] A code search across all repos finds no remaining callers. Include cron jobs, scripts and other services.
- [ ] DNS, gateway and service-discovery entries are removed or point elsewhere, and nothing resolves to the legacy component.

## Data
- [ ] All data that the legacy component owns is migrated or archived on purpose, and its new owner is recorded.
- [ ] Counts, checksums or a reconciliation query verify the migration. A finished job is not proof.
- [ ] Backups of the legacy data are kept as policy requires before anything is deleted.

## Operations
- [ ] Alerts, dashboards and on-call runbooks for the legacy component are retired or point elsewhere.
- [ ] CI/CD pipelines, deploy targets and infrastructure for the legacy component are removed.
- [ ] Feature flags and routing rules for the migration are removed, and no unused toggle remains.

## Code and knowledge
- [ ] The legacy code is deleted. Do not comment it out, because version history keeps it.
- [ ] Documentation and architecture diagrams are updated, and an ADR records the decommission decision. Use the architecture-decision-records skill.
- [ ] The rollback window is formally closed. The team accepts that restoring legacy now means a restore from backup and no longer a routing change.

## Final gate
- [ ] Every box above links to evidence. An unchecked box blocks decommission. Schedule the missing work and do not proceed.
