# OperateInstances

## Question

A company is launching a new web service on an Amazon ECS cluster. Company policy requires that
the security group on the cluster instances block all inbound traffic but HTTPS (port 443). The cluster
consists of 100 Amazon EC2 instances. Security engineers are responsible for managing and updating
the cluster instances. The security engineering team is small, so any management efforts must be
minimized.
How can the service be designed to meet these operational requirements?

* A) Change the SSH port to 2222 on the cluster instances with a user data script. Log in to each instance
using SSH over port 2222.
* B) Change the SSH port to 2222 on the cluster instances with a user data script. Use AWS Trusted Advisor
to remotely manage the cluster instances over port 2222.
* C) Launch the cluster instances with no SSH key pairs. Use the Amazon Systems Manager Run Command
to remotely manage the cluster instances.
* D) Launch the cluster instances with no SSH key pairs. Use AWS Trusted Advisor to remotely manage the
cluster instances.

## Answer

`C`: The Systems Manager Run Command requires no inbound ports to be open; it operates entirely over
outbound HTTPS (which is open by default for security groups). A and B are ruled out because the requirements
clearly state that the only inbound port to be open is 443. D is ruled out because Trusted Advisor does perform
management functions.

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

You can then simply get the output of the Association:

```
?> aws s3 cp s3://operateinstances-bucket-19gkj77ofk5ae/logs/3f0ae441-1217-4dd5-96c1-bd74ffb11038/i-05fad181bb2022a6c/awsrunShellScript/0.awsrunShellScript/stdout
?> cat stdout
Hello from association...

```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name OperateInstances
```
