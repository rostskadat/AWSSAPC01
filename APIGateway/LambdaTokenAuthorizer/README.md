# LambdaTokenAuthorizer

This scenario demonstrates a API access control based on [Lambda Token authorizers](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-controlling-access-to-apis.html#serverless-controlling-access-to-apis-lambda-token-authorizer)

The strategy consists in taking the value of the HTTP 'Authorization' header from the request and then checking that token against the 

## Start

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01"
``` 

## Calling the API

If you call it without `Authorization` header or with the `Authorization` header set to an invalid value (try `deny` or none), you will get:

```
?> curl -k $ApiGatewayApi
{"message":"Unauthorized"}
```

and if you call it by setting the `Authorization` header to `allow` you will get:
```
?> curl -k -H 'Authorization: allow' $ApiGatewayApi
{"message": "Hello World!", "location": "18.202.226.154"}
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name LambdaTokenAuthorizer
```
