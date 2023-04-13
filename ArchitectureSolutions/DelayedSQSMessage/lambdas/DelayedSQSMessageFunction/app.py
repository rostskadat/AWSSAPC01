import boto3
import datetime
import json
import logging
import os

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    for record in event["Records"]:
        logger.info("Processing message '%s' ...", record["messageId"])
        try:
            message_body = json.loads(record["body"])
            if "timestamp" in message_body:
                logger.info("Message was sent @ '%s'. It is now '%s'", message_body["timestamp"], datetime.datetime.now())
        except Exception as e:
            logger.error(e)
        
        