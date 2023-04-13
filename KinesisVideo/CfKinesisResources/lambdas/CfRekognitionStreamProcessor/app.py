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
    rekognition = boto3.client('rekognition')
except Exception as e:
    helper.init_failure(e)

@helper.create
def create_stream_processor(event, context):
    """Create a Rekognition StreamProcessor

    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)

    if 'Name' not in parameters:
        parameters["Name"] = get_random_name(event)

    try: 
        threshold = parameters["Settings"]["FaceSearch"]["FaceMatchThreshold"]
        parameters["Settings"]["FaceSearch"]["FaceMatchThreshold"] = float(threshold)
    except KeyError:
        pass

    logger.debug("Creating StreamProcessor '%s' ...", parameters["Name"])
    response = rekognition.create_stream_processor(**parameters)
    physical_id = parameters["Name"]
    helper.Data.update({ "Arn": response['StreamProcessorArn'] })
    return physical_id

@helper.update
def update_stream_processor(event, context):
    """Update the StreamProcessor.
    """
    physical_id = event['PhysicalResourceId']
    logger.warning("Updating an StreamProcessor is not supported: %s", physical_id)
    return physical_id

@helper.delete
def delete_stream_processor(event, context):
    """Delete the StreamProcessor.
    """
    try:
        physical_id = event['PhysicalResourceId']
        rekognition.delete_stream_processor(Name=physical_id)
    except ResourceNotFoundException: 
        pass
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type CfRekognitionStreamProcessor

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
