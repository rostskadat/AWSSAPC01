import boto3
import logging
import os
import time

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
TARGET_BUCKET = os.getenv('TARGET_BUCKET')
SLEEP = int(os.getenv('SLEEP'))

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    s3 = boto3.resource('s3')
except Exception as e:
    logger.error(e, exc_info=True)


def lambda_handler(event, _):
    """Copy the file from the SOURCE_BUCKET to the TARGET_BUCKET.

    Args:
        event ([type]): the EventBridge Event
        context ([type]): the call context
    """
    target_bucket = s3.Bucket(TARGET_BUCKET)
    for record in event["Records"]:
        source_bucket = record["s3"]["bucket"]["name"]
        source_key = record["s3"]["object"]["key"]
        target_object = target_bucket.Object(source_key)
        target_object.copy({
            'Bucket': source_bucket,
            'Key': source_key
        })
    # To make sure that we are not too fast
    time.sleep(SLEEP)
