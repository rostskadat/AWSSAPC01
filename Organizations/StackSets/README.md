# StackSets

## Question

A company has multiple AWS accounts. The company has integrated its on-premises Active Directory
with AWS SSO to grant Active Directory users least privilege abilities to manage infrastructure across all
the accounts.
A solutions architect must integrate a third-party monitoring solution that requires read-only access
across all AWS accounts. The monitoring solution will run in its own AWS account.

How can the monitoring solution be given the required permissions?

* A) Create a user in an AWS SSO directory and assign a read-only permissions set. Assign all AWS accounts to be monitored to the new user. Provide the third-party monitoring solution with the user name and password.
* B) Create an IAM role in the organization's master account. Allow the AWS account of the third-party monitoring solution to assume the role.
* C) Invite the AWS account of the third-party monitoring solution to join the organization. Enable all features.
* D) Create an AWS CloudFormation template that defines a new IAM role for the third-party monitoring solution with the account of the third party listed in the trust policy. Create the IAM role across all linked AWS accounts by using a stack set.

## Answer

`D` – AWS CloudFormation StackSets can deploy the IAM role across multiple accounts with a single operation.
A is incorrect because credentials supplied by AWS SSO are temporary, so the application would lose
permissions and have to log in again. B would grant access to the master account only. C is incorrect because
accounts belonging to an organization do not receive permissions in the other accounts.

## Starting

You must first make sure that all feature are enabled in the master account

```shell
aws organizations enable-all-features
```

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can now access the account by assuming the <MonitoringRole>

But first you'll need to list the linked account that belong to the OrganizationalUnit <DeploymentTargetOu>

```shell
aws organizations list-accounts-for-parent --parent-id <DeploymentTargetOu> | jq -r '.Accounts[].Id'
123456789012
```

Then assume the role in the linked account (make sure to use the correct Account Id)

```shell
aws --profile <MonitoringUsername> sts assume-role --role-arn arn:aws:iam::123456789012:role/MonitoringRole-eu-west-1 --role-session-name MONITOR-SECURITY
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name StackSets
```
