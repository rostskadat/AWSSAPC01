from __future__ import print_function
from crhelper import CfnResource
from CfCloudWatchResources import get_random_name
import boto3
import time
import json
import logging

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    logs = boto3.client('logs')
except Exception as e:
    helper.init_failure(e)
    
def _get_policy_name(parameters, create: bool = False, event: dict = None):
    policy_name = parameters.pop('PolicyName', parameters.pop('policyName', None))
    if not policy_name:
        if create:
            policy_name = get_random_name(event)
    return policy_name

def _get_policy_document(parameters):
    policy_document = parameters["PolicyDocument"]
    if isinstance(policy_document, dict):
        policy_document = json.dumps(policy_document)
    elif isinstance(policy_document, str):
        pass
    else:
        raise ValueError("PolicyDocument must be a Dictionary or a String")
    return policy_document

@helper.create
def create_resource_policy(event, context):
    """Create a CloudWatch Logs ResourcePolicy

    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    policy_name = _get_policy_name(parameters, True, event)
    logger.debug("Creating CloudWatch Logs ResourcePolicy '%s' ...", policy_name)
    policy_document = _get_policy_document(parameters)
    response = logs.put_resource_policy(policyName=policy_name, policyDocument=policy_document)
    physical_id = response["resourcePolicy"]["policyName"]
    return physical_id

@helper.update
def update_resource_policy(event, context):
    """Update the CloudWatch Logs ResourcePolicy
    """
    physical_id = event['PhysicalResourceId']
    parameters.pop('ServiceToken', None)
    policy_name = _get_policy_name(parameters)
    if policy_name != physical_id:
        logger.info("Creating new ResourcePolicy '%s' ...", policy_name)
    response = logs.put_resource_policy(policyName=policy_name, policyDocument=parameters["PolicyDocument"])
    physical_id = response["resourcePolicy"]["policyName"]
    return physical_id

@helper.delete
def delete_resource_policy(event, context):
    """Delete the CloudWatch Logs ResourcePolicy
    """
    try:
        physical_id = event['PhysicalResourceId']
        logger.debug("Deleting CloudWatch Logs ResourcePolicy '%s' ...", physical_id)
        logs.delete_resource_policy(policyName=physical_id)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    logger.info(event)
    helper(event, context)
