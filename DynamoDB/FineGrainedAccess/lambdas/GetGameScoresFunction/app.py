from boto3.dynamodb.conditions import Key
import boto3
import datetime
import json
import logging
import os

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
TABLE_NAME = os.getenv('TABLE_NAME')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def default(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def lambda_handler(event, context):
    sourceIp = event.get('requestContext', {}).get(
        'identity', {}).get('sourceIp', None)
    if sourceIp:
        try:
            item = table.get_item(Key={'id': sourceIp})['Item']
        except Exception as e:
            logger.error(str(e))
            item = {"error": str(e)}
    else:
        # Perform a scan
        item= []
        scan_kwargs = {
            # 'FilterExpression': Key('year').between(*year_range),
            'ProjectionExpression': "id, score, #timestamp",
            'ExpressionAttributeNames': {"#timestamp": "timestamp"}
        }
        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = table.scan(**scan_kwargs)
            item.extend(response.get('Items', []))
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

    return {
        "statusCode": 200,
        "headers": {
            # In order to configure CORS while using Lambda Proxy integration
            # it is important to add the following header (no set by
            # APIGateway... )
            # "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(
            {"event": event,
             "context": context,
             "sourceIp": sourceIp,
             "item": item
             },
            default=default)
    }
