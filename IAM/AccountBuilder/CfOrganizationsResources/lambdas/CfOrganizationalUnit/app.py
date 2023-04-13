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
def create_ou(event, context):
    """Create a account.

    This function will create an Account. It take take the same parameters as the 
    https://docs.aws.amazon.com/organizations/latest/APIReference/API_CreateAccount.html API
    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    name = parameters['Name']
    parent_id = parameters.get('ParentId', None)
    if not parent_id:
        # If no parent is specified, use the first root. 
        parent_id = organizations.list_roots().get('Roots')[0].get('Id')
    response = organizations.create_organizational_unit(ParentId=parent_id, Name=name)
    physical_id = response["OrganizationalUnit"]['Id']
    helper.Data.update({ 
        "Arn": response["OrganizationalUnit"]['Arn'],
        "Name": response["OrganizationalUnit"]['Name']
        })
    return physical_id

@helper.update
def update_ou(event, context):
    """Update the Organizational Unit.
    """
    physical_id = event['PhysicalResourceId']
    new_parameters = event['ResourceProperties']
    name = new_parameters.pop('Name', None)
    if name:
        response = organizations.update_organizational_unit(
            OrganizationalUnitId=physical_id, 
            Name=name)
    physical_id = response['OrganizationalUnit']['Id']
    helper.Data.update({ 
        "Arn": response["OrganizationalUnit"]['Arn'],
        "Name": response["OrganizationalUnit"]['Name']
        })
    return physical_id

@helper.delete
def delete_ou(event, context):
    """Delete the Organizational Unit.
    """
    try:
        physical_id = event['PhysicalResourceId']
        organizations.delete_organizational_unit(OrganizationalUnitId=physical_id)
    except Exception as e:
        logger.error(str(e))

def lambda_handler(event, context):
    """Lambda function to create CustomResource of type CfAccount

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
