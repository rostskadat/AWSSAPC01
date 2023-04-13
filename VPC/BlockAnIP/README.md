# BlockAnIP

Showcase how to block an IP. It specifically demonstrate the difference between

* NACL + ALB (w/ security group)
* NACL + NLB (no security group)
* WAF Rule in ALB
* CloudFront + WAF Rule
* 

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json BlockAnIPFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-BlockAnIP
```
