# MigrateHadoop

## Question

A company is migrating an Apache Hadoop cluster from its data center to AWS. The cluster consists
of 60 VMware Linux virtual machines (VMs). During the migration cluster, downtime should be
minimized.

Which process will minimize downtime?

* A) Use the AWS Management Portal for vCenter to migrate the VMs to AWS as Amazon EC2 instances.
* B) Use AWS Server Migration Service (AWS SMS) to migrate the VMs to AWS as AMIs. Launch the cluster on AWS as Amazon EC2 instances from the migrated AMIs.
* C) Create Open Virtualization Archive (OVA) files of the VMs. Upload the OVA files to Amazon S3. Use VM Import/Export to create AMIs from the OVA files.  Launch the cluster on AWS as Amazon EC2 instances from the AMIs.
* D) Export the Hadoop Digital File System (HDFS) data from the VMs to a new Amazon Aurora DB cluster. Launch a new Hadoop cluster on Amazon EC2 instances. Import the data from the Aurora database to HDFS on the new cluster.

## Answer

`B`: AWS SMS uploads each VM incrementally, so it can upload the servers while the data center cluster is still
running. The data center cluster must be shut down prior to the final incremental sync of all the VMs only.

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Test locally

With SAM you can test your function locally:

```
sam local invoke --event events/events.json MigrateHadoopFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name MigrateHadoop
```
