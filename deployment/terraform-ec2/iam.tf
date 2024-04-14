resource "aws_iam_policy" "secrets_manager_policy" {
  name        = "SecretsManagerAccessPolicy"
  description = "Policy to access specific secrets in AWS Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "secretsmanager:GetSecretValue"
        Effect   = "Allow"
        Resource = [
          "arn:aws:secretsmanager:${var.aws_region}:${var.aws_account_id}:secret:local/dev/postgres/*",
        ]
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "user_secrets_policy_attachment" {
  user       = var.aws_user  # Replace with your actual IAM user name
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
}
