#!/usr/bin/env python
"""
Generate streams events
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import sys
import boto3
import json
import numpy as np
import uuid
import time

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create SQS client
kinesis = boto3.client('kinesis')

def put_records(stream_name, records):
    logger.info("Sending batch of '%d' events ...", len(records))
    response = kinesis.put_records(StreamName=stream_name, Records=records)
    if response['FailedRecordCount'] > 0:
        for record in response['Records']:
            if "ErrorMessage" in record:
                logger.error("Failed event: %s, %s", record["ErrorCode"], record["ErrorMessage"])
    return []


def generate_events(args):
    rng = np.random.default_rng()
    while True:
        records = []
        for _ in range(abs(args.device_count)):
            device_id = str(uuid.uuid4())
            logger.info("Generating events for device '%s' ...", device_id)
            for value in rng.normal(50, 20, args.event_count):
                payload = json.dumps({"DeviceId": device_id, "DeviceValue": value})
                records.append({'Data': payload, 'PartitionKey':device_id})
                if len(records) == 500:
                    records = put_records(args.stream_name, records)
                    time.sleep(1)
        if len(records) > 0:
            put_records(args.stream_name, records)
        if not args.continuous:
            break

def parse_command_line():
    parser = ArgumentParser(
        prog='generate_events', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--stream-name', help='The name of the stream to send events to', required=True)
    parser.add_argument(
        '--device-count', type=int, help='Number of device to simulate', required=False, default=100)
    parser.add_argument(
        '--event-count', type=int, help='Number of events to send per device', required=False, default=100)
    parser.add_argument(
        '--continuous', action="store_true", help='Number of events to send per device', required=False, default=False)
    parser.set_defaults(func=generate_events)
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
