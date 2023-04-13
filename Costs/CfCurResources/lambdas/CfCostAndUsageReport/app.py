from __future__ import print_function
from crhelper import CfnResource
from CfCurResources import get_random_name
import boto3
import time
import logging

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Look at documentation in https://github.com/aws-cloudformation/custom-resource-helper
helper = CfnResource()

try:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur.html
    cur = boto3.client('cur')
except Exception as e:
    helper.init_failure(e)

def _get_report_definition(report_name):
    """Return the report definition corresponding to the given ReportName
    """
    for page in cur.get_paginator('describe_report_definitions').paginate():
        for report_definition in page['ReportDefinitions']:
            if report_name == report_definition['ReportName']:
                return report_definition
    raise ValueError("Invalid report_name %s", report_name)


@helper.create
def create_report(event, context):
    """Create a Cost and Usage Report

    """
    parameters = event['ResourceProperties']
    parameters.pop('ServiceToken', None)

    report_definition = parameters["ReportDefinition"]
    report_name = report_definition.get("ReportName", None)
    if not report_name:
        report_name = get_random_name(event)
        report_definition["ReportName"] = report_name
    if 'RefreshClosedReports' in report_definition:
        report_definition["RefreshClosedReports"] = report_definition["RefreshClosedReports"] == 'true'

    logger.debug("Creating Cost and Usage Report '%s' ...", report_name)
    cur.put_report_definition(ReportDefinition=report_definition)
    physical_id = report_name
    return physical_id

@helper.update
def update_report(event, context):
    """Update the report.
    """
    physical_id = event['PhysicalResourceId']
    new_parameters = event['ResourceProperties']
    new_parameters.pop('ServiceToken', None)
    report_definition = new_parameters['ReportDefinition']
    cur.modify_report_definition(ReportName=physical_id, ReportDefinition=report_definition)
    return physical_id

@helper.delete
def delete_report(event, context):
    """Delete the report.
    """
    try:
        physical_id = event['PhysicalResourceId']
        cur.delete_report_definition(ReportName=physical_id)
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
