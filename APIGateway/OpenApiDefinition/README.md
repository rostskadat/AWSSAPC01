# OpenApiDefinition

This demonstrate the integration between the OpenAPI standard and AWS APIGateway integration.
For more details look [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-swagger-extensions-integration.html)

## Start 

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

You then need to change the `x-amazon-apigateway-integration/uri` referencing the lambda function with the `FunctionArn` and then deploy again.

## Test locally

With SAM you can test your function locally:

```
sam local invoke --event events/events.json OpenApiDefinitionFunction
```

## Calling the API

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
aws cloudformation delete-stack --stack-name OpenApiDefinition
```
