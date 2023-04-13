# SSLForALB

This scenario showcases the use of an SSL certifiate with an Application LoadBalancer. The ALB serves the SSL certificate from ACM.

## Building

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can analyse the certificate from the command line

```
curl -v http://<EC2InstancePublicDnsName>

curl -v -k https://<LoadBalancerDNSName>

curl -v https://<RecordSet>

```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-SSLForALB
```
