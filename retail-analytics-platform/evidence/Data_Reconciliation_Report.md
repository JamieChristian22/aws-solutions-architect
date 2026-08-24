# Retail Data Reconciliation Report

## Control Totals
Every daily ingestion batch should reconcile:
- source order count
- ingested order count
- curated order count
- net-sales total
- returned-unit total

## Example Acceptance Logic
A batch passes when:
- count variance = 0
- net-sales variance < $0.01 rounding tolerance per batch
- all store/product/channel keys resolve
- no future-dated transactions beyond configured tolerance

Failed batches remain in landing/quarantine and do not overwrite the prior trusted curated partition.
