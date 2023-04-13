#!/bin/bash

STACK_NAME="SAPC01-OpsWorksHelloWorld-bucket"

sam build --template template-bucket.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-bucket.toml

BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `Bucket`].OutputValue' --output text)

# berks generate spurious tmp directory that fails the deployment
#berks package --berksfile=cookbook/Berksfile cookbook.tgz
TMP=$(mktemp -d)
berks vendor --berksfile cookbook/Berksfile --delete $TMP
tar -C $TMP -czf $TMP.tar.gz .
aws s3 cp $TMP.tar.gz s3://${BUCKET_NAME}/cookbook.tar.gz
rm -rf $TMP

# not really building, but...
TMP=$(mktemp)
tar -C node-mysql-crud-app -czf $TMP.tar.gz .
aws s3 cp $TMP.tar.gz s3://${BUCKET_NAME}/node-mysql-crud-app.tar.gz
rm -rf $TMP

sam build --template template-opsworks.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-opsworks.toml \
    --parameter-overrides BucketName=${BUCKET_NAME} 

rm -f samconfig.toml
