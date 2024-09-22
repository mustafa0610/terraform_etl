# S3 Bucket to store raw data
resource "aws_s3_bucket" "etl_data_bucket" {
  bucket = "etl-pipeline-data-bucket"

  tags = {
    Name = "ETL Data Bucket"
  }
}

# Disable block public access to allow bucket policies
resource "aws_s3_bucket_public_access_block" "public_access_block" {
  bucket = aws_s3_bucket.etl_data_bucket.id

  block_public_acls   = false
  block_public_policy = false
}

# Allow public read access
resource "aws_s3_bucket_policy" "etl_bucket_policy" {
  bucket = aws_s3_bucket.etl_data_bucket.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "${aws_s3_bucket.etl_data_bucket.arn}/*"
        }
    ]
}
EOF
}
