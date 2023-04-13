#!/usr/bin/env python
"""
List all faces from MP4
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from os.path import isfile
import boto3
import imageio
import json
import logging
import sys
import visvis as vv

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def list_faces_from_mp4(args):
    """Extract the image from the video file

    Args:
        args (namespace): the args found on the command line.
    """
    if not isfile(args.video):
        raise ValueError("Invalid --video argument: %s no such file", args.video)
    if not isfile(args.faces):
        raise ValueError("Invalid --faces argument: %s no such file", args.faces)
    video = imageio.get_reader(args.video,  'ffmpeg', print_info = args.debug)
    logger.debug("Video: %s", video.get_meta_data())
    fps = video.get_meta_data()['fps']
    
    with open(args.faces) as fh:
        faces = json.load(fh)["Faces"]

    for face in faces:
        timestamp = face["Timestamp"]
        bb = face["Face"]["BoundingBox"]
        print ("extract_image_from_mp4.py --video %s --timestamp %0.1f --top %0.3f --left %0.3f --height %0.3f --width %0.3f --output %s%d.png" % (args.video, float(timestamp)/1000, bb["Top"], bb["Left"], bb["Width"], bb["Height"], args.output, timestamp))

def parse_command_line():
    parser = ArgumentParser(prog='extract_image_from_mp4',
                            description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--video', help='The name of the video file', required=True)
    parser.add_argument(
        '--faces', help='The json file with Face information', required=True)
    parser.add_argument(
        '--output', help='The pattern for the frames', required=False, default='frame-at-')
    parser.set_defaults(func=list_faces_from_mp4)
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
