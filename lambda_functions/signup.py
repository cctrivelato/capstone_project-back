import os
import json
import boto3
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event: any, context: any):
    try:
        body = json.loads(event["body"])

        firstname = body["firstname"]
        lastname = body["lastname"]
        phoneNum = body["phoneNum"]
        email_add = body["email_add"]
        pwd = body["pwd"]
        user_type = body["Type"]

        dynamodb = boto3.resource("dynamodb")
        table_name = os.environ["TABLE_NAME"]
        table = dynamodb.Table(table_name)

        item = {
            'User_Type': user_type,
            'FirstName': firstname,
            'LastName': lastname,
            'Phone': phoneNum,
            'Email': email_add,
            'Password': pwd
        }
        logger.info(f"Inserting item: {json.dumps(item)}")

        response = table.put_item(Item=item)

        logger.info(f"DynamoDB response: {json.dumps(response)}")

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": f"Successfully Subscribed {firstname} {lastname}. Your type of User: {user_type}. Thank you!"})
        }

    except Exception as e:
        logger.error(f"Error inserting item: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": f"Failed to insert item: {str(e)}"})
        }