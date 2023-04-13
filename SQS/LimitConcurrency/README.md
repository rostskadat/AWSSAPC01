# LimitConcurrency

## Question

A company operates an ecommerce application on Amazon EC2 instances behind an Application
Load Balancer. The instances run in an Amazon EC2 Auto Scaling group across multiple Availability
Zones. After an order is successfully processed, the application immediately posts order data to an
external third-party affiliate tracking system that pays sales commissions for order referrals. During a
highly successful marketing promotion, the number of EC2 instances increased from 2 to 20. The
application continued to work correctly, but the increased request rate overwhelmed the third-party
affiliate and resulted in failed requests.

Which combination of architectural changes could ensure that the entire process functions correctly
under load? (Select TWO.)

* A) Move the code that calls the affiliate to a new AWS Lambda function. Modify the application to invoke the Lambda function asynchronously.
* B) Move the code that calls the affiliate to a new AWS Lambda function. Modify the application to place the order data in an Amazon SQS queue. Trigger the Lambda function from the queue.
* C) Increase the timeout of the new AWS Lambda function.
* D) Adjust the concurrency limit of the new AWS Lambda function.
* E) Increase the memory of the new AWS Lambda function.

## Answer

`B,D` Putting the messages in a queue (B) will decouple the main application from calls to the affiliate. That
will not only protect the main application from the reduced capacity of the affiliate, it will also allow failed requests
to automatically go back to the queue. Limiting number of concurrent executions (D) will prevent overwhelming
the affiliate application. A is incorrect because, while asynchronously invoking the Lambda function will reduce
load on the EC2 instances, it will not lower the number of requests to the affiliate application. C is incorrect
because, while it will allow the Lambda function to wait longer for the external call to return, it does not reduce the
load on the affiliate application (which will still be overwhelmed). E is incorrect because adjusting the memory will
have no effect on the interaction between the Lambda function and the affiliate application.

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Test locally

With SAM you can test your function locally:

```
sam local invoke --event events/events.json LimitConcurrencyFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name LimitConcurrency
```
