from __future__ import print_function
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
def create_trusted_key_group(event, context):
    """Creates a key group that you can use with CloudFront signed URLs and signed cookies .
    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    distribution_id = parameters['DistributionId']
    key_group_id = parameters['KeyGroupId']
    distribution_response = cloudfront.get_distribution_config(Id=distribution_id)
    distribution_config = distribution_response['DistributionConfig']
    etag = distribution_response['ETag']
    items = distribution_config.get('DefaultCacheBehavior', {}).get('TrustedKeyGroups', {}).get('Items', [])
    if key_group_id in items:
        raise ValueError(f"Key Group {key_group_id} is already associated with Distribution {distribution_id}")
    items.append(key_group_id)
    distribution_config['DefaultCacheBehavior']['TrustedKeyGroups'] = {
        'Enabled': len(items) > 0,
        'Quantity': len(items),
        'Items': items
    }
    cloudfront.update_distribution(
        Id=distribution_id, 
        DistributionConfig=distribution_config,
        IfMatch=etag)
    return True

@helper.update
def update_trusted_key_group(event, context):
    """Updates a key group.
    """
    physical_id = event['PhysicalResourceId']
    old_parameters = event['OldResourceProperties']
    new_parameters = event['ResourceProperties']
    if old_parameters['DistributionId'] != new_parameters['DistributionId'] or old_parameters['KeyGroupId'] != new_parameters['KeyGroupId']:
        delete_trusted_key_group(event, context)
        return create_trusted_key_group(event, context)
    return physical_id

@helper.delete
def delete_trusted_key_group(event, context):
    """Updates a key group.
    """
    try:
        parameters = event['ResourceProperties']
        distribution_id = parameters['DistributionId']
        key_group_id = parameters['KeyGroupId']
        distribution_response = cloudfront.get_distribution_config(Id=distribution_id)
        distribution_config = distribution_response['DistributionConfig']
        etag = distribution_response['ETag']
        items = distribution_config.get('DefaultCacheBehavior', {}).get('TrustedKeyGroups', {}).get('Items', [])
        if key_group_id not in items:
            logger.warning(f"Key Group {key_group_id} is not associated with Distribution {distribution_id}")
            return
        items.remove(key_group_id)
        distribution_config['DefaultCacheBehavior']['TrustedKeyGroups'] = {
            'Enabled': len(items) > 0,
            'Quantity': len(items),
            'Items': items
        }
        cloudfront.update_distribution(
            Id=distribution_id, 
            DistributionConfig=distribution_config,
            IfMatch=etag)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type Account Policy (SCP, etc)
    """
    helper(event, context)
