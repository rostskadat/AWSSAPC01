#!/usr/bin/env python
"""
Extract a still image from a video file
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from os.path import isfile
import boto3
import imageio
import logging
import sys
import visvis as vv

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def extract_image_from_mp4(args):
    """Extract the image from the video file

    Args:
        args (namespace): the args found on the command line.
    """
    if not isfile(args.video):
        raise ValueError("Invalid --video argument: %s no such file", args.video)
    video = imageio.get_reader(args.video,  'ffmpeg', print_info = args.debug)
    logger.debug("Video: %s", video.get_meta_data())
    fps = video.get_meta_data()['fps']
    
    image_index = int(fps * args.timestamp)
    image = video.get_data(image_index)
    if args.top and args.left and args.width and args.height:
        (height, width, _) = image.shape
        y1 = int(height * args.top)
        y2 = int(height * (args.top + args.height))
        x1 = int(width * args.left)
        x2 = int(width * (args.left + args.width))
        logger.debug ("Cutting (%d, %d), (%d, %d) out of (%d, %d)" % (y1, x1, y2, x2, width, height))
        image = image[y1:y2, x1:x2]
    imageio.imwrite(args.output, image)
    if args.show:
        app = vv.use()
        vv.imshow(image)
        app.Run()
        

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
        '--timestamp', type=float, help='The timestamp of the image to extract after the start of the video in seconds', required=True)
    parser.add_argument(
        '--width', type=float, help='The bounding box coordinate', required=False, default=None)
    parser.add_argument(
        '--height', type=float, help='The bounding box coordinate', required=False, default=None)
    parser.add_argument(
        '--left', type=float, help='The bounding box coordinate', required=False, default=None)
    parser.add_argument(
        '--top', type=float, help='The bounding box coordinate', required=False, default=None)
    parser.add_argument(
        '--output', help='The name of the PNG file', required=True)
    parser.add_argument(
        '--show', action="store_true", help='Show the resulting image', required=False, default=False)
    parser.set_defaults(func=extract_image_from_mp4)
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
