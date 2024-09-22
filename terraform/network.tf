# Create an Internet Gateway for the VPC
resource "aws_internet_gateway" "etl_igw" {
  vpc_id = aws_vpc.etl_vpc.id

  tags = {
    Name = "ETL Internet Gateway"
  }
}

# Create a Route Table for the VPC
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.etl_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.etl_igw.id
  }

  tags = {
    Name = "ETL Public Route Table"
  }
}

# Associate the Route Table with the Public Subnet
resource "aws_route_table_association" "public_subnet_association" {
  subnet_id      = aws_subnet.etl_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}
