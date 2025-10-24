resource "aws_kms_key" "phi_data" {
  description             = "KMS CMK for encrypting PHI data in S3 and Athena"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = {
    Purpose   = "HealthcareDataPlatform"
    ManagedBy = "Terraform"
  }
}

resource "aws_kms_alias" "phi_alias" {
  name          = "alias/phi-data-key"
  target_key_id = aws_kms_key.phi_data.key_id
}