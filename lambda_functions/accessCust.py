from project import jwt
import json
import os
import logging
import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ["TABLE_NAME"]

def get_user_from_dynamodb(user_id):
    table = dynamodb.Table(table_name)
    
    try:
        response = table.get_item(Key={"CustomerID": user_id})
        return response.get("Item") 
    
    except (BotoCoreError, ClientError) as e:
        print(f"DynamoDB error: {e}")
        return None

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS, GET",
        "Access-Control-Allow-Headers": "Authorization, Content-Type"
    }

    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight successful"})
        }

    # Get Authorization header
    auth_header = event.get("headers", {}).get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return {
            "statusCode": 401,
            "headers": headers,
            "body": json.dumps({"message": "Unauthorized"})
        }

    token = auth_header.split(" ")[1]

    try:
        SECRET_KEY = os.environ["JWT_SECRET"]   
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        user_id = decoded_token.get("CustomerID")  # Assuming 'CustomerID' is in the payload
        if not user_id:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Invalid token structure"})
            }

        # Query DynamoDB for the user
        user = get_user_from_dynamodb(user_id)
        if not user:
            return {
                "statusCode": 404,
                "headers": headers,
                "body": json.dumps({"message": "User not found"})
            }

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": f"Welcome back, {user.get('FirstName')}!"})
        }

    except jwt.ExpiredSignatureError:
        return {
            "statusCode": 401,
            "headers": headers,
            "body": json.dumps({"message": "Token expired"})
        }

    except jwt.InvalidTokenError:
        return {
            "statusCode": 401,
            "headers": headers,
            "body": json.dumps({"message": "Invalid token"})
        }
    
{
  "statusCode": 200,
  "headers": {
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"success\": true, \"redirect_url\": \"/C:/Users/ctrivelato/Documents/GitHub/capstone_project-front/customer_page/customer_home.html\", \"token\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJDdXN0b21lcklEIjoiMTIzNDUiLCJleHAiOjE3NDE5MDM0NDcsImlhdCI6MTc0MTg5OTg0N30.TFt9w-n7wa8jDFS4SfA8WcFFQrQxhk0A-YGf94pRIS0\"}"
}