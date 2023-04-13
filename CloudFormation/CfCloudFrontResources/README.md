# CloudFormation / CfCloudFrontKeyGroup

Several Custom Resource to use CloudFront's PublicKey / KeyGroup in your template

You can use it as follow in your template

```yaml

  PublicKey:
    Type: Custom::CfCloudFrontPublicKeyFunction
    Version: "1.0"
    Properties:
      ServiceToken:
        Fn::Sub: "arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:CfCloudFrontPublicKeyFunction"
      PublicKeyConfig:
        EncodedKey: 
          Ref: EncodedKey
        Comment: Key to sign URLs in the S3Distribution

  KeyGroup:
    Type: Custom::CfCloudFrontKeyGroupFunction
    Version: "1.0"
    Properties:
      ServiceToken:
        Fn::Sub: "arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:CfCloudFrontKeyGroupFunction"
      KeyGroupConfig:
        Items:
          - Ref: PublicKey
        Comment: Key Group associated with the S3Distribution

  TrustedKeyGroupAssociation:
    Type: Custom::CfCloudFrontTrustedKeyGroupAssociationFunction
    Version: "1.0"
    Properties:
      ServiceToken:
        Fn::Sub: "arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:CfCloudFrontTrustedKeyGroupAssociationFunction"
      DistributionId: 
        Ref: Distribution
      KeyGroupId:
        Ref: KeyGroup

  Distribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      ...

```

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json CfCloudFrontKeyGroupFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-CfCloudFrontKeyGroup
```

## Details

*Author*: rostskadat
