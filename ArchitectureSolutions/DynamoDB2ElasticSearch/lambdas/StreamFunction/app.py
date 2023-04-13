from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import json
import logging
import os

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
ES_ENDPOINT = os.getenv('ES_ENDPOINT')
ES_INDEX = os.getenv('ES_INDEX')
ES_DOC_TYPE = os.getenv('ES_DOC_TYPE')
REGION = os.getenv('AWS_REGION')

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, REGION, 'es', session_token=credentials.token)
es = Elasticsearch(
    hosts = [{'host': ES_ENDPOINT, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# As per https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-request-signing.html#es-request-signing-python
def lambda_handler(event, context):
    logger.info(event)
    for record in event["Records"]:
        if record["eventName"] == "REMOVE":
            continue
        id = record["dynamodb"]["Keys"]["id"]["S"]
        new_image = record["dynamodb"]["NewImage"]
        logger.info("Adding record %s to ElasticSearch...", id)
        for k, v in new_image.items():
            new_image[k] = list(v.values())[0]
        try:
            es.index(index=ES_INDEX, doc_type=ES_DOC_TYPE, id=id, body=new_image)
        except Exception as e:
            logger.error(str(e))
    return True