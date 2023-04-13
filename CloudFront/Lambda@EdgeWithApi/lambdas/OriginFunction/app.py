import json

def lambda_handler(event, context):
    """Just output everything from the event
    """    
    return {
        "statusCode": 200,
        "headers": {
            # In order to configure CORS while using Lambda Proxy integration 
            # it is important to add the following header (no set by
            # APIGateway... )
            # "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json" 
        },
        "body": json.dumps(event),
    }
