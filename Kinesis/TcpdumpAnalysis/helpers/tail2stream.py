#!/usr/bin/env python
"""
This helper simply stream the content of a file to a Kinesis Stream.
NOTE: Contrary to the Kinesis Agent that only streams to Kinesis Data Firehose,
this script allows to monitor a file and then produce a stream of data, that can 
then be ingested into Kinesis Stream. However since Kinesis Data Analytics also 
allow a Kinesis Data Firehose as input, it is kind or redundant.
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import boto3
import logging
import re
import subprocess
import sys

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def tail2stream(args):
    """Sends data from the input file to the given stream

    Args:
        args (namespace): the args found on the command line.
    """
    kinesis = boto3.client('kinesis')
    if 'input_file' in args:
        f = subprocess.Popen(['tail', '-F', args.input_file],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        raise ValueError("NOT_IMPLEMENTED")

    # timestamp protocol src.src_port > dst.dst_port: details
    # ^(\S+)\s(\S+)\s(\S+\.\S+)\s>\s(\S+\.\S+):\s(.*)$
    i = 0
    line_interval = 100
    compiled = re.compile(args.input_format)

    while True:
        line = f.stdout.readline().decode('utf-8')
        matches = compiled.match(line)
        if matches:
            csv_data = ','.join(list(matches.groups()))
            response = kinesis.put_record(
                StreamName=args.stream_name,
                Data=csv_data,
                PartitionKey=args.input_file)  # I always want the same stream
            if 'ShardId' not in response:
                logger.error(response)
            else:
                i = i+1
                if (i % line_interval) == 0: logger.info(f"Sent {line_interval} records")
        else:
            logger.error(f"Ignoring line '{line}'")


def parse_command_line():
    parser = ArgumentParser(
        prog='tail2stream', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--stream-name', help='The name of the stream to send the records to', required=True)
    parser.add_argument(
        '--input-file', help='The local file to follow. Mutually exclusive with the command parameter', required=False)
    parser.add_argument(
        '--input-format', help='The regexp to split the input line', required=True)
    parser.add_argument(
        '--command', help='The command to execute. Mutually exclusive with the intput-file parameter', required=False)
    parser.set_defaults(func=tail2stream)
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
