from AuroraAutoScaling import is_cluster_stable
import boto3
import json
import logging
import os
import random
import string

DB_INSTANCE_CLASS = os.getenv("DB_INSTANCE_CLASS")
DB_CLUSTER_IDENTIFIER = os.getenv("DB_CLUSTER_IDENTIFIER")
MONITORING_INTERVAL = os.getenv("MONITORING_INTERVAL")
MONITORING_ROLE_ARN = os.getenv("MONITORING_ROLE_ARN")

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
rds = boto3.client('rds')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _get_random_string(length):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(length))


def lambda_handler(event, context):
    # I loop through all the instances associated with the cluster 
    # to check if the cluster is in a stable state...
    if not is_cluster_stable(rds, DB_CLUSTER_IDENTIFIER): 
        logger.warn("A Scaling Event is in progress. Bailing out!")
        return
    db_instance_id = 's' + _get_random_string(14).lower()
    logger.info(f"Creating new DB instance {db_instance_id} for cluster {DB_CLUSTER_IDENTIFIER}")
    response = rds.create_db_instance(
        DBInstanceIdentifier=db_instance_id,
        DBInstanceClass=DB_INSTANCE_CLASS,
        Engine="aurora",
        DBClusterIdentifier=DB_CLUSTER_IDENTIFIER,
        MonitoringInterval=int(MONITORING_INTERVAL),
        MonitoringRoleArn=MONITORING_ROLE_ARN
        )
    logger.info(response)
