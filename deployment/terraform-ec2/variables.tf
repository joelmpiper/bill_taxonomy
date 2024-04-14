variable "aws_region" {
  description = "AWS region to launch servers."
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
  default     = null
}

variable "aws_user" {
  description = "AWS Account ID"
  type        = string
  default     = null
}
