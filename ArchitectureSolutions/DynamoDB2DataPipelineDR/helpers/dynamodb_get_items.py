#!/bin/env python3
"""
Dump items from a DynamoDB Table
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime, timedelta
from faker import Faker
from functools import partial
from jinja2 import Environment, FileSystemLoader
from random import randint
import boto3
import json
import logging
import os
import sys

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')

def dynamodb_get_items(args):
    count = int(client.scan(
        TableName=args.table_name,
        Select='COUNT')['Count'])
    table = dynamodb.Table(args.table_name)
    response = table.scan()
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    i = 0
    for item in items:
        logger.info("Retrieveed Item %d/%d: %s", i, count, item)
        i += 1

def parse_command_line():
    parser = ArgumentParser(prog='dynamodb_get_items', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument('--table-name', help='The Table name', required=True)
    parser.add_argument('--count', type=int, help='The number of item to write', required=False, default=1)
    parser.set_defaults(func=dynamodb_get_items)
    return parser.parse_args()

def main():
    args = parse_command_line()
    try:
        if args.debug:
            logger.setLevel(logging.DEBUG)
        if args.profile:
            boto3.setup_default_session(profile_name=args.profile)
        return args.func(args)
    except Exception as e:
        logging.error(e, exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
