#!/bin/env python
"""
Help to test Transfer Acceleration
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from botocore.config import Config
from datetime import datetime
from functools import partial
from io import BytesIO
import logging
import os
import sys
import boto3


logging.basicConfig(format="%(asctime)s | %(levelname)-5s | %(module)s:%(lineno)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
logger = logging.getLogger()


def parse_command_line():
    parser = ArgumentParser(
        prog="S3TxObject",
        description=__doc__,
        formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False)
    parser.add_argument("--use-accelerate-endpoint", action="store_true", default=False)
    parser.add_argument("--bucket-name", help="The bucket name")
    parser.add_argument("--key", help="The key")
    parser.set_defaults(func=partial(_general_help, parser))
    ps = parser.add_subparsers(title='Subcommands')
    p = ps.add_parser("put", description=__doc__)
    p.add_argument("--size", type=int, default=1024*1024*10)  # 10MB
    p.set_defaults(func=put)
    p = ps.add_parser("get", description=__doc__)
    p.set_defaults(func=get)
    return parser.parse_args()


def _general_help(parser, _):
    parser.print_help(sys.stderr)


def _get_client(args):
    resource = boto3.resource(
        "s3",
        config=Config(
            s3={ "use_accelerate_endpoint": args.use_accelerate_endpoint}
            )
        )
    return resource.meta.client


def get(args):
    """Obtain a file from a bucket.

    Args:
        args ([type]): [description]
    """
    data = BytesIO()
    s3 = _get_client(args)
    start = datetime.now()
    s3.download_fileobj(args.bucket_name, args.key, data)    
    elapsed = (datetime.now() - start).total_seconds()
    logger.info(f"GET s3://{args.bucket_name}/{args.key} took {elapsed}s")



def put(args):
    """Put a file in a bucket.

    Args:
        args ([type]): [description]
    """
    s3 = _get_client(args)
    data = BytesIO()
    data.write(os.urandom(args.size))
    data.seek(0)
    start = datetime.now()
    s3.upload_fileobj(data, args.bucket_name, args.key)
    elapsed = (datetime.now() - start).total_seconds()
    logger.info(f"PUT s3://{args.bucket_name}/{args.key} took {elapsed}s")


def main():
    args = parse_command_line()
    try:
        if args.debug:
            logger.setLevel(logging.DEBUG)
        args.func(args)
        return 0
    except ValueError as e:
        logging.error(e)
        return 1
    except Exception as e:
        logging.error(e, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
