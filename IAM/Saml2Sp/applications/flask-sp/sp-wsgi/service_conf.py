from saml2.assertion import Policy
from urllib.parse import urlparse
import saml2.xmldsig as ds
import os


SP_URL_BASE = os.getenv('SP_URL_BASE', "http://localhost:8087")
_o = urlparse(SP_URL_BASE)
HOST = _o.hostname
HTTPS = _o.scheme == 'https'
if _o.port:
    PORT = _o.port
elif HTTPS:
    PORT = 443 
else:
    PORT = 80

if os.getenv('IS_DOCKERISED', None):
    HOST = '0.0.0.0'
    PORT = 8087
    HTTPS = False

SIGN_ALG = None
DIGEST_ALG = None
#SIGN_ALG = ds.SIG_RSA_SHA512
#DIGEST_ALG = ds.DIGEST_SHA512

# Which groups of entity categories to use
POLICY = Policy(
    {
        "default": {"entity_categories": ["swamid", "edugain"]}
    }
)

# HTTPS cert information
SERVER_CERT = "pki/mycert.pem"
SERVER_KEY = "pki/mykey.pem"
CERT_CHAIN = ""
