# ManagedLogs

Showcase the different AWS Managed logs and their exploitation in Athena:

* S3 Access Logs
* VPC Flow Logs
* CloudTrail Logs
* Route53 Access Logs

* Load Balancers (ALB, NLB)
* CloudFront Access Logs
* AWS Config

Namely it will create the different resources, configure the corresponding logs and create the associated Athena Query (when logs are in S3) ...

## Building

Some of the resources already exists and therefore are just updated with the log configuration.

You can start with the main resources in the stack:

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

### Route 53

You need to stream your `Route 53` Access Logs to CloudWatch. From there you can use the stack [CloudWatch2S3](https://raw.githubusercontent.com/CloudSnorkel/CloudWatch2S3/master/CloudWatch2S3.template) to stream your `Route 53` Access Logs to S3. From there you can use the Athena Query to create the corresponding table and associated query.

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json ManagedLogsFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ManagedLogs
```
