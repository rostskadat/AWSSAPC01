# Q02-SqsAutoscaling

## Question


```
Users of an image processing application experience long delays waiting for their images to process when the application experiences unpredictable periods of heavy usage. 
The architecture consists of a web tier, an Amazon Simple Queue Service (Amazon SQS) standard queue, and message consumers running on Amazon EC2 instances. 
When there is a high volume of requests, the message backlog in Amazon SQS spikes. 
A solutions architect is tasked with improving the performance of the application while keeping costs low. 

Which solution meets these requirements?

A. Purchase enough Dedicated Instances to meet the peak demand and deploy them for the consumers.

B. Convert the existing Amazon SQS queue to an Amazon SQS FIFO queue and increase the visibility timeout.

C. Configure an AWS Lambda function to scale out the number of consumer instances when the message backlog grows.

D. Run the message consumer instances in an Auto Scaling group configured to scale out and in based upon the ApproximateNumberOfMessages Amazon CloudWatch metric.

```

## Answer

`D`


## Build the stack

```bash
sam build
sam deploy
```

## How to test:

Execute the `generate_message.py` to generate messages, after a while you should receive the message sent by the Alarm.

```bash
./app/generate_message.py --queue-url <QueueUrl> --count 20 --delay 60
```

Further more you can watch the Autoscaling Group add new instances:

```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names <AutoscalingGroupName> | jq '.AutoScalingGroups[0].Instances'
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name Q02
```
