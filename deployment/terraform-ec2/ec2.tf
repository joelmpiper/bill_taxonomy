resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.ec2_role.name
}

resource "aws_instance" "example" {
  ami           = "ami-051f8a213df8bc089"  # Ensure this AMI is valid in your region
  instance_type = "t2.micro"
  key_name      = "MyKeyPair"  # Referencing the key pair resource
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  user_data = file("${path.module}/../ec2_startup.sh")

  security_groups = [aws_security_group.example_sg.name]

  tags = {
    Name = "MyExampleInstance"
  }
}

resource "aws_security_group" "example_sg" {
  name        = "example_sg"
  description = "Allow necessary traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "vpc-04236860" # Ensure this references an existing VPC or define it if not yet created
}
