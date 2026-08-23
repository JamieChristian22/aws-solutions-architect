locals {
  common_tags = {
    Environment        = var.environment
    Application        = var.project_name
    Owner              = "platform-team"
    CostCenter         = "CC-4100"
    ManagedBy          = "terraform"
    DataClassification = "confidential"
  }

  public_subnets  = ["10.40.0.0/24", "10.40.1.0/24"]
  app_subnets     = ["10.40.10.0/24", "10.40.11.0/24"]
  db_subnets      = ["10.40.20.0/24", "10.40.21.0/24"]
}
