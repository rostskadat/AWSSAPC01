from __future__ import print_function
from crhelper import CfnResource
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    organizations = boto3.client('organizations')
except Exception as e:
    helper.init_failure(e)

@helper.create
def create_policy(event, context):
    """Create a Policy.
    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    response = organizations.create_policy(**parameters)
    policy_summary = response["Policy"]["PolicySummary"]
    physical_id = policy_summary["Id"]
    helper.Data.update({ "Arn": policy_summary['Arn'] })
    return physical_id

@helper.update
def update_policy(event, context):
    """Update the Policy.
    """
    physical_id = event['PhysicalResourceId']
    new_parameters = event['ResourceProperties']
    new_parameters.pop('ServiceToken', None)
    new_parameters.pop('Type', None)
    response = organizations.update_policy(PolicyId=physical_id, **new_parameters)
    policy_summary = response["Policy"]["PolicySummary"]
    physical_id = policy_summary["Id"]
    helper.Data.update({ "Arn": policy_summary['Arn'] })
    return physical_id

@helper.delete
def delete_policy(event, context):
    """Delete the Policy.
    """
    try:
        physical_id = event['PhysicalResourceId']
        organizations.delete_policy(PolicyId=physical_id)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type Account Policy (SCP, etc)
    """
    helper(event, context)
