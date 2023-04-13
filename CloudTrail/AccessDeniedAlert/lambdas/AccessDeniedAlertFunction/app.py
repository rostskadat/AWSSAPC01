from base64 import b64decode
import boto3
import json
import logging
import os
import zlib

ALERT_TOPIC = os.getenv("ALERT_TOPIC")
#THIS_DIR = os.path.dirname(os.path.abspath(__file__))
#jenv = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
sns = boto3.client('sns')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def decode(data):
    compressed_payload = b64decode(data)
    json_payload = zlib.decompress(compressed_payload, 16+zlib.MAX_WBITS)
    return json.loads(json_payload)

def lambda_handler(event, context):
    """Handle a CloudTrail delivery event. 
    
    Events are already filtered in the SubscriptionFilter

    Args:
        event (dict): The CloudWatch log event
        context (dict): The Lambda function context
    """
    data = decode(event["awslogs"]["data"])
    log_group = data["logGroup"]
    for log_event in data["logEvents"]:
        parameters = {
            "Subject": f"Found 1 suspicious CloudTrail events.",
            "Message": log_event["message"]
        }
        sns.publish(TopicArn=ALERT_TOPIC, **parameters)

