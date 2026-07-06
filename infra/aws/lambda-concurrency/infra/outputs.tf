output "plain_url" {
  value = aws_lambda_function_url.plain.function_url
}

output "lwa_url" {
  value = aws_lambda_function_url.lwa.function_url
}
