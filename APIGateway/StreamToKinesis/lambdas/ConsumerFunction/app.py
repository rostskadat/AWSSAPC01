from botocore.exceptions import ClientError
import base64
import boto3
import json
import logging
import os

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
TABLE_NAME = os.getenv('TABLE_NAME')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

try:
    dynamodb = boto3.resource('dynamodb')
except Exception as e:
    logger.error(e, exc_info=True)


def lambda_handler(event, _):
    table = dynamodb.Table(TABLE_NAME)
    for record in event["Records"]:
        smartmeter_id = record["kinesis"]["partitionKey"]
        timestamp = record["kinesis"]["approximateArrivalTimestamp"]
        data = json.loads(base64.b64decode(record["kinesis"]["data"]).decode("utf-8"))
        try:
            table.put_item(
                Item={
                    'SmartMeterId': smartmeter_id,
                    'Timestamp': timestamp,
                    'Data': data
                }
            )
        except ClientError as e:
            logger.error(e, exc_info=True)
