#!/bin/sh

aws --region eu-west-1 cloudformation delete-stack --stack-name SAPC01-DRSolution
aws --region us-east-1 cloudformation delete-stack --stack-name SAPC01-DRSolution
