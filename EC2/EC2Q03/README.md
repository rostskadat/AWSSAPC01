# EC2Q03

## Question

```
A company has used Amazon EC2 Spot Instances for a demonstration. 
The demonstration is complete and a solutions architect must now remove the Spot Instances. 
Which action should the solutions architect take to remove the Spot Instances?

A. Cancel the Spot request.

B. Terminate the Spot Instances.

C. Cancel the Spot request and then terminate the instances.

D. Terminate the Spot Instances and then cancel the Spot request.

```

## Build the stack

```bash
sam build
sam deploy
```

## Testing the stack 

You should then receive 5 emails when the stack is created (or when the price is right)

You can then cancel the spot request
```bash
aws ec2 cancel-spot-fleet-requests --terminate-instances --spot-fleet-request-ids <SpotFleet> 
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name EC2Q03
```
