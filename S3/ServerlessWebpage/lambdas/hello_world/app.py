import json


def lambda_handler(event, context):
    """Return a simple "Hello World" message

    Args:
        event ([type]): The API event that triggered the call
        context ([type]): The context of the lambda execution

    Returns:
        an API Gateway compatible json
    """
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "message": "hello world",
        })
    }
