from jinja2 import Environment, FileSystemLoader, Template
from smart_open import open
import boto3
import json
import logging
import os

ALERT_TOPIC = os.getenv("ALERT_TOPIC")
FILTER_S3_OBJECT = os.getenv("FILTER_S3_OBJECT")
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

with open(FILTER_S3_OBJECT, 'rb') as ifh:
    FILTERS = json.load(ifh)['Filters']

jenv = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
sns = boto3.client('sns')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def match_filters(trail_record):
    """Returns whether the trail record matches the Filters.
    Implicit 'and'

    Args:
        trail_record (dict): a CloudTrail record

    Returns:
        bool: True if it matches, False otherwise
    """    
    for f in FILTERS:
        for key, value in f.items():
            if trail_record.get(key, None) != value:
                return False
    return True

def lambda_handler(event, context):
    """Handle a CloudTrail delivery event from the S3 bucket.

    Args:
        event (dict): The S3 Bucket put event
        context (dict): The Lambda function context
    """
    alert_events = []    
    for s3_record in event['Records']:
        bucket_name = s3_record["s3"]["bucket"]["name"]
        object_key = s3_record["s3"]["object"]["key"]
        s3_url = "s3://%s/%s" % (bucket_name, object_key)
        with open(s3_url, 'rb') as ifh:
            json_object = json.load(ifh)
        for trail_record in json_object["Records"]:
            if match_filters(trail_record):
                alert_events.append(trail_record)

    logger.info(f"Found {len(alert_events)} events matching filters in {s3_url}")
    if len(alert_events) > 0:
        parameters = {
            "Subject": f"Found {len(alert_events)} suspicious CloudTrail events.",
            "Message": jenv.get_template('alert_email.txt.jinja2').render(alert_events=alert_events)
        }
        sns.publish(TopicArn=ALERT_TOPIC, **parameters)

