# ScalingPolicies

Showcase the different Scaling policies:

* Step
* Target
* Scheduled

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Once build, you can login into the instances of the different `AutoScalingGroup` and try to send their CPUUtilization above the 40% threshold.
But first you need to figure out the `PublicDnsName` of the instances in the different `AutoScalingGroup` 

```shell
instance_id=$(aws autoscaling describe-auto-scaling-instances | jq -r '.AutoScalingInstances[] | select (.AutoScalingGroupName == "<StepScalingAutoScalingGroup>") | .InstanceId')
ssh $(aws ec2 describe-instances --instance-id $instance_id --query "Reservations[0].Instances[0].PublicDnsName" --output text)

$ # Start a CPU hog
$ openssl speed -multi $(nproc --all) > /dev/null 2>&1 &
```


In order to do that you can use the `stress` tool (installed by default).

```shell
./stress --cpu 1
```

In response to that load, the different autoscaling group will response differently...

For the `ScheduledScalingAutoScalingGroup`, the scale out will happen 3 times an hour at `:00`, `:20`, `:40`, while the scale in will happen at `:10`, `:30`, `:50`

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ScalingPolicies
```
