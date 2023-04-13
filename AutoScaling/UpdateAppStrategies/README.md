# UpdateAppStrategies

Showcase the different update strategies of an application.

* LaunchTemplate version, same TargetGroup
* LaunchTemplate version, different TargetGroup
* Route53 weighted records

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Updating the LaunchTemplate version

```shell
sam local invoke --event events/events.json UpdateAppStrategiesFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-UpdateAppStrategies
```
