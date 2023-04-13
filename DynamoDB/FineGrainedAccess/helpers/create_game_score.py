#!/bin/env python3
"""
Create some game score
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from faker import Faker
from random import randint
from datetime import datetime, timedelta
import gettext
import logging
import sys
import boto3
import json
import os
from jinja2 import Environment, FileSystemLoader
import requests

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')


def create_game_score(args):
    identity = None
    if args.identity == 'ip':
        try:
            identity = requests.get(
                "http://checkip.amazonaws.com/").text.replace("\n", "")
        except requests.RequestException as e:
            # Send some context about this error to Lambda Logs
            logging.error(e)
            raise e
    else:
        identity = args.identity
    table = dynamodb.Table(args.table_name)
    template = Environment(loader=FileSystemLoader(
        searchpath=[os.path.dirname(__file__)])).get_template(args.template)
    context = {
        'id': identity,
        'score': randint(0, 100),
        'timestamp': (datetime.today() - timedelta(seconds=randint(1, 31536000))).isoformat(),
    }
    item = json.loads(template.render(context))
    table.put_item(Item=item)
    logger.info("Successfully put Item '%s' in Table '%s", identity, args.table_name)


def parse_command_line():
    parser = ArgumentParser(prog='create_game_score',
                            description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument('--table-name', help='The Table name', required=True)
    parser.add_argument('--identity', help='The Identity (either ip or the AWS Access Key', required=False, default='ip')
    parser.add_argument('--template', help='The json file containing the game template data. Default to game_score.json.jinja2',
                        required=False, default='game_score.json.jinja2')
    parser.set_defaults(func=create_game_score)
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
