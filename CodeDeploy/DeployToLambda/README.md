# CodeDeploy / DeployToLambda

Showcase using CodeDeploy to update Lambda function

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json DeployToLambdaFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-DeployToLambda
```

## References 

* [tutorial-lambda-sam](https://docs.aws.amazon.com/codedeploy/latest/userguide/tutorial-lambda-sam.html)

## Details

*Author*: rostskadat
