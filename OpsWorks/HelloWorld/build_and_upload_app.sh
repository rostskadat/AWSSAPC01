#!/bin/bash
STACK_NAME="SAPC01-OpsWorksHelloWorld-bucket"
BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `Bucket`].OutputValue' --output text)

TMP=$(mktemp)
tar -C node-mysql-crud-app -czf $TMP --exclude=node_modules .
aws s3 rm s3://${BUCKET_NAME}/node-mysql-crud-app.tar.gz
aws s3 cp $TMP s3://${BUCKET_NAME}/node-mysql-crud-app.tar.gz
rm -rf $TMP

