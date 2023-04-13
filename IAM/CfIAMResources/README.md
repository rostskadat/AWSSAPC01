# IAM / CfIAMResources

Several Custom Resource to use IAM SAML Provider.

*BEWARE* In order to use the `CfIAMSamProviderFunction.SAMLMetadataDocumentUrl` attribute you will need to deploy your function into a VPC

You can use it as follow in your template

```yaml
  SAMLProvider:
    Type: Custom::CfIAMSamProviderFunction
    Version: "1.0"
    Properties:
      ServiceToken:
        Fn::Sub: "arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:CfIAMSamProviderFunction"
      SAMLMetadataDocumentUrl: "https://federation.example.com/FederationMetadata/2007-06/FederationMetadata.xml"
```

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json CfIAMSamProviderFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name CfIAMResources
```

## Details

*Author*: rostskadat
