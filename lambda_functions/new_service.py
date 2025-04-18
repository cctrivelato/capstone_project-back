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
        petname = body["petname"]
        pet_type = body["PetType"]
        service_num = body["ServiceID"]
        email_addr = body["Email"]
        step = 0

        dynamodb = boto3.resource("dynamodb")
        table_name = os.environ["TABLE_NAME"]
        table = dynamodb.Table(table_name)

        item = {
            'ServiceID': service_num,
            'CustomerFirstName': firstname,
            'Email': email_addr,
            'PetName': petname,
            'PetType': pet_type,
            'Step': step
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
            "body": json.dumps({"message": f"Successfully added a new service status update for {firstname}. Your Service Number is: {service_num}. Thank you!"})
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