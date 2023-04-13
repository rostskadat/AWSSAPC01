#!/usr/bin/env python
"""
Allow to put a file in S3 using different kind of encryption.
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from Crypto.Cipher import AES
import base64
import boto3
import json
import logging
import struct
import sys
import os
import random

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def pad(s): return s.decode('ascii') + (16 - len(s) % 16) * ' '


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk = pad(chunk)
                outfile.write(encryptor.encrypt(chunk))
    return out_filename


def do_client_side_encryption(args):
    kms = boto3.client('kms')
    data_key = kms.generate_data_key(KeyId=args.cse, KeySpec='AES_128')
    ciphertext_blob = base64.b64encode(data_key.get('CiphertextBlob')).decode('ascii')
    print(f"{{b64}}ciphertext_blob='{ciphertext_blob}'")
    plaintext_key = data_key.get('Plaintext')
    out_filename = encrypt_file(plaintext_key, args.src_file)
    s3 = boto3.client('s3')
    with (open(out_filename, 'rb')) as fh:
        kwargs = {
            'Bucket': args.bucket,
            'Key': args.key,
            'Body': fh,
        }
        response = s3.put_object(**kwargs)
        print(json.dumps(response, indent=2, sort_keys=True))

def do_server_side_encryption(args, secret_key_bytes):
    s3 = boto3.client('s3')
    secret_key_str = base64.b64encode(secret_key_bytes).decode('ascii')
    print(f"{{b64}}ssec='{secret_key_str}'")
    with (open(args.src_file, 'rb')) as fh:
        kwargs = {
            'Bucket': args.bucket,
            'Key': args.key,
            'SSECustomerAlgorithm': 'AES256',
            'SSECustomerKey': secret_key_bytes,
            'Body': fh,
        }
        response = s3.put_object(**kwargs)
        print(json.dumps(response, indent=2, sort_keys=True))


def s3_put_object(args):
    """Put an object in S3...

    Args:
        args (namespace): the args found on the command line.
    """
    if not args.ssec and not args.cse:
        # SSE with default key
        secret_key_bytes = os.urandom(32)
        do_server_side_encryption(args, secret_key_bytes)
    elif args.ssec:
        # SSE with provided key
        secret_key_bytes = base64.b64decode(args.ssec)
        do_server_side_encryption(args, secret_key_bytes)
    elif args.cse:
        # Client Side encryption
        do_client_side_encryption(args)
    else:
        raise ValueError('Options --ssec and --cse are mutually exclusive...')


def parse_command_line():
    parser = ArgumentParser(
        prog='s3_put_object', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument('--src-file', help='The local file', required=True)
    parser.add_argument(
        '--bucket', help='The S3 bucket to put the object into', required=True)
    parser.add_argument('--key', help='The S3 object key', required=True)
    parser.add_argument(
        '--ssec', help='Specify the SSE-C encryption and the corresponding key. Mutually exclusive with --cse. If none are specified use ssec with generated key.', required=False, default=None)
    parser.add_argument(
        '--cse', help='Specify the KMS Key Id to use when doing Envelope Encryption. Mutually exclusive with --ssec', required=False, default=None)
    parser.set_defaults(func=s3_put_object)
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
