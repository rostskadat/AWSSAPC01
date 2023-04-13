#!/bin/bash

BASE_DIR=$(dirname $0)
TEMPLATE_DIR=${BASE_DIR}/template/basic

[ ! -d "${TEMPLATE_DIR}" ] && echo "This script must be run within the SAPC01 project directory" && exit 1

Service="$1"
Sample="$2"
Description="$3"

if [ -z "${Service}" ] || [ -z "${Sample}" ]; then
    echo "Usage: $(basename $0) Service Sample"
    echo "Both service and sample are madatory"
    exit 1
fi
[ -z "${Description}" ] && Description="Short Description about ${Service} / ${Sample}"

    #--no-interactive \
sam init --location template/basic \
    --output-dir ${BASE_DIR}/${Service} \
    --name ${Sample} \
    --extra-context "{ \"service\": \"${Service}\", \"author\": \"$(whoami)\", \"description\": \"${Description}\" }"
