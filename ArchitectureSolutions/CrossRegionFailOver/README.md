# ArchitectureSolutions / CrossRegionFailOver

Showcase a Cross Region Failover for EC2 resourcs and for RDS:
* RDS Cross Region read replica
* RDS Snaphost Copy
* EC2 Snaphost Copy

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

First you need to retrive the value of the `usernmae` and `password`

```shell
aws secretsmanager get-secret-value --secret-id <Secret> | jq -r '.SecretString' | jq -r '.username'
aws secretsmanager get-secret-value --secret-id <Secret> | jq -r '.SecretString' | jq -r '.password'
```

Once the stack is build, you can try the following scenarios:

* Create an RDS Cross Region read replica to showcase a MultiSite DR strategy
* Copy an RDS Snaphost to another region to showcase a Backup restaure / Pilot light / Warm Standby DR strategy
* Copy an EC2 Snaphost to another region to showcase a Backup restaure / Pilot light / Warm Standby DR strategy

### RDS CrossRegion Read Replica

*BEWARE* The CrossRegion Read Replica only works if the `DBInstance` is encrypted with your own KMS Key (i.e. not the default `aws/rds` key)

This is as simple as building the same stack making sure to properly specify the `SourceRegion` and the `SourceDBInstanceIdentifier`:

```shell
sam build 
sam deploy --region us-east-1 --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --guided
```

*NOTE* make sure to specify the `SourceRegion` and `SourceDBInstanceIdentifier` properly

* Connect to the instance in the DR Region and check that the DB has been populated with the content of the `SourceRegion`:
```shell
?> ssh <EC2Instance>
mysql --host=<DBInstanceEndpointAddress> --port=<DBInstanceEndpointPort> "--user=$username" "--password=$password" ${DBName} < /select.sql
item_id item_key        item_value
1       key1    value1
2       key2    value2
```

### RDS CrossRegion Snapshot Copy

The CrossRegion Snapshot copy consists in creating a snapshot and using the CLI to copy it to the DR Region

```shell
aws rds describe-db-snapshots --filters "Name=db-instance-id,Values=<DBInstance>" | jq -r '.DBSnapshots[0].DBSnapshotIdentifier'
rds:sdhie6ou17y04q-2021-03-17-08-35
```

* Copy the Snapshot to another region

```shell
aws rds --region us-east-1 copy-db-snapshot --source-region eu-west-1 --source-db-snapshot-identifier arn:aws:rds:eu-west-1:AccountId:snapshot:<DBSnapshotIdentifier> --target-db-snapshot-identifier <DBInstance>-from-eu-west-1 --kms-key-id <Key>
{
    "DBSnapshot": {
        "DBSnapshotIdentifier": "sdhie6ou17y04q-from-eu-west-1",
        "DBInstanceIdentifier": "sdhie6ou17y04q",
        "Engine": "mysql",
        "AllocatedStorage": 20,
        "Status": "pending",
```

* Once ready create a new DBInstance from this Snapshot:

```shell
aws rds --region us-east-1 restore-db-instance-from-db-snapshot --db-snapshot-identifier <DBInstance>-from-eu-west-1 --db-instance-identifier <DBInstance>-from-eu-west1
{
    "DBInstance": {
        "DBInstanceIdentifier": "sdhie6ou17y04q-from-eu-west-1",
        "DBInstanceClass": "db.m5.large",
        "Engine": "mysql",
        "DBInstanceStatus": "creating",
```

* You now have a standalone DBInstance in your new region...

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-CrossRegionFailOver
```

## References

* [cross-region-read-replicas-for-amazon-rds-for-mysql](https://aws.amazon.com/blogs/aws/cross-region-read-replicas-for-amazon-rds-for-mysql/)
* [cross-region-snapshot-copy-for-amazon-rds](https://aws.amazon.com/blogs/aws/cross-region-snapshot-copy-for-amazon-rds/)


## Details

*Author*: rostskadat
