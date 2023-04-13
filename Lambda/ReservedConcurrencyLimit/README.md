# Lambda / ReservedConcurrencyLimit

Use reserved concurrency limit to throttle number of lambda execution.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Using `bulk_s3_put_objects.py` you can upload may object and see how the `ReservedConcurrentExecutions` is reached and trigger the alarm

```shell
helpers\s3_put_objects.py --bucket <SourceBucket> --count 1000 --size 128
INFO:root:Uploading object 1/1000 to s3://sapc01-reservedconcurrencylimit-sourcebucket-m1lqyf8gzkah/0a37945a-c7fe-4d8d-8758-c4eb97afb2c0
...
```

Then open the [CloudWatch Alarm Console](https://eu-west-1.console.aws.amazon.com/cloudwatch/home?region=eu-west-1#alarmsV2:?~(alarmStateFilter~'ALARM))

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ReservedConcurrencyLimit
```

## Details

*Author*: rostskadat
