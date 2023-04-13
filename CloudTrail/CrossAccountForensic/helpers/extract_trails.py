#!/usr/bin/env python
"""
Given a path and the name of the deleted bucked, it will track back to the actual IAM user from a cross account trail
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from functools import partial
from jinja2 import Environment, BaseLoader
from os.path import basename, dirname, join, abspath
import datetime
import logging
import sys
import boto3
import json
import gzip
import time
import uuid
import os

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def extract_trails(args):
    """Extract the information about the Event that triggered the bucket deletion

    Args:
        args (namespace): the args found on the command line.
    """
    trails = []
    for root, dirs, files in os.walk(abspath(args.trails_dir)):
        trails.extend(list(map(lambda f: join(root,f), files)))
    records = []
    for trail in trails:
        if not trail.endswith('.gz'):
            continue
        with gzip.open(trail, 'rb') as f:
            recs = json.loads(f.read())["Records"]
            logger.debug("Decompressing '%s' and adding %d records ...", basename(trail), len(recs))
            records.extend(recs)
    delete_events = []
    logger.debug("Analyzing %d records ...", len(records))
    for record in records:
        logger.debug("Analyzing event '%s' ...", record["eventID"])
        if record["eventName"] == "DeleteBucket":
            delete_events.append(record)
    if len(delete_events) == 0:
        logger.error("Did not detect any DeleteBucket events!")
        exit(1)
    logger.info("Detected %d DeleteBucket events ...", len(delete_events))
    for delete_event in delete_events:
        if delete_event.get("requestParameters", {}).get("bucketName", {}) == args.bucket_name:
            logger.info("Event 'DeleteBucket' detected on bucket '%s': %s", args.bucket_name, json.dumps(delete_event, indent=2, default=default))
    assume_role_events = []
    for record in records:
        logger.debug("Analyzing event '%s' ...", record["eventID"])
        if record["eventName"] == "AssumeRole" and record["userIdentity"]["type"] != "AWSService":
            assume_role_events.append(record)
    if len(assume_role_events) == 0:
        logger.error("Did not detect any AssumeRole events!")
        exit(1)
    logger.info("Detected %d AssumeRole events ...", len(assume_role_events))
    for assume_role_event in assume_role_events:
        logger.info("Event 'AssumeRole' detected: %s", assume_role_event["eventID"])

def parse_command_line():
    parser = ArgumentParser(
        prog='extract_trails', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument('--trails-dir', help='The path where the trails are located', required=True)
    parser.add_argument('--bucket-name', help='The name of the bucket that was deleted', required=True)
    parser.set_defaults(func=extract_trails)
    return parser.parse_args()


def main():
    args = parse_command_line()
    try:
        if args.debug:
            logger.setLevel(logging.DEBUG)
        return args.func(args)
    except Exception as e:
        logging.error(e, exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
