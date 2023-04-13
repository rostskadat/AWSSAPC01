# SQS / DelayedSQSMessage

Showcase delayed SQS message

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can then send a message to the queue using the `Delay` attribute of the `send_message` method:

```shell
python3 ..\..\helpers\sqs_send_message.py --queue-url <Queue> --count 1 --message-delay 120
INFO | Found credentials in shared credentials file: ~/.aws/credentials
Sent message (0/1): 4d328a7e-4d7d-47f1-9a86-81d55d2c1087
```

Then when looking at the processing time for the given message you will see the delayed action in the log of the Lambda function:

```
[INFO] 2021-01-07T11:02:50.784Z fcef2d70-fd42-5419-a8ad-750011c8b7ce Message was sent @ '2021-01-07 12:00:49.993840'. It is now '2021-01-07 11:02:50.784236' 
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-DelayedSQSMessage
```

## Details

*Author*: rostskadat
