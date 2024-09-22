resource "aws_security_group" "redshift_sg" {
  name   = "redshift_sg"
  vpc_id = aws_vpc.etl_vpc.id

  # Allow traffic from the entire VPC CIDR block
  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.etl_vpc.cidr_block]  # Allow all internal traffic from VPC
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Redshift Security Group"
  }
}
# Security Group for EC2 instance
resource "aws_security_group" "ec2_sg" {
  name   = "ec2_sg"
  vpc_id = aws_vpc.etl_vpc.id

  # Allow SSH access from your IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["78.55.199.124/32"]  # Replace with your public IP
  }

  # Allow EC2 instance to access Redshift on port 5439
  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.etl_vpc.cidr_block]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "EC2 Security Group"
  }
}
