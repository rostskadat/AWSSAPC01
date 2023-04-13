# LambdaRequestAuthorizer

This scenario demonstrates a API access control based on [Lambda Request authorizers](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-controlling-access-to-apis.html#serverless-controlling-access-to-apis-lambda-request-authorizer)

The strategy consists in taking the value of the HTTP 'auth' request parameter and then checking that token

## Start

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01"
``` 

## Calling the API

If you call it without `auth` parameter or with the `auth` parameter set to an invalid value (try `deny` or none), you will get:

```
?> curl -k $ApiGatewayApi
{"message":"Unauthorized"}
```

and if you call it by setting the `auth` parameter to `allow` you will get:
```
?> curl -k "$ApiGatewayApi?auth=allow"
{"message": "Hello World!", "location": "3.249.47.241"}
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name LambdaRequestAuthorizer
```
