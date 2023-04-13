#!/usr/bin/env python
"""
Start parrallel consumers to saturate the Lambda Function
Inspired from https://pymotw.com/2/threading/
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime, timedelta
import boto3
import logging
import threading
import requests
import sys
import time

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def consume(api_url):
    while True:
        requests.get(api_url)


def start_consumers(args):
    logger.info("Starting %d consumers ..." % args.consumers)
    consumers = []
    for i in range(args.consumers):
        consumer = threading.Thread(
            target=consume, name=str(i), args=(args.api_url, ))
        consumer.start()
        consumers.append(consumer)
    logger.info("Consumers started.")


def parse_command_line():
    parser = ArgumentParser(
        prog='start_consumers', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--api-url', help='The URL of the function', required=True)
    parser.add_argument('--consumers', type=int,
                        help='The number of parrallel consumer', required=False, default=10)
    parser.set_defaults(func=start_consumers)
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
        logger.error(e, exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
