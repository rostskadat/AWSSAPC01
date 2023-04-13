# ELBQ20

## Question

```
A company currently runs its website on Amazon EC2 instances behind an Application Load Balancer that is configured as the origin for an Amazon CloudFront distribution. 
The company wants to protect against cross-site scripting and SQL injection attacks.

Which approach should a solutions architect recommend to meet these requirements?

A. Enable AWS Shield Advanced and list the CloudFront distribution as a protected resource.

B. Define an AWS Firewall Manager Shield Advanced policy that blocks cross-site scripting and SQL injection attacks.

C. Set up AWS WAF on the CloudFront distribution with conditions and rules that block cross-site scripting and SQL injection attacks.

D. Deploy AWS Firewall Manager on the EC2 instances and create conditions and rules that block cross-site scripting and SQL injection attacks.

```

## Answer

`C`

## Building the stack

*Note*: part of the WAF Stack must be created first and in the `us-east-1` region...

```bash
sam build --template template-waf.yml
sam deploy --region us-east-1 --stack-name ELBQ20WAF

sam build --template template.yml
sam deploy --region eu-west-1
```

## Testing the stack

First open the `LoadBalancerDNSName` and the CloudFront `DistributionDomainName`. 

*Note* the protocol and the fact that the hostname alternate...

```bash
?> while (true); do curl -s -k -H 'Content: No-cache' http://<LoadBalancerDNSName>/ ; sleep 1 ; done
<html><body>public-hostname: ec2-52-51-237-214.eu-west-1.compute.amazonaws.com</body></html>
<html><body>public-hostname: ec2-52-212-145-51.eu-west-1.compute.amazonaws.com</body></html>
?> while (true); do curl -s -k -H 'Content: No-cache' http://<DistributionDomainName>/ ; sleep 1 ; done
<html><body>public-hostname: ec2-52-212-145-51.eu-west-1.compute.amazonaws.com</body></html>
<html><body>public-hostname: ec2-52-212-145-51.eu-west-1.compute.amazonaws.com</body></html>
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws s3 rm --recursive <Bucket>
aws cloudformation delete-stack --stack-name ELBQ20
aws cloudformation delete-stack --stack-name ELBQ20WAF --region us-east-1
```
