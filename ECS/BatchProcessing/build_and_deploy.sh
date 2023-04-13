#!/bin/sh

sam build --template template-ecr.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-ecr.toml

ECR_STACK_NAME=SAPC01-BatchProcessing-ecr

container_repository_url=$(aws cloudformation describe-stacks --stack-name ${ECR_STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `ContainerRepositoryUrl`].OutputValue' --output text)
container_image_repository=$(aws cloudformation describe-stacks --stack-name ${ECR_STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `ContainerImageRepository`].OutputValue' --output text)

docker build --tag ${container_image_repository} ../../helpers/dockers/download-daily-alerts
$(aws --region eu-west-1 ecr get-login --no-include-email)
docker push ${container_image_repository}

sam build --template template.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" \
        --config-file samconfig.toml --parameter-overrides "DownloadImageRepository=${container_image_repository}"