# HtmlForm

## Question

A team is building an HTML form hosted in a public Amazon S3 bucket. The form uses JavaScript to
post data to an Amazon API Gateway endpoint. The endpoint is integrated with AWS Lambda
functions. The team has tested each method in the API Gateway console and received valid responses.

Which combination of steps must be completed for the form to successfully post to the API Gateway and
receive a valid response? (Select TWO.)

* A) Configure the S3 bucket to allow cross-origin resource sharing (CORS).
* B) Host the form on Amazon EC2 rather than Amazon S3.
* C) Request a limit increase for API Gateway.
* D) Enable cross-origin resource sharing (CORS) in API Gateway.
* E) Configure the S3 bucket for web hosting.

## Answer

`D/E`:

```bash
sam build 
sam deploy --stack-name HtmlForm --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --capabilities CAPABILITY_IAM --region eu-west-1
``` 

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name HtmlForm
```
