import json
import os
import boto3
import logging
import datetime
from project import jwt

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ["TABLE_NAME"]
SECRET_KEY = os.environ["JWT_SECRET"]
table = dynamodb.Table(table_name)

def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def lambda_handler(event, context):
    try:
        # Parse request body if it's a string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])  # Parse JSON string to dictionary
        else:
            body = event  # If it's already a dictionary, use it directly
        
        staffID = body.get('ID')
        password = body.get('pwd')

        staffID = body['ID']  
        password = body['pwd']  
        
        
        response = table.get_item(
            Key={
                'StaffID': staffID
            }
        )
            
        # Check if the item exists
        if 'Item' in response:
            if response['Item']['Password'] == password:
                token = generate_jwt(staffID)
                return {
                    'statusCode': 200,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'success': True, 'redirect_url': '/index.html', 'token': token})
                }
            else:
                return {
                    'statusCode': 401,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'success': False, 'message': 'Invalid password'})
                }
        else:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'success': False, 'message': 'User not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

# test   
{
  "httpMethod": "POST",
  "body": "{\"ID\": \"17452\", \"pwd\": \"123\"}"
}