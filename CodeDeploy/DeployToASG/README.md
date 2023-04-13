# CodeDeploy / DeployToASG

Showcase how to deploy to ASG (In place deploymemnt)

## Building

* Build the resources required by the stack

```shell
sam build --template template-bucket.yaml
sam deploy --guided
``` 

* Build and deploy the main stack

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json DeployToASGFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-DeployToASG
```

## References:

* [integrations-aws-elastic-load-balancing](https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html)

## Details

*Author*: rostskadat
