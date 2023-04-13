# Secrets

This scenario showcase the different uses of ParameterStore, such as plaintext parameters, parameter hierarchy, access control, acces to secret manager, etc

## Building

Since CloudFormation does not allow the creation of SecureString parameter, you must create it before hand. 
*BEWARE*: The name `ParameterStoreSecureString` is important

```bash
aws ssm put-parameter --name ParameterStoreSecureString --value "SecureStringValue" --type SecureString
``` 

Then you can build the stack itself

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Just retrieve the S3 Object created with the different parameter and check that they match.

```
aws s3 cp <ParameterDump>
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-Secrets
aws ssm delete-parameter --name ParameterStoreSecureString
```
