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
    params = event.get("queryStringParameters", None)

    if params and params.get("key", None) == "error":
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json" 
            },
            "body": json.dumps({
                "message": "You set the 'key' query parameter to 'error'. Returning error ...",
                "location": "SynchronousFunction"
            }),
        }
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json" 
        },
        "body": json.dumps({
            "message": "To simulate an error set the 'key' query parameter to 'error'.",
            "location": "SynchronousFunction"
        }),
    }
