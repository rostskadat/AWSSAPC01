#!/bin/sh

BucketName="$1"
[ ! -z "${BucketName}" ] || BucketName="sapc01-deploytoasg-bucket-bucket-kr34pi588pzi"

tar cvzf application.tgz appspec.yml ../../helpers/applications/flask-hello-world scripts etc

aws s3 cp application.tgz s3://${BucketName}/

sam build && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01"