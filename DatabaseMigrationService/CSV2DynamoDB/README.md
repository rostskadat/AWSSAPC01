# DatabaseMigrationService / CSV2DynamoDB

Showcase import of CSV into DynamoDB using DMS, when endpoint for specific DB does not exists.

*NOTE* in order to avoid problems with datatype, "migrate" all as string...

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You will need to upload the CSV file to the S3 bucket `Bucket`

```shell
unzip ../../helpers/resources/LOAD00000001.csv.zip -d /tmp
aws s3 cp /tmp/LOAD00000001.csv <S3URL>
```

Then you will be able to trigger the Migration Task

```shell
aws dms start-replication-task-assessment-run \
    --replication-task-arn <ReplicationTaskArn> \
    --service-access-role-arn <ServiceAccessRoleArn> \
    --result-location-bucket <ResultLocationBucket> \
    --result-location-folder <ResultLocationFolder> \
    -assessment-run-name Assessment-run-$(date +'%Y-%m-%d-%H-%M-%S')
aws dms start-replication-task --replication-task-arn <ReplicationTaskArn> --start-replication-task-type start-replication
```

Once done you will be able to get the items created in the DynamoDb table:

```shell
../../helpers/dynamodb_get_items.py --table-name issues
```




## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-CSV2DynamoDB
```

## Details

*Author*: rostskadat
