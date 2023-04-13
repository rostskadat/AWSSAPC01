#!/usr/bin/env python
"""
Get a Kinesis Video Media
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import sys
import boto3

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create SQS client


def kinesis_get_media(args):
    """Get the given media from Kinesis Video Stream

    Args:
        args (namespace): the args found on the command line.
    """
    kinesis = boto3.client('kinesis-video-media')
    parameters = {
        "StartSelector": {
            "StartSelectorType": args.start_selector_type
        }
    }
    if 'stream_arn' in args:
        parameters["StreamARN"] = args.stream_arn
    elif 'stream_name' in args:
        parameters["StreamName"] = args.stream_name
    else:
        raise ValueError("You must specify one of '--stream-name' or '--stream-arn'")
    response = client.get_media(**parameters)
    print(response)


def parse_command_line():
    parser = ArgumentParser(prog='kinesis_get_media',
                            description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--stream-name', help='The name of the stream to get the media from', required=False, default=None)
    parser.add_argument(
        '--stream-arn', help='The Arn of the stream to get the media from', required=False, default=None)
    parser.add_argument(
        '--start-selector-type', help='The start selector type', required=False, default='EARLIEST')
    parser.set_defaults(func=kinesis_get_media)
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
