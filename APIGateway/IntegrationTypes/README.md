# IntegrationTypes

Showcases the 3 differents types of API Gateway integration:

* HTTP backend
* Lambda Function
* AWS Service (SNS Publish)

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Caveats

If you are experimenting with this stack and add `AWS::ApiGateway::Resource` after the creation of the APIGW, your new `Resource` will not be automatically deployed, and you will need to deploy it manually, either through the Console or through the AWSCLI.

Reference at [cloudformation-does-not-redeploy-your-apig](https://medium.com/@dalumiller/cloudformation-does-not-redeploy-your-apig-how-to-fix-that-b0a61aafe220)

## Testing

You can then call a simple `curl` on each of the integration endpoint:


```shell
curl <ApiFriendlyUrl>/lambda
{"message": "Hello World from Lambda!"}
curl <ApiFriendlyUrl>/http
{"message":"Hello World from Flask!"}
curl <ApiFriendlyUrl>/service?Message=Hello
{
  "PublishResponse": {
    "PublishResult": {
      "MessageId": "61f87429-db2d-59e1-833a-2c33e0c00960",
      "SequenceNumber": null
    },
    "ResponseMetadata": {
      "RequestId": "284c0291-7ef0-521a-b251-5a8b451de29b"
    }
  }
}
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-IntegrationTypes
```
