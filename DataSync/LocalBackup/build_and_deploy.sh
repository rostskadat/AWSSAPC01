#!/bin/sh

STACK_NAME="SAPC01-LocalBackup-agent"

sam build --template template-agent.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-agent.toml

AGENT_ADDRESS=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `EC2Instance`].OutputValue' --output text)
ACTIVATION_KEY=$(curl --silent --head "http://${AGENT_ADDRESS}/?gatewayType=SYNC&activationRegion=eu-west-1&endpointType=PUBLIC" | grep ^Location: | sed -E 's/.*activationKey=([^&]*).*/\1/')

ParameterOverridesOption=
ParameterOverridesValue=
if [ ! -z "${ACTIVATION_KEY}" ]; then
    # First time around
    echo "Activating Agent..."
    ParameterOverridesOption=--parameter-overrides
    ParameterOverridesValue="ActivationKey=${ACTIVATION_KEY}"
fi
sam build --template template-datasync.yaml && \
    sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" --config-file samconfig-datasync.toml \
    ${ParameterOverridesOption} ${ParameterOverridesValue}
