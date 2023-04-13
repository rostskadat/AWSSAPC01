#!/bin/sh

rm -f samconfig.toml
cp samconfig-root.toml samconfig.toml
sam build --template template-root.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01"

rm -f samconfig.toml
cp samconfig-child.toml samconfig.toml
sam build --template template-child.yaml && \
    sam deploy --profile AF090536@123456789012 --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01"

rm -f samconfig.toml

