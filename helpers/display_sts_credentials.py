#!/usr/bin/env python
"""
Display in a bash / cmd compatible format the credentials from STS.
This is meant as a helper when testing STS credentials. 
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import sys
import boto3

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create SQS client


def display_sts_credentials(args):
    """Displays the STS credentials to use.

    Args:
        args (namespace): the args found on the command line.
    """
    sts = boto3.client('sts')
    parameters = {
        "RoleArn": args.role_arn,
        "RoleSessionName": args.role_session_name
    }
    if args.external_id:
        parameters["ExternalId"] = args.external_id
    response = sts.assume_role(**parameters)
    credentials = response["Credentials"]
    if sys.platform == "win32":
        cmd = "SET"
    else:
        cmd = "export"
    print("%s AWS_ACCESS_KEY_ID=%s" % (cmd, credentials["AccessKeyId"]))
    print("%s AWS_SECRET_ACCESS_KEY=%s" %
          (cmd, credentials["SecretAccessKey"]))
    print("%s AWS_SESSION_TOKEN=%s" % (cmd, credentials["SessionToken"]))


def parse_command_line():
    parser = ArgumentParser(prog='display_sts_credentials',
                            description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--role-arn', help='The Role ARN to assume', required=True)
    parser.add_argument('--role-session-name',
                        help='The Role Session name', required=True)
    parser.add_argument(
        '--external-id', help='The external-id for the session', required=False)
    parser.set_defaults(func=display_sts_credentials)
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
