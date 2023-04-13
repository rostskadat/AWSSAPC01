# ConcurrentExecutions

## Question

A retail company runs a serverless mobile app built on Amazon API Gateway, AWS Lambda, Amazon
Cognito, and Amazon DynamoDB. During heavy holiday traffic spikes, the company receives complaints
of intermittent system failures. Developers find that the API Gateway endpoint is returning 502 Bad
Gateway errors to seemingly valid requests.

Which method should address this issue?
* A) Increase the concurrency limit for Lambda functions and configure notification alerts to be sent by
Amazon CloudWatch when the ConcurrentExecutions metric approaches the limit.
* B) Configure notification alerts for the limit of transactions per second on the API Gateway endpoint and
create a Lambda function that will increase this limit, as needed.
* C) Shard users to Amazon Cognito user pools in multiple AWS Regions to reduce user authentication
latency.
* D) Use DynamoDB strongly consistent reads to ensure the latest data is always returned to the client
application.

## Answer

`A` The 502 internal server errors will be returned intermittently by API Gateway if the Lambda function
exceeds concurrency limits. `B` is incorrect because, in this case, API Gateway would return a 429 error for too
many requests. `C` is incorrect because the error occurs when calling the API Gateway endpoint, not during the
authentication process. `D` is incorrect because stale data would not cause a bad gateway error.

## Start

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Test locally

With SAM you can test your function locally:

```
sam local invoke --event events/events.json ConcurrentExecutionsFunction
```

## Start the clients

The idea is to saturate the Lambda Function through the API Gateway. That can be achieved by launching many consumers in parrallel:

```bash
start_consumer.py --url $ApiGatewayApi --consumers 10
```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name ConcurrentExecutions
```
