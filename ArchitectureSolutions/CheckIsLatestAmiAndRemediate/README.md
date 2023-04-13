# Config / CheckIsLatestAmiAndRemediate

Showcase a Config rule to alert and remediate the use of unapproved AMI.
It creates 2 small instances, one with a Compliant AMI and the other one with a non-compliant AMI.
You must accept the subscription in order to receive the SNS notification by email.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

* Evaluate the `ConfigRule` and wait for it to complete

```shell
aws configservice start-config-rules-evaluation --config-rule-names <ConfigRule>
``` 

* After a while the compliance status should be refreshed:

```shell
aws configservice get-compliance-details-by-config-rule --config-rule-name <ConfigRule>
{
  "EvaluationResults": [
    {
      "EvaluationResultIdentifier": {
        "EvaluationResultQualifier": {
          "ConfigRuleName": "SAPC01-CheckIsLatestAmiAndRemediate-ConfigRule-1BSAXOIFITWGC",
          "ResourceType": "AWS::EC2::Instance",
          "ResourceId": "i-07df08ac62c798332"
        },
        "OrderingTimestamp": 1616434649
      },
      "ComplianceType": "COMPLIANT",
      "ResultRecordedTime": 1616434954.361,
      "ConfigRuleInvokedTime": 1616434953.508
    },
    {
      "EvaluationResultIdentifier": {
        "EvaluationResultQualifier": {
          "ConfigRuleName": "SAPC01-CheckIsLatestAmiAndRemediate-ConfigRule-1BSAXOIFITWGC",
          "ResourceType": "AWS::EC2::Instance",
          "ResourceId": "i-0f203f82ec43ad926"
        },
        "OrderingTimestamp": 1616435003
      },
      "ComplianceType": "NON_COMPLIANT",
      "ResultRecordedTime": 1616435018.707,
      "ConfigRuleInvokedTime": 1616435018.448
    }
  ]
}
```

* *Optional* Start the remediation process:

```shell
aws configservice start-remediation-execution --resource-keys resourceType=<ResourceType>,resourceId=<ResourceId> --config-rule-name <ConfigRule>
...
```

* You will then receive an email asking you to approve the action 

```shell
aws ssm send-automation-signal --automation-execution-id a02e203a-9782-4c7e-8883-65e6ca8ff53c --signal-type Approve --payload Comment="Approve from Cli"
```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-CheckIsLatestAmiAndRemediate
```

## Details

*Author*: rostskadat

## References 

* Schema for the different [resource-types](https://github.com/awslabs/aws-config-resource-schema/tree/master/config/properties/resource-types) as per the config events