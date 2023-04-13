from __future__ import print_function
from crhelper import CfnResource
from CfKinesisResources import get_random_name
import boto3
import time
import logging

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    kinesisvideo = boto3.client('kinesisvideo')
except Exception as e:
    helper.init_failure(e)

@helper.create
def create_stream(event, context):
    """Create a KinesisVideo Stream.

    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)

    if 'StreamName' not in parameters:
        parameters["StreamName"] = get_random_name(event)
    if 'DataRetentionInHours' in parameters:
        parameters["DataRetentionInHours"] = int(parameters["DataRetentionInHours"])

    logger.debug("Creating Kinesis Video Stream '%s' ...", parameters["StreamName"])
    response = kinesisvideo.create_stream(**parameters)
    physical_id = response['StreamARN']
    return physical_id

@helper.update
def update_stream(event, context):
    """Update the stream.
    """
    physical_id = event['PhysicalResourceId']
    new_parameters = event['ResourceProperties']
    new_parameters.pop('ServiceToken', None)
    new_parameters.pop('Type', None)
    response = kinesisvideo.update_stream(StreamARN=physical_id, **new_parameters)
    return physical_id

@helper.delete
def delete_stream(event, context):
    """Delete the stream.
    """
    try:
        physical_id = event['PhysicalResourceId']
        kinesisvideo.delete_stream(StreamARN=physical_id)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type CfKinesisVideoStream

    Parameters
    ----------
    event: dict, required
        Custom Resource request: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requests.html

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    CustomResourceResponse: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html
    """
    helper(event, context)
