# S3TransferAcceleration 

## Build the stack

```bash
?> sam build
?> sam deploy
```

## Test 

Start an instance in Sydney and upload a file to the bucket using the specific endpoint:

```bash
?> S3TxObject.py --bucket-name s3transferacceleration-sourcebucket-ykowyllcizli --key normal.bin put
...
INFO  | S3TxObject:84 | PUT s3://s3transferacceleration-sourcebucket-ykowyllcizli/normal.bin took 48.20324s
?> S3TxObject.py --bucket-name s3transferacceleration-sourcebucket-ykowyllcizli --key normal.bin --use-accelerate-endpoint put
...
INFO  | S3TxObject:84 | PUT s3://s3transferacceleration-sourcebucket-ykowyllcizli/normal.bin took 26.88169s
```

## Delete the stack

```bash
?> aws s3 rm --recursive s3://s3transferacceleration-sourcebucket-ykowyllcizli
?> aws cloudformation delete-stack --stack-name S3TransferAcceleration
```


