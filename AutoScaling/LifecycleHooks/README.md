# LifecycleHooks

Showcase the different Lifecycle Hooks available during autoscaling

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Just launch and terminate an instance to call the corresponding Lambda function...

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-LifecycleHooks
```
