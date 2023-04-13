# Glue / ETL2Athena

Showcase AWS Glue. It loads a CSV file into Glue, transform the content and output the result in S3. Furthermore an Athena query is available for querying the resulting data.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Before testing you'll need to upload the sample data to the `InputBucket`:

```shell
aws s3 cp ..\..\helpers\resources\LOAD00000001.csv s3://<InputBucket>/LOAD00000001.csv
```

You can then start the `Crawler` to get create the table 

```shell
aws glue start-crawler --name <Crawler>
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ETL2Athena
```

## Details

*Author*: rostskadat
