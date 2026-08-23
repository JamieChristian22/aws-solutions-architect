variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "dr_region" {
  type    = string
  default = "us-west-2"
}

variable "project_name" {
  type    = string
  default = "northstar-platform"
}

variable "environment" {
  type    = string
  default = "prod"
}

variable "vpc_cidr" {
  type    = string
  default = "10.40.0.0/16"
}

variable "db_name" {
  type    = string
  default = "northstar"
}

variable "db_username" {
  type    = string
  default = "northstar_admin"
}

variable "container_image" {
  type    = string
  default = "public.ecr.aws/nginx/nginx:stable"
}

variable "certificate_arn" {
  type        = string
  description = "ACM certificate ARN supplied through environment configuration for HTTPS."
  sensitive   = false
  default     = ""
}
