# FinOps and Cost Optimization

This is an **architecture planning model**, not a live AWS invoice.

| Metric | Modeled Value |
|---|---:|
| Baseline | $11,500/month |
| Optimization backlog | $1,520/month |
| Optimized run rate | $9,980/month |
| Annualized opportunity | $18,240/year |
| Reduction | 13.2% |

## Major Levers
- OpenSearch sizing and index lifecycle.
- Parquet conversion and partition pruning.
- S3 lifecycle.
- Kinesis mode review after measured traffic stabilizes.
- Lambda memory/duration tuning.
- CloudWatch log retention.

## Cost Guardrails
- budget alerts at 50/80/100%
- cost anomaly review
- service-level cost allocation tags
- Athena workgroup scan limits
- OpenSearch storage/JVM dashboards
- event-volume anomaly alarm
