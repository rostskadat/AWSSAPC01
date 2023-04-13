from __future__ import print_function
from botocore.exceptions import ClientError
from crhelper import CfnResource
import boto3
import logging
import time

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    sts = boto3.client('sts')
except Exception as e:
    helper.init_failure(e)

def assume_role(account_id, account_role_name):
    role_arn = 'arn:aws:iam::' + account_id + ':role/' + account_role_name
    response = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="NewAccountRole",
        DurationSeconds=900)
    credentials = response.get('Credentials', None)
    if not credentials:
        raise ClientError("Invalid role '%s': can't assume role." % role_arn)
    return credentials

def get_client(service, credentials, region):
    return boto3.client('cloudformation', 
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name=region)

@helper.create
def create_association(event, context):
    """Create a AccountBaselineAssociation.

    This means applying the CloudFormation template found in S3.
    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    
    account_id = parameters['AccountId']
    template_url = parameters['TemplateUrl']
    region = parameters['Region']
    stack_name = parameters['StackName']
    account_role_name = parameters['AccountRoleName']
    parameters = parameters.get('Parameters', {})
    
    logger.info("Assuming role '%s' in account %s ...", account_role_name, account_id)
    cloudformation = get_client('cloudformation', assume_role(account_id, account_role_name), region)

    logger.info("Creating Stack '%s' in account %s from template %s ...", stack_name, account_id, template_url)
    logger.info(parameters)
    response = cloudformation.create_stack(
        StackName = stack_name,
        TemplateURL = template_url,
        Parameters = parameters,
        NotificationARNs=[],
        Capabilities=[ 'CAPABILITY_NAMED_IAM', 'CAPABILITY_NAMED_IAM' ],
        OnFailure='ROLLBACK',
        Tags=[ 
            { 'Key': 'ManagedResource', 'Value': 'True' },
        ]
    )
    return response['StackId']

@helper.update
def update_association(event, context):
    """Update the AccountBaselineAssociation.

    This means applying the CloudFormation template found in S3.
    """
    physical_id = event['PhysicalResourceId']
    
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    
    account_id = parameters['AccountId']
    template_url = parameters['TemplateUrl']
    region = parameters['Region']
    stack_name = parameters['StackName']
    account_role_name = parameters['AccountRoleName']
    parameters = parameters.get('Parameters', {})
    
    logger.info("Assuming role '%s' in account %s ...", account_role_name, account_id)
    cloudformation = get_client('cloudformation', assume_role(account_id, account_role_name), region)

    logger.info("Updating CloudFormation stack %s ...", physical_id)
    response = cloudformation.update_stack(
        StackName = stack_name,
        TemplateURL = template_url,
        Parameters = parameters,
        Capabilities=[ 'CAPABILITY_NAMED_IAM', 'CAPABILITY_NAMED_IAM' ],
        Tags=[ 
            { 'Key': 'ManagedResource', 'Value': 'True' },
        ]
    )
    return physical_id

@helper.delete
def delete_association(event, context):
    """Delete the AccountBaselineAssociation.

    This means deleting the stack associated with the given CloudFormation 
    template.
    """
    physical_id = event['PhysicalResourceId']
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)
    account_id = parameters['AccountId']
    region = parameters['Region']
    account_role_name = parameters['AccountRoleName']
    logger.info("Deleting CloudFormation stack %s in account %s ...", physical_id, account_id)
    cloudformation = get_client('cloudformation', assume_role(account_id, account_role_name), region)
    cloudformation.delete_stack(StackName=physical_id)
    stack_status = None
    while stack_status != 'DELETE_FAILED' and stack_status != 'DELETE_COMPLETE':
        time.sleep(1)
        response = cloudformation.describe_stacks(StackName=physical_id)
        stack_status = response["Stacks"][0].get("StackStatus", 'DELETE_COMPLETE')

    if stack_status != 'DELETE_COMPLETE':
        raise ClientError("Failed to delete stack %s in account %s" % (physical_id, account_id))

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
