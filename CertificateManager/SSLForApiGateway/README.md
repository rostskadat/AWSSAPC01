# SSLForApiGateway

This scenario showcases the use of an SSL certifiate for a backend API Gateway.

## Building

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

All call should be reachable and give you the same message

```shell
curl -s <ApiGatewayUrl> | jq
{
  "message": "Hello World!",
  "location": "54.246.52.205"
}
curl -s <UserFriendlyName> | jq
{
  "message": "Hello World!",
  "location": "54.246.52.205"
}
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-SSLForApiGateway
```
