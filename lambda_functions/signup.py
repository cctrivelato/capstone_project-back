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
        staffID = body["ID"]

        dynamodb = boto3.resource("dynamodb")
        table_name = os.environ["TABLE_NAME"]
        table = dynamodb.Table(table_name)

        item = {
            'StaffID': staffID,
            'FirstName': firstname,
            'LastName': lastname,
            'Phone': phoneNum,
            'EmailAddress': email_add,
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
            "body": json.dumps({"message": f"Successfully Subscribed {firstname} {lastname}. Thank you!"})
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

# test 

{
    "body": "{\"firstname\": \"John\", \"lastname\": \"Doe\", \"phoneNum\": \"1234567890\", \"email_add\": \"john.doe@example.com\", \"pwd\": \"securepass\", \"ID\": \"12345\"}"
}
