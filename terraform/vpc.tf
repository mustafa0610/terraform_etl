# Create a VPC
resource "aws_vpc" "etl_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "ETL VPC"
  }
}

# Public Subnet for the VPC
resource "aws_subnet" "etl_subnet" {
  vpc_id            = aws_vpc.etl_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "ETL Public Subnet"
  }
}
