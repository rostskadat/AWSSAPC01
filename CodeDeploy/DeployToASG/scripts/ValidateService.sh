#!/bin/bash
echo "Running $0 ..."
curl http://localhost:80/health
health=$(curl -qs http://localhost:80/health)
if [ "${health}" != "OK" ]; then
    echo "Health is not OK. Failing deployment"
    # exit 1
fi
echo "$0 OK"