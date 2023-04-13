import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Return the event. 

    This method is mainly used to keep track of logged users
    """
    logger.info("Authentication successful")
    logger.info("Trigger function = %s", event['triggerSource'])
    logger.info("User pool = %s", event['userPoolId'])
    logger.info("App client ID = %s", event['callerContext']['clientId'])
    logger.info("User ID = %s", event['userName'])
    return event
