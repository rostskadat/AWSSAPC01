#!/usr/bin/env python
"""
Send a message to the specified SQS queue. 
It is meant to ease testing SQS sample scenarios.
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
import uuid

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def sqs_send_message(args):
    """Sends an sqs message on the specified queue

    Args:
        args (namespace): the args found on the command line.
    """
    sqs = boto3.client('sqs')

    with open(abspath(args.message_body), 'r') as f:
        template = Environment(loader=BaseLoader).from_string(
            json.dumps(json.load(f)))
    i = 0
    message_group_id = str(uuid.uuid4())
    for i in range(abs(args.count)):
        timestamp = datetime.datetime.now()
        if args.queue_url.endswith('.fifo'):
            response = sqs.send_message(
                QueueUrl=args.queue_url,
                MessageBody=template.render({"timestamp": timestamp}),
                DelaySeconds=abs(args.message_delay),
                MessageGroupId=message_group_id
            )
        else:
            response = sqs.send_message(
                QueueUrl=args.queue_url,
                MessageBody=template.render({"timestamp": timestamp}),
                DelaySeconds=abs(args.message_delay)
            )
        print("Sent message (%d/%d): %s" %
              (i, args.count, response['MessageId']))
        time.sleep(args.delay)


def parse_command_line():
    parser = ArgumentParser(
        prog='sqs_send_message', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--queue-url', help='The URL of the input queue', required=True)
    parser.add_argument(
        '--count', type=int, help='Number of message to send', required=False, default=100)
    parser.add_argument('--delay', type=float,
                        help='Number of second to wait between messages', required=False, default=1)
    parser.add_argument('--message-delay', type=int,
                        help='Initial number of second to wait before the message is visible to consumer', required=False, default=0)
    parser.add_argument('--message-body', help='The json file containig the message payload',
                        required=False, default=join(dirname(__file__), "sqs_send_message-body.json"))
    parser.set_defaults(func=sqs_send_message)
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
