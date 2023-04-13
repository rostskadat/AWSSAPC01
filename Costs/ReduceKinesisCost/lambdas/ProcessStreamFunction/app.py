from datetime import datetime
import base64
import boto3
import json
import logging
import os
import requests

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
s3 = boto3.resource('s3')

BUCKET_NAME = os.getenv('BUCKET_NAME')
S3_PREFIX = os.getenv('S3_PREFIX')


def lambda_handler(event, context):
    """Processes records from Kinesis Stream and store the result in S3.
    """
    for record in event["Records"]:
        kinesis = record['kinesis']
        timestamp = datetime.utcfromtimestamp(
            kinesis['approximateArrivalTimestamp']).strftime('%Y-%m-%d %H:%M:%S')
        payload = json.loads(base64.b64decode(kinesis['data']).decode('ascii'))
        device_id = payload['DeviceId']
        device_value = payload['DeviceValue']
        s3_object = s3.Object(BUCKET_NAME, S3_PREFIX + "/" + record['eventID'])
        s3_object.put(Body='{} {} {}'.format(
            timestamp, device_id, device_value).encode('ascii'))
