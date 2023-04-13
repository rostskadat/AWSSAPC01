# ArchitectureSolutions / S3TransferAccCloudFront

Showcase how to accelerate S3 upload / download:
* S3 Transfer Acceleration
* Cloudfront with PUT / POST for upload

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

First connect to the `EC2Instance` in your home region, create the big file and upload it to the `CentralBucket` bucket

```shell
ssh <EC2Instance>
?> dd if=/dev/urandom of=/tmp/BIG_RANDOM_FILE bs=1M count=1024
?> time aws s3 cp /tmp/BIG_RANDOM_FILE s3://<CentralBucket>
upload: ../../tmp/BIG_RANDOM_FILE to s3://sapc01-s3transferacccloudfront-centralbucket-ud4rsca7cyz7/BIG_RANDOM_FILE

real	0m9.364s
user	0m7.645s
sys	    0m5.925s
```

Then launch an instance in the `ap-southeast-2` region and connect to it:

```shell
ami=$(aws --region ap-southeast-2 ssm get-parameter --name /aws/service/ami-amazon-linux-latest/amzn-ami-hvm-x86_64-gp2 | jq -r .Parameter.Value)
aws --region ap-southeast-2 ec2 create-key-pair --key-name KEYPAIR_20210105 | jq -r .KeyMaterial > KEYPAIR_20210105.pem
aws --region ap-southeast-2 ec2 run-instances --image-id ${ami} --count 1 --instance-type t2.micro --key-name KEYPAIR_20210105
aws --region ap-southeast-2 ec2 describe-instances --instance-ids i-08a019fa188081c35
ssh -i KEYPAIR_20210105.pem ec2-13-236-178-224.ap-southeast-2.compute.amazonaws.com
?> 
```

Then download / upload a large file to the `CentralBucket` bucket:

* without Transfer Acceleration 

```shell
?> time aws s3 cp s3://<CentralBucket>/BIG_RANDOM_FILE /tmp/BIG_RANDOM_FILE 
download: s3://sapc01-s3transferacccloudfront-centralbucket-ud4rsca7cyz7/BIG_RANDOM_FILE to ../../tmp/BIG_RANDOM_FILE

real	0m51.699s
user	0m6.635s
sys	0m2.651s
?> time aws s3 cp /tmp/BIG_RANDOM_FILE s3://<CentralBucket>
upload: ../../tmp/BIG_RANDOM_FILE to s3://sapc01-s3transferacccloudfront-centralbucket-ud4rsca7cyz7/BIG_RANDOM_FILE

real	0m35.358s
user	0m7.348s
sys	0m2.196s
```

* with [Transfer Acceleration](https://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration.html#transfer-acceleration-getting-started). Note how the multipart upload of the `aws s3` API speed things up quite substantially!
```shell
?> aws s3api put-bucket-accelerate-configuration --bucket <CentralBucket> --accelerate-configuration Status=Enabled
?> time aws --region ap-southeast-2 --endpoint-url https://<CentralBucket>.s3-accelerate.amazonaws.com s3api get-object --bucket <CentralBucket> --key BIG_RANDOM_FILE /tmp/BIG_RANDOM_FILE
{
    "AcceptRanges": "bytes", 
    "ContentType": "binary/octet-stream", 
    "LastModified": "Wed, 06 Jan 2021 16:49:42 GMT", 
    "ContentLength": 1073741824, 
    "ETag": "\"98f734ecf6cdc1fb6e2318deefd2a70d-128\"", 
    "Metadata": {}
}

real	2m55.146s
user	0m4.773s
sys	0m2.549s

?> time aws --region ap-southeast-2 s3api put-object --bucket <CentralBucket> --key BIG_RANDOM_FILE --body /tmp/BIG_RANDOM_FILE
{
    "ETag": "\"bcd0578958160cd02664d278dbf94939\""
}

real	2m51.350s
user	0m8.083s
sys	0m2.190s
?> time aws --region ap-southeast-2 --endpoint-url https://<CentralBucket>.s3-accelerate.amazonaws.com s3api put-object --bucket <CentralBucket> --key BIG_RANDOM_FILE --body /tmp/BIG_RANDOM_FILE
{
    "ETag": "\"bcd0578958160cd02664d278dbf94939\""
}

real	2m38.789s
user	0m6.661s
sys	0m0.822s

?> aws s3api put-bucket-accelerate-configuration --bucket <CentralBucket> --accelerate-configuration Status=Suspended

```

* through Cloudfront

```shell
?> time curl https://<S3DistributionDomainName>/BIG_RANDOM_FILE --output /tmp/BIG_RANDOM_FILE
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 1024M  100 1024M    0     0  18.1M      0  0:00:56  0:00:56 --:--:-- 18.3M

real	0m56.550s
user	0m1.313s
sys	0m2.372s
?> time curl -X POST --data-binary @/tmp/BIG_RANDOM_FILE https://<S3DistributionDomainName>/BIG_RANDOM_FILE

```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-S3TransferAccCloudFront
aws --region ap-southeast-2 ec2 delete-key-pair --key-name KEYPAIR_20210105
```

## Details

*Author*: rostskadat
