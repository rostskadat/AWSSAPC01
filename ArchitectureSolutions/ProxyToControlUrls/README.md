# VPC / ProxyToControlUrls

Showcase an architecture where only a specific set of URL are allowed to be accessed by instances.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json ProxyToControlUrlsFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ProxyToControlUrls
```

## Details

*Author*: rostskadat
