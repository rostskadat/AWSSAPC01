from cdhelper import CodeDeployHelper, SUCCEEDED, FAILED, UNKNOWN
import boto3
import json
import logging

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
codedeploy = boto3.client('codedeploy')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

helper = CodeDeployHelper()

@helper.post_traffic
def post_traffic_handler(event, context):
    logger.info(json.dumps(event))
    return SUCCEEDED

def lambda_handler(event, context):
    """Lambda function to call the PreTraffic / PostTraffic decorated functions
    """
    helper(event, context)
