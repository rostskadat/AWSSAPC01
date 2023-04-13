#!/usr/bin/env python
"""
Generate a Signed URL
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from functools import partial
import boto3
import datetime
import logging
import os
import sys
import time

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def rsa_signer(private_key_file, message):
    if not os.path.isfile(private_key_file):
        raise ValueError(
            "Invalid '--private-key-file' parameter: No such file '{private_key_file}'")
    with open(private_key_file, 'rb') as fh:
        private_key = serialization.load_pem_private_key(
            fh.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def get_expiry():
    ts = time.time()
    return ts


def generate_cf_credentials(args):
    """Generate the URL to retrieve an object from CloudFront protected by a Signed URL

    Args:
        args (namespace): the args found on the command line.
    """
    # The URL is built according to https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-canned-policy.html
    resource_path = f"https://{args.distribution}/{args.s3_key}"
    date_greater_than = datetime.datetime.now() + datetime.timedelta(0, args.not_before)
    date_less_than = datetime.datetime.now() + datetime.timedelta(0, args.not_after)
    ip_address = args.only_ip

    cloudfront_signer = CloudFrontSigner(
        args.public_key_id, partial(rsa_signer, args.private_key_file))


    # Create a signed url that will be valid until the specfic expiry date
    # provided 
    if args.use_custom:
        # using a custom policy
        policy = cloudfront_signer.build_policy(resource_path, date_less_than, date_greater_than, ip_address)
    else:
        # using a canned policy.
        policy = cloudfront_signer.build_policy(resource_path, date_less_than)
    policy = policy.encode('utf8')
    print ("Execute the following command:\n")
    if args.set_cookie:
        encoded_policy = cloudfront_signer._url_b64encode(policy).decode('utf8')
        signature = cloudfront_signer._url_b64encode(cloudfront_signer.rsa_signer(policy)).decode('utf8')
        print(f"curl \\\n\t-b 'CloudFront-Policy={encoded_policy}'\\\n\t-b 'CloudFront-Signature={signature}'\\\n\t-b 'CloudFront-Key-Pair-Id={args.public_key_id}'\\\n\t{resource_path}")
    else:
        if args.use_custom:
            signed_url = cloudfront_signer.generate_presigned_url(resource_path, policy=policy)
        else:
            signed_url = cloudfront_signer.generate_presigned_url(resource_path, date_less_than=date_less_than)
        print(f"curl '{signed_url}'")


def parse_command_line():
    parser = ArgumentParser(
        prog='generate_cf_credentials',
        description=__doc__,
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('--debug', action="store_true",
                        help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--distribution', help='The Cloudfront distribution FQDN.', required=True)
    parser.add_argument('--s3-key', help='The S3 object key.', required=True)
    parser.add_argument(
        '--private-key-file', help='The file cntaining the Private Key used to sign URLs.', required=True)
    parser.add_argument(
        '--public-key-id', help='The Public Key Id whose Private Key part is used to sign URLs.', required=True)
    parser.add_argument(
        '--use-custom', action="store_true", help='Indicate whether to use a custom policy or a canned policy.', required=False, default=False)
    parser.add_argument(
        '--not-before', type=int, help='The number of seconds for the link to be valid. Default to 0 seconds.', required=False, default=0)
    parser.add_argument(
        '--not-after', type=int, help='The number of seconds for the link to expire. Default to 60 seconds.', required=False, default=60)
    parser.add_argument(
        '--only-ip', help='The Ip Address to restrict the download to. Not restricted by default.', required=False, default=None)
    parser.add_argument('--set-cookie', action="store_true",
                        help='Use Signed Cookies instead of Signed URLs.', required=False, default=False)
    parser.set_defaults(func=generate_cf_credentials)
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
