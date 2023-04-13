#!/usr/bin/env python
"""
Simulate receiving and retrying the message reception using the ReceiveRequestAttemptId SQS Message attribute 
"""
import datetime
import time
import json
import logging
import sys
import uuid
from argparse import ArgumentParser, RawTextHelpFormatter

import boto3

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def default(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def sqs_receive_and_retry_messages(args):
    """Receive and retry an SQS Message
    Args:
        args (namespace): the args found on the command line.
    """
    sqs = boto3.client('sqs')

    receive_request_attempt_id = str(uuid.uuid4())
    logger.info("ReceiveRequestAttemptId=%s", receive_request_attempt_id)
    response = sqs.receive_message(
        QueueUrl=args.queue_url,
        MaxNumberOfMessages=args.count,
        ReceiveRequestAttemptId=receive_request_attempt_id
    )
    for message in response.get("Messages", []):
        logger.info("Processing message %s ...", message["MessageId"])
    logger.info("Simulating long processing and failure (no delete)")
    # Should return the same messages as the previous call despite the message being within the Visibility timeout
    time.sleep(args.delay)
    logger.info("Retrying ")
    response = sqs.receive_message(
        QueueUrl=args.queue_url,
        MaxNumberOfMessages=args.count,
        ReceiveRequestAttemptId=receive_request_attempt_id
    )
    entries=[]
    for message in response.get("Messages", []):
        logger.info("Reprocessing message %s ...", message["MessageId"])
        entries.append({"Id": str(uuid.uuid4()), "ReceiptHandle": message["ReceiptHandle"]})
    if len(entries) > 0:
        logger.info("Deleting the processed messages...")
        sqs.delete_message_batch(
            QueueUrl=args.queue_url,
            Entries=entries
        )
    else:
        logger.info("No message to delete...")



def parse_command_line():
    parser = ArgumentParser(
        prog='sqs_receive_and_retry_messages', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--queue-url', help='The URL of the input queue', required=True)
    parser.add_argument(
        '--count', type=int, help='Number of message to receive', required=False, default=1)
    parser.add_argument(
        '--delay', type=int, help='Number of second to wait before retrying the messages', required=False, default=5)
    parser.set_defaults(func=sqs_receive_and_retry_messages)
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
