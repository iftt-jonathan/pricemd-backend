# Route configuration
locals {
  lambda_zip = "lambda-output.zip"
  lambda_layer_zip = "lambda-layer.zip"
  runtime = "python3.12"

  lambda_functions = [
    { route = "POST /api/v1/procedure/search", handler = "lambda.routes.procedure_router.search_handler" },
    { route = "GET /api/v1/procedure/{procedureId}/by-insurance/{insuranceId}", handler = "lambda.routes.procedure_router.get_handler" }
  ]
}

# Infrastructure setup
provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  description = "IAM policy for logging from a lambda"
  policy      = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Action   = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      Effect   = "Allow"
      Resource = "arn:aws:logs:*:*:*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

locals {
  # Name each lambda according to its route
  lambda_map = { for fn in local.lambda_functions : fn.route => {
    function_name = replace(fn.route, "/[^a-zA-Z0-9]/", "_")
    handler       = fn.handler
  }}
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename            = local.lambda_layer_zip
  layer_name          = "pricemd_layer"
  description         = "Layer for shared libraries"
  compatible_runtimes = [local.runtime]
}

resource "aws_lambda_function" "lambdas" {
  for_each      = local.lambda_map
  function_name = each.value.function_name
  role          = aws_iam_role.lambda_role.arn
  handler       = each.value.handler
  runtime       = local.runtime
  layers        = [aws_lambda_layer_version.lambda_layer.arn]

  filename         = local.lambda_zip
  source_code_hash = filebase64sha256(local.lambda_zip)
}

resource "aws_apigatewayv2_api" "http_api" {
  name          = "pricemd"
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key", "X-Amz-Security-Token"]
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integrations" {
  for_each             = local.lambda_map
  api_id               = aws_apigatewayv2_api.http_api.id
  integration_type     = "AWS_PROXY"
  integration_uri      = aws_lambda_function.lambdas[each.key].invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "lambda_routes" {
  for_each  = local.lambda_map
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = each.key
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integrations[each.key].id}"
}

resource "aws_lambda_permission" "api_gateway_permissions" {
  for_each      = local.lambda_map
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambdas[each.key].function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}

# Output API Gateway URL
output "api_gateway_url" {
  value = aws_apigatewayv2_api.http_api.api_endpoint
}


data "aws_s3_bucket" "existing_bucket" {
  bucket = "428-pricemd"
}

# Upload the API Gateway URL to a specific path in the PriceMD bucket
resource "aws_s3_object" "api_gateway_url_file" {
  bucket  = data.aws_s3_bucket.existing_bucket.id
  key     = "api/url-latest"
  content = aws_apigatewayv2_api.http_api.api_endpoint
  acl     = "private" # currently private, we might need to set up an API key so that people can't spam this
}
