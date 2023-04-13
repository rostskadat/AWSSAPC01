from io import BytesIO
import boto3
import datetime
import logging
import os
import PIL.ExifTags
import PIL.Image

IS_DEBUG = os.getenv('IS_DEBUG', 'False').lower() == 'true'
BUCKET_NAME = os.getenv('BUCKET_NAME')
TABLE_NAME = os.getenv('TABLE_NAME')

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if IS_DEBUG else logging.INFO)


def _process_exif(image: PIL.Image):
    raw_exif_data = image.getexif()
    exif_data = {}
    for k, v in PIL.ExifTags.TAGS.items():
        if k in raw_exif_data:
            value = str(raw_exif_data[k])
        else:
            continue
        exif_data[v] = value
    return exif_data


def lambda_handler(event, context):
    iterator = event["iterator"]
    key = iterator["keys"][iterator["index"]]
    logger.debug(f"Processing s3://{BUCKET_NAME}/{key} ...")
    body = s3.get_object(Bucket=BUCKET_NAME, Key=key)['Body'].read()
    with PIL.Image.open(BytesIO(body)) as img:
        exif_data = _process_exif(img)
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item={
            "id": key,
            "exif_data": exif_data,
            "timestamp": datetime.datetime.today().isoformat()
        })
        logger.info(f"Successfully processed Image s3://{BUCKET_NAME}/{key}")
    return True
