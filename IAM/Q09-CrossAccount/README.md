# IAMQ09

## Question

```
A company uses one AWS account to run production workloads and has a separate AWS account for the security team. 
During periodic audits, the security team needs to view certain account settings and resource configurations in the other AWS account.

How can a solutions architect provide the required access to the security team following the principle of least privilege?

A. Create an IAM user for each security team member on the production account. 
   Attach a permissions policy that provides the permissions required by the security team to each user.

B. Create an IAM role in the production account. Attach a permissions policy that provides the permissions required by the security team. 
   Add the security team account to the trust policy.

C. Create a new IAM user in the production account. Assign administrative privileges to the user. 
   Allow the security team to use this account to log in to the systems that need to be accessed.

D. Create an IAM user for each security team member on the production account. 
   Attach a permissions policy that provides the permissions required by the security team to a new IAM group. Assign the security team members to the group.

```

## Build the stack

```bash
sam build
sam deploy
```

## Testing the stack 

You should now be able to use the Profile of the Security User in order to list the instances in the production organization

Look at this [HOWTO](https://aws.amazon.com/blogs/security/how-to-use-a-single-iam-user-to-easily-access-all-your-accounts-by-using-the-aws-cli/)

As a Security Team member you need to configure a new CLI profile that references the Role you created in the stack

```bash
aws configure set profile.SecurityUser_Audit.role_arn <SecurityAuditRoleArn>
aws configure set profile.SecurityUser_Audit.source_profile SecurityUser
```

As a result in your AWS credentials `~/.aws/credentials` you will have the following

```ini
[SecurityUser]
aws_access_key_id = <ACCESS_KEY_ID>
aws_secret_access_key = <SECRET_ACCESS_KEY>

[SecurityUser_Audit]
role_arn = <SecurityAuditRoleArn>
source_profile = SecurityUser
```

The following command showcase the priviledge escalation. The first action is done in the realm of the SecurityTeam, while the second call is done in the realm of the parent organization

```bash
aws ec2 describe-instances
aws --profile SecurityUser_Audit ec2 describe-instances
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name IAMQ09
```
