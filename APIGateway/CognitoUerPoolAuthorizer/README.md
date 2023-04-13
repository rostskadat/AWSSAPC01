# CognitoUerPoolAuthorizer

This scenario demonstrates a API access control based on [Cognito User Pools](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-controlling-access-to-apis.html#serverless-controlling-access-to-apis-cognito-user-pool)

*NOTE* that the `PostAuthenticationFunction` is only used to show that the user was properly logged. It does not participate in the authentication or access control flow.

## Start

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01"
``` 

## Change the user password for 1 login

Before being able to call the API you must obtain a token, for the DemoUser. You must have obtain the password in your email.

```
?> ./users/change_user_password.py \
    --user-pool-id <UserPoolId> \
    --client-id <ClientId> \
    --username <Username> \
    --current-password "%Y3bYaTU" \
    --new-password "uR#69Jwd2#Ith@j4"
```

## obtain a token to call the API

```
?> ./users/get_token.py \
    --user-pool-id <UserPoolId> \
    --client-id <ClientId> \
    --username <Username> \
    --password "uR#69Jwd2#Ith@j4"
```

and extract the `IdToken`


## Calling the API

If you call it without `Authorization` header or with the `Authorization` header set to an invalid value (try `deny` or none), you will get:

```
?> curl -k $ApiGatewayApi
{"message":"Unauthorized"}
```

and if you call it by setting the `Authorization` header to `IdToken` you will get:
```
?> curl -k -H "Authorization: $IdToken" $ApiGatewayApi
{"message": "Hello World!", "location": "3.249.220.254"}
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name CognitoUerPoolAuthorizer
```
