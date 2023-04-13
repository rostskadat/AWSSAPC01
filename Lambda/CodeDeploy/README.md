# CodeDeploy

Showcases a Lambda Deployment using different update strategy with CodeDeploy.

* Linear: grow traffic every N minutes until
* Canary: try X percent then 100%
* AllAtOnce: immediate

A good reference is available at [demo-lambda-safe-deployments](https://github.com/Versent/demo-lambda-safe-deployments)

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can simply test your newly created function by calling `curl` on the `ApiUrl` while deploying a new version.
You'll see that the version change from one version to the next using the [Canary10Percent10Minutes](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html) strategy

```shell
while true; do curl -s <ApiUrl> | jq -r ".environment.AWS_LAMBDA_FUNCTION_VERSION" ; sleep 1 ; done
10
...
11
10
...
11
11
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-CodeDeploy
```
