#!/bin/sh

STACK_NAME="SAPC01-RedisSession-bucket"

sam build --template template-bucket.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-bucket.toml

BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `Bucket`].OutputValue' --output text)

# not really building, but...
TMP=$(mktemp).zip
pushd node-app
zip -r --exclude=node_modules/* $TMP .
aws s3 cp $TMP s3://${BUCKET_NAME}/node-app.zip
rm -rf $TMP
popd

sam build --template template-app.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-app.toml \
    --parameter-overrides BucketName=${BUCKET_NAME} 



