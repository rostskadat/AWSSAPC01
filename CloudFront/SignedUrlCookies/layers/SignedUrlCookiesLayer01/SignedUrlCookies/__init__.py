from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import os

def rsa_signer(pk_filename, message):
    # Is it an absolute path?
    if not os.path.isfile(pk_filename):
        # let's try a relative path from here
        pk_filename = os.path.join(os.path.dirname(__file__), pk_filename)
    if not os.path.isfile(pk_filename):
        raise ValueError(f"Invalid 'pk_filename': No such file '{pk_filename}'")
    # If you get Permission denied: '/opt/python/SignedUrlCookies/SAPC01-DEFAULT-KEY'" 
    # make sure the file has rw-r--r-- permission
    with open(pk_filename, 'rb') as fh:
        private_key = serialization.load_pem_private_key(
            fh.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())
