# Invocations

Showcase the 3 different kind of Lambda invocations:
* Synchronous (APIGateway) 
* Asynchronous (S3 Event + DLQ) 
* Event Source Mapping (DynamoDB Stream, SQS+DLQ)

Each invocation type require a different Error handling:
* Synchronous: the client is in charge of error handling + exponential backof, etc
* Asynchronous: the event generator will handle 3 erros and then send the event to the DLQ
* Event Source Mapping: stop the batch until the error is properly handled or transfered to the DLQ

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing Synchronous Invocations


You can test the Synchronous invocations by calling a simple curl on the function endpoint. You can simulate an error by adding the query parameter `key=error`

```shell
curl -v <ApiUrl>
{"message": "To simulate an error set the 'key' query parameter to 'error'.", "location": "SynchronousFunction"}

curl -v <ApiUrl>?key=error
> GET /Prod/SynchronousFunction?key=error HTTP/2
...
< HTTP/2 400 
...
{"message": "You set the 'key' query parameter to 'error'. Returning error ...", "location": "SynchronousFunction"}[rostskadat@sorgenfri Invocations]$ 
```

## Testing Asynchronous Invocations


After confirming the subscription, you can upload object to S3 and depending on their key this will be processed or not. If the processing of the key fails 3 time, you should recieve and email indicating the error:

```shell
aws s3 cp README.MD s3://<Bucket>
# Everything goes well and the S3 object is correctly processed

aws s3 cp README.MD s3://<Bucket>/error
# The special key 'error' trigger a processing failure that ersult in an email being sent to the DLQ
...

{
  "Type" : "Notification",
...
  "Message" : "{\"Records\":[{\"eventVersion\":\"2.1\",\"eventSource\":\"aws:s3\",\"awsRegion\":\"eu-west-1\",\"eventTime\":\"2020-11-01T11:34:19.856Z\",\"eventName\":\"ObjectCreated:Put\",\"userIdentity\":{\"principalId\":\"AWS:AIDAIG32FXIV6KU7KTP7W\"},\"requestParameters\":{\"sourceIPAddress\":\"90.162.185.145\"},\"responseElements\":{\"x-amz-request-id\":\"4DB05C26A0B8F082\",\"x-amz-id-2\":\"Lq1o48G7UOvkbdjDwiRZVnbve0xdWh47UrJO916PJwtPJSpiV9jibPTa+wqUcmpYMnstYbtqLKyKEJMA+B7fNVSbU8T3OL/6BIWz1IciL0E=\"},\"s3\":{\"s3SchemaVersion\":\"1.0\",\"configurationId\":\"9c5cd639-506c-4c7e-bba4-34ee85d7435f\",\"bucket\":{\"name\":\"sapc01-invocations-bucket-7s93fvqeatih\",\"ownerIdentity\":{\"principalId\":\"A1L66XQ8A8IMOE\"},\"arn\":\"arn:aws:s3:::sapc01-invocations-bucket-7s93fvqeatih\"},\"object\":{\"key\":\"error\",\"size\":1028,\"eTag\":\"e742f12f6b2cdb4edc6b50c1536f6098\",\"sequencer\":\"005F9E9D4191F9DBEF\"}}}]}",
...
  "MessageAttributes" : {
    "RequestID" : {"Type":"String","Value":"815f0dbe-36ad-45cd-9f97-68e487fb861a"},
    "ErrorCode" : {"Type":"Number","Value":"200"},
    "ErrorMessage" : {"Type":"String","Value":"Simulating Error"}
  }
}
```

## Testing Event Source Mapping Invocations

After confirming the subscription, you can send a message to the SQS queue with whatever body you wish

```shell
../../helpers/sqs_send_message.py  --queue-url <Queue> --count 10 --message-body events/simulate-sqs-message-ok.json
# Everything goes well and the SQS Queue should now be empty

...


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-Invocations
```
