#!/bin/sh

sam build && \
    sam local invoke --event events/create-saml-provider.json CfIAMSamProviderFunction