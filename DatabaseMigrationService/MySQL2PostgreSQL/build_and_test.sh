#!/bin/sh

sam build && \
    sam local invoke --event events/event.json MySQL2PostgreSQLFunction