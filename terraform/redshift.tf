# Redshift Subnet Group
resource "aws_redshift_subnet_group" "redshift_subnet_group" {
  name        = "redshift-subnet-group"
  description = "Subnet group for Redshift"
  subnet_ids  = [aws_subnet.etl_subnet.id]

  tags = {
    Name = "Redshift Subnet Group"
  }
}

# Redshift Cluster
resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier  = "redshift-cluster-1"
  database_name       = "dev"  # Default Redshift database
  master_username     = "masteruser"
  master_password     = "SuperSecurePassword123!"
  node_type           = "dc2.large"
  cluster_type        = "single-node"
  publicly_accessible = true

  # Attach the Redshift security group
  vpc_security_group_ids = [aws_security_group.redshift_sg.id]

  # Use the subnet group
  cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet_group.name

  tags = {
    Name = "Redshift Cluster"
  }

  # Prevent Terraform from trying to modify these attributes unless explicitly changed
  lifecycle {
    ignore_changes = [
      cluster_identifier,
      database_name,
      master_username,
      master_password
    ]
  }
}


