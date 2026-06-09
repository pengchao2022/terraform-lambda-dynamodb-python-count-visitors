provider "aws" {
  region = "us-east-1"
  
}

# call a module
module "dynamodb" {
  source = "git::https://github.com/pengchao2022/aws-terraform-modules.git//modules/dynamoDB?ref=dynamoDB-1.0"

  table_name = "visit-count"
  
  
}

module "lambda" {
  source = "git::https://github.com/pengchao2022/aws-terraform-modules.git//modules/lambda?ref=lambda-1.3"
  # force re-deploy when python code get changed
  source_code_hash = filebase64sha256("${path.module}/lambda_function.py")

  # write the variables according to the lambda nodule variables.tf
  function_name = "maxwell-prod-visit-counter"
  source_file   = "${path.module}/lambda_function.py"

  table_name    = module.dynamodb.table_name
  table_arn     = module.dynamodb.table_arn
  
  
}

module "api_gateway" {
  source = "git::https://github.com/pengchao2022/aws-terraform-modules.git//modules/api_gateway?ref=api_gateway-1.4"
  
  api_name = "visit-counter-api"
  lambda_invoke_arn    = module.lambda.lambda_invoke_arn
  lambda_function_name = module.lambda.lambda_name 

  create_iam_resources = true
}

# outputs API URL
output "api_endpoint_url" {
  value = module.api_gateway.invoke_url

}

  
