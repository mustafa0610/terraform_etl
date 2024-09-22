# Output the EC2 instance's public IP for SSH access
output "ec2_public_ip" {
  value = aws_instance.ec2_instance.public_ip
  description = "Public IP of the EC2 instance"
}

# Output the S3 bucket name
output "s3_bucket_name" {
  value = aws_s3_bucket.etl_data_bucket.bucket
  description = "S3 Bucket for raw data"
}

# Output the Redshift cluster endpoint
output "redshift_endpoint" {
  value = aws_redshift_cluster.redshift_cluster.endpoint
  description = "Redshift cluster endpoint"
}
