# BatchProcessing

This sample show case the batch processing of the Daily ZTF Alerts Tarball. For more information about ZTF, look [here](https://ztf.uw.edu/alerts/public/)

It specifically showcase the use of en ECS cluster with EC2 provisioning for batch processing (i.e. Task vs Service). It demonstrate: 
* Autoscaling 
* Integration with other AWS services (S3, DynamoDB, SQS, EFS)
* Athena AVRO parsing

Note: since we need to have extensible storage to download / decompress the the daily ZTF Alerts tarball, we use `EFS` instead of an `EBS` volume (the tarball varies between 7.4MB and 73GB). However we still use `S3` for long term storage, due to its cost advantage compared to `EFS` .


## References:

* [tutorial-cluster-auto-scaling-cli](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/tutorial-cluster-auto-scaling-cli.html)

## Building

You first need to create the ECR Repository

```shell
sam build --template template-ecr.yaml
sam deploy --guided
``` 

Then you can build the docker image and upload it to the newly created ECR

```shell
docker build --tag <ContainerRepositoryUrl> ../../helpers/dockers/download-daily-alerts
$(aws --region eu-west-1 ecr get-login --no-include-email)
docker push <ContainerRepositoryUrl>
``` 

You can investigate the different ECS-optimized AMI for your region with the following command:


Once the docker image has been built and uploaded, you can launch the main stack (as the `TaskDefinition` use the newly created image).

```shell
sam build 
sam deploy --guided
``` 

## AVRO Schema

They are available here:

* https://raw.githubusercontent.com/ZwickyTransientFacility/ztf-avro-alert/master/schema/alert.avsc
* https://raw.githubusercontent.com/ZwickyTransientFacility/ztf-avro-alert/master/schema/candidate.avsc
* https://raw.githubusercontent.com/ZwickyTransientFacility/ztf-avro-alert/master/schema/prv_candidate.avsc
* https://raw.githubusercontent.com/ZwickyTransientFacility/ztf-avro-alert/master/schema/cutout.avsc

They are necessary to create the Athena table that will be able to process the S3 avro files...

**BEWARE** You must use [avro-tools-1.8.2.jar](https://repo1.maven.org/maven2/org/apache/avro/avro-tools/1.8.2/avro-tools-1.8.2.jar) to generate the schema:

```
java -jar ../avro-tools-1.8.2.jar getschema 1351500626315015010.avro
```

After that you can kind of generate the corresponding table with a series of jq call:

```
cat queries/alerts.avsc | jq -r '.fields[4].type.fields[] | "\(.name):\(.type) COMMENT [[\(.doc)]],"'
```

## Triggering the download of a ZTF Alerts tarball

You can trigger the download of a specific ZTF Alerts tarball by invoking the command:

```shell
./helpers/trigger-download-daily-alerts.py \
    --cluster <Cluster> \
    --task-definition <DownloadTaskDefinition> \
    --container-name <DownloadContainerName> 
    --command "/download-daily-alerts/download-daily-alerts.sh --bucket <Bucket> --date 20190302"
```

Then you can check the status of the task by running the following command:

```shell 
aws ecs describe-tasks --tasks <TaskArn> --cluster <Cluster> --query "tasks[0].containers[? name == '<DownloadContainerName>' ].lastStatus" --output text
RUNNING
```

## Testing autoscaling 

If you try to trigger a second `Task` while the first one is running, and the memory required by the `TaskDefinition` is greater than the memory available in your registered ECS Instances, you will get a failure:

```shell
./helpers/trigger-download-daily-alerts.py \
    --cluster <Cluster> \
    --task-definition <DownloadTaskDefinition> \
    --container-name <DownloadContainerName> \
    --capacity-provider <CapacityProvider> \
    --command "/download-daily-alerts/download-daily-alerts.sh --bucket <Bucket> --date 20190302"
...
INFO | {'tasks': [], 'failures': [{'arn': 'arn:aws:ecs:eu-west-1:123456789012:container-instance/a36aefd295b14543b8b3329043aa1304', 'reason': 'RESOURCE:MEMORY'}], 'ResponseMetadata': {'RequestId': '99982660-61c7-4d4f-b2c8-4dfdb3eb4bc9', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '99982660-61c7-4d4f-b2c8-4dfdb3eb4bc9', 'content-type': 'application/x-amz-json-1.1', 'content-length': '149', 'date': 'Sat, 31 Oct 2020 10:00:20 GMT'}, 'RetryAttempts': 0}}
```

However in the background the `CapacityProvider` might already provisioning some instances and if you wait for them to enter service, you'll be able to resubmit your `Task`:

```shell
./helpers/trigger-download-daily-alerts.py \
    --cluster <Cluster> \
    --task-definition <DownloadTaskDefinition> \
    --container-name <DownloadContainerName> \
    --capacity-provider <CapacityProvider> \
    --command "/download-daily-alerts/download-daily-alerts.sh --bucket <Bucket> --date 20190302"
...
INFO | {'tasks': [{'attachments': [], 'availabilityZone': 'eu-west-1a', 'clusterArn': 'arn:aws:ecs:eu-west-1:123456789012:cluster/SAPC01-BatchProcessing-Cluster', 'containerInstanceArn': 'arn:aws:ecs:eu-west-1:123456789012:container-instance/SAPC01-BatchProcessing-Cluster/e271058622804ba4a9da4b60c301b526', 'containers': [{'containerArn': 'arn:aws:ecs:eu-west-1:123456789012:container/92148b90-a6ac-483a-b558-c96e09f88932', 'taskArn': 'arn:aws:ecs:eu-west-1:123456789012:task/SAPC01-BatchProcessing-Cluster/abf182b10cab42bdbeac4480e65e8406', 'name': 'ZTFAlertsDownload', 'image': '123456789012.dkr.ecr.eu-west-1.amazonaws.com/containerimagerepository-elgmbzygjkql:latest', 'lastStatus': 'PENDING', 'networkInterfaces': [], 'cpu': '0'}], 'cpu': '256', 'createdAt': datetime.datetime(2020, 10, 31, 15, 51, 46, 718000, tzinfo=tzlocal()), 'desiredStatus': 'RUNNING', 'group': 'family:ZTFAlerts', 'lastStatus': 'PENDING', 'launchType': 'EC2', 'memory': '512', 'overrides': {'containerOverrides': [{'name': 'ZTFAlertsDownload', 'command': ['/download-daily-alerts/download-daily-alerts.sh', '--bucket', 'sapc01-batchprocessing-bucket-1hlsfu07ggmgo', '--date', '20201023']}], 'inferenceAcceleratorOverrides': []}, 'tags': [], 'taskArn': 'arn:aws:ecs:eu-west-1:123456789012:task/SAPC01-BatchProcessing-Cluster/abf182b10cab42bdbeac4480e65e8406', 'taskDefinitionArn': 'arn:aws:ecs:eu-west-1:123456789012:task-definition/ZTFAlerts:7', 'version': 1}], 'failures': [], 'ResponseMetadata': {'RequestId': 'eaf71273-b158-4bc6-874b-5aa7af0cd2cf', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'eaf71273-b158-4bc6-874b-5aa7af0cd2cf', 'content-type': 'application/x-amz-json-1.1', 'content-length': '1366', 'date': 'Sat, 31 Oct 2020 14:51:45 GMT'}, 'RetryAttempts': 0}}
```

### If it does not scale

If it does not scale when you submit a new Task, it is probably related to a IAM profile for your ECS Container Instances that does not have the proper policy attached. You can diagnose such a problem by checking the attachement status for your Cluster `CapacityProvider`.

If you are missing the `AmazonEC2ContainerServiceforEC2Role`, `AmazonEC2ContainerServiceAutoscaleRole` IAM roles on your ECS Container Instances the attachment will fail and appear as:

```shell
aws ecs describe-clusters --clusters <Cluster> --include ATTACHMENTS
{    "clusters": [        {
            "clusterArn": "arn:aws:ecs:eu-west-1:123456789012:cluster/SAPC01-BatchProcessing-Cluster",
....
            "attachments": [                {
                    "id": "b736f344-3d79-41b3-b99a-05867f840f2e",
                    "status": "FAILED",
```

After addin the proper roles, you can see the attachment has the correct status:

```shell
aws ecs describe-clusters --clusters <Cluster> --include ATTACHMENTS
{    "clusters": [        {
            "clusterArn": "arn:aws:ecs:eu-west-1:123456789012:cluster/SAPC01-BatchProcessing-Cluster",
....
            "attachments": [                {
                    "id": "e5ec9b05-6772-4b1d-9277-fc2a24bad65e",
                    "status": "CREATED",
```

## Updating the docker image

If you want to update the Docker Image and trigger the deployement of the new image you can

```shell
cd flask-hello-world
docker build --tag <ContainerRepositoryUrl> .
$(aws --region eu-west-1 ecr get-login --no-include-email)
docker push <ContainerRepositoryUrl>
aws ecs update-service --cluster <Cluster> --service <Service> --force-new-deployment
```

## Jupyter Notebook can be used (AWS EMR)

Jupyter notebook can be used to analyse the data in S3...
But how to load the data from S3 into Jupyter. Maybe use `smart_open`

### Run the notebook locallly:


```shell
jupyter notebook
```


## SSM Parameter for latest AMI

Look at the [SamApplications/EC2Instance](../SamApplications/EC2Instance/README.md#ssm-parameter-for-latest-ami) for more details

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-BatchProcessing
```
