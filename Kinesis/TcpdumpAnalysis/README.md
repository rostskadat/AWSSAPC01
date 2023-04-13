# Kinesis / TcpdumpAnalysis

Showcase the use of Kinesis services and KPL/KCL libraries. It simply create an EC2 Instance whose `tcpdump` trace is streamed to `Kinesis Data Firehose`. This stream is sent on to an S3 Bucket. Additionally a `Kinesis Stream` is also read and a `Kinesis Data Analytics` will analyse the stream content to search for the given string.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Once everything is up and running, you must first copy the helpers `helpers/tail2stream.py` to the instance:

```shell
scp -i .ssh/SAPC01.pem helpers/tail2stream.py ec2-user@<EC2Instance>:tail2stream.py
``` 

Then login into `EC2Instance` and start pumping into the `Stream`

```shell
python3 tail2stream.py --stream-name <Stream> --input-file /var/log/tcpdump.log --input-format '^(\S+)\s(\S+)\s(\S+\.\S+)\s>\s(\S+\.\S+):\s(.*)$'
```

This will stream data in CSV format to the given stream, once there they can be read by the Kinesis Data Analysis `Application`
If you run the SQL application you will see how the different IP are conecting to the `EC2Instance` over time...

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-TcpdumpAnalysis
```

## Details

*Author*: rostskadat
