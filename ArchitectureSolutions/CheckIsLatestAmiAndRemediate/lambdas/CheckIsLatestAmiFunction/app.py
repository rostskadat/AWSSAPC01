from confighelper import ConfigRuleHelper
import boto3
import datetime
import dateutil
import decimal
import json
import logging
import os

LATEST_AMI = "/aws/service/ami-amazon-linux-latest"

ssm = boto3.client('ssm')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

helper = ConfigRuleHelper()

VALID_IMAGE_IDS = []
try:
    paginator = ssm.get_paginator('get_parameters_by_path')
    for page in paginator.paginate(Path=LATEST_AMI, Recursive=True):
        VALID_IMAGE_IDS.extend(
            list(map(lambda c: c['Value'], page['Parameters'])))
except Exception as e:
    helper.init_failure(e)


@helper.config_rule
def check_is_latest_ami(rule_parameters, configuration_item):
    if (configuration_item["resourceType"] != 'AWS::EC2::Instance'):
        return "NOT_APPLICABLE"
    elif configuration_item["configuration"]["imageId"] in VALID_IMAGE_IDS:
        return "COMPLIANT"
    return "NON_COMPLIANT"


def lambda_handler(event, context):
    helper(event, context)
