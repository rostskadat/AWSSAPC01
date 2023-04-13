#!/usr/bin/env python
"""
Start the observer for ConcurrentExecutions
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime, timedelta
import boto3
import logging
import threading
import requests
import sys
import time
import pytz

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def start_observer(args):
    cloudwatch = boto3.resource('cloudwatch')
    metric = cloudwatch.Metric(args.namespace, args.name)
    while True:
        end = datetime.utcnow() - args.offset*timedelta(seconds=args.period)
        start = end - args.number_or_period*timedelta(seconds=args.period)
        statistics = metric.get_statistics(
            StartTime=start,
            EndTime=end,
            Period=args.period,
            Statistics=[args.statistic])
        value = statistics["Datapoints"][0]
        logging.info("%s->%s: %s=%s" % (start.strftime('%H:%M'),
                                        end.strftime('%H:%M'), args.statistic, value[args.statistic]))
        time.sleep(60)


def parse_command_line():
    parser = ArgumentParser(
        prog='start_observer', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--offset', type=int, help='Number of period in past', required=False, default=5)
    parser.add_argument('--namespace', help='The Metrics namespace',
                        required=False, default='AWS/Lambda')
    parser.add_argument('--name', help='The Metrics namespace',
                        required=False, default='ConcurrentExecutions')
    parser.add_argument('--statistic', help='The statistic',
                        required=False, default='Maximum')
    parser.add_argument(
        '--period', type=int, help='The period in seconds', required=False, default=60)
    parser.add_argument('--number-or-period', type=int,
                        help='Number of period to retrieve', required=False, default=1)
    parser.set_defaults(func=start_observer)
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
        logger.error(e, exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
