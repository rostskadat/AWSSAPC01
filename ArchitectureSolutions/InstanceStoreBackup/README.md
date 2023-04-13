# ArchitectureSolutions / InstanceStoreBackup

Showcase Instance Store Backup. As explained in (creating-an-ami-instance-store)[https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-instance-store.html#bundle-ami-prerequisites]

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

After creating the instance you can use the AWS CLI to create an instance snapshot that has a backup for the ephemeral storage.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-InstanceStoreBackup
```

## Details

*Author*: rostskadat
