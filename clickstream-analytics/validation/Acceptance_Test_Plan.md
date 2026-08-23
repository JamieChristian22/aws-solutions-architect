# Acceptance Test Plan

| Test | Pass Condition |
|---|---|
| Schema sample validation | 100% valid sample events accepted |
| CDK/Python syntax | compile succeeds |
| Sustained load | 1,000 events/sec for 30 min |
| Peak load | 5,000 events/sec for 10 min |
| API latency | p95 <250 ms |
| Iterator age | returns <60 sec after burst |
| Invalid schema | rejected with HTTP 400 |
| Oversized payload | rejected with HTTP 413 |
| S3 freshness | p95 <15 min |
| OpenSearch freshness | p95 <60 sec |
| Error isolation | poison record enters error/replay workflow |
| DR tabletop | 60-minute RTO procedure validated |
