#!/usr/bin/env python
"""
Allow to get a file in S3 using different kind of encryption.
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from Crypto.Cipher import AES
import base64
import boto3
import datetime
import json
import logging
import struct
import sys
import os
import random

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)
    return out_filename


def do_simple_get(args):
    s3 = boto3.client('s3')
    with (open(args.dst_file, 'wb')) as fh:
        if args.range:
            logger.debug(f"Getting Range {args.range} from s3://{args.bucket}/{args.key} ...")
            kwargs = {
                'Bucket': args.bucket,
                'Key': args.key,
                'Range': args.range
            }
            response = s3.get_object(**kwargs)
            fh.write(response.pop('Body').read())
        else:
            logger.debug(f"Downloading s3://{args.bucket}/{args.key} ...")
            s3.download_fileobj(args.bucket, args.key, fh)
        logger.info(f"Written content to {args.dst_file}.")


def do_client_side_decryption(args):
    kms = boto3.client('kms')
    plaintext_key = kms.decrypt(CiphertextBlob=base64.b64decode(
        args.cse_cyphertext_blob)).get('Plaintext')
    s3 = boto3.client('s3')
    with (open(args.dst_file, 'wb')) as fh:
        kwargs = {
            'Bucket': args.bucket,
            'Key': args.key
        }
        response = s3.get_object(**kwargs)
        fh.write(response.pop('Body').read())
    out_filename = decrypt_file(plaintext_key, args.dst_file)
    print(out_filename)


def do_server_side_decryption(args, secret_key_bytes):
    s3 = boto3.client('s3')
    secret_key_str = base64.b64encode(secret_key_bytes).decode('ascii')
    print(f"{{b64}}ssec='{secret_key_str}'")
    with (open(args.dst_file, 'wb')) as fh:
        kwargs = {
            'Bucket': args.bucket,
            'Key': args.key,
            'SSECustomerAlgorithm': 'AES256',
            'SSECustomerKey': secret_key_bytes,
        }
        response = s3.get_object(**kwargs)
        fh.write(response.pop('Body').read())
        print(json.dumps(response, indent=2, sort_keys=True, default=default))


def s3_get_object(args):
    """Get an object from S3

    Args:
        args (namespace): the args found on the command line.
    """
    if not args.ssec and not args.cse_cyphertext_blob:
        # do simple get_object without encryption
        logger.debug("No encryption required")
        do_simple_get(args)
    elif args.ssec:
        # SSE with provided key
        secret_key_bytes = base64.b64decode(args.ssec)
        do_server_side_decryption(args, secret_key_bytes)
    elif args.cse_cyphertext_blob:
        # Client Side encryption
        do_client_side_decryption(args)
    else:
        raise ValueError('Options --ssec and --cse are mutually exclusive...')


def parse_command_line():
    parser = ArgumentParser(
        prog='s3_get_object', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--bucket', help='The S3 bucket to put the object into', required=True)
    parser.add_argument('--key', help='The S3 object key', required=True)
    parser.add_argument('--dst-file', help='The local file', required=True)
    parser.add_argument(
        '--range', help='The range to download. If not specified will use the download_fileobj API.', required=False, default=None)
    parser.add_argument(
        '--ssec', help='Specify the SSE-C encryption and the corresponding key. Mutually exclusive with --cse. If none are specified use ssec with generated key.', required=False, default=None)
    parser.add_argument(
        '--cse-cyphertext-blob', help='Specify the KMS Key Id to use when doing Envelope Encryption. Mutually exclusive with --ssec', required=False, default=None)
    parser.set_defaults(func=s3_get_object)
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
