# CloudTrail / CrossAccountForensic

Showcase how to trace a DeleteBucket event from a CrossAccount Role...

## Building

*Requirements*:
* You must have 2 account, the `RootAccount` and the `ChildAccount`
* You must a IAM user in each account...

Build the root stack with a profile in the `RootAccount` (i.e. `n090536@123456789012`)

```shell
sam build --template template.yaml && \
    sam deploy --profile n090536@123456789012 --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01"
```

## Testing

* In the `RootAccount` (i.e `n090536@123456789012`) create an S3 bucket whose deletion you want to track down

```shell
export AWS_DEFAULT_REGION=eu-west-1
aws --profile n090536@123456789012 s3api create-bucket --bucket to-be-deleted-123456789012 --create-bucket-configuration LocationConstraint=eu-west-1
{
    "Location": "http://to-be-deleted-123456789012.s3.amazonaws.com/"
}
```

* In the `RootAccount` (i.e `n090536@123456789012`) modify the `RootTrail` to make it an Organization Trail
```shell
aws --profile n090536@123456789012 cloudtrail update-trail --name <RootTrail> --is-organization-trail 
```

* Start the RootTrail:

```shell
aws --profile n090536@123456789012 cloudtrail start-logging --name <RootTrail>
```

* In the `ChildAccount` (i.e `AF090536@123456789012`) assume the `RoleToAssume` (from the `RootAccount`):

```shell
aws --profile AF090536@123456789012 sts assume-role --role-arn arn:aws:iam::123456789012:role/SAPC01-CrossAccountForensic-root-RoleToAssume-7S2NTMS7VJER --role-session-name SAPC01-SessionToDeleteBucket --duration-seconds 3600 > /tmp/credentials.json
```

* Then, Assuming the role `RoleToAssume`, delete the bucket in the `RootAccount`

```shell
export AWS_ACCESS_KEY_ID=$(cat credentials.json | jq -r .Credentials.AccessKeyId)
export AWS_SECRET_ACCESS_KEY=$(cat credentials.json | jq -r .Credentials.SecretAccessKey)
export AWS_SESSION_TOKEN=$(cat credentials.json | jq -r .Credentials.SessionToken)
aws sts get-caller-identity
{
    "UserId": "AROA3QU7W3EA2ZHRQTVP7:SAPC01-SessionToDeleteBucket",
    "Account": "123456789012",
    "Arn": "arn:aws:sts::123456789012:assumed-role/SAPC01-CrossAccountForensic-root-RoleToAssume-7S2NTMS7VJER/SAPC01-SessionToDeleteBucket"
}
aws s3 rb s3://to-be-deleted-123456789012
``` 

* Stop the RootTrail:

```shell
aws --profile n090536@123456789012 cloudtrail stop-logging --name <RootTrail>
```

Finally use the `helpers/extract_trails.sh` to lookup who called the "DeleteBucket" operation

```shell
aws --profile n090536@123456789012 s3 sync <RootLogsBucket> trails/

./helpers/extract_trails.sh trails "to-be-deleted-123456789012"
```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-CrossAccountForensic
```

## Details

*Author*: rostskadat

## References:

* [how-to-audit-cross-account-roles-using-aws-cloudtrail-and-amazon-cloudwatch-events](https://aws.amazon.com/blogs/security/how-to-audit-cross-account-roles-using-aws-cloudtrail-and-amazon-cloudwatch-events/)