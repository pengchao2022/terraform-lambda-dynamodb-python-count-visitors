import json
import boto3
import os

def lambda_handler(event, context):
    # 1. 尝试解析 API Gateway 传来的 body
    try:
        # 如果是 API Gateway 触发，body 是 JSON 字符串
        body = json.loads(event.get("body", "{}"))
        user = body.get("user")
    except:
        # 如果是测试触发（直接传字典），则直接获取
        user = event.get("user")

    if not user:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": "Missing 'user' parameter"})
        }

    # 2. DynamoDB 操作
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)

    # 获取当前计数
    response = table.get_item(Key={"user": user})
    visit_count = response.get("Item", {}).get("visit_count", 0)

    # 增加计数并更新
    visit_count += 1
    table.put_item(Item={"user": user, "visit_count": visit_count})

    # 3. 返回符合 API Gateway 格式的响应
    message = f"Hello {user}! You have visited us {visit_count} times."
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": message})
    }