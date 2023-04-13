#!/bin/bash

PublicIp="$1"
ActivationRegion="$2"

if [ -z "${PublicIp}" ] || [ -z "${ActivationRegion}" ]; then
    echo "Usage: $(basename $0) PublicIp ActivationRegion"
    echo "Both PublicIp and ActivationRegion are madatory"
    exit 1
fi

if redirect_url=$(curl -f -s -S -w '%{redirect_url}' "http://${PublicIp}/?activationRegion=${ActivationRegion}"); then
    activation_key_param=$(echo "${redirect_url}" | grep -oE 'activationKey=[A-Z0-9-]+')
    echo "${activation_key_param}" | cut -f2 -d=
else
    exit 1
fi
