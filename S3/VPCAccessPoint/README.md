# VPCEndpoint

Showcase an S3 AccessPoint in a VPC. 

Reference [here](https://aws.amazon.com/about-aws/whats-new/2019/12/amazon-s3-access-points-manage-data-access-at-scale-shared-data-sets/)

Tutorial available [here](https://aws.amazon.com/blogs/storage/managing-amazon-s3-access-with-vpc-endpoints-and-s3-access-points/)

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Check that you can only access the `PublicOnlyBucket` from the Internet, more specifically only from the `AllowAccesFromPublicIp`

```shell
aws s3 cp <PublicOnlyS3Object> /tmp/s3object
```

When you try from the `InstancePublicDnsName` instance, it fails 

```shell
aws s3 cp <PublicOnlyS3Object> /tmp/s3object
fatal error: An error occurred (403) when calling the HeadObject operation: Forbidden

aws s3api get-object --key s3object --bucket <AccessPointArn> s3object

An error occurred (AccessDenied) when calling the GetObject operation: Access Denied
```

When you do that with the `PrivateOnlyS3Object` it only works from the `InstancePublicDnsName` instance

```shell
aws s3 cp <PrivateOnlyS3Object> /tmp/s3object
fatal error: An error occurred (403) when calling the HeadObject operation: Forbidden
```

While it is working from the `InstancePublicDnsName` instance (using the `AccessPointArn` command)

```shell
aws s3api get-object --key s3object --bucket <AccessPointArn> s3object
```



## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-VPCAccessPoint
```
