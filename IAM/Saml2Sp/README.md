# IAM / Saml2Sp

Showcase the use of SAML to connect a SP and an IDP.

The stack is composed of 2 pieces:

* The IdP: Use a Cognito Pool as IdP
* The SP: A simple Flask Application

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can deploy a new version of the services:

```shell
cluster=$(aws cloudformation describe-stacks --stack-name SAPC01-Saml2Sp --query 'Stacks[0].Outputs[?@.OutputKey == `Cluster`].OutputValue' --output text)
sp_service=$(aws cloudformation describe-stacks --stack-name SAPC01-Saml2Sp --query 'Stacks[0].Outputs[?@.OutputKey == `SPService`].OutputValue' --output text)
idp_service=$(aws cloudformation describe-stacks --stack-name SAPC01-Saml2Sp --query 'Stacks[0].Outputs[?@.OutputKey == `IdPService`].OutputValue' --output text)

# Update the Services ...
aws ecs update-service --force-new-deployment --enable-execute-command --cluster ${cluster} --service ${idp_service}
aws ecs update-service --force-new-deployment --enable-execute-command --cluster ${cluster} --service ${sp_service}
```

You can also execute command directly in your containers as per [ecs-exec](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html#ecs-exec-enabling-and-using)

```shell
cluster=$(aws cloudformation describe-stacks --stack-name SAPC01-Saml2Sp --query 'Stacks[0].Outputs[?@.OutputKey == `Cluster`].OutputValue' --output text)
taskArns=$(aws ecs list-tasks --cluster ${cluster} --output text --query 'taskArns')
aws ecs describe-tasks --cluster ${cluster} --tasks ${taskArns} --query 'tasks[].{taskArn:taskArn, name:overrides.containerOverrides[0].name}'
...
aws ecs execute-command --cluster ${cluster} --task ${taskArn} --container ${name} --interactive --command "/bin/bash"
```

Once you are happy you can open the `SPRecordSetUrl` in your browser and login with `testuser`:`qwerty`



## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-Saml2Sp
```

## Details

*Author*: rostskadat
