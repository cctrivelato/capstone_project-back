import json
import os
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')

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
    # Define the DynamoDB table name
    table_name = os.environ["TABLE_NAME"] 
    
    # Get the reference to the DynamoDB table
    table = dynamodb.Table(table_name)
    
    # Query the table to find services in progress
    try:
        # Parse request body if it's a string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])  # Parse JSON string to dictionary
        else:
            body = event  # If it's already a dictionary, use it directly
        
        email_addr = body.get('Email')
        user_type = body.get('Type')

        if user_type == 'Staff':
            response = table.scan(
                FilterExpression=Attr('Step').lte(4)
            )

        else:
            response = table.scan(
                FilterExpression=Attr('Email').eq(email_addr) & Attr('Step').lte(4)
            )
        
        services_in_progress = response.get('Items', [])
        
        # Convert Decimal to float before returning
        services_in_progress = decimal_to_float(services_in_progress)
        
        # Return the response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'services': services_in_progress,
                'count': len(services_in_progress)
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Allow all origins
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'  # Allow specific methods
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            }
        }