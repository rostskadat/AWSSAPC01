from __future__ import print_function
from crhelper import CfnResource
import boto3
import time
import logging

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    organizations = boto3.client('organizations')
except Exception as e:
    helper.init_failure(e)

def _get_source_parent_id(account_id):
    """Return the root / ou of the given Account Id
    """
    for root_page in organizations.get_paginator('list_roots').paginate():
        for root in root_page['Roots']:
            source_parent_id = root['Id']
            for account_page in organizations.get_paginator('list_accounts_for_parent').paginate(ParentId=source_parent_id):
                for account in account_page['Accounts']:
                    if account_id == account['Id']:
                        return source_parent_id
    raise ValueError("Invalid account_id %s", account_id)

def _wait_for_account_to_stabilize(create_account_request_id):
    create_account_status = organizations.describe_create_account_status(CreateAccountRequestId=create_account_request_id)['CreateAccountStatus']
    while (create_account_status['State'] == 'IN_PROGRESS'):
        time.sleep(1)
        create_account_status = organizations.describe_create_account_status(CreateAccountRequestId=create_account_request_id)['CreateAccountStatus']
    if (create_account_status['State'] == 'FAILED'):
        logger.error("Account Creation Failed. Reason : %s", create_account_status['FailureReason'])
        raise ValueError(create_account_status['FailureReason'])
    return create_account_status['AccountId']

@helper.create
def create_account(event, context):
    """Create a account.

    This function will create an Account. It take take the same parameters as the 
    https://docs.aws.amazon.com/organizations/latest/APIReference/API_CreateAccount.html API
    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    destination_parent_id = parameters.pop('DestinationParentId', None)

    logger.debug("Creating account '%s' ...", parameters["AccountName"])
    response = organizations.create_account(**parameters)
    create_account_request_id = response['CreateAccountStatus']['Id']
    account_id = _wait_for_account_to_stabilize(create_account_request_id)

    if destination_parent_id:
        logger.debug("Moving account '%s' to OU %s ...", account_id, destination_parent_id)
        source_parent_id = _get_source_parent_id(account_id)
        organizations.move_account(
            AccountId=account_id,
            DestinationParentId=destination_parent_id,
            SourceParentId=source_parent_id)
    logger.info("Account '%s' succesfully created", parameters["AccountName"])            
    response = organizations.describe_account(AccountId=account_id)
    helper.Data.update({
        "Arn": response['Account']['Arn'],
        "Email": response['Account']['Email'],
        "Name": response['Account']['Name'],
        "LoginURL" : "https://"+account_id+".signin.aws.amazon.com/console"
        })
    #    "TrustedMasterAccountRoleArn": role.get_arn()
    return account_id

@helper.update
def update_account(event, context):
    """Update the account. NOT IMPLEMENTED.
    """
    physical_id = event['PhysicalResourceId']
    logger.warning("Updating an account is not supported: %s", physical_id)
    return physical_id

@helper.delete
def delete_account(event, context):
    """Delete the account. NOT IMPLEMENTED.
    """
    physical_id = event['PhysicalResourceId']
    logger.warning("Deleting an account is not supported: %s", physical_id)

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
