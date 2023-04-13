# StorageGateway / FileGatewayOnEC2

Showcase a Storage Gateway on EC2 with an EC2 Client. 
Create an NFS File Share and mount it on a Client.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

*BEWARE* This is the part that is the most prone to failure. Make sure your instance has stabilzed before creating the Storage Gateway...

You can create the Storage Gateway from the [console](https://eu-west-1.console.aws.amazon.com/storagegateway/create/gateway?region=eu-west-1) as there are no Storage Gateway resources in CloudFormation :(

*or* you can do it through the command line:

1. Get the activation key by login into the `FileGatewayInstance`:

```shell
?> ssh admin@<FileGatewayInstance>
...	
	Get activation key
	
	Enter region (e.g. us-east-1): eu-west-1
	
	Select network type:
	 1: Public
	 2: VPC (PrivateLink)
	
	Press "x" to exit
	
	Select network type or exit: 2
	
	VPC endpoint (DNS/IP): <VPCEndpointRegionalPublicDNS>
	
	Activation key: FSEJ6-2FVI2-9THOC-PUUF0-DC2TD
	
	Press Return to Continue
``` 

2. Active the gateway and create a AWS StorageGateway `FileGateway` (*BEWARE* the `--gateway-type` is `FILE_S3`)

```shell
?> aws storagegateway activate-gateway \
	--gateway-name FileGatewayInstance --gateway-timezone GMT+1:00 --gateway-region eu-west-1 --gateway-type FILE_S3 \
	--activation-key <ActivationKey> 
```

3. After that you need to add cache and create the fileshare

```shell
?> aws storagegateway list-local-disks \
	--gateway-arn <GatewayArn> | jq '.Disks[].DiskId'
?> aws storagegateway add-cache --disk-ids /dev/xvdb \
	--gateway-arn <GatewayArn>
?> aws storagegateway create-nfs-file-share --client-token FileGatewayInstance \
	--role <FileGatewayRole> \
	--location-arn <BucketArn>/nfs-file-share/ \
	--gateway-arn <GatewayArn>
```

You can then open the client and moount te given file share:

```shell
?> ssh ec2-user@<Client>
...
mount -t nfs -o nolock,hard <FileGatewayInstance>:/<Bucket> /mnt
# And then write some file that you will see appear in the S3 bucket:
for i in $(seq 1 10); do dd if=/dev/urandom of=/mnt/$(date +'%Y%m%d')-random.$(printf "%02d" $i) bs=1024 count=$(expr 1024 \* 1024); done
...
# and then check that they are in S3:
aws s3 ls s3://<Bucket>/nf-file-share/
2021-03-05 12:17:08 1073741824 20210305-random.01
...
```

4. Do the same with the `CachedGateway` (*BEWARE* the `--gateway-type` is `CACHED `)

```shell
?> aws storagegateway activate-gateway \
	--gateway-name CachedGatewayInstance --gateway-timezone GMT+1:00 --gateway-region eu-west-1 --gateway-type CACHED \
	--activation-key <ActivationKey> 
?> aws storagegateway list-local-disks \
	--gateway-arn <GatewayArn> | jq '.Disks[].DiskId'
?> aws storagegateway add-cache --disk-ids /dev/xvdb \
	--gateway-arn <GatewayArn>
?> aws storagegateway add-upload-buffer --disk-ids /dev/xvdc \
	--gateway-arn <GatewayArn>
?> aws storagegateway  describe-gateway-information \
	--gateway-arn <GatewayArn> | jq '.GatewayNetworkInterfaces[0].Ipv4Address'
?> aws storagegateway create-cached-iscsi-volume --client-token CachedGatewayInstance --volume-size-in-bytes $(expr 1024 \* 1024 \* 1024 \* 100) --target-name target-iscsi \
	--network-interface-id <Ipv4Address> \
	--gateway-arn <GatewayArn>
{
    "VolumeARN": "arn:aws:storagegateway:eu-west-1:123456789012:gateway/sgw-5129C938/volume/vol-07F38431B92233B6A",
    "TargetARN": "arn:aws:storagegateway:eu-west-1:123456789012:gateway/sgw-5129C938/target/iqn.1997-05.com.amazon:target-iscsi"
}
```

### Testing a iScsi Volume from the VolumeGateway

As per the [initiator-connection-common](https://docs.aws.amazon.com/storagegateway/latest/userguide/initiator-connection-common.html#ConfiguringiSCSIClientInitiatorRedHatClient) and also [CHAP Authentication](https://docs.aws.amazon.com/storagegateway/latest/userguide/initiator-connection-common.html#ConfiguringiSCSIClientInitiatorCHAP)

Log onto the `Client`

```shell
?> yum install -y iscsi-initiator-utils
?> systemctl enable iscsid
?> systemctl start iscsid
?> systemctl status iscsid
iscsid.service - Open-iSCSI
   Loaded: loaded (/usr/lib/systemd/system/iscsid.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2021-01-11 09:17:01 UTC; 5min ago
...
?> /sbin/iscsiadm --mode discovery --type sendtargets --portal <CachedGatewayInstance>:3260
10.0.3.122:3260,1 iqn.1997-05.com.amazon:target-iscsi
?> /sbin/iscsiadm --mode node --targetname iqn.1997-05.com.amazon:target-iscsi --portal <CachedGatewayInstance>:3260,1 --login
Logging in to [iface: default, target: iqn.1997-05.com.amazon:target-iscsi, portal: 10.0.3.122,3260] (multiple)
Login to [iface: default, target: iqn.1997-05.com.amazon:target-iscsi, portal: 10.0.3.122,3260] successful.
```

You then need to format and mount the volume:

```shell
fdisk /dev/sda
mkfs.ext3 /dev/sda1
mount /dev/sda1 /mnt_volume
for i in $(seq 1 10); do dd if=/dev/urandom of=/mnt_volume/$(date +'%Y%m%d')-random.$(printf "%02d" $i) bs=1024 count=$(expr 1024 \* 1024); done
...

```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-FileGatewayOnEC2
```

## Details

*Author*: rostskadat
