# S3 / ByteRangeFetch

Showcase the use of Byte Range when calling S3::GetObject API.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Then create a file, and upload it to the S3 `Bucket`

```shell
rm -f s3object
for i in $(seq 1 16); do printf "%-1024d" $i >> s3object; done
aws s3 cp s3object s3://<Bucket>
```

Then you can use the `s3_get_object.py`:

```shell
# Getting the first 1024 bytes
python3 s3_get_object.py --bucket <Bucket> --key s3object --dst-file s3object.remote --range "bytes=0-1023"
INFO | Found credentials in shared credentials file: ~/.aws/credentials
INFO | Written content to s3object.remote.
# Checking the length
wc -c s3object.remote 
1024 s3object.remote
# And the content
cat s3object.remote | sed -E 's/^(....).*/\1/
1   
```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ByteRangeFetch
```

## Details

*Author*: rostskadat
