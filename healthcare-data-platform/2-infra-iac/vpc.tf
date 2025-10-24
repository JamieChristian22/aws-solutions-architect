resource "aws_vpc" "hcp_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name    = "hcp-vpc"
    Purpose = "HealthcareDataPlatform"
  }
}

resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.hcp_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "hcp-private-1"
  }
}

resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.hcp_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "hcp-private-2"
  }
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.hcp_vpc.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = [aws_vpc.hcp_vpc.main_route_table_id]

  tags = {
    Name = "hcp-s3-endpoint"
  }
}