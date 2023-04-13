# Q02

## Question

```
You have been asked to migrate a 10 GB unencrypted EBS volume to an encrypted volume for security purposes. What are three key steps required as part of the migration?
 
A. pause the unencrypted instance
 
B. create a new encrypted volume of the same size and availability zone
 
C. create a new encrypted volume of the same size in any availability zone
 
D. start converter instance
 
E. shutdown and detach the unencrypted instance
```

## Answer

`E, B, D`

```bash
aws ec2 create-volume --availability-zone eu-west-1a --size 10 --no-encrypted | jq '.VolumeId'
volume_id=vol-063486f562017a44c
aws ec2 create-snapshot --volume-id $volume_id | jq '.SnapshotId'
snapshot_id=snap-0cfcc3810026b0127
aws ec2 create-volume --availability-zone eu-west-1b --encrypted --snapshot-id $snapshot_id | jq '.VolumeId'

aws ec2 delete-volume --volume-id vol-063486f562017a44c
aws ec2 delete-volume --volume-id vol-0c8ca3433ec9076de
aws ec2 delete-snapshot --snapshot-id snap-0cfcc3810026b0127

``` 
