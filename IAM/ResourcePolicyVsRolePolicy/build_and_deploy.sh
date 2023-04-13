#!/bin/sh

# This will create the necessary resources in the Linked Account
Account="$1"
if [ -z "${Account}" ]; then
    echo "Usage $(basename $0) ( master | linked )"
    exit 1
elif [ "${Account}" = "master" ]; then
    Profile="n090536"
elif [ "${Account}" = "linked" ]; then
    Profile="AF090536-CfAccount"
else
    echo "Usage $(basename $0) ( master | linked )"
    exit 1
fi

rm -f samconfig.toml
cp "samconfig-${Account}-account.toml" samconfig.toml
sam build --profile "${Profile}" --template-file "template-${Account}-account.yaml" && \
    sam deploy --profile "${Profile}" --template-file "template-${Account}-account.yaml" \
        --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01"
rm -f samconfig.toml
