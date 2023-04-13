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
def create_policy_attachment(event, context):
    """Create a Policy Attachment.
    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    organizations.attach_policy(**parameters)
    return True

@helper.update
def update_policy_attachment(event, context):
    """Update the Policy Attachment.
    """
    physical_id = event['PhysicalResourceId']
    old_parameters = event['OldResourceProperties']
    old_parameters.pop('ServiceToken', None)
    organizations.detach_policy(**old_parameters)
    new_parameters = event['ResourceProperties']
    new_parameters.pop('ServiceToken', None)
    organizations.attach_policy(**new_parameters)
    return physical_id

@helper.delete
def delete_policy_attachment(event, context):
    """Delete the Policy Attachment.
    """
    try:
        parameters = event['ResourceProperties']
        parameters.pop('ServiceToken', None)
        organizations.detach_policy(**parameters)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type Account Policy (SCP, etc)
    """
    helper(event, context)
