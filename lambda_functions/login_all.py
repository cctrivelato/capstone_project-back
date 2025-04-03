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

def generate_jwt(email, user_type):
    payload = {
        "Email": email,
        "User_Type": user_type,
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
        
        email = body.get('Email')
        password = body.get('pwd')
        user_type = body.get('Type')

        email = body['Email']  
        password = body['pwd']
        user_type = body.get('Type')
        
        response = table.get_item(
            Key={
                'Email': email
            }
        )
            
        # Check if the item exists
        if 'Item' in response:
            if response['Item']['Password'] == password:
                token = generate_jwt(email, user_type)
                return {
                    'statusCode': 200,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'success': True, 'redirect_url': 'loading.html', 'token': token})
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
    
{
  "httpMethod": "POST",
  "body": "{\"ID\": \"12345\", \"pwd\": \"securepass\"}"
}