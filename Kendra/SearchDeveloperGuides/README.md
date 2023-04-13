# Kendra / SearchDeveloperGuides

Showcase a simple Kendra Index to search Developer Guides

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You will need to upload some `pdf` Developer Guides

```shell
curl -# https://docs.aws.amazon.com/IAM/latest/UserGuide/iam-ug.pdf -o /tmp/iam-ug.pdf 
curl -# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-ug.pdf -o /tmp/ec2-ug.pdf 
curl -# https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-userguide.pdf -o /tmp/s3-userguide.pdf 
curl -# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-ug.pdf -o /tmp/rds-ug.pdf 
find /tmp -type f -name '*.pdf' -exec aws s3 cp {} s3://<Bucket> \;
```

Once uploaded you'll need to trigger the indexing process

```shell
aws kendra start-data-source-sync-job --id <DataSource> --index-id <Index>
...
while (true); do aws kendra list-data-source-sync-jobs --id <DataSource> --index-id <Index> | jq -r '.History[0].Status' ; sleep 10 ; done
SYNCING_INDEXING
...
SUCCEEDED
```

Then you'll be able to query the given index using the [search_kendra_index.py](helpers/search_kendra_index.py)

```shell
./helpers/search_kendra_index.py --index-id <Index> --query-text "Are search hits automatically highlighted?"
-------------------
Type: ANSWER
By default, requests
are processed with the simple query parser. You can specify options for the selected parser, filter and
sort the results, and browse the configured facets. The search hits are automatically highlighted in
...
```

You can also use the `CustomDataSource` to upload your own documents using the [index_local_documents.py](helpers/index_local_documents.py)

```shell
./helpers/index_local_documents.py --index-id <Index> --datasource-id <CustomDataSource> --root-dir ../../helpers/resources/
```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-SearchDeveloperGuides
```

## Details

*Author*: rostskadat
