# SSH access
resource "aws_key_pair" "ec2_key_pair" {
  key_name   = "my-key"  # for future reference
  public_key = file("####PATH_TO_PUBLIC_KEY####")  # ("~/.ssh/id_rsa.pub") normally
}

# ec2 in public subnet
resource "aws_instance" "ec2_instance" {
  ami           = "ami-0c02fb55956c7d316"  # amazon linux 2
  instance_type = "t2.micro"  

  key_name      = aws_key_pair.ec2_key_pair.key_name

  # public IP
  associate_public_ip_address = true

  # public subnet and security group
  subnet_id              = "####SUBNET_ID####"  # put subnet id according to location
  vpc_security_group_ids = ["[aws_security_group.ec2_sg.id]"]  
  # iam role fr access to s3 and redshift
  iam_instance_profile = "aws_iam_instance_profile.etl_instance_profile.name"   
  tags = {
    Name = "ETL Pipeline EC2"  # for referal in console
}
