# Capacity Model
- Fleet: 10,000
- Sustained: 166.67 msg/sec
- Peak: 1,000 msg/sec
- Daily messages: 14,400,000
- Raw GB/day: 7.373
- Raw GB/month: 221.18
- Parquet GB/month: 55.30

On-demand Kinesis is selected for reconnect bursts. Firehose targets <15-minute lake freshness. Load gates: normal fleet load for 30 minutes and 1,000 msg/sec burst for 10 minutes.
