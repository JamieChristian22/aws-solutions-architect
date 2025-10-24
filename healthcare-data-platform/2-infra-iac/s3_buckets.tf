resource "aws_s3_bucket" "raw" {
  bucket         = "hcp-raw-zone"
  force_destroy  = true

  versioning { enabled = true }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "aws:kms"
        kms_master_key_id = aws_kms_key.phi_data.id
      }
    }
  }

  lifecycle_rule {
    id      = "archive"
    enabled = true
    transition {
      days          = 90
      storage_class = "DEEP_ARCHIVE"
    }
  }

  tags = {
    Environment = "prod"
    DataZone    = "raw"
  }
}

resource "aws_s3_bucket" "curated" {
  bucket = "hcp-curated-zone"

  versioning { enabled = true }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "aws:kms"
        kms_master_key_id = aws_kms_key.phi_data.id
      }
    }
  }

  tags = {
    Environment = "prod"
    DataZone    = "curated"
  }
}

resource "aws_s3_bucket" "analytics" {
  bucket = "hcp-analytics-zone"

  versioning { enabled = true }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "aws:kms"
        kms_master_key_id = aws_kms_key.phi_data.id
      }
    }
  }

  lifecycle_rule {
    id      = "glacier"
    enabled = true

    transition {
      days          = 60
      storage_class = "GLACIER"
    }
  }

  tags = {
    Environment = "prod"
    DataZone    = "analytics"
  }
}