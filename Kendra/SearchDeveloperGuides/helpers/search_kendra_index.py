#!/usr/bin/env python
"""
Send a query to the Kendra Index
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from functools import partial
from jinja2 import Environment, BaseLoader
from os.path import dirname, join, abspath
import datetime
import logging
import sys
import boto3
import json
import time


logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def search_kendra_index(args):
    """Send a query to the Kendra index

    Args:
        args (namespace): the args found on the command line.
    """
    kendra = boto3.client('kendra')
    
    response = kendra.query(IndexId = args.index_id, QueryText = args.query_text)
    for result_item in response['ResultItems']:

        print('-------------------')
        print('Type: ' + str(result_item['Type']))
        
        if result_item['Type'] == 'ANSWER':
            answer_text = result_item['DocumentExcerpt']['Text']
            print(answer_text)
        if result_item['Type'] == 'DOCUMENT':
            if 'DocumentTitle' in result_item:
                document_title = result_item['DocumentTitle']['Text']
                print('Title: ' + document_title)
            document_text = result_item['DocumentExcerpt']['Text']
            print(document_text)

def parse_command_line():
    parser = ArgumentParser(
        prog='search_kendra_index', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--index-id', help='The id of the Kendra Index', required=True)
    parser.add_argument(
        '--query-text', help='The query to perform', required=True)
    parser.set_defaults(func=search_kendra_index)
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
