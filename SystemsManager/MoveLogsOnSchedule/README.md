# SystemsManager / MoveLogsOnSchedule

Showcase how to move an instance logs to an S3 bucket on schedule

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

After creating the stack and waiting for 30' you should be able to see the different logs that where uploaded:

```shell
aws s3 ls --recursive s3://<Bucket>
2021-02-08 16:08:53       3137 AWSDocumentAssociation/gunicorn.log
2021-02-08 16:08:45       3137 DocumentAssociation/gunicorn.log
2021-02-08 16:13:21       3137 MaintenanceWindowTask/gunicorn.log
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-MoveLogsOnSchedule
```

## Details

*Author*: rostskadat
