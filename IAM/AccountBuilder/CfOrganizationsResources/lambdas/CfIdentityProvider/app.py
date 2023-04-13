from __future__ import print_function
from crhelper import CfnResource
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    iam = boto3.client('iam')
    s3 = boto3.client('s3')
except Exception as e:
    helper.init_failure(e)

def get_federation_metadata(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read()    
    return body

def _list_saml_providers():
    existing_providers = []
    for provider in iam.list_saml_providers()['SAMLProviderList']:
        existing_providers.append(provider['Arn'])
    return existing_providers

@helper.create
def create_saml_provider(event, context):
    """Create a SAML Provider.
    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)

    name = parameters['Name']
    bucket = parameters['Bucket']
    key = parameters['Key']

    for arn in _list_saml_providers():
        if arn.split('/')[1] == name:
            logger.warn(name + ' already exists as a provider')
            return arn
        
    response = iam.create_saml_provider(SAMLMetadataDocument=get_federation_metadata(bucket, key), Name=name)
    physical_id = response["SAMLProviderArn"]
    return physical_id

@helper.update
def update_saml_provider(event, context):
    """Update the Organizational Unit.
    """
    physical_id = event['PhysicalResourceId']
    new_parameters = event['ResourceProperties']
    saml_metadata_document = new_parameters.pop('SAMLMetadataDocument', None)
    response = iam.update_saml_provider(
        SAMLProviderArn=physical_id, 
        SAMLMetadataDocument=saml_metadata_document)
    physical_id = response['SAMLProviderArn']
    return physical_id

@helper.delete
def delete_saml_provider(event, context):
    """Delete the SAML Identity Provider.
    """
    try:
        physical_id = event['PhysicalResourceId']
        iam.delete_saml_provider(SAMLProviderArn=physical_id)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type CfIdentityProvider.
    """
    helper(event, context)

