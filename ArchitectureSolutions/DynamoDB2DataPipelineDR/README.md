# ArchitectureSolutions / DynamoDB2DataPipelineDR

Showcase DR for DynamoDB using DataPipeline. 

It schedules an Export to S3 in the current region and after it finishes it schedule a import in the Recovery Region

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

First create some data:

```shell
./helpers/dynamodb_put_item.py --table-name <SourceTable> --count 200
```

Then wait 15 minutes for the `ExportPipeline` to execute...

Finally check that the items have been loaded in the `DRTable`:

```shell
./helpers/dynamodb_get_items.py --table-name <DRTable>
INFO:botocore.credentials:Found credentials in shared credentials file: ~/.aws/credentials
INFO:root:Retrieveed Item 0/200: {'username': 'Johnathan Calderon', 'id': 'u-00120', 'age': '23', 'timestamp': '2020-12-17T18:33:35.712952'}
INFO:root:Retrieveed Item 1/200: {'username': 'Danielle Gonzalez', 'id': 'u-00018', 'age': '49', 'timestamp': '2020-10-24T18:33:31.554726'}
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-DynamoDB2DataPipelineDR
```

## Details

*Author*: rostskadat
