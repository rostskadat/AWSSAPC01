from __future__ import print_function
from botocore.credentials import (
    AssumeRoleCredentialFetcher,
    CredentialResolver,
    DeferredRefreshableCredentials
)
from botocore.exceptions import ClientError
from botocore.session import Session
from botocore.vendored import requests
from CfCloudFrontResources import get_random_name
from crhelper import CfnResource
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    cloudformation =boto3.client("cloudformation") 
    lambda_client = boto3.client("lambda")
    events_client = boto3.client("events")
except Exception as e:
    helper.init_failure(e)

class AssumeRoleProvider(object):
    METHOD = 'assume-role'

    def __init__(self, fetcher):
        self._fetcher = fetcher

    def load(self):
        return DeferredRefreshableCredentials(
            self._fetcher.fetch_credentials,
            self.METHOD
        )

def _get_cfn_parameters(event):
    params = []
    for p in event['ResourceProperties']['CfnParameters'].keys():
        params.append(
            {"ParameterKey": p, "ParameterValue": event['ResourceProperties']['CfnParameters'][p]})
    return params


def _assume_role(session: Session,
                role_arn: str,
                duration: int = 3600,
                session_name: str = None) -> Session:
    # noinspection PyTypeChecker
    fetcher = AssumeRoleCredentialFetcher(
        session.create_client,
        session.get_credentials(),
        role_arn,
        extra_args={
            'DurationSeconds': duration,
            'RoleSessionName': session_name
        }
    )
    role_session = Session()
    role_session.register_component(
        'credential_provider',
        CredentialResolver([AssumeRoleProvider(fetcher)])
    )
    return role_session


def get_client(service, event, context):
    role_arn = None
    if 'RoleArn' in event['ResourceProperties']:
        role_arn = event['ResourceProperties']['RoleArn']
    region = context.invoked_function_arn.split(":")[3]
    if "Region" in event["ResourceProperties"].keys():
        region = event["ResourceProperties"]["Region"]
    if event['RequestType'] == 'Update':
        old_role = None
        if 'RoleArn' in event['OldResourceProperties'].keys():
            old_role = event['OldResourceProperties']['RoleArn']
        if role_arn != old_role:
            raise ValueError(
                "Changing the role ARN for stack updates is not supported")
        old_region = context.invoked_function_arn.split(":")[3]
        if "Region" in event['OldResourceProperties'].keys():
            old_region = event['OldResourceProperties']['Region']
        if region != old_region:
            raise ValueError(
                "Changing the region for stack updates is not supported")
    if role_arn:
        sess = _assume_role(Session(), role_arn,
                           session_name="QuickStartCfnStack")
        client = sess.create_client(service, region_name=region)
    else:
        client = boto3.client(service, region_name=region)
    return client


@helper.create
def create_stack(event, context):
    """
    Create a cfn stack using an assumed role
    """
    cloudformation = get_client("cloudformation", event, context)
    parent_stack_id = event['ResourceProperties']['ParentStackId']
    parent_stack_name = parent_stack_id.split("/")[1]
    parent_properties = cloudformation.describe_stacks(StackName=parent_stack_name)[
        'Stacks'][0]
    response = cloudformation.create_stack(
        StackName=get_random_name(event),
        TemplateURL=event['ResourceProperties']['TemplateURL'],
        Parameters=_get_cfn_parameters(event),
        Capabilities=parent_properties.get('Capabilities', []),
        DisableRollback=parent_properties['DisableRollback'],
        NotificationARNs=parent_properties['NotificationARNs'],
        RollbackConfiguration=parent_properties['RollbackConfiguration'],
        Tags=[{
            'Key': 'ParentStackId',
            'Value': parent_stack_id
        }] + parent_properties['Tags']
    )
    return response['StackId']


@helper.update
def update_stack(event, context):
    """
    Update a cfn stack using an assumed role
    """
    physical_resource_id = event["PhysicalResourceId"]
    try:
        cloudformation = get_client("cloudformation", event, context)
        cloudformation.update_stack(
            StackName=physical_resource_id,
            TemplateURL=event['ResourceProperties']['TemplateURL'],
            Parameters=_get_cfn_parameters(event),
            Capabilities=event['ResourceProperties'].get('capabilities', []),
            Tags=[{
                'Key': 'ParentStackId',
                'Value': event['ResourceProperties']['ParentStackId']
            }]
        )
    except ClientError as e:
        if "No updates are to be performed" not in str(e):
            raise
    return physical_resource_id


@helper.delete
def delete_stack(event, context):
    """
    Delete a cfn stack using an assumed role
    """
    physical_resource_id = event["PhysicalResourceId"]
    if '[$LATEST]' in physical_resource_id:
        # No stack was created, so exiting
        return physical_resource_id, {}
    cloudformation = get_client("cloudformation", event, context)
    cloudformation.delete_stack(StackName=physical_resource_id)
    return physical_resource_id


def lambda_handler(event, context):
    """Lambda function to create CustomResource of type Account Policy (SCP, etc)
    """
    helper(event, context)
