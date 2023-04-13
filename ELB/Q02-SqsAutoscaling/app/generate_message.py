#!/usr/bin/env python
"""
Generate a message
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import sys
import boto3
import json
import uuid
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create SQS client
sqs = boto3.client('sqs')


def generate_message(args):
    for i in range(abs(args.count)):
        payload = json.dumps({ "message": str(uuid.uuid4()) })
        response = sqs.send_message(
            QueueUrl=args.queue_url,
            MessageBody=payload
        )
        print("Sent message (%d/%d): %s" % (i, args.count, response['MessageId']))
        time.sleep(args.delay)


def parse_command_line():
    parser = ArgumentParser(prog='generate_message', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--queue-url', help='The URL of the input queue', required=True)
    parser.add_argument('--count', type=int, help='Number of message to send', required=False, default=100)
    parser.add_argument('--delay', type=float, help='Number of second to wait between messages', required=False, default=1)
    parser.set_defaults(func=generate_message)
    return parser.parse_args()


def main():
    args = parse_command_line()
    try:
        return args.func(args)
    except Exception as e:
        logging.error(e, exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
