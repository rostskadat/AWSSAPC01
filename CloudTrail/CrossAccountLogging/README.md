# CrossAccountLogging

This sample showcases a account CloudTrail that call a lambda function upon reception of an event for a call to emr:ListClusters.
It demonstrate an Eventbridge event between CloudTrail, and Lambda, and also a Multi Account trail.

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

Just call `emr:ListClusters` in on of the monitored Account. The `CrossAccountLoggingFunction` should be called and you should receive an email

```
aws cloudtrail start-logging --name <Trail>
aws --profile <LinkedAccountUser> emr list-clusters
aws cloudtrail stop-logging --name <Trail>
```

After 5 minutes you should receive an email, detecting the suspicious API call

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-CrossAccountLogging
```
