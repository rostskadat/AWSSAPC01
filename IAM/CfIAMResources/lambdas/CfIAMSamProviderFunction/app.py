from __future__ import print_function
from CfResources import get_random_name
from crhelper import CfnResource
import boto3
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    iam = boto3.client('iam')
except Exception as e:
    helper.init_failure(e)

def _get_document(parameters):
    # Url takes precedence
    document_url = parameters.get('SAMLMetadataDocumentUrl', None)
    document = parameters.get('SAMLMetadataDocument', None)
    
    if document_url and document:
        raise ValueError("Either SAMLMetadataDocument or SAMLMetadataDocumentUrl must be defined, but not both")
    if not document_url and not document:
        raise ValueError("At least on of SAMLMetadataDocument or SAMLMetadataDocumentUrl must be defined")
    if document_url:
        try:
            document = requests.get(document_url).text
            logger.debug("Downloaded SAML Metadata Document from %s", document_url)
        except Exception as e:
            logger.error("Failed to download SAML Metadata Document from %s", document_url)
            logger.error("Make sure you deployed your Function into a VPC with Internet Access")
    return document
    

@helper.create
def create_resource(event, context):
    """Creates a SAML Provider
    """
    parameters = event['ResourceProperties']

    # If Name is not specified, we create a random one.
    name = parameters.get('Name', None)
    if not name:
        name = get_random_name(event)

    response = iam.create_saml_provider(
        Name=name,
        SAMLMetadataDocument=_get_document(parameters)
    )
    physical_id = response["SAMLProviderArn"]
    return physical_id


@helper.update
def update_resource(event, context):
    """Updates a SAML Provider
    """
    physical_id = event['PhysicalResourceId']
    old_parameters = event['OldResourceProperties']['KeyGroupConfig']
    new_parameters = event['ResourceProperties']['KeyGroupConfig']

    old_name = old_parameters.get('Name', None)
    new_name = new_parameters.get('Name', None)

    if old_name and old_name != new_name:
        delete_resource(event, context)
        return create_resource(event, context)

    response = iam.update_saml_provider(
        SAMLProviderArn=physical_id, 
        SAMLMetadataDocument=_get_document(new_parameters)
    )
    return physical_id


@helper.delete
def delete_resource(event, context):
    """Delete the SAML Provider
    """
    try:
        physical_id = event['PhysicalResourceId']
        iam.delete_saml_provider(SAMLProviderArn=physical_id)
    except Exception as e:
        logger.error(str(e))


def lambda_handler(event, context):
    """Lambda function to create CustomResource of type SAML Provider
    """
    helper(event, context)
