# AccessDeniedAlert

This scenario show case a CloudTrail Trail that stream to CloudWatch and trigger an email when an access denied is encountered...

## Building

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

Unfortunately the CloudFormation `AWS::CloudTrail::Trail` does not expose the `IsOrganizationTrail` parameter yet. You have to set it by hand.

```bash
aws organizations enable-aws-service-access --service-principal cloudtrail.amazonaws.com
aws cloudtrail update-trail --name <Trail> --is-organization-trail
``` 

## Testing

Just try to list the S3 `Bucket` from the monitored Account. You should receive an email.

```
aws cloudtrail start-logging --name <Trail>
aws --profile <LinkedAccountUser> s3 ls s3://<Bucket>/

An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
aws cloudtrail stop-logging --name <Trail>
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-AccessDeniedAlert
```
