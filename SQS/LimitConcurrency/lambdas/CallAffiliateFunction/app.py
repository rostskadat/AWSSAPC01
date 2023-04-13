import boto3
import json
import logging
import os

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
sqs = boto3.client('sqs')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUEUE_URL = os.getenv('QUEUE_URL')

def lambda_handler(event, context):
    for record in event["Records"]:
        logger.info("Processing event %s from queue '%s' ...", record["messageId"], QUEUE_URL)
        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=record['receiptHandle'])
        
        