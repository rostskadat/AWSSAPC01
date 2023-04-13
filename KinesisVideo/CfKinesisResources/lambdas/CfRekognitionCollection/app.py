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
def create_collection(event, context):
    """Create a Rekognition collection

    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)

    if 'CollectionId' not in parameters:
        parameters["CollectionId"] = get_random_name(event)

    logger.debug("Creating Collection '%s' ...", parameters["CollectionId"])
    response = rekognition.create_collection(**parameters)
    physical_id = parameters["CollectionId"]
    helper.Data.update({ "Arn": response['CollectionArn'] })
    helper.Data.update({ "FaceModelVersion": response['FaceModelVersion'] })
    return physical_id

@helper.update
def update_collection(event, context):
    """Update the collection.
    """
    physical_id = event['PhysicalResourceId']
    logger.warning("Updating an collection is not supported: %s", physical_id)
    return physical_id

@helper.delete
def delete_collection(event, context):
    """Delete the collection.
    """
    try:
        physical_id = event['PhysicalResourceId']
        rekognition.delete_collection(CollectionId=physical_id)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type CfRekognitionCollection

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
