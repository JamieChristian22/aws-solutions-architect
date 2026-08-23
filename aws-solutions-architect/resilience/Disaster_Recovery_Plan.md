# Disaster Recovery Plan

## Objectives
- Primary: `us-east-1`
- DR: `us-west-2`
- Regional RTO: 60 minutes
- Transactional RPO target: 15 minutes

## Strategy
Warm standby/rebuildable application tier with replicated/recoverable data. Terraform recreates regional infrastructure. Critical object data uses replication where justified. Database recovery uses cross-region backups/snapshots and documented restore automation.

## Regional Recovery Procedure
1. Declare regional disaster after incident-command approval.
2. Freeze nonessential deployments.
3. Confirm latest recoverable database point and replicated object state.
4. Deploy/validate DR network, load balancer, compute, IAM, and observability from Terraform.
5. Restore database in `us-west-2`.
6. Inject DR secrets/configuration.
7. Run smoke tests and data integrity validation.
8. Increase DR service desired count to production level.
9. Switch Route 53/edge origin to DR.
10. Monitor error rate, latency, and data writes.
11. Record actual RTO/RPO achieved.

## Failback
Failback is a planned change, not an automatic reversal. Re-synchronize data, validate primary environment, schedule maintenance window, shift traffic, and monitor.

## Quarterly Test Evidence
Record start/end time, restore point, infrastructure deployment result, smoke-test results, data checks, DNS cutover duration, lessons learned, and action owners.
