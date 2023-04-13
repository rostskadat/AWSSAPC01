#!/bin/sh

sam build --template template-ecr.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-ecr.toml

ECR_STACK_NAME=SAPC01-Microservice-ecr

container_repository_url=$(aws cloudformation describe-stacks --stack-name ${ECR_STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `ContainerRepositoryUrl`].OutputValue' --output text)
container_image_repository=$(aws cloudformation describe-stacks --stack-name ${ECR_STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `ContainerImageRepository`].OutputValue' --output text)

pushd flask-hello-world
docker build --tag ${container_image_repository} .
$(aws --region eu-west-1 ecr get-login --no-include-email)
docker push ${container_image_repository}
popd

sam build --template template.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" \
        --config-file samconfig.toml --parameter-overrides "ContainerImageRepository=${container_image_repository}"