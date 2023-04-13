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
        key = record["s3"]["object"]["key"]
        logger.info(f"Processing S3Object {key} ...")
        if key == "error":
            raise ValueError ("Simulating Error")
