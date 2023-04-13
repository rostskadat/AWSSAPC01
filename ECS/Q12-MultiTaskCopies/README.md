# ECSQ12

## Question

```
A solutions architect is designing a solution to run a containerized web application using Amazon Elastic Container Service (Amazon ECS). 
The solutions architect wants to minimize costs by running multiple copies of a task on each container instance.

Which solution for routing the requests will meet these requirements?

A. Configure an Application Load Balancer to distribute the requests using path-based routing.

B. Configure an Application Load Balancer to distribute the requests using dynamic host port mapping.

C. Configure an Amazon Route 53 alias record set to distribute the requests with a failover routing policy.

D. Configure an Amazon Route 53 alias record set to distribute the requests with a weighted routing policy.

```

## Answer

```
B
```

## Build the stack

```bash
sam build
sam deploy
```

## Build the docker image

```bash
$(aws ecr get-login --no-include-email)
docker build --rm -t <RepositoryUrl>:latest node-web-app-q12
docker push <RepositoryUrl>:latest
```

## Test it locally

```bash
?> docker run -p 49160:8080 -d <RepositoryUrl>:latest
7feae1a1bad41d6e6f23d174a65a97eb59d5ad27bcad2ae78b0f00c9b44fccfa
?> curl http://localhost:49160/
Hello World
?> docker rm --stop 7feae1a1bad41d6e6f23d174a65a97eb59d5ad27bcad2ae78b0f00c9b44fccfa
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name ECSQ12
```
