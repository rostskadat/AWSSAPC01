#!/bin/bash

sam build --template template-ecr.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-ecr.toml

ECR_STACK_NAME=SAPC01-Saml2Sp-ecr

container_repository_url=$(aws cloudformation describe-stacks --stack-name ${ECR_STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `ContainerRepositoryUrl`].OutputValue' --output text)
container_image_repository=$(aws cloudformation describe-stacks --stack-name ${ECR_STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `ContainerImageRepository`].OutputValue' --output text)

cat <<EOF
**********************************
MAKE SURE TO KEEP THE URLs IN SYNC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
EOF
pushd applications > /dev/null
bash ./build.sh "${container_repository_url}"
popd

sam build --template template.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" \
        --config-file samconfig.toml --parameter-overrides "ContainerImageRepository=${container_image_repository}"