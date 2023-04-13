# BucketPolicies

This scenario showcase different BucketPolicies with conditions:

* Use S3 bucket for policy to:
  * Grant public access to the bucket
  * Force objects to be encrypted at upload
  * Grant access to another account (Cross Account)
* Optional Conditions on:
  * Public IP or Elastic IP (not on Private IP)
  * Source VPC or Source VPC Endpoint – only works with VPC Endpoints
  * CloudFront Origin Identity


More details available [here](https://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html)

More information about Policy condition can be found [here](https://docs.aws.amazon.com/AmazonS3/latest/dev/amazon-s3-policy-keys.html)

## Building

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

The S3 Object in the `PublicBucket` should be accessible through a simple `curl`:

```shell
# Testing public read
curl <PublicS3ObjectUrl>
Hello World!

```

The upload of an un-encrypted object to the `ForceEncryptionBucket` will fail (explicitly denied):

```shell
aws s3 cp <ForceEncryptionS3Object> /tmp/s3object
aws s3 cp /tmp/s3object <ForceEncryptionS3Object>

upload failed: .\s3object to s3://sapc01-bucketpolicies-forceencryptionbucket-15dg94o0dv5xp/s3object An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
```

Finally you can try to access the `GrantAccessBucket` from the external account
```shell
aws --profile AF090536-CfAccount s3 cp <GrantAccessS3Object> /tmp/s3object
aws --profile AF090536-CfAccount s3 cp /tmp/s3object <GrantAccessS3Object>
```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-BucketPolicies
```
