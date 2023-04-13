def is_cluster_stable(rds, db_cluster_id: str):
    instance_filter = {'Name':'db-cluster-id', 'Values': [db_cluster_id]}
    for page in rds.get_paginator('describe_db_instances').paginate(Filters=[instance_filter]):
        for db_instance in page["DBInstances"]:
            if db_instance["DBInstanceStatus"] != "available":
                return False
    return True

