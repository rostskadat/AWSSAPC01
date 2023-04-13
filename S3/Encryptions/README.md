# Encryptions

Showcase the 4 different kind of S3 encryptions:

* SSE-S3: encrypts S3 objects using keys handled & managed by AWS
* SSE-KMS: leverage AWS Key Management Service to manage encryption keys
* SSE-C: when you want to manage your own encryption keys
* Client Side Encryption

You can start the Cloudtrail in order to look at the Encryption API Calls

## Building

You must first execute the Athena query to create the Athena DB to analyse the logs. And set the `AthenaDB` parameter accordingly

```sql
CREATE DATABASE s3_cloudtrail_events_db
```

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You first start the `Trail` and then put & retrieve an Object in that bucket
```
echo "Hello World" > /tmp/s3object
aws cloudtrail start-logging --name <Trail>
aws s3 cp /tmp/s3object s3://<SSES3Bucket>/
aws s3 cp /tmp/s3object s3://<SSEKMSBucket>/
./helpers/s3_put_object.py --src-file /tmp/s3object --bucket <SSECBucket> --key s3object --ssec fIKRpVw3zT6+Ca2plrukqcA9sBKNLnv26Mx4c0SOxa8=
./helpers/s3_get_object.py --dst-file /tmp/s3object --bucket <SSECBucket> --key s3object --ssec fIKRpVw3zT6+Ca2plrukqcA9sBKNLnv26Mx4c0SOxa8=
./helpers/s3_put_object.py --src-file /tmp/s3object --bucket <ClientSideEncryptionBucket> --key s3object.enc --cse <S3CMKKey>
aws s3 cp s3://<ClientSideEncryptionBucket>/ /tmp/s3object 
./helpers/s3_get_object.py --dst-file /tmp/s3object --bucket <ClientSideEncryptionBucket> --key s3object.enc --cse-cyphertext-blob <ciphertext_blob>
aws cloudtrail stop-logging --name <Trail>
# Wait for up to 15' for logs to appear...
```

## Monitoring with Athena

More info available [here](https://docs.aws.amazon.com/AmazonS3/latest/dev/cloudtrail-request-identification.html)


You can then execute the Athena queries:
* `CloudTrailLogCreateTable`
* `S3OperattionWithEncryption`

You might get something like this:

```csv
eventtime	eventname	bucketName	key	SSEApplied	responseelements
2020-10-22T16:45:14Z	PutObject	"sapc01-encryptions-sses3bucket-1uh713kxhzqeo"	"s3object"	"Default_SSE_S3"	{"x-amz-server-side-encryption":"AES256"}
2020-10-22T16:45:29Z	HeadObject	"sapc01-encryptions-sses3bucket-1uh713kxhzqeo"	"s3oject"		null
2020-10-22T16:45:57Z	ListObjects	"sapc01-encryptions-sses3bucket-1uh713kxhzqeo"			null
2020-10-22T16:46:08Z	HeadObject	"sapc01-encryptions-sses3bucket-1uh713kxhzqeo"	"s3object"		null
2020-10-22T16:46:08Z	GetObject	"sapc01-encryptions-sses3bucket-1uh713kxhzqeo"	"s3object"		null
2020-10-22T16:46:35Z	PutObject	"sapc01-encryptions-ssekmsbucket-1gmcp2x5p2zal"	"s3object"	"Default_SSE_KMS"	{"x-amz-server-side-encryption":"aws:kms","x-amz-server-side-encryption-aws-kms-key-id":"arn:aws:kms:eu-west-1:123456789012:key/13a4bb02-e753-4e2b-9180-8fd95828b3ee"}
2020-10-22T16:47:06Z	HeadObject	"sapc01-encryptions-ssekmsbucket-1gmcp2x5p2zal"	"s3object"		null
2020-10-22T16:47:07Z	GetObject	"sapc01-encryptions-ssekmsbucket-1gmcp2x5p2zal"	"s3object"		null
2020-10-22T16:48:25Z	PutObject	"sapc01-encryptions-ssecbucket-2v4p94c3ue01"	"s3object"	"SSE_C"	{"x-amz-server-side-encryption-customer-algorithm":"AES256"}
2020-10-22T16:49:07Z	GetObject	"sapc01-encryptions-ssecbucket-2v4p94c3ue01"	"s3object"		null

```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-Encryptions
```
