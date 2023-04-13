#!/bin/sh

sam build && \
    sam local invoke --event events/APIGWAuthorizeAllow.json LambdaRequestAuthorizerFunction && \
    sam local invoke --event events/APIGWAuthorizeDeny.json LambdaRequestAuthorizerFunction    