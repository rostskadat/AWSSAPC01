#!/bin/sh

sam build && \
    sam local invoke AWSVPCFunction --env-vars environments/AWSVPCFunction.json