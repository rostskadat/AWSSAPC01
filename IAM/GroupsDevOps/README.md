# GroupsDevOps

## Question

A company has two AWS accounts: one for production workloads and one for development workloads.
Creating and managing these workloads are a development team and an operations team. The company
needs a security strategy that meets the following requirements:

* Developers need to create and delete development application infrastructure.
* Operators need to create and delete both development and production application infrastructure.
* Developers should have no access to production infrastructure.
* All users should have a single set of AWS credentials.

What strategy meets these requirements?

* A) 
    * In the development account:
        * Create a development IAM group with the ability to create and delete application infrastructure.
        * Create an IAM user for each operator and developer and assign them to the development group.
    * In the production account:
        * Create an operations IAM group with the ability to create and delete application infrastructure.
        * Create an IAM user for each operator and assign them to the operations group.

* B)
    * In the development account:
        * Create a development IAM group with the ability to create and delete application infrastructure.
        * Create an IAM user for each developer and assign them to the development group.
        * Create an IAM user for each operator and assign them to the development group and the operations group in the production account.
    * In the production account:
        * Create an operations IAM group with the ability to create and delete application infrastructure.
* C)
    * In the development account:
        * Create a shared IAM role with the ability to create and delete application infrastructure in the production account.
        * Create a development IAM group with the ability to create and delete application infrastructure.
        * Create an operations IAM group with the ability to assume the shared role.
        * Create an IAM user for each developer and assign them to the development group.
        * Create an IAM user for each operator and assign them to the development group and the operations group.

* D)
    * In the development account:
        * Create a development IAM group with the ability to create and delete application infrastructure.
        * Create an operations IAM group with the ability to assume the shared role in the production account.
        * Create an IAM user for each developer and assign them to the development group.
        * Create an IAM user for each operator and assign them to the development group and the operations group.
    * In the production account:
        * Create a shared IAM role with the ability to create and delete application infrastructure.
        * Add the development account to the trust policy for the shared role.

## Answer

`D` – This is the only response that will work and meets the requirements. It follows the standard guidelines for
granting cross-account access between two accounts that you control. A requires two sets of credentials for
operators, which breaks the requirements. B will not work, as an IAM user cannot be added to an IAM group in a
different account. C will not work, as a role cannot grant access to resources in another account; the shared role
must be in the account with resources it manages.

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

*BTW*: The account created with the stack [AccountBuilder](../AccountBuilder) trust the Master account by default (cf. the `OrganizationAccountAccessRole` in the sub account). Furthermore an explicit "Deny" policy is created in case the Developer user is an `Administrator`, in which case it would have permission to assume the role

## Test

List instances in the developer account using a Developer profile
```bash
aws --profile <Developer> ec2 describe-instances --query "Reservations[0].Instances[0].[InstanceId, InstanceType]"
[
    "i-08523f952e13eadb8",
    "c5.large"
]
```

And now using an Operator profile (should get the same thing)
```bash
aws --profile <Operator> ec2 describe-instances --query "Reservations[0].Instances[0].[InstanceId, InstanceType]"
[
    "i-08523f952e13eadb8",
    "c5.large"
]
```

Now try to get that information for the Production account. First verify your identity

```bash
aws --profile <Developer> sts get-caller-identity
{
    "UserId": "AIDAIG32FXIV6KU7KTP7W",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/rostskadat"
}
aws --profile <Operator> sts get-caller-identity
{
    "UserId": "AIDAJ3KZEWPB666E5FI24",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/batch-build"
}
```

Now let's assume the role in the dependant account. It should fail for <Developer> and succeed to <Operator>
```bash
aws --profile <Developer> sts assume-role --role-arn "arn:aws:iam::<Account>:role/OrganizationAccountAccessRole" --role-session-name AWSCLI-Session

An error occurred (AccessDenied) when calling the AssumeRole operation: User: arn:aws:iam::123456789012:user/rostskadat is not authorized to perform: sts:AssumeRole on resource: arn:aws:iam::610150951079:role/OrganizationAccountAccessRole
```

However when running as <Operator> we do obtain get credentials:

```bash
aws --profile <Operator> sts assume-role --role-arn "arn:aws:iam::<Account>:role/OrganizationAccountAccessRole" --role-session-name AWSCLI-SessionOperator

{
    "Credentials": {
        "AccessKeyId": "ASIAY4D6UVCTZGT6R36E",
        "SecretAccessKey": "WJgRbJdIgDBXzaGvn4//Xe+1I79Uc4UALjhBUt8v",
        "SessionToken": "FwoGZXIvYXdzEGMaDHpXqFOSzWDzNvp7VCK7AQh/cMJ0LyTIpCOG/oOI7EE2PqJtBeITbtyy8sAzu8+ZlcdgWK1aNQuWEpF/KFKtqJhODVhAqGjeP7Gm+yiIYUhaKGrDX83cR8lCY/pYGABplHlHv40j1mh5xYuwhobz+Dl8qmER4j9V4bE3UUHYiNJ+GGcopGqonsYYH1z0obPsUYuVOHEZRqBw6lDXtmj+nVjHYZfvz7JBtIkwlD58QvZopSu1nVaovyb8SLqO2Ri8uQvbUQ1KJVhnVaYo5caQ/AUyLU50hyvUF/1xH2fNWNoKjeVc9Gx2AMpUDe1JdbaMAwH6q8+YqFqvmJO9Q6rOlA==",
        "Expiration": "2020-10-12T10:35:33Z"
    },
    "AssumedRoleUser": {
        "AssumedRoleId": "AROAY4D6UVCTS2CWA5LQV:AWSCLI-SessionOperator",
        "Arn": "arn:aws:sts::610150951079:assumed-role/OrganizationAccountAccessRole/AWSCLI-SessionOperator"
    }
}
```

You can then use these credentials to administer the <Production> account

```
export AWS_ACCESS_KEY_ID=ASIAY4D6UVCTZGT6R36E
export AWS_SECRET_ACCESS_KEY=WJgRbJdIgDBXzaGvn4//Xe+1I79Uc4UALjhBUt8v
export AWS_SESSION_TOKEN=FwoGZXIvYXdzEGMaDHpXqFOSzWDzNvp7VCK7AQh/cMJ0LyTIpCOG/oOI7EE2PqJtBeITbtyy8sAzu8+ZlcdgWK1aNQuWEpF/KFKtqJhODVhAqGjeP7Gm+yiIYUhaKGrDX83cR8lCY/pYGABplHlHv40j1mh5xYuwhobz+Dl8qmER4j9V4bE3UUHYiNJ+GGcopGqonsYYH1z0obPsUYuVOHEZRqBw6lDXtmj+nVjHYZfvz7JBtIkwlD58QvZopSu1nVaovyb8SLqO2Ri8uQvbUQ1KJVhnVaYo5caQ/AUyLU50hyvUF/1xH2fNWNoKjeVc9Gx2AMpUDe1JdbaMAwH6q8+YqFqvmJO9Q6rOlA==
aws sts get-caller-identity
{
    "UserId": "AROAY4D6UVCTS2CWA5LQV:AWSCLI-SessionOperator",
    "Account": "610150951079",
    "Arn": "arn:aws:sts::610150951079:assumed-role/OrganizationAccountAccessRole/AWSCLI-SessionDeveloper"
}
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name GroupsDevOps
```
