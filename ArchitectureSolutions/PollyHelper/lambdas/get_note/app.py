from boto3.dynamodb.conditions import Key, Attr
import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CORS_ALLOW_ORIGIN = os.environ['CORS_ALLOW_ORIGIN']
TABLE_NAME = os.environ['TABLE_NAME']

table = boto3.resource('dynamodb').Table(TABLE_NAME)


def lambda_handler(event, context):
    """Return the Notes corresponding to this noteId.

    Args:
        event ([type]): [description]
        context ([type]): [description]

    Returns:
        [type]: [description]
    """
    try:
        logger.info(json.dumps(event, indent=2))
        params = event.get('queryStringParameters', {})
        note_id = params["noteId"] if params and "noteId" in params else None
        if note_id and note_id != '*':
            logger.info(f"Looking up Note {note_id}")
            items = table.query(KeyConditionExpression=Key('id').eq(note_id))
        else:
            logger.info("Scanning whole table")
            items = table.scan()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': CORS_ALLOW_ORIGIN,
                "Access-Control-Allow-Methods": "GET",
                'Content-Type': 'application/json'
            },
            'body': json.dumps(items["Items"])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': CORS_ALLOW_ORIGIN,
                "Access-Control-Allow-Methods": "GET",
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"message": str(e)})
        }

