import json
import logging

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json" 
        },
        "body": json.dumps({
            "location": "SignedCookies"
        }),
    }
