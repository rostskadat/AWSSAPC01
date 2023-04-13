# AWSBatch / Overview

An overview of AWS Batch

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

Once the docker image has been built and uploaded, you can launch the main stack (as the `JobDefinition` use the newly created image).

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json OverviewFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-Overview
```

## Details

*Author*: rostskadat
