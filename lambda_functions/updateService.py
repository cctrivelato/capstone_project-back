import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Methods": "OPTIONS, POST"
    }

    try:
        body = json.loads(event['body'])
        service_id = body.get('ServiceID')
        new_step = body.get('Step')

        if not service_id or new_step is None:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "Missing ServiceID or Step"})
            }

        # Get the existing item
        response = table.get_item(Key={'ServiceID': service_id})

        if 'Item' not in response:
            return {
                "statusCode": 404,
                "headers": headers,
                "body": json.dumps({"error": "ServiceID not found"})
            }

        item = response['Item']
        item['Step'] = Decimal(str(new_step))  # Ensure it's stored as Decimal

        # Put the updated item back into the table
        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "Step updated successfully", "service": item}, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
