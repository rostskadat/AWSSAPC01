#!/bin/bash
STACK_NAME="SAPC01-RedisSession-bucket"
BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `Bucket`].OutputValue' --output text)

TMP=$(mktemp).zip
pushd node-app
zip -r --exclude=node_modules/* --exclude=target/* $TMP .
aws s3 rm s3://${BUCKET_NAME}/node-app.zip
aws s3 cp $TMP s3://${BUCKET_NAME}/node-app.zip
popd
cp $TMP node-app.zip
# rm -rf $TMP
