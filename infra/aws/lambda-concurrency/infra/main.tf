terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda" {
  name               = "lambda-concurrency-exp"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

resource "aws_iam_role_policy_attachment" "logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

locals {
  plain_zip = "${path.module}/../dist/plain.zip"
  lwa_zip   = "${path.module}/../dist/lwa.zip"
  # Public Web Adapter layer, latest version published in this region.
  lwa_layer = "arn:aws:lambda:${var.region}:753240598075:layer:LambdaAdapterLayerX86:28"
}

resource "aws_lambda_function" "plain" {
  function_name                  = "concurrency-plain"
  role                           = aws_iam_role.lambda.arn
  runtime                        = "nodejs22.x"
  handler                        = "lambda.handler"
  architectures                  = ["x86_64"]
  filename                       = local.plain_zip
  source_code_hash               = filebase64sha256(local.plain_zip)
  timeout                        = 30
  memory_size                    = 512
  reserved_concurrent_executions = var.reserved_concurrency

  environment {
    variables = {
      SLEEP_MS = tostring(var.sleep_ms)
    }
  }
}

resource "aws_lambda_function" "lwa" {
  function_name                  = "concurrency-lwa"
  role                           = aws_iam_role.lambda.arn
  runtime                        = "nodejs22.x"
  handler                        = "run.sh"
  architectures                  = ["x86_64"]
  filename                       = local.lwa_zip
  source_code_hash               = filebase64sha256(local.lwa_zip)
  timeout                        = 30
  memory_size                    = 512
  reserved_concurrent_executions = var.reserved_concurrency
  layers                         = [local.lwa_layer]

  environment {
    variables = {
      AWS_LAMBDA_EXEC_WRAPPER      = "/opt/bootstrap"
      PORT                         = "8000"
      AWS_LWA_READINESS_CHECK_PATH = "/healthz"
      RUST_LOG                     = "info"
      SLEEP_MS                     = tostring(var.sleep_ms)
    }
  }
}

resource "aws_lambda_function_url" "plain" {
  function_name      = aws_lambda_function.plain.function_name
  authorization_type = "NONE"
}

resource "aws_lambda_function_url" "lwa" {
  function_name      = aws_lambda_function.lwa.function_name
  authorization_type = "NONE"
}

# authorization_type = NONE still needs a resource policy granting public invoke.
resource "aws_lambda_permission" "plain_url" {
  statement_id           = "AllowPublicFunctionUrl"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.plain.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}

resource "aws_lambda_permission" "lwa_url" {
  statement_id           = "AllowPublicFunctionUrl"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.lwa.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}
