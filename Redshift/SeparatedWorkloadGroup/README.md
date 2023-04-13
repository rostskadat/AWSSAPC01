# Redshift / SeparatedWorkloadGroup

Showcase the use of WorkloadGroup to avoid impacting 2 tasks...

This relies heavily on [getting-started](https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html)

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Once created you will need to create the different table and upload the sample data to the s3 bucket

```shell
curl https://docs.aws.amazon.com/redshift/latest/gsg/samples/tickitdb.zip -o tickitdb.zip
unzip tickitdb.zip
...
aws s3 sync . s3://<Bucket>
```

Then use the aws cli to execute the SQL statements to bootstrap the cluster

```shell
cat resources/bootstrap.sql | sed -e 's#<Bucket>#<Bucket>#;s#<ClusterRole>#<ClusterRole>#' > bootstrap.sql
aws redshift-data execute-statement --cluster-identifier <Cluster> --database dev --db-user root --secret-arn <Secret> --statement-name BOOTSTRAP --sql file://./bootstrap.sql | jq '.Id'
aws redshift-data describe-statement --id <Id> | jq '.Status'
FINISHED
```

Once the database has been bootstrapped it is possible to assign a query to a specific queue by using:

```sql
SET query_group TO 'QueueLabel';
```

Look at the [resources/queries.sql] for an example.

```shell
aws redshift-data execute-statement --cluster-identifier <Cluster> --database dev --db-user root --secret-arn <Secret> --statement-name BOOTSTRAP --sql file://./resources/queries.sql | jq '.Id'
aws redshift-data describe-statement --id <Id> | jq '.Status'
FINISHED
```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-SeparatedWorkloadGroup
```

## Details

*Author*: rostskadat
