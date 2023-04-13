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
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    try:
        location = requests.get("http://checkip.amazonaws.com/").text.replace("\n", "")
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        logging.error(e)
        raise e

    return {
        "statusCode": 200,
        "headers": {
            # In order to configure CORS while using Lambda Proxy integration 
            # it is important to add the following header (no set by
            # APIGateway... )
            # "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json" 
        },
        "body": json.dumps({
            "message": "Hello World!",
            "location": location
        }),
    }
