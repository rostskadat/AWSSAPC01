from datetime import datetime
import base64
import boto3
import json
import logging
import os
import requests

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
athena = boto3.client('athena')

BUCKET_NAME = os.getenv('BUCKET_NAME')
DATABASE = os.getenv('DATABASE')
QUEUE_NAME = os.getenv('QUEUE_NAME')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

OUTLIERS_SQL = """
SELECT *
FROM "reducekinesiscostdb"."device_logs"
WHERE devicevalue < 10;
"""

def lambda_handler(event, context):
    response = athena.start_query_execution(
        QueryString=OUTLIERS_SQL,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': 's3://%s/athena_result/' % BUCKET_NAME
        }
    )

