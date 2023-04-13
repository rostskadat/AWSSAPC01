from __future__ import print_function
from crhelper import CfnResource
from CfManagedBlockchainResources import get_random_name
import boto3
import time
import logging

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    managedblockchain = boto3.client('managedblockchain')
except Exception as e:
    helper.init_failure(e)

@helper.create
def create_proposal(event, context):
    """Create a ManagedBlockchain Proposal.

    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)

    logger.debug("Creating ManagedBlockchain Proposal '%s' ...", parameters["StreamName"])
    response = managedblockchain.create_proposal(**parameters)
    physical_id = response['ProposalId']
    return physical_id

@helper.update
def update_proposal(event, context):
    """Update the ManagedBlockchain Proposal.
    """
    physical_id = event['PhysicalResourceId']
    logger.debug("Updating ManagedBlockchain Proposal '%s' is not suported ...", physical_id)
    return physical_id

@helper.delete
def delete_proposal(event, context):
    """Delete the ManagedBlockchain Proposal.
    """
    try:
        physical_id = event['PhysicalResourceId']
        logger.debug("Updating ManagedBlockchain Proposal '%s' is not suported ...", physical_id)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type ManagedBlockchain Proposal

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
