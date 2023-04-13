#!/usr/bin/env python
"""
Get a user token
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import boto3
import logging
import sys

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_token(args):
    logger.info("Initiating Auth challenge ...")
    cognito = boto3.client('cognito-idp')
    response = cognito.admin_initiate_auth(
        UserPoolId=args.user_pool_id,
        ClientId=args.client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            'USERNAME': args.username,
            'PASSWORD': args.password
        }
    )
    authentication_result = response['AuthenticationResult']
    logger.info("AccessToken=%s", authentication_result['AccessToken'])
    logger.info("RefreshToken=%s", authentication_result['RefreshToken'])
    logger.info("IdToken=%s", authentication_result['IdToken'])


def parse_command_line():
    parser = ArgumentParser(
        prog='get_token', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--user-pool-id', help='The user pool id where the user is connected', required=True)
    parser.add_argument(
        '--client-id', help='The app client id to connect with', required=True)
    parser.add_argument('--username', help='The user name', required=True)
    parser.add_argument('--password', help='The password', required=True)
    parser.set_defaults(func=get_token)
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
