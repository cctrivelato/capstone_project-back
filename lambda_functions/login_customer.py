import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ["TABLE_NAME"]
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Parse request body if it's a string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])  # Parse JSON string to dictionary
        else:
            body = event  # If it's already a dictionary, use it directly
        
        customerID = body.get('ID')
        password = body.get('pwd')

        customerID = body['ID']  
        password = body['pwd']  
        
        
        response = table.get_item(
            Key={
                'CustomerID': customerID
            }
        )
            
        # Check if the item exists
        if 'Item' in response:
            if response['Item']['Password'] == password:
                return {
                    'statusCode': 200,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'success': True, 'redirect_url': '/welding_home.html'})
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