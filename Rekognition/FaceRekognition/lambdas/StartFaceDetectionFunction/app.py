import boto3
import logging
import os

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
TOPIC_ARN = os.getenv("TOPIC_ARN")
ROLE_ARN = os.getenv("ROLE_ARN")

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    client = boto3.client('rekognition')
except Exception as e:
    logging.error(e, exc_info=True)
    raise e

def lambda_handler(event, context):
    logger.info(event)
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        video = {'S3Object': {'Bucket': bucket, 'Name': key}}
        response = client.start_face_detection(
            Video=video,
            NotificationChannel={ 'SNSTopicArn': TOPIC_ARN, 'RoleArn': ROLE_ARN }
        )
        logger.info("Rekognition started job %s ...", response["JobId"])
