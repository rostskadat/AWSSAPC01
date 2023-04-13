#!/bin/bash

repository_url=$1
if [ -z "${repository_url}" ]; then
    ECR_STACK_NAME=SAPC01-OpenId-ecr
    repository_url=$(aws cloudformation describe-stacks --stack-name ${ECR_STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `ContainerRepositoryUrl`].OutputValue' --output text)
fi
$(aws ecr get-login --no-include-email)
docker build -t "${repository_url}:latest" oidc-server
docker push "${repository_url}:latest"
