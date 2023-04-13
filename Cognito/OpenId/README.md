# Cognito / OpenId

Showcase the use of Cognito with an LDAP backend to authenticate/authorize Users.

Look at [python-openid](https://github.com/openid/python-openid/tree/master/examples) for example of OpenId Client

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json OpenIdFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-OpenId
```

## Details

*Author*: rostskadat
