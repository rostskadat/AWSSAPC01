#!/bin/bash
echo "Running $0 ..."
yum install -y python3 python3-pip
pip3 --disable-pip-version-check install gunicorn==20.0.4
pip3 --disable-pip-version-check install -r /flask-hello-world/requirements.txt
echo "$0 OK"