from io import BytesIO
import boto3
import logging
import os
import PIL.ExifTags
import PIL.Image

IS_DEBUG = os.getenv('IS_DEBUG', 'False').lower() == 'true'
BUCKET_NAME = os.getenv('BUCKET_NAME')
THUMBNAIL_BUCKET_NAME = os.getenv('THUMBNAIL_BUCKET_NAME')
MAX_SIZE = list(map(int, os.getenv('MAX_SIZE', '128x128').split('x')))

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if IS_DEBUG else logging.INFO)


def __get_safe_ext(key):
    ext = os.path.splitext(key)[-1].strip('.').upper()
    if ext in ['JPG', 'JPEG']:
        return 'JPEG'
    elif ext in ['PNG']:
        return 'PNG'
    else:
        raise Exception('Extension is invalid')


def lambda_handler(event, context):
    iterator = event["iterator"]
    key = iterator["keys"][iterator["index"]]
    logger.debug(f"Processing s3://{BUCKET_NAME}/{key} ...")
    body = s3.get_object(Bucket=BUCKET_NAME, Key=key)['Body'].read()
    with PIL.Image.open(BytesIO(body)) as img:
        thumbnail = img.thumbnail(MAX_SIZE)
        buffer = BytesIO()
        img.save(buffer, __get_safe_ext(key))
        buffer.seek(0)
        sent_data = s3.put_object(
            Bucket=THUMBNAIL_BUCKET_NAME, Key=key, Body=buffer)
        if sent_data['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception(
                f"Failed to upload thumbnail {key} to bucket {THUMBNAIL_BUCKET_NAME}")
        logger.info(
            f"Successfully uploaded thumbnail to s3://{THUMBNAIL_BUCKET_NAME}/{key}")
    return True
