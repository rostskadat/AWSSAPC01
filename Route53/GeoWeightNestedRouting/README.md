# Route53 / GeoWeightNestedRouting

Showcase a nested geolocation and weight base routing. While the top level routing is geolocation based, the routing policy within the region is weighted.

*NOTE*: the underlying resources are different S3 bucket to make things easier to test.

*NOTE*: that we only discriminate on whether the client's IP is in France or not.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

In order to test you will need to be able to fake a request originating from France (i.e. create an instance in `eu-west-3`)

On that instance you see either `L1W1` or `L1W2` (50% each)
In any other region you will see either `L2W1` or `L2W2` (50% each)

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-GeoWeightNestedRouting
```

## Details

*Author*: rostskadat
