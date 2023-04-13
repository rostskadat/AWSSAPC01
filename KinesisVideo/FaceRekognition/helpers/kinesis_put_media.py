#!/usr/bin/env python
"""
Put a Video file into a Kinesis Video Stream

Reference: https://stackoverflow.com/questions/59481174/amazon-aws-kinesis-video-boto-getmedia-putmedia

See ArchitectureSolutions\DynamoDB2ElasticSearch\lambdas\StreamFunction\app.py for request authentication

"""
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import sys
import boto3
import time
import requests

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class data_iter:
    
    def __init__(self, video_file: str):
        self._data = ''
        if True:
            #localfile = '6-step_example.webm.360p.webm' # upload ok
            #localfile = 'big-buck-bunny_trailer.webm' # error fragment duration over limit
            with open(video_file, 'rb') as image:
                request_parameters = image.read()
                self._data = request_parameters
        self._pointer = 0
        self._size = len(self._data)
    def __iter__(self):
        return self
    def next(self):
        if self._pointer >= self._size:
            raise StopIteration  # signals "the end"
        left = self._size - self._pointer
        chunksz = 16000
        if left < 16000:
            chunksz = left
        pointer_start = self._pointer
        self._pointer += chunksz
        print("Data: chunk size %d" % chunksz)
        return self._data[pointer_start:self._pointer]

#
# References:
# https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/API_dataplane_PutMedia.html
# https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-java/blob/master/src/main/demo/com/amazonaws/kinesisvideo/demoapp/PutMediaDemo.java
#
def kinesis_put_media(args):
    """Put the given media to Kinesis Video Stream

    Args:
        args (namespace): the args found on the command line.
    """
    kinesis = boto3.client('kinesisvideo')
    
    params = {
        'x-amzn-fragment-acknowledgment-required': '1',
        'x-amzn-fragment-timecode-type': 'ABSOLUTE',
        'x-amzn-producer-start-timestamp': repr(time.time())
    }
    
    if args.stream_arn:
        data_endpoint = kinesis.get_data_endpoint(StreamARN=args.stream_arn, APIName='PUT_MEDIA')['DataEndpoint']
        params['x-amzn-stream-arn'] = args.stream_arn
    elif args.stream_name:
        data_endpoint = kinesis.get_data_endpoint(StreamName=args.stream_name, APIName='PUT_MEDIA')['DataEndpoint']
        params['x-amzn-stream-name'] = args.stream_name
    else:
        raise ValueError("You must specify one of '--stream-name' or '--stream-arn'")

    logger.info("DataEndpoint=%s", data_endpoint)
    endpoint_url = data_endpoint + '/putMedia'
    logger.info("endpoint_url=%s", endpoint_url)
    
    response = requests.post(endpoint_url, data=data_iter(args.video_file), headers=headers)
    print(response)


def parse_command_line():
    parser = ArgumentParser(prog='kinesis_put_media',
                            description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--stream-name', type=str, help='The name of the stream to get the media from', required=False, default=None)
    parser.add_argument(
        '--stream-arn', type=str, help='The Arn of the stream to get the media from', required=False, default=None)
    parser.add_argument(
        '--start-selector-type', help='The start selector type', required=False, default='EARLIEST')
    parser.add_argument(
        '--video-file', help='The video file to upload', required=True)
    parser.set_defaults(func=kinesis_put_media)
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
