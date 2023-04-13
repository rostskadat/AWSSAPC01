#!/bin/sh
# The LambdaExecution must be configured in your ~/.aws/credentials like this
#
# [LambdaExecution]
# role_arn = StreamFunctionRole.Arn
# source_profile = default
# 
sam build && \
    sam local invoke --event events/modify.json --env-vars environments\environment.json --profile LambdaExecution StreamFunction
