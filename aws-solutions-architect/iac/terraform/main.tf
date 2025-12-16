# Terraform – AWS Baseline Infrastructure
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "logs" {
  bucket = "example-log-bucket"
}
