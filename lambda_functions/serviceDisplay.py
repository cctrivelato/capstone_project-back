import json
import os
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

# Function to convert DynamoDB Decimal to float
def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(v) for v in obj]
    else:
        return obj

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',  # Restrict in production
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'OPTIONS, POST'
    }

    if event.get("httpMethod") == "OPTIONS":
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight successful'})
        }

    try:
        body = json.loads(event.get("body", "{}"))
        service_id = body.get("ServiceID")

        if not service_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Missing ServiceID'})
            }

        service = table.get_item(Key={'ServiceID': str(service_id)})

        response = decimal_to_float(service)

        if 'Item' not in response:
            return {
                'statusCode': 404,
                'serviceID': service_id,
                'headers': headers,
                'body': json.dumps({f'error': 'ServiceID not found'})
            }

        step = response['Item'].get('Step', 1)
        status = response.get("Item")

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'Step': step, "petType": f"{status.get('PetType')}", "petName": f"{status.get('PetName')}"})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'serviceID': service_id,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
