# AWSConfig

Showcase the use of AWS Config, with an autoremediation that sends an email in order to add the missing tag

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

* Remove the Tag `PLATFORM` from the nstance `InstanceId`

```shell
aws ec2 delete-tags --resources <InstanceId> --tags Key=PLATFORM
```

* Re-evaluate the `ConfigRuleForEC2ResourceTags` 

```shell
aws configservice start-config-rules-evaluation --config-rule-names <ConfigRuleForEC2ResourceTags>
```

* You can see the `InstanceId` appear in the list of non-compliant resources

```shell
aws configservice describe-compliance-by-config-rule --config-rule-names <ConfigRuleForEC2ResourceTags>
```

* Obtain more details with:

```shell
aws configservice get-compliance-details-by-config-rule --compliance-types NON_COMPLIANT --config-rule-name <ConfigRuleForEC2ResourceTags> \
--query 'EvaluationResults[?@.EvaluationResultIdentifier.EvaluationResultQualifier.ResourceType == `AWS::EC2::Instance`].EvaluationResultIdentifier.EvaluationResultQualifier.ResourceId'
```

* Describe the remediation configurations:

```shell
aws configservice describe-remediation-configurations --config-rule-names <ConfigRuleForEC2ResourceTags>
{
    "RemediationConfigurations": [{
        "ConfigRuleName": "SAPC01-AWSConfig-ConfigRuleForEC2ResourceTags-1LCGBQZENBUPE",
```

* And finally remediate the problem:

```shell
aws configservice start-remediation-execution --config-rule-name <ConfigRuleForEC2ResourceTags> --resource-keys resourceType=AWS::EC2::Instance,resourceId=<InstanceId>
{
    "FailedItems": []
}
```

You should have received an email.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-AWSConfig
```
