# ServiceControlPolicy

This sample showcases the use of an SCP and Tag policy on a linked account.

## Building

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Once the policy is attached to an account of your choice, all EMR API calls will be denied:

```shell
aws --profile OrganizationAccountAccessRole@662408148766 emr list-clusters

An error occurred (AccessDeniedException) when calling the ListClusters operation: User: arn:aws:sts::662408148766:assumed-role/OrganizationAccountAccessRole/botocore-session-1620058525 is not authorized to perform: elasticmapreduce:ListClusters on resource: * with an explicit deny
```

Further more a tag policy will be applied forcing resource to be tagged with the permitted values:

As per [tag-policies-enforcement](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies-enforcement.html)

```shell
aws --profile OrganizationAccountAccessRole@662408148766 ec2 create-security-group \
    --description "Failed to create SG because of invalid tag" \
    --group-name INVALID-TAG-SG \
    --tag-specifications "ResourceType=security-group,Tags=[{Key=PLATFORM,Value=INVALID_VALUE}]"

An error occurred (TagPolicyViolation) when calling the CreateSecurityGroup operation: The tag policy does not allow the specified value for the following tag key: 'PLATFORM'.
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-ServiceControlPolicy
```
