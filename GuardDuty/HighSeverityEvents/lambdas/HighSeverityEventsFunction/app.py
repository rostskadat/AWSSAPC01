import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # this function is called either through CloudWatch Event or an SNS subscription.
    # just dumping the event to see its content
    logging.info(event)
