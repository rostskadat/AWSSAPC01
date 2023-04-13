# Microservice

Showcase the use of ECS in a Microservice Architecture:
* Integration with Application LoadBalancer
* AutoScaling
* Service Directory integration

## Building

You first need to create the ECR Repository

```shell
sam build --template template-ecr.yaml
sam deploy --guided
``` 

Then you can build the docker image and upload it to the newly created ECR

```shell
cd flask-hello-world
docker build --tag <ContainerRepositoryUrl> .
$(aws --region eu-west-1 ecr get-login --no-include-email)
docker push <ContainerRepositoryUrl>
``` 

Once the docker image has been built and uploaded, you can launch the main stack (as the `TaskDefinition` use the newly created image).

```shell
sam build 
sam deploy --guided
``` 
## Testing the loadbalancer integration

You can simply curl the `RecordSetUrl` as this will transfer your request to the underlying ECS Service

```shell
curl -s <RecordSetUrl>
<!doctype html>

<html lang="en-us">
...
``` 

## Testing the service integration

You can see the service discovery by login in into the `EC2Instance` and opening the `PrivateDnsNamespaceUrl`

```shell
curl -s <PrivateDnsNamespaceUrl>
<!doctype html>

<html lang="en-us">
...

```


## Testing the autoscaling feature

You can see the autoscaling feature backed into the stack by launching the following small script that will continuously request the server.

```shell
while (true); do
    for i in $(seq 1 100); do 
        #while (true); do 
            curl -s <RecordSetUrl> | grep process_time | sed -E 's#.*<code>([^<]+)</code>.*#\1#' & 
        #done &
    done
done
``` 

You can then open the `DashboardUrl` to look at the scaling of your cluster

## SSM Parameter for latest AMI

Look at the [SamApplications/EC2Instance](../SamApplications/EC2Instance/README.md#ssm-parameter-for-latest-ami) for more details

## Updating the docker image

If you want to update the Docker Image and trigger the deployement of the new image you can

```shell
cd flask-hello-world
docker build --tag <ContainerRepositoryUrl> .
$(aws --region eu-west-1 ecr get-login --no-include-email)
docker push <ContainerRepositoryUrl>
aws ecs update-service --cluster <Cluster> --service <Service> --force-new-deployment
```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-Microservice
```
