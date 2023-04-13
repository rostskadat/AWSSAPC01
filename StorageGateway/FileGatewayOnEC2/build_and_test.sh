#!/bin/sh

sam build && \
    sam local invoke --event events/event.json FileGatewayOnEC2Function