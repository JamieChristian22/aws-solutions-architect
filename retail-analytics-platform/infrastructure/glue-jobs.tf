resource "aws_glue_job" "raw_to_staged" {
  name     = "raw-to-staged-job"
  role_arn = aws_iam_role.glue_etl.arn
  command {
    name            = "glueetl"
    script_location = "s3://retail-analytics-platform/scripts/transform_raw_to_staged.py"
    python_version  = "3"
  }
  default_arguments = {
    "--RAW_PATH"    = "s3://retail-analytics-platform/raw/"
    "--STAGED_PATH" = "s3://retail-analytics-platform/staged/"
  }
}
