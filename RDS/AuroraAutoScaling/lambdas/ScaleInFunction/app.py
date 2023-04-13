from AuroraAutoScaling import is_cluster_stable
import boto3
import json
import logging
import os
import random
import string

DB_CLUSTER_IDENTIFIER = os.getenv("DB_CLUSTER_IDENTIFIER")

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
rds = boto3.client('rds')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # I loop through all the instances associated with the cluster 
    # to check if the cluster is in a stable state...
    if not is_cluster_stable(rds, DB_CLUSTER_IDENTIFIER): 
        logger.warn("A Scaling Event is in progress. Bailing out!")
        return
    readers = []
    logger.info(f"Retrieving all the readers from cluster {DB_CLUSTER_IDENTIFIER} ...")
    for page in rds.get_paginator('describe_db_clusters').paginate(DBClusterIdentifier=DB_CLUSTER_IDENTIFIER):
        for db_cluster in page["DBClusters"]:
            for db_cluster_member in db_cluster["DBClusterMembers"]:
                if not db_cluster_member["IsClusterWriter"]:
                    readers.append(db_cluster_member["DBInstanceIdentifier"])
    
    if len(readers) > 0:
        logger.info(f"Determining the oldest reader ...")
        instance_filter = {'Name':'db-instance-id', 'Values': readers}
        oldestCreationTime = None
        oldestDBInstanceIdentifier = None
        for page in rds.get_paginator('describe_db_instances').paginate(Filters=[instance_filter]):
            for db_instance in page["DBInstances"]:
                if not oldestCreationTime or db_instance["InstanceCreateTime"] < oldestCreationTime:
                    oldestCreationTime = db_instance["InstanceCreateTime"]
                    oldestDBInstanceIdentifier = db_instance["DBInstanceIdentifier"]
        if oldestDBInstanceIdentifier:
            logger.info(f"Removing oldest reader {oldestDBInstanceIdentifier} ...")
            rds.delete_db_instance(
                DBInstanceIdentifier=oldestDBInstanceIdentifier,
                SkipFinalSnapshot=True
            )
        logger.info(f"Cluster {DB_CLUSTER_IDENTIFIER} has been successfully scaled down")
    else:
        logger.info(f"No Reader to terminate in Cluster {DB_CLUSTER_IDENTIFIER}")
