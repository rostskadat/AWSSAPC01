#!/bin/sh

STACK_NAME="SAPC01-Architecture-bucket"

sam build --template template-bucket.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-bucket.toml

BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `Bucket`].OutputValue' --output text)

# not really building, but...
bash flask-hello-world/create_zip_for_eb.sh
aws s3 cp flask-hello-world/build/flask-hello-world.zip s3://${BUCKET_NAME}
rm -rf flask-hello-world/build/flask-hello-world.zip

sam build --template template-app.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-app.toml \
    --parameter-overrides BucketName=${BUCKET_NAME} 
