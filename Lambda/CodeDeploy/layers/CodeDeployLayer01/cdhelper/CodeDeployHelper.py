# -*- coding: utf-8 -*-
"""
"""

from __future__ import print_function
import logging
import boto3

logger = logging.getLogger(__name__)

SUCCEEDED = 'Succeeded'
FAILED = 'Failed'
PENDING ='Pending'
IN_PROGRESS = 'InProgress'
SKIPPED = 'Skipped'
UNKNOWN = 'Unknown'

class CodeDeployHelper(object):
    """Helper Class to implement PreTraffic and PostTraffic lambda function

    This class allows you to easily implement a CodeDeploy PreTraffic or a PostTraffic hook, in odrer to implement blue/green deployment with CodeDeploy.
    It provides 2 decorators `pre_traffic` and `post_traffic` to set on your function.

    Args:
        object ([type]): [description]
    """
    def __init__(self):
        # N/A
        self._func = None
        self._request_type = None

    def __call__(self, event, context):
        status = IN_PROGRESS
        try:
            status = self._func(event, context) if self._func else SUCCEEDED
        except Exception as e:
            logger.error(e, exc_info=True)
            status = FAILED
        try:
            codedeploy = boto3.client('codedeploy')
            codedeploy.put_lifecycle_event_hook_execution_status(
                deploymentId=event["DeploymentId"],
                lifecycleEventHookExecutionId=event["LifecycleEventHookExecutionId"],
                status=status)
        except Exception as e:
            logger.error(e, exc_info=True)

    def pre_traffic(self, func):
        self._func = func
        self._request_type = 'pre_traffic'
        return func

    def post_traffic(self, func):
        self._func = func
        self._request_type = 'post_traffic'
        return func
