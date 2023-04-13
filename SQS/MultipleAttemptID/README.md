# SQS / MultipleAttemptID

Showcase how the SQS AttemptId is used to retry a failed message

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

After creating the stack simply send some messages to the `PrintQueue` and look at the Cloudwatch Logs to see how the lambda function uses the `ReceiveRequestAttemptId` to retry the message

```shell
../../helpers/sqs_send_message.py --queue-url <PrintQueue> --count 10
``` 

Once the messages have been sent, you can use the `sqs_receive_and_retry_messages.py`:

```shell
./helpers/sqs_receive_and_retry_messages.py --queue-url <PrintQueue> --count 5
INFO | Found credentials in shared credentials file: ~/.aws/credentials
INFO | ReceiveRequestAttemptId=924315b8-88be-4f17-ae20-83a94511ef80
INFO | Processing message 1da7bcf5-b96a-4e06-8170-d48e94697231 ...
INFO | Processing message 001a4dea-bb87-4d81-8e73-ca8ba94afae6 ...
INFO | Processing message 4f36f13c-354b-4953-95e2-2343eb642fa8 ...
INFO | Processing message 314203d9-46b9-4d9c-b5fb-0e4bcf2ad6cf ...
INFO | Processing message d8d9d894-5365-42b4-b5ee-7f00e3a7d7e3 ...
INFO | Simulating long processing and failure (no delete)
INFO | Retrying 
INFO | Reprocessing message 1da7bcf5-b96a-4e06-8170-d48e94697231 ...
INFO | Reprocessing message 001a4dea-bb87-4d81-8e73-ca8ba94afae6 ...
INFO | Reprocessing message 4f36f13c-354b-4953-95e2-2343eb642fa8 ...
INFO | Reprocessing message 314203d9-46b9-4d9c-b5fb-0e4bcf2ad6cf ...
INFO | Reprocessing message d8d9d894-5365-42b4-b5ee-7f00e3a7d7e3 ...
INFO | Deleting the processed messages...
``` 

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-MultipleAttemptID
```

## Details

*Author*: rostskadat
