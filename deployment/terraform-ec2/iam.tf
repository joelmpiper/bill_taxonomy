resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "ec2.amazonaws.com",
        },
        Effect = "Allow",
        Sid = "",
      },
    ]
  })
}

resource "aws_iam_policy" "secrets_manager_policy" {
  name        = "SecretsManagerAccessPolicy"
  description = "Policy to access specific secrets in AWS Secrets Manager"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "secretsmanager:GetSecretValue",
        Effect   = "Allow",
        Resource = "arn:aws:secretsmanager:${var.aws_region}:${var.aws_account_id}:secret:local/dev/postgres/*"
      },
    ]
  })
}

resource "aws_iam_policy_attachment" "secrets_policy_attachment" {
  name       = "example-secrets-policy-attachment"
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
  roles      = [aws_iam_role.ec2_role.name]
}
