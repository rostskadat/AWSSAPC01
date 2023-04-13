#!/bin/sh

sam build && \
    sam local invoke --event events/APIGWAuthorizeAllow.json LambdaTokenAuthorizerFunction