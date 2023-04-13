#!/bin/bash
STACK_NAME="SAPC01-OpsWorksHelloWorld-bucket"
BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `Bucket`].OutputValue' --output text)
# berks generate spurious tmp directory that fails the deployment
#berks package --berksfile=cookbook/Berksfile cookbook.tgz
TMP=$(mktemp -d)
berks vendor --berksfile cookbook/Berksfile --delete $TMP
tar -C $TMP -czf $TMP.tar.gz .
aws s3 rm s3://${BUCKET_NAME}/cookbook.tar.gz
aws s3 cp $TMP.tar.gz s3://${BUCKET_NAME}/cookbook.tar.gz
rm -rf $TMP
