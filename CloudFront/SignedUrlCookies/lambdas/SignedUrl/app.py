from functools import partial
from SignedUrlCookies import rsa_signer
from botocore.signers import CloudFrontSigner
import datetime
import logging
import os

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
# DISTRIBUTION = os.getenv("DISTRIBUTION") # in order to avoid circular dependencies
PUBLIC_KEY_ID = os.getenv("PUBLIC_KEY_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

NOT_BEFORE = int(os.getenv("NOT_BEFORE", "0"))
NOT_AFTER = int(os.getenv("NOT_AFTER", "60"))
IP_ADDRESS = os.getenv("IP_ADDRESS", None)

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    resource_path = event["queryStringParameters"]["url"]
    date_greater_than = datetime.datetime.now() + datetime.timedelta(0, NOT_BEFORE)
    date_less_than = datetime.datetime.now() + datetime.timedelta(0, NOT_AFTER)
    cloudfront_signer = CloudFrontSigner(
        PUBLIC_KEY_ID,
        partial(rsa_signer, PRIVATE_KEY))
    signed_url = cloudfront_signer.generate_presigned_url(
        resource_path, date_less_than=date_less_than)
    logger.info(f"Redirecting to {signed_url}")
    return {
        "statusCode": 302,
        "headers": {
            "Location": signed_url
        }
    }
