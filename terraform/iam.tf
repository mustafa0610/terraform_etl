# IAM Role for EC2 to access S3 and Redshift
resource "aws_iam_role" "etl_role" {
  name = "etl-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach policy for EC2 to access S3 and Redshift
resource "aws_iam_role_policy" "etl_role_policy" {
  name = "ETLRolePolicy"
  
  # Corrected: Added the "role" argument that references the IAM role created above
  role = aws_iam_role.etl_role.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "${aws_s3_bucket.etl_data_bucket.arn}",
        "${aws_s3_bucket.etl_data_bucket.arn}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "redshift:DescribeClusters",
        "redshift:DescribeLoggingStatus",
        "redshift-data:ExecuteStatement"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

# Attach the IAM Role to the EC2 instance
resource "aws_iam_instance_profile" "etl_instance_profile" {
  name = "etl-instance-profile"
  role = aws_iam_role.etl_role.name
}
