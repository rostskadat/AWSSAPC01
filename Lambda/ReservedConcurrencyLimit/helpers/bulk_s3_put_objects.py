#!/usr/bin/env python
"""
Put a series of random object in a bucket.
Usefull to test the ReservedConcurrentExecutions metric.
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import boto3
import logging
import os
import sys
import uuid

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def s3_put_objects(args):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(args.bucket)
    for i in range(0, args.count):
        key = str(uuid.uuid4())
        logger.info("Uploading object %d/%d to s3://%s/%s",
                    i+1,
                    args.count,
                    args.bucket,
                    key)
        s3_object = bucket.Object(key)
        s3_object.put(Body=os.urandom(args.size))


def parse_command_line():
    parser = ArgumentParser(
        prog='display_sts_credentials',
        description=__doc__,
        formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug',
        required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service',
        required=False, default=None)
    parser.add_argument(
        '--bucket', help='The profile to use to call the sts service',
        required=False, default=None)
    parser.add_argument(
        '--count', type=int, help='The number of object to put',
        required=False, default=1)
    parser.add_argument(
        '--size', type=int, help='The number of bytes each object will have. '
        'Default to 1MB.',
        required=False,
        default=1024*1024)
    parser.set_defaults(func=s3_put_objects)
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
        logging.error(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
