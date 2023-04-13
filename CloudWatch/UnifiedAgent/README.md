# CloudWatch / UnifiedAgent

Showcases the use of the CloudWatch Unified Agent. Look at [cloudwatch-push-metrics-unified-agent](https://aws.amazon.com/premiumsupport/knowledge-center/cloudwatch-push-metrics-unified-agent/) for more details.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can then open the CloudWatch Metrics Explorer and select the metrics for `InstanceId`

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-UnifiedAgent
```

## Details

*Author*: rostskadat
