from __future__ import print_function
from CfCloudFrontResources import get_random_name
from crhelper import CfnResource
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    cloudfront = boto3.client('cloudfront')
except Exception as e:
    helper.init_failure(e)

@helper.create
def create_key_group(event, context):
    """Creates a key group that you can use with CloudFront signed URLs and signed cookies .
    """
    parameters = event['ResourceProperties']['KeyGroupConfig']

    # If Name is not specified, we create a random one.
    name = parameters.get('Name', None)
    if not name:
        name = get_random_name(event)

    response = cloudfront.create_key_group(KeyGroupConfig={
        'Name': name,
        'Items': parameters['Items'],
        'Comment': parameters.get('Comment', '')
    })
    physical_id = response["KeyGroup"]["Id"]
    helper.Data.update({"Location": response['Location']})
    return physical_id


@helper.update
def update_key_group(event, context):
    """Updates a key group.
    """
    physical_id = event['PhysicalResourceId']
    old_parameters = event['OldResourceProperties']['KeyGroupConfig']
    new_parameters = event['ResourceProperties']['KeyGroupConfig']

    old_name = old_parameters.get('Name', None)
    new_name = new_parameters.get('Name', None)

    if old_name != new_name:
        # How to inform that a new resource is required?
        create_key_group(event, context)
        return delete_key_group(event, context)

    response = cloudfront.get_key_group_config(Id=physical_id)
    etag = response['ETag']
    key_group_config = response['KeyGroupConfig']

    # we can only update the comment and items. Any other field will generate the
    # creation of a new key
    response = cloudfront.update_key_group(Id=physical_id, KeyGroupConfig={
        'Name': key_group_config['Name'],
        'Items': new_parameters.get('Items', []),
        'Comment': new_parameters.get('Comment', '')},
        IfMatch=etag)
    physical_id = response["KeyGroup"]["Id"]
    return physical_id


@helper.delete
def delete_key_group(event, context):
    """Updates a key group.
    """
    try:
        physical_id = event['PhysicalResourceId']
        etag = cloudfront.get_key_group_config(Id=physical_id)['ETag']
        cloudfront.delete_key_group(Id=physical_id, IfMatch=etag)
    except Exception as e:
        logger.error(str(e))


def lambda_handler(event, context):
    """Lambda function to create CustomResource of type Account Policy (SCP, etc)
    """
    helper(event, context)
