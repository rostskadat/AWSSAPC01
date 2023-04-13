from urllib.parse import parse_qs
import logging

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    request = event["Records"][0]["cf"]["request"]
    if "querystring" in request:
        o = parse_qs(request["querystring"])
        if 'lang' in o:
            request["uri"] = "/{}/index.html".format(o["lang"][0])
    return request

