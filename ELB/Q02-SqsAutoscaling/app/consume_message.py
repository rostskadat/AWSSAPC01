#!/usr/bin/env python
"""
Consume messages
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from random import randint
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


def consume_message(args):
    r = 0
    i = 0
    while True:
        if i >= args.expected:
            logging.info("Received all epxected messages")
            break
        response = sqs.receive_message(
            QueueUrl=args.queue_url,
            WaitTimeSeconds=20,
            MaxNumberOfMessages=args.batch
        )
        r += 1
        if 'Messages' not in response:
            logging.info("Empty rersponse...")
            time.sleep(args.delay)
            continue
        for message in response['Messages']:
            if randint(1, 100) <= args.failure_ratio:
                print("Simulating failed message (%d/%d, request #%d): %s" % (i, args.expected, r, message['MessageId']))
            else:                
                print("Processed message (%d/%d, request #%d): %s" % (i, args.expected, r, message['MessageId']))
                sqs.delete_message(
                    QueueUrl=args.queue_url, 
                    ReceiptHandle=message['ReceiptHandle']
                )
            i += 1
        time.sleep(args.delay)


def parse_command_line():
    parser = ArgumentParser(prog='consume_message', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--queue-url', help='The URL of the input queue', required=True)
    parser.add_argument('--batch', type=int, help='Number of message to receive in one go', required=False, default=10)
    parser.add_argument('--expected', type=int, help='Number of message to receive', required=False, default=100)
    parser.add_argument('--delay', type=float, help='Number of second to wait between messages', required=False, default=1)
    parser.add_argument('--failure-ratio', type=int, help='Number of message to fail out of 100. Default to 1', required=False, default=1)
    parser.set_defaults(func=consume_message)
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
