# HOWTO

## Get the default VPC?

```shell
aws ec2 describe-vpcs --query 'Vpcs[?@.IsDefault].VpcId' --output text
```

## Get the public subnets?

```shell
aws ec2 describe-subnets --query 'Subnets[?@.VpcId == `${VPC_ID}` && @.MapPublicIpOnLaunch == `true`].SubnetId' --output text
```

## Get the private subnets?

```shell
aws ec2 describe-subnets --query 'Subnets[?@.VpcId == `${VPC_ID}` && @.MapPublicIpOnLaunch == `false`].SubnetId' --output text
```

## Get the default route table?

```shell
aws ec2 describe-route-tables --query 'RouteTables[?@.VpcId == `${VPC_ID}` ]' --output text
```

## Get the Secret Value?

This is useful to quickly get the Secret value whithout opening the console

```shell
aws secretsmanager get-secret-value --secret-id ${SECRET_ARN} --query 'SecretString' --output text | jq -r .password
```

## Get the Outputs of a stack?

This is useful to quickly get the stack Outputs whithout opening the console

```shell
aws cloudformation describe-stacks --query 'Stacks[0].Outputs' --stack-name ${STACK_NAME} 
```

## Get the Console Output of an Instance?

This is useful to troubleshoot an instance startup, whithout login in

```shell
aws ec2 get-console-output --instance-id ${INSTANCE_ID} --latest --query 'Output' --output text
```

## Get all non nested stacks' name?

```shell
aws cloudformation describe-stacks --query 'Stacks[?@.ParentId == null].StackName'
```

## Get all nested stacks' name?

```shell
aws cloudformation describe-stacks --query 'Stacks[?@.ParentId != ``].StackName'
```

## Get all drifted stack?

```shell
aws cloudformation list-stacks --query 'StackSummaries[?@.DriftInformation.StackDriftStatus == `DRIFTED`].StackName'
```