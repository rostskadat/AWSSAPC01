#!/usr/bin/env python
"""
Give a high level report of the drifts detected in your account
"""
from builtins import Exception, int, isinstance, print
from argparse import ArgumentParser, RawTextHelpFormatter
#from jinja2 import Environment, BaseLoader
import boto3
import datetime
import json
import logging
import sys
import time

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def cf_get_drift_summary(args):
    """Sends an sqs message on the specified queue

    Args:
        args (namespace): the args found on the command line.
    """
    cf = boto3.client('cloudformation')

    stack_names = []
    if args.stack_name:
        stack_names.append(args.stack_name)
    else:
        # Only stacks that have stabilized
        for page in cf.get_paginator('list_stacks').paginate(StackStatusFilter=["CREATE_COMPLETE", "ROLLBACK_COMPLETE", "UPDATE_COMPLETE", "UPDATE_ROLLBACK_COMPLETE"]):
            for stack in page["StackSummaries"]:
                # Only top level stacks
                if "ParentId" not in stack:
                    stack_names.append(stack["StackName"])
        stack_names.sort()

    # Let's trigger the drift detection
    stack_drift_detection_ids = {}
    if args.stack_name and args.stack_drift_detection_id:
        logger.info(
            f"Waiting for drift {args.stack_drift_detection_id} for Stack {args.stack_name} to complete ...")
        stack_drift_detection_ids[args.stack_name] = args.stack_drift_detection_id
    else:
        for stack_name in stack_names:
            logger.info(f"Detecting drift for Stack {stack_name} ...")
            response = cf.detect_stack_drift(StackName=stack_name)
            stack_drift_detection_ids[stack_name] = response["StackDriftDetectionId"]

    # And wait for each one...
    for (stack_name, stack_drift_detection_id) in stack_drift_detection_ids.items():
        completed = False
        in_sync = True
        while not completed:
            response = cf.describe_stack_drift_detection_status(
                StackDriftDetectionId=stack_drift_detection_id)
            completed = response["DetectionStatus"] == "DETECTION_COMPLETE"
            if not completed:
                logger.info(
                    f"Waiting for drift detection to complete for Stack {stack_name}...")
                time.sleep(1)
            else:
                in_sync = response["StackDriftStatus"] == "IN_SYNC"
        if not in_sync:
            response = cf.describe_stack_resource_drifts(
                StackName=stack_name,
                StackResourceDriftStatusFilters=['MODIFIED', 'DELETED', 'NOT_CHECKED'])
            logger.info(
                f"Stack {stack_name} has drifted (Analysed w/ {stack_drift_detection_id}):")
            print(json.dumps(response, indent=2, default=default))
        else:
            logger.info(f"Stack {stack_name} is IN_SYNC")


def parse_command_line():
    parser = ArgumentParser(
        prog='cf_get_drift_summary', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--stack-name', help='Limit drift detection to this stack', required=False, default=None)
    parser.add_argument(
        '--stack-drift-detection-id', help='Wait for the given drift id to complete and present it', required=False, default=None)
    parser.add_argument(
        '--sleep', type=int, help='The number of seconds to sleep between each call to AWS', required=False, default=10)
    parser.set_defaults(func=cf_get_drift_summary)
    return parser.parse_args()


def main():
    args = parse_command_line()
    try:
        if args.debug:
            logger.setLevel(logging.DEBUG)
        if args.profile:
            boto3.setup_default_session(profile_name=args.profile)
        return args.func(args)
    except Exception as e:
        logging.error(e, exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
