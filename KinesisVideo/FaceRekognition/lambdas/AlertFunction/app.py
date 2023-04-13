import boto3
import datetime
import json
import logging
import os
import requests

# Extract from the lambda function all costly action such as setting up a
# connection to a DB, etc...
SNS_TOPIC = os.getenv('SNS_TOPIC')

# Use logs in order to have formatted output that can be easily parsed.
logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def default(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def lambda_handler(event, context):
    logger.debug(event)
    matchedFace = 0
    unmatchedFace = 0
    for record in event["Records"]:
        # Kinesis data is base64 encoded so decode here
        load = Buffer(record["kinesis"]["data"], 'base64').toString('ascii')
        payload = json.loads(load)
        if payload.get("FaceSearchResponse", None):
            for face in  payload["FaceSearchResponse"]:
                matched_faces = face.get("MatchedFaces", [])
                if len(matched_faces) == 0:
                    unmatchedFace += 1
                for matched_face in matched_faces:
                    matchedFace += 1
    if matchedFace > 0 or unmatchedFace > 0:
        params = {
            "Message": '%d Known Person(s) found, %d Unknown Person(s) in Video Feed' % (matchedFace, unmatchedFace),
            "TopicArn": SNS_TOPIC
        }
        boto3.client('sns').publish(**params)
                    