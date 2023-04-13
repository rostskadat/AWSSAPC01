# DynamoDB,ElasticSearch / DynamoDB2ElasticSearch

Showcase the use of DynamoDB, Stream and ElasticSearch together

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You first need to load some data

```shell
?> ..\..\helpers\csv2dynamodb.py --table-name <Table> --filename ..\..\helpers\resources\funds.csv --schema ..\..\helpers\resources\funds-schema.json --table-key-source ISIN_FONDO
```

In order to test the `StreamFunction` locally you must ajust your `~/.aws/credentials` to specify the Role Arn used with the specific profile 

```ini
[LambdaExecution]
role_arn = StreamFunctionRole.Arn
source_profile = default
```

After that you need to map the `StreamFunctionRole` to access the system:

* in you elastic search console, tab overview, click in the Kibana link
* Once logged in Kibana click in the security menu option
* Go to Role Mapping option
* Select role `all_access` and click *Mapped Users*
* Add the `StreamFunctionRole` ARN 

Then you can test the `StreamFunction` locally:

```shell
sam local invoke --event events/event.json --env-vars environments\environment.json --profile LambdaExecution StreamFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-DynamoDB2ElasticSearch
```

## Details

*Author*: rostskadat

## Reference

* [es-request-signing](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-request-signing.html#es-request-signing-python)