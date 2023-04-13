# StepFunctions / Integrations

Showcase different integration patterns with StepFunctions. Basically it will download the ZTF Daily Alert tarball, uncompress it into an EFS FS, and sends an SNS notification with the number of files found

Ref: [concepts-service-integrations](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-service-integrations.html)

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

Then you can build the main stack

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

If you run your task from console, you must make sure to select the Plaform `1.4.0` and not `LATEST`

```shell

aws ecs run-task \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-b09099d4,subnet-f76b6581],securityGroups=[sg-e1435287],assignPublicIp=ENABLED}" \
    --platform-version 1.4.0 \
    --launch-type FARGATE \
    --cluster SAPC01-Integrations-Cluster-pvWvr8szzATg \
    --task-definition arn:aws:ecs:eu-west-1:123456789012:task-definition/ZTFAlerts:10 | jq '.tasks[0].taskArn'

aws ecs describe-tasks \
    --cluster SAPC01-Integrations-Cluster-pvWvr8szzATg \
    --tasks arn:aws:ecs:eu-west-1:123456789012:task/SAPC01-Integrations-Cluster-pvWvr8szzATg/452d4cd8d69849e3b1fa6c311f5433bc 
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-Integrations
aws cloudformation delete-stack --stack-name SAPC01-Integrations-ecr
```

## Details

*Author*: rostskadat
