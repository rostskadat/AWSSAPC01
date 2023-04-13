# RDS / AuroraAutoScaling

Showcase Aurora Autoscaling for Master / Replica setup. It works by bumping the `CPUUtilization` on the Cluster. Thatin turn will trigger an alarm that will scale the Aurora Cluster by adding a Read Replica. Once the `CPUUtilization` is back to normal the Read Replica is terminated.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
```

## Testing

* Retrieve the secret to connect to the Database

```shell
MASTER_PASSWORD=$(aws secretsmanager get-secret-value --query 'SecretString' --output text --secret-id "<Secret>" | jq -r '.password')
```

* Bootstrap the DB:  

```shell
mysql --user=root --password --port=3306 --host=<DBClusterEndpointAddress> < resources/bootstrap.sql
Enter password: 
...
```

* Execute the Busy loop script on the `DBClusterReadEndpointAddress` and watch the Cluster scale out.

*BEWARE* Make sure to use the Read Replica in order to spread the load. If you use the Writer endpoint the load will not come down. as more Read replicas are added to the Cluster.

```shell
while true; do
    python helpers/db_busy_loop.py --nb-threads 500 \
        --user root --password <MASTER_PASSWORD> \
        --host <DBClusterReadEndpointAddress> --database dev \
        --sql-file resources/busy_loop.sql
done
```
```shell
aws rds describe-db-clusters --query 'DBClusters[0].DBClusterMembers' --db-cluster-identifier <DBCluster>
[
    {
        "DBInstanceIdentifier": "sd12zkorv7r7l7f",
        "IsClusterWriter": false,
        "DBClusterParameterGroupStatus": "in-sync",
        "PromotionTier": 1
    },
    {
        "DBInstanceIdentifier": "sd1luw29k5ib0dk",
        "IsClusterWriter": true,
        "DBClusterParameterGroupStatus": "pending-reboot",
        "PromotionTier": 1
    }
]
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-AuroraAutoScaling
```

## Details

*Author*: rostskadat
