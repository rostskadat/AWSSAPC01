#!/bin/sh

sam build && \
    sam local invoke --event events/create.json CfCloudWatchLogsResourcePolicy && \
    sam local invoke --event events/delete.json CfCloudWatchLogsResourcePolicy 