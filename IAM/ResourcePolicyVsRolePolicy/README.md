# ResourcePolicyVsRolePolicy

This sample show case several things:

* Difference between IAM Role and S3 Bucket Policy when accessing a Bucket.
* Simple Condition and Policy Variable use

## Building

You'll need to build resourecs in both the master account and the linked account

```shell
./build_and_deploy.sh master
./build_and_deploy.sh linked
``` 

## Testing

Let's check that we do not have improper access.

* Access `BucketWithBucketPolicy`. Using user without access:

```shell
aws --profile <NoAccessUser> s3 ls s3://<BucketWithBucketPolicy>/

An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
```

* Access `BucketWithRole`. Using user without access:

```shell
aws --profile <NoAccessUser> s3 ls s3://<BucketWithRole>/

An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
``` 

* Access `BucketWithBucketPolicy`. Using your own credentials

```shell
aws --profile <Username> s3 ls s3://<BucketWithBucketPolicy>/
```

* Access `BucketWithRole`. Note how the access is *denied*
```shell
aws --profile <Username> s3 ls s3://<BucketWithRole>/

An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
``` 

* Obtain STS credentials...

```shell
aws --profile <Username> sts assume-role --role-arn <BucketRoleArn> --role-session-name AWSCLI-SessionOperator
{
    "Credentials": {
        "AccessKeyId": "ASIAY4D..."
        ...
    }
}
export AWS_ACCESS_KEY_ID=ASIAY4D...
export AWS_SECRET_ACCESS_KEY=WJgR...
export AWS_SESSION_TOKEN=FwoGZ...

``` 

* Access `BucketRoleArn`.  Using sts credentials.

```shell
aws s3 ls s3://<BucketWithRole>/
```

* *Note* that anyother action is `denied` with this role
```shell
aws s3 ls s3://<BucketWithBucketPolicy>/

An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
``` 

## Testing Conditions:


* Access `BucketWithBucketConditionPolicy`. A request from the forbidden IP will fail

```shell
aws --profile <Username> s3 ls s3://<BucketWithBucketConditionPolicy>/

An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws --profile n090536 cloudformation delete-stack --stack-name ResourcePolicyVsRolePolicy
aws --profile AF090536-CfAccount cloudformation delete-stack --stack-name ResourcePolicyVsRolePolicy
```
