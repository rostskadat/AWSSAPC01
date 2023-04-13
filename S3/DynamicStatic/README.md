# DynamicStatic

## Question

```
You can add the question here in order to get an idea of what the project is all about
 
A. Answer 1
B. Answer 2
C. Answer 3
```

## Answer

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json DynamicStaticFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-DynamicStatic
```
