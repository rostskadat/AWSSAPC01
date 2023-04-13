#!/usr/bin/env python
"""
This helper simply stream a Kinesis Stream to stdout.
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import base64
import boto3
import datetime
import json
import logging
import re
import subprocess
import sys
import time

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def tail_stream(args):
    """Output the given stream to stdout

    Args:
        args (namespace): the args found on the command line.
    """
    kinesis = boto3.client('kinesis')

    # Get ShardId from stream
    response = kinesis.describe_stream(StreamName=args.stream_name)
    shard_id = response["StreamDescription"]["Shards"][0]["ShardId"]

    logger.info("Break with [ Ctrl + C ]")

    # Get ShardIterator from Stream & ShardId
    response = kinesis.get_shard_iterator(
        StreamName=args.stream_name,
        ShardId=shard_id,
        ShardIteratorType="TRIM_HORIZON")
    shard_iterator = response["ShardIterator"]
    while True:
        response = kinesis.get_records(ShardIterator=shard_iterator)
        for record in response["Records"]:
            record["Data"] = record["Data"].decode("utf-8").replace("\t", '    ')
            logger.info(json.dumps(record, indent=2, sort_keys=True, default=default))
        shard_iterator = response["NextShardIterator"]
        time.sleep(args.sleep)


def parse_command_line():
    parser = ArgumentParser(
        prog='tail_stream', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--stream-name', help='The name of the stream to send the records to', required=True)
    parser.add_argument(
        '--sleep', type=int, help='The number of seconds to sleep between each call to GetRecords', required=False, default=10)
    parser.set_defaults(func=tail_stream)
    return parser.parse_args()


def main():
    args = parse_command_line()
    try:
        if args.debug:
            logger.setLevel(logging.DEBUG)
        if args.profile:
            boto3.setup_default_session(profile_name=args.profile)
        return args.func(args)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
