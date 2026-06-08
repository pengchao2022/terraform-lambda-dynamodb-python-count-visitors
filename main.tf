provider "aws" {
  region = "us-east-1"
  
}

# call a module
module "dynamodb" {
  source = "git::https://github.com/pengchao2022/aws-terraform-modules.git//modules/dynamoDB?ref=dynamoDB-1.0"

  table_name = "visit-count"
  
  
}

module "lambda" {
  source = "git::https://github.com/pengchao2022/aws-terraform-modules.git//modules/lambda?ref=lambda-1.0"

  # write the variables according to the lambda nodule variables.tf
  function_name = "maxwell-prod-visit-counter"
  source_file   = "${path.module}/lambda_function.py"

  table_name    = module.dynamodb.table_name
  table_arn     = module.dynamodb.table_arn
  
  
}