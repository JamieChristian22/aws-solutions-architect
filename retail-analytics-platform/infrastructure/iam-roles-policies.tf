resource "aws_iam_role" "lambda_ingest" {
  name = "lambda-ingest-pos"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_ingest_policy" {
  name = "lambda-ingest-pos-policy"
  role = aws_iam_role.lambda_ingest.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["kinesis:PutRecord"]
      Resource = "*"
    },{
      Effect   = "Allow"
      Action   = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      Resource = "*"
    }]
  })
}
