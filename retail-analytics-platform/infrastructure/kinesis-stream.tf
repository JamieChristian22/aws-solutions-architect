resource "aws_kinesis_stream" "pos_stream" {
  name             = "retail-pos-stream"
  shard_count      = 1
  retention_period = 24
  shard_level_metrics = ["IncomingBytes","OutgoingBytes","WriteProvisionedThroughputExceeded"]
}
