# ReduceKinesisCost

## Question

A solutions architect needs to reduce costs for a big data application. The application environment
consists of hundreds of devices that send events to Amazon Kinesis Data Streams. The device ID is used
as the partition key, so each device gets a separate shard. Each device sends between 50 KB and 450 KB
of data per second. The shards are polled by an AWS Lambda function that processes the data and stores
the result on Amazon S3.

Every hour, an AWS Lambda function runs an Amazon Athena query against the result data that identifies
any outliers and places them in an Amazon SQS queue. An Amazon EC2 Auto Scaling group of two EC2
instances monitors the queue and runs a short (approximately 30-second) process to address the
outliers. The devices submit an average of 10 outlying values every hour.

Which combination of changes to the application would MOST reduce costs? (Select TWO.)

* A) Change the Auto Scaling group launch configuration to use smaller instance types in the same instance family.
* B) Replace the Auto Scaling group with an AWS Lambda function triggered by messages arriving in the Amazon SQS queue.
* C) Reconfigure the devices and data stream to set a ratio of 10 devices to 1 data stream shard.
* D) Reconfigure the devices and data stream to set a ratio of 2 devices to 1 data stream shard.
* E) Change the desired capacity of the Auto Scaling group to a single EC2 instance.

## Answer

`B, D` The average amount of used each hour is about 300 seconds (10 events x 30 seconds). While
A and E would both reduce costs, they both involve paying for one or more EC2 instances sitting unused for
3,300 or more seconds per hour. B involves paying for the small amount of compute time required to process the
outlying values only. Both C and D reduce the shard hour costs of the Kinesis data stream, but C will not work
because the amount of data would exceed the 1 MBps limit of a single shard.



```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Test locally

With SAM you can test your function locally:

```
sam build
sam local invoke ProcessStreamFunction --event events/KinesisProcess.json --env-vars environments/ProcessStreamFunction.json
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name ReduceKinesisCost
```
