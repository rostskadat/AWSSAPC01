# EC2 / Hibernate

Showcase how to hibernate the an instance

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

* Curl the `EC2Instance` to start a background task:

```shell
curl <EC2Instance>
ssh <EC2Instance> 'while (true); do cat /tmp/gunicorn-background-task-* ; echo ; sleep 10 ; done'
2021-02-08'T'15:54:02
2021-02-08'T'15:54:12
2021-02-08'T'15:54:22
...
^C
```

* Then hibernate the instance and wait for it to be `stopped`

```shell
aws ec2 stop-instances --instance-ids <InstanceId> --hibernate
...
aws ec2 describe-instances --instance-ids <InstanceId> | jq '.Reservations[].Instances[0].State.Name'
"stopped"
```

* Then restart the instance and wait for it to be `running`. *BEWARE* The FQDN might have changed

```shell
aws ec2 start-instances --instance-ids <InstanceId> --hibernate
...
aws ec2 describe-instances --instance-ids i-0cbc7c047185b96f8 | jq '.Reservations[].Instances[0].State.Name'
"running"
aws ec2 describe-instances --instance-ids i-0cbc7c047185b96f8 | jq '.Reservations[].Instances[0].PublicDnsName'
"ec2-52-17-140-150.eu-west-1.compute.amazonaws.com"
```

* Then SSH again, you should see the background task running as before:


```shell
ssh ec2-52-17-140-150.eu-west-1.compute.amazonaws.com 'while (true); do cat /tmp/gunicorn-background-task-* ; echo ; sleep 10 ; done'
2021-02-08'T'16:01:20
2021-02-08'T'16:01:20
...
^C
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-Hibernate
```

## Details

*Author*: rostskadat
