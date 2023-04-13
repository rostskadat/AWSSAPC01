import boto3
import os

BUCKET_NAME = os.getenv('BUCKET_NAME')

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    keys = []
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=BUCKET_NAME):
        if page['KeyCount'] > 0:
            keys.extend(list(map(lambda c: c['Key'], page['Contents'])))
    return {
        "index": -1,
        "keys": keys,
        "count": len(keys),
        "continue": len(keys) > 0
    }
