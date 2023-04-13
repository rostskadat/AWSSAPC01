import os
import json
import logging
import boto3

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
BUCKET_NAME = os.environ.get("BUCKET_NAME")
s3 = boto3.client('s3')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    keys = []
    for root_page in s3.get_paginator('list_objects_v2').paginate(Bucket=BUCKET_NAME):
        keys.extend(list(map(lambda c: c['Key'], root_page['Contents'])))
    return {
        "statusCode": 200,
        "headers": {
            # In order to configure CORS while using Lambda Proxy integration
            # it is important to add the following header (no set by
            # APIGateway... )
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(
            {"keys": keys}
        ),
    }
