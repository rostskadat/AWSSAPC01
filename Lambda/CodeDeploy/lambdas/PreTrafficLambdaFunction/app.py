from cdhelper import CodeDeployHelper, SUCCEEDED, FAILED, UNKNOWN
from os import environ
import boto3
import json
import logging

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
client = boto3.client('lambda')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

helper = CodeDeployHelper()

@helper.pre_traffic
def pre_traffic_handler(event, context):
    function_to_test = environ["NEW_VERSION"]
    do_validation_checks = environ["HOOK_ENABLED"]
    logger.info(f"Testing new function version: {function_to_test}")

    # Perform validation of the newly deployed Lambda version
    pre_traffic_testing = UNKNOWN
    try:
        response = client.invoke(FunctionName=function_to_test,InvocationType="RequestResponse")
        if response:
            result = json.loads(response["Payload"])
            logger.info("Result: " +  json.dumps(result))
            logger.info(do_validation_checks)
            logger.info(result.message)
            if do_validation_checks == "false":
                pre_traffic_testing = SUCCEEDED
                logger.info("Validation testing bypassed due to Env Var HookEnabled")
            elif result["message"] == "Hello World!":
                pre_traffic_testing = SUCCEEDED
                logger.info ("Validation testing succeeded!")
            else:
                pre_traffic_testing = FAILED
                logger.error ("Validation testing failed!")
    except Exception as e:
        logger.error(e, exc_info=True)
        pre_traffic_testing = FAILED

    pre_traffic_testing = SUCCEEDED
    logger.info(f"Final PreTraffic Testing: {pre_traffic_testing} ")
    return pre_traffic_testing

def lambda_handler(event, context):
    """Lambda function to call the PreTraffic / PostTraffic decorated functions
    """
    helper(event, context)
