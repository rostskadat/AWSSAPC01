# HighSeverityEvents

## Question
A web hosting company has enabled Amazon GuardDuty in every AWS Region for all of its accounts. A
system administrator must create an automated response to high-severity events.

How should this be accomplished?

* A) Create rules through VPC Flow Logs that trigger an AWS Lambda function that programmatically
addresses the issue.
* B) Create an Amazon CloudWatch Events rule that triggers an AWS Lambda function that programmatically
addresses the issue.
* C) Configure AWS Trusted Advisor to trigger an AWS Lambda function that programmatically addresses the
issue.
* D) Configure AWS CloudTrail to trigger an AWS Lambda function that programmatically addresses the
issue.


## Answer

`B` – GuardDuty findings can be sent to CloudWatch Events. Neither VPC Flow Logs
nor AWS CloudTrail can trigger a Lambda function. Trusted Advisor is a recommendation service, and is not
suited for this scenario.

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Test locally

With SAM you can test your function locally:

```
sam local invoke --event events/events.json HighSeverityEventsFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name HighSeverityEvents
```
