#!/bin/sh

sam build && \
    sam local invoke --event events/event.json MgH2MEFunction