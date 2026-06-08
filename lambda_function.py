import json
import boto3
import os

def lambda_handler(event, context):
    # try to parse the data from API Gateway
    try:
        # if it's API Gateway then body should be json
        body = json.loads(event.get("body", "{}"))
        user = body.get("user")
    except:
        
        user = event.get("user")

    if not user:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": "Missing 'user' parameter"})
        }

    # dynamodb operation
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)

    # get the current count
    response = table.get_item(Key={"user": user})
    visit_count = response.get("Item", {}).get("visit_count", 0)

    # increment the count and update
    visit_count += 1
    table.put_item(Item={"user": user, "visit_count": visit_count})

    # returns a response conforming to the API Gateway format
    message = f"Hello {user}! You have visited us {visit_count} times."
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": message})
    }