variable "aws_region" {
  description = "AWS region for the provider"
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "aws_user" {
  description = "AWS IAM user name"
  type        = string
}

