import boto3
import simplejson as json
import logging
import requests
import os

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
TABLE_NAME = os.getenv('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')

# Use logs in order to have formatted output that can be easily parsed.
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        location = requests.get("http://checkip.amazonaws.com/").text.replace("\n", "")
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        logging.error(e)
        raise e

    table = dynamodb.Table(TABLE_NAME)
    response = table.update_item(
        Key={ 'location': location },
        UpdateExpression="SET seen = if_not_exists (seen, :c) + :i",
        ExpressionAttributeValues={ ':c': 0, ':i': 1 },
        ReturnValues="UPDATED_NEW"
    )
    return {
        "statusCode": 200,
        "headers": {
            # In order to configure CORS while using Lambda Proxy integration 
            # it is important to add the following header (no set by
            # APIGateway... )
            # "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json" 
        },
        "body": json.dumps(response["Attributes"], use_decimal=True),
    }
