# Debt item schema

Write one YAML document per item. Keep the field names exact so that tools can filter the backlog.

```yaml
id: DEBT-0001
title: short imperative summary
layer: code | architecture | organizational
evidence:
  - "src/billing/coupons.py:120-180 (hotspots.py: 23 commits, 640 lines)"
  - "incident INC-2041 postmortem, section 'root cause'"
impact: 1 | 2 | 3
impact_justification: one line tied to the rubric's definition
blast_radius: 1 | 2 | 3
blast_radius_justification: one line that names the caller or dependency check
fix_cost: 1 | 2 | 3
fix_cost_is_estimate: true
priority: 1-9
quadrant: reckless-deliberate | prudent-deliberate | reckless-inadvertent | prudent-inadvertent | unknown
proposed_action: concrete next step that matches the layer's kind of fix
spike_required: true | false
related_items: [DEBT-0002]
owner: team or person, or unassigned
status: proposed | accepted | scheduled | in-progress | paid | rejected
```

Rules:
- `priority` must equal `impact × blast_radius`. A mismatch fails validation.
- `evidence` is never empty. Reject an item that has no evidence.
- Set `spike_required: true` when `fix_cost` is 3 and `priority` is 6 or higher.
- The tracker keeps the history of status changes. The item file holds only the current status.
