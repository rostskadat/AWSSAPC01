# VPCEndpoint

This sample showcases different Lambda deployments:
* AWS owned VPC
* Private VPC Deployment
And in each case the implication to access resources that are with our own VPC..
* RDS instance without Public IP.
* Use of a VPCEndoint for DynamoDB

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

```shell
curl -s <ApiUrl>/AWSVPCFunction | jq
{
  "url": {
    "status": "fulfilled",
    "value": 290146
  },
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-VPCEndpoint
```
