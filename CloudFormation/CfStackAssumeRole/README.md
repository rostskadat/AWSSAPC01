# CloudFormation / CfCloudFrontKeyGroup

A Custom Resource to use CloudFront's KeyGroup in your template

Look at [cloudformation-cross-account](https://github.com/aws-quickstart/quickstart-examples/tree/main/samples/cloudformation-cross-account)

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
