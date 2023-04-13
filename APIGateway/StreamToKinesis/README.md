# ApiGateway / StreamToKinesis

Showcase streaming call to an API Gateway to a Kinesis Stream and process them later. IOT stuff

Heavily influenced by [integrating-api-with-aws-services-kinesis](https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-kinesis.html)

It also showcase how to transform the incoming request by adding the `StreamName`

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Send data from the smart meter:

```shell
curl -X POST -H "Content-Type: application/json" --data @resources/smart_meter_message.json <ApiFriendlyUrl>
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-StreamToKinesis
```

## Details

*Author*: rostskadat
