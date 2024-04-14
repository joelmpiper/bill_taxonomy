resource "aws_instance" "example" {
  ami           = "ami-051f8a213df8bc089"  # Replace with a valid AMI for your region
  instance_type = "t2.micro"

  tags = {
    Name = "MyExampleInstance"
  }
}
