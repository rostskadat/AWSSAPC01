# BillingAlarm

## Question

An enterprise has a large number of AWS accounts owned by separate business groups. One of the accounts was recently compromised. The attacker launched a large number of instances, resulting in a high bill for that account.

The security breach was addressed, but management has asked a solutions architectto develop a solution to prevent excessive spending in all accounts. Each business group wants to retain full control over its AWSaccount.

Which solution should the solutions architectrecommend to meet these requirements?
* A) Use AWS Organizations to add each AWS account to the master account. Create a service control policy (SCP) that uses the ec2:instanceTypecondition key to prevent the launch of high-cost instance types in each account.
* B) Attach a new customer-managed IAM policy to an IAM group in each account that uses theec2:instanceTypecondition keyto preventthe launch of high-cost instance types. Place all of the existing IAM users in each group.
* C) Enable billing alerts on each AWS account. Create Amazon CloudWatch alarms that send an Amazon SNS notification to the account administrator whenever their account exceeds the spending budget.
* D) Enable Cost Explorer in each account. Regularly review the Cost Explorer reports for each account to ensure spending does not exceed the planned budget.

## Answer

`C`: retain full control and has automatic alert.

```bash
sam build 
sam deploy --stack-name BillingAlarm --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --capabilities CAPABILITY_IAM --region eu-west-1
``` 

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name BillingAlarm
```
