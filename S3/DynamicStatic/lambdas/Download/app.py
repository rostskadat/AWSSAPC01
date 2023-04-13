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
    key = event.get("queryStringParameters", {}).get("key", None)
    if not key:
        raise ValueError("Missing parameter 'key'")
    response = s3.generate_presigned_url(
        'get_object', Params={'Bucket': BUCKET_NAME, 'Key': key}, ExpiresIn=360)
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
            {"url": response}
        ),
    }
