#!/bin/sh

sam build && \
    sam local invoke --event events/event.json CSV2DynamoDBFunction