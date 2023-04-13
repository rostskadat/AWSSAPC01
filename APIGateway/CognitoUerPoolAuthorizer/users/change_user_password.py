#!/usr/bin/env python
"""
Change a user password after its initial import.
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import sys
import boto3

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def change_user_password(args):
    logger.info("Initiating Auth challenge ...")
    cognito = boto3.client('cognito-idp')
    response = cognito.admin_initiate_auth(
        UserPoolId=args.user_pool_id,
        ClientId=args.client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            'USERNAME': args.username,
            'PASSWORD': args.current_password
        }
    )
    logger.info("Changing password ...")
    response = cognito.respond_to_auth_challenge(
        ClientId=args.client_id,
        Session=response['Session'],
        ChallengeName='NEW_PASSWORD_REQUIRED',
        ChallengeResponses={
            'USERNAME': args.username,
            'NEW_PASSWORD': args.new_password
        }
    )
    logger.info(response)
    logger.info("Password change successfully")


def parse_command_line():
    parser = ArgumentParser(prog='change_user_password',
                            description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--user-pool-id', help='The user pool id where the user is connected', required=True)
    parser.add_argument(
        '--client-id', help='The app client id to connect with', required=True)
    parser.add_argument('--username', help='The user name', required=True)
    parser.add_argument('--current-password',
                        help='The current password', required=True)
    parser.add_argument(
        '--new-password', help='The new password', required=True)
    parser.set_defaults(func=change_user_password)
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
