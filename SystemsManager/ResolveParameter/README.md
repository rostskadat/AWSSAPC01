# ResolveParameter

This scenario show case the use of Public SSM parameters in a cloudstack formation.
An complete list of available parameters can be found [here](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-public-parameters.html)

You can check that the AMI was properly set in all cases by simply output the system log and look for the `ImageId` string

```shell
aws ec2 get-console-output --instance-id <InstanceId> --latest
```

## Build

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name ResolveParameter
```
