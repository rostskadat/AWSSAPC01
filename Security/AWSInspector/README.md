# AWSInspector

Showcase the use of AWS Inspector on an EC2Instance

## Obtaining the list of available Rule Packages

```shell
aws inspector describe-rules-packages --rules-package-arns $(aws inspector list-rules-packages --query rulesPackageArns --output text)
```

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json AWSInspectorFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-AWSInspector
```
