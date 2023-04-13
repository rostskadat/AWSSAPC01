# SSLForNLB

This scenario showcases the use of an SSL certifiate with a TCP NetworkLoadBalancer. The EC2 Instance serves the SSL certificate. It retrieve the SSL private key from the SSM Parameter Store.

## Building

Since CloudFormation does not allow the creation of SecureString parameter, you must create the initial certificate secrets by hand.

*BEWARE*: The name `ParameterStoreSecureString` is important

```bash
aws ssm put-parameter --cli-input-json file://ssm-parameters/sapc01-nlb.key.json
aws ssm put-parameter --cli-input-json file://ssm-parameters/sapc01-nlb.cer.json
aws ssm put-parameter --cli-input-json file://ssm-parameters/dhparams.json
``` 

After that you can run the stack to get the stored parameter

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can analyse the certificate from the command line

```
curl -v -k https://<EC2InstancePublicDnsName>

curl -v -k https://<LoadBalancerDNSName>

curl -v https://<RecordSet>

```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-SSLForNLB
```
