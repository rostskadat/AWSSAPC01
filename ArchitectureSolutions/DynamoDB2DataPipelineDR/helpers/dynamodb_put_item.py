#!/bin/env python3
"""
Put some items into DynamoDB
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

def dynamodb_put_item(args):
    current_count = int(client.scan(
        TableName=args.table_name,
        Select='COUNT')['Count'])
    table = dynamodb.Table(args.table_name)
    search_dir = os.path.abspath(os.path.dirname(__file__))
    logger.debug("Looking up template %s in %s", args.template, search_dir)
    template = Environment(loader=FileSystemLoader(searchpath=[search_dir])).get_template(args.template)
    with table.batch_writer() as batch:
        for count in range(args.count):
            context = {
                'id': 'u-%05d' % (current_count + count + 1),
                'username': Faker().name(), 
                'timestamp': (datetime.today() - timedelta(days=randint(1,100))).isoformat(),
                'age': randint(18, 85)
            }
            item = json.loads(template.render(context))
            batch.put_item(Item=item)
            logger.info("Added %s (%s)", context['username'], context['id'])

def parse_command_line():
    parser = ArgumentParser(prog='dynamodb_put_item', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument('--table-name', help='The Table name', required=True)
    parser.add_argument('--template', help='The json file containing the template data. Default to item_template.json.jinja2', required=False, default='item_template.json.jinja2')
    parser.add_argument('--count', type=int, help='The number of item to write', required=False, default=1)
    parser.set_defaults(func=dynamodb_put_item)
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
