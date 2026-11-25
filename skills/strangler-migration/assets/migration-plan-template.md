# Migration plan from {legacy component} to {target}

**Owner:** {person or team who keeps this plan current}
**Inventory source:** {file or command that produced the list of routes and components, and the path it is saved at}
**Validation:** every route below exists in the inventory, and every inventory entry belongs to a slice or is marked stay-legacy. {validated yes or no, and the discrepancies found and fixed}

## Slices

| Order | Slice (routes or components) | Why this order | Characterization tests | Contract tests | Data ownership |
|-------|------------------------------|----------------|------------------------|----------------|----------------|
| 1 | {for example GET /coupons} | {thin, low risk, useful by itself} | {path, green on legacy} | {path} | {who owns the data after the shift} |

Stay-legacy, not migrated: {entries and the reason for each}

## Facade

- Mechanism: {API gateway, reverse proxy, or in-process router}
- Initial state: it forwards everything to legacy, and the contract tests are green
- Routing config location: {path}

## Traffic shift per slice

| Slice | Shift steps (percentages or cohorts) | Observation window | Success signals | Rollback (the exact routing change) |
|-------|--------------------------------------|--------------------|-----------------|-------------------------------------|
| 1 | {1%, then 10%, then 50%, then 100%} | {duration and what you watch} | {error rate, latency, and business metrics that match legacy} | {switch route X back to legacy, with no redeploy} |

Observability prerequisite: metrics and logs exist on both paths before the first shift. {links}

## Decommission criteria

- All slices have shifted and have been stable for {observation window}
- Logs or metrics show zero legacy traffic
- `references/decommission-checklist.md` is complete

## Risks and open questions

- {risk}: {mitigation or owner}
