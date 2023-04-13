# ManagedBlockchain / HelloWorld

Showcase a simple Hyperledger blockchain

*Reference*:
* [build-and-deploy-an-application-for-hyperledger-fabric-on-amazon-managed-blockchain](https://aws.amazon.com/blogs/database/build-and-deploy-an-application-for-hyperledger-fabric-on-amazon-managed-blockchain/)

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json HelloWorldFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-HelloWorld
```

## Details

*Author*: rostskadat
