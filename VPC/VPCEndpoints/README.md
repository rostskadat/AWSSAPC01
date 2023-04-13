# VPC / VPCEndpoints

Showcase the different VPC endpoints. More specifically it will showcase:
* S3 VPC Gateway Endpoint
* SQS VPC Interface Endpoint

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Access to the `Bucket` from `Instance` should succeed:

```shell
ssh ec2-user@<Instance>
?> touch /tmp/test ; aws s3 cp /tmp/test s3://sapc01-vpcendpoints-bucket-ob286qsafqv7/
upload: ../../tmp/test to s3://sapc01-vpcendpoints-bucket-ob286qsafqv7/test
?> aws s3 ls s3://sapc01-vpcendpoints-bucket-ob286qsafqv7/
2020-12-16 18:23:36          0 test
```

Access to the `Bucket` from `MyIP` should fail:

```shell
aws s3 cp /tmp/test s3://sapc01-vpcendpoints-bucket-ob286qsafqv7
upload failed: ../../tmp/test to s3://sapc01-vpcendpoints-bucket-ob286qsafqv7/test An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
```

Access to the `Queue` from `Instance` should succeed:

```shell
ssh ec2-user@<Instance>
?> aws --region eu-west-1 sqs send-message --queue-url <SQSEndpointUrl> --message-body Hello
{
    "MD5OfMessageBody": "8b1a9953c4611296a827abf8c47804d7", 
    "MessageId": "ca6535ed-a932-4b9e-a579-ae2e2a19aa3d"
}
aws --region eu-west-1 sqs receive-message --queue-url <SQSEndpointUrl>
{
    "Messages": [
        {
            "Body": "Hello", 
            "ReceiptHandle": "AQEBwBNZ8acUhIkV3POZmz+nfh76ts8SyzRBof829lvwk9XX/rbHmGEnND/gHCDcA02Hg3alHYL7LQxHDd759Krviei6MPtGnDp8r1X3M4L4GwWaT/2Z/ARHAwTQfjQBqv9AmFuJ45YTF8QG5RQpve6duh14VqwdKhMND9Hz1Gxkdp5jT7y28zaRcMsl7Rhral21V6ZhSJsTlDHY29jPUBQJZNvBdhLfnFAFTBBXFcG9/B0r1Iw6UD8kcEvBMhvSCRvK/ae5A0kG8rdHLwduFi0KZKddPbtHS4d9lmN/lS1aTMd6oRRKom5OWm6yZVS5dp2vl33BrMwkkT8TM6LjB8w4H18bL0EopDaTWDMEPQ31Pk2Ty+mI32vIUS7TTy2rQQ/jQgi5kh4wtnYu2+L+toFdCWFpXQQbfTljfRx2Lw5mK+Q=", 
            "MD5OfBody": "8b1a9953c4611296a827abf8c47804d7", 
            "MessageId": "ca6535ed-a932-4b9e-a579-ae2e2a19aa3d"
        }
    ]
}
```

Access to the `Queue` from `MyIP` should fail:

```shell
aws --region eu-west-1 sqs send-message --queue-url <Queue> --message-body "HELLO FROM MyIP"

An error occurred (AccessDenied) when calling the SendMessage operation: Access to the resource https://eu-west-1.queue.amazonaws.com/ is denied.
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-VPCEndpoints
```

## Details

*Author*: rostskadat
