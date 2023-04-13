import boto3
import json
import os
import uuid

CORS_ALLOW_ORIGIN = os.environ['CORS_ALLOW_ORIGIN']
TABLE_NAME = os.environ['TABLE_NAME']
BUCKET_NAME = os.environ['BUCKET_NAME']
SNS_TOPIC = os.environ['SNS_TOPIC']

table = boto3.resource('dynamodb').Table(TABLE_NAME)
sns = boto3.client('sns')

def lambda_handler(event, context):
    """[summary]

    Args:
        event ([type]): [description]
        context ([type]): [description]

    Returns:
        [type]: [description]
    """
    note_id = str(uuid.uuid4())

    params = json.loads(event.get('body', "{}"))
    voice = params["voice"] if "voice" in params else None
    text = params["text"] if "text" in params else None

    if voice and text:
        # Creating new record in DynamoDB table
        table.put_item(
            Item={
                'id': note_id,
                'text': text,
                'voice': voice,
                'status': 'PROCESSING'
            }
        )

        # Sending notification about new post to SNS
        sns.publish(TopicArn=SNS_TOPIC, Message=note_id)

        status_code = 200
        body = json.dumps({"noteId": note_id})
    else:
        status_code = 400
        body = json.dumps({"message": "Invalid request. 'voice' and 'text' are required"})

    return {
        "statusCode": status_code,
        "headers": {
            'Access-Control-Allow-Origin': CORS_ALLOW_ORIGIN,
            "Access-Control-Allow-Methods": "POST",
        },
        "body": body
    }
