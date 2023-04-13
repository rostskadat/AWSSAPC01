# WAF / ProtectResources

Showcase the use of WAF to protect a CloudFront distribution with backend S3 and ALB.

*BEWARE* This stack is created in the `us-east-1` region in order to be able to create the WebACL

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

### Get the log of your lambda function:

If you need to look at the CloudWatch logs of your Lambda@Edge function you can find out in which region they are located by running the following script

```shell
FUNCTION_NAME=<FunctionName>
for region in $(aws ec2 describe-regions | jq -r '.Regions[].RegionName'); do 
    for loggroup in $(aws logs describe-log-groups --log-group-name "/aws/lambda/us-east-1.${FUNCTION_NAME}" --region $region | jq -r '.logGroups[].logGroupName'); do
        echo ${region} ${loggroup}
    done
done
eu-west-2 /aws/lambda/us-east-1.SAPC01-ProtectCloudFront-LambdaAtEdgeFunction-6G80TVN6KSW
```

* Check that the resources are not accessible directly:

```shell
> curl -k <DirectStaticUrl>
<?xml version="1.0" encoding="UTF-8"?>
<Error><Code>AccessDenied</Code><Message>Access Denied</Message><RequestId>0KKHCTXCMFG8J5BJ</RequestId><HostId>PkWHvNn2XHopgLy1dQm4UGR8bu3E0SVtx1dbT5xybhRWVxbUJS/MTTD4yRZlBi5iYoKDQyJYIok=</HostId></Error>
> curl -k <DirectDynamicUrl>
{"message":"Forbidden"}
```

* Then check that the resources are accessibles through the CloudFront Distribution:

```shell
> curl -k <DistributionStaticUrl>
<!doctype html><html lang="en"><body>This is the static content page</body></html>
> curl -k <DistributionDynamicUrl>
<!doctype html><html lang='en'><body>This is the dynamic content page</body></html>
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ProtectResources
```

## Details

*Author*: rostskadat
