# Redshift / DRSolution

Showcase a DR solution for an encrypted Redshift cluster.

## Building

You first have to create the resources in both the source region and the DR region

```shell
bash build_and_deploy.sh
``` 

* Then create a the `SnapshotCopyGrant` on the KMS key in the destination region `us-east-1` 

```shell
aws --region us-east-1 redshift create-snapshot-copy-grant --snapshot-copy-grant-name SAPGRANT --kms-key-id <Key>
{
    "SnapshotCopyGrant": {
        "SnapshotCopyGrantName": "sapgrant",
        "KmsKeyId": "arn:aws:kms:us-east-1:123456789012:key/e3910c54-cd12-4809-a47b-e0a29ff5f2d2",
        "Tags": []
    }
}
```

* Then configure the cluster to do cross-region snapshot:

```shell
aws redshift enable-snapshot-copy --destination-region us-east-1 --retention-period 1 --manual-snapshot-retention-period 1 --snapshot-copy-grant-name sapgrant --cluster-identifier <Cluster>
{
    "Cluster": {
        "ClusterIdentifier": "sapc01-drsolution-cluster-c1iev4bup0xh",
...
```

* Then create a snapshot of your cluster:

```shell
aws redshift create-cluster-snapshot --manual-snapshot-retention-period 1 --snapshot-identifier 'my-cross-region-snapshot' --cluster-identifier <Cluster>
{
    "Snapshot": {
        "SnapshotIdentifier": "my-cross-region-snapshot",
        "ClusterIdentifier": "sapc01-drsolution-cluster-c1iev4bup0xh",
        "SnapshotCreateTime": "2021-03-14T10:52:14.585Z",
...
```

## Testing

* First check that your snaphost is available in the destination region `us-east-1`

```shell
aws --region us-east-1 redshift describe-cluster-snapshots
{
    "Snapshots": [
        {
            "SnapshotIdentifier": "copy:my-cross-region-snapshot",
            "ClusterIdentifier": "sapc01-drsolution-cluster-c1iev4bup0xh",
            "SnapshotCreateTime": "2021-03-14T10:52:34.548Z",}
```

*Note* the new `SnapshotIdentifier`

* Then restaure the snaphost in the destination region `us-east-1`

```shell
aws --region us-east-1 redshift restore-from-cluster-snapshot --snapshot-identifier copy:my-cross-region-snapshot --cluster-identifier <Cluster> --node-type dc2.large --number-of-nodes 1
{
    "Cluster": {
        "ClusterIdentifier": "sapc01-drsolution-cluster-c1iev4bup0xh",
        "NodeType": "dc2.large",
        "ClusterStatus": "creating",
```

* Soon enough you will see the new cluster in the destination region `us-east-1`
```shell
aws --region us-east-1 redshift describe-clusters --cluster-identifier <Cluster> | jq -r '.Clusters[0].ClusterAvailabilityStatus'
Available
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws --region eu-west-1 cloudformation delete-stack --stack-name SAPC01-DRSolution
aws --region us-east-1 cloudformation delete-stack --stack-name SAPC01-DRSolution
```

## Details

*Author*: rostskadat
