# FinOps Optimization Business Case

This is a modeled business case built from the repository's baseline. It is not a live AWS Cost Explorer export.

## Decision Sequence
1. Remove clearly idle resources.
2. Apply storage/log lifecycle changes.
3. Observe 30-day utilization.
4. Rightsize compute and database.
5. Evaluate Graviton compatibility.
6. Purchase commitments only after the post-rightsizing baseline stabilizes.

## Governance Guardrail
Savings projections are not counted as realized savings until the associated technical change is implemented and the next billing period confirms the reduction.
