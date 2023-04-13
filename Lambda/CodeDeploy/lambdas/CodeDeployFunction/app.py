import json
import logging
from os import environ

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    stage = event["requestContext"]["stage"]
    environment = {}
    for k,v in environ.items():
        if k.startswith("AWS_") or k.startswith("LAMBDA_"):
            environment[k] = v
    # This is the latest version
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json" 
        },
        "body": json.dumps({
            "stage": stage,
            "environment": environment
        }),
    }
