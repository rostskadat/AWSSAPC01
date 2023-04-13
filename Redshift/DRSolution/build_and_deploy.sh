#!/bin/sh

sam build --template template-cluster.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --config-file samconfig-cluster.toml --tags "PLATFORM=SAPC01"

sam build --template template-drregion.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --config-file samconfig-drregion.toml --tags "PLATFORM=SAPC01"

