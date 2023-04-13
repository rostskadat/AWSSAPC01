import json
import logging
import requests

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    for record in event.get("Records", []): 
        message_id = record["messageId"]
        body = json.loads(record["body"])
        logger.info(f"Processing SQS Message {message_id} ...")
        if body.get("message", None) == "error":
            raise ValueError ("Simulating Error")
        #sqs.delete_message(QueueUrl=record[eventSourceARN], ReceiptHandle=record['receiptHandle'])
