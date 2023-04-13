from elasticsearch import Elasticsearch
import json
import logging
import os

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

DOMAIN_NAME = os.environ.get("DOMAIN_NAME", None)
DOMAIN_ENDPOINT = os.environ.get("DOMAIN_ENDPOINT", None)

es = Elasticsearch([{'scheme': 'https', 'host': DOMAIN_ENDPOINT, 'port': 443}])
if not es.ping():
    raise ValueError(f"Can not connect to ElasticSearch at {DOMAIN_ENDPOINT}")


def lambda_handler(event, context):
    """Record in ElasticSearch any event from S3

    Args:
        event (map): Description of the event
        context (map): the context of the call
    """
    for record in event["Records"]:
        try:
            es.index(index="s3records", doc_type='record', body=record)
        except Exception as e:
            logger.error(e)
