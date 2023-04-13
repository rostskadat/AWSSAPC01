# DirectoryService / EC2WithSimpleADAccount

Showcase how to integrate an EC2 Instance with a Simple AD directory

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json EC2WithSimpleADAccountFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-EC2WithSimpleADAccount
```

## Details

*Author*: rostskadat
