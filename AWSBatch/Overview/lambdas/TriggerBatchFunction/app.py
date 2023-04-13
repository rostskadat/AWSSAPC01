import boto3
import json
import logging
import os
import random
import string
import time

def get_random_job_name(job_definition):
    prefix = job_definition.split(':')[5].split('/')[1]
    suffix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    prefix_length = len(prefix)
    suffix_length = len(suffix)
    if prefix_length + suffix_length > 127:
        prefix = prefix[:127-suffix_length]
    return prefix + '-' + suffix

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
JOB_QUEUE = os.environ.get('JOB_QUEUE')
JOB_DEFINITION = os.environ.get('JOB_DEFINITION')
JOB_NAME = os.environ.get('JOB_NAME', get_random_job_name(JOB_DEFINITION))

batch = boto3.client('batch')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def default(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def lambda_handler(event, context):
    try:
        logger.info(f"Submitting Job {JOB_NAME} to Queue {JOB_QUEUE} from Definiton {JOB_DEFINITION} ...")
        response = batch.submit_job(
            jobName=JOB_NAME,
            jobQueue=JOB_QUEUE,
            jobDefinition=JOB_DEFINITION)
        status_code = 200
        body = json.dumps(response, default=default)
    except Exception as e:
        status_code = 500
        body = str(e)
        logger.error(body)
    return {
        "statusCode": status_code,
        "headers": {
            # In order to configure CORS while using Lambda Proxy integration 
            # it is important to add the following header (no set by
            # APIGateway... )
            # "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json" 
        },
        "body": body
    }
