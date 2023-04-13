#!/usr/bin/env python
"""
Allow to get a file in S3 using different kind of encryption.
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import boto3
import logging
import sys
import requests

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def s3_download_presigned_url(args):
    """Get an object from S3 using a presigned url

    Args:
        args (namespace): the args found on the command line.
    """
    s3 = boto3.client('s3')
    response = s3.generate_presigned_url('get_object',
                                         Params={'Bucket': args.bucket,
                                                 'Key': args.key},
                                         ExpiresIn=args.expiration)
    print(f"presigned_url={response}")
    s3_response = requests.get(response)
    if args.dst_file:
        with open(args.dst_file, 'wb') as fh:
            fh.write(s3_response.content)
    else:
        print(s3_response.content.decode('ascii'))


def parse_command_line():
    parser = ArgumentParser(
        prog='s3_download_presigned_url', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--bucket', help='The S3 bucket to put the object into', required=True)
    parser.add_argument('--key', help='The S3 object key', required=True)
    parser.add_argument('--expiration', type=int,
                        help='The number of seconds for the link to expire', required=False, default=3600)
    parser.add_argument(
        '--dst-file', help='The file to save the S3 object to. Stdout if not specified', required=False, default=None)
    parser.set_defaults(func=s3_download_presigned_url)
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
