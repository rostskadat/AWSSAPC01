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
def create_public_key(event, context):
    """Uploads a public key to CloudFront that you can use with signed URLs and signed cookies , or with field-level encryption.
    """
    parameters = event['ResourceProperties']['PublicKeyConfig']

    # If Name is not specified, we create a random one.
    name = parameters.get('Name', None)
    if not name:
        name = get_random_name(event)

    response = cloudfront.create_public_key(PublicKeyConfig={
        'CallerReference': event['ServiceToken'],
        'Name': name,
        'EncodedKey': parameters['EncodedKey'],
        'Comment': parameters.get('Comment', '')
    })
    physical_id = response["PublicKey"]["Id"]
    helper.Data.update({"Location": response['Location']})
    return physical_id


@helper.update
def update_public_key(event, context):
    """Update the Policy.
    """
    physical_id = event['PhysicalResourceId']
    old_parameters = event['OldResourceProperties']['PublicKeyConfig']
    new_parameters = event['ResourceProperties']['PublicKeyConfig']

    old_name = old_parameters.get('Name', None)
    new_name = new_parameters.get('Name', None)

    if old_name != new_name or old_parameters['EncodedKey'] != new_parameters['EncodedKey']:
        # How to inform that a new resource is required?
        delete_public_key(event, context)
        return create_public_key(event, context)

    # we can only update the comment. Any other field will generate the
    # creation of a new key
    response = cloudfront.get_public_key_config(Id=physical_id)
    etag = response['ETag']
    public_key_config = response['PublicKeyConfig']
    response = cloudfront.update_public_key(Id=physical_id, PublicKeyConfig={
        'CallerReference': public_key_config['CallerReference'],
        'Name': public_key_config['Name'],
        'EncodedKey': public_key_config['EncodedKey'],
        'Comment': new_parameters.get('Comment', '')},
        IfMatch=etag)
    physical_id = response["PublicKey"]["Id"]
    return physical_id


@helper.delete
def delete_public_key(event, context):
    """Remove a public key you previously added to CloudFront.
    """
    try:
        physical_id = event['PhysicalResourceId']
        etag = cloudfront.get_public_key_config(Id=physical_id)['ETag']
        cloudfront.delete_public_key(Id=physical_id, IfMatch=etag)
    except Exception as e:
        logger.error(str(e))


def lambda_handler(event, context):
    """Lambda function to create CustomResource of type Account Policy (SCP, etc)
    """
    helper(event, context)
