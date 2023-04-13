import json
import boto3
import os
from contextlib import closing
from boto3.dynamodb.conditions import Key, Attr
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ['TABLE_NAME']
BUCKET_NAME = os.environ['BUCKET_NAME']

table = boto3.resource('dynamodb').Table(TABLE_NAME)
s3 = boto3.client('s3')
polly = boto3.client('polly')


def lambda_handler(event, context):

    note_id = event["Records"][0]["Sns"]["Message"]
    logger.debug(f"Procesing Note {note_id}")
    
    # Retrieving information about the post from DynamoDB table
    post_item = table.query(
        KeyConditionExpression=Key('id').eq(note_id)
    )
    text = post_item["Items"][0]["text"]
    voice = post_item["Items"][0]["voice"] 
    rest = text

    # Because single invocation of the polly synthesize_speech api can 
    # transform text with about 1,500 characters, we are dividing the 
    # post into blocks of approximately 1,000 characters.
    text_blocks = []
    while (len(rest) > 1100):
        begin = 0
        end = rest.find(".", 1000)

        if (end == -1):
            end = rest.find(" ", 1000)
            
        text_block = rest[begin:end]
        rest = rest[end:]
        text_blocks.append(text_block)
    text_blocks.append(rest)            

    # For each block, invoke Polly API, which will transform text into audio
    for text_block in text_blocks: 
        response = polly.synthesize_speech(
            OutputFormat='mp3',
            Text=text_block,
            VoiceId=voice
        )
        
        #Save the audio stream returned by Amazon Polly on Lambda's temp 
        # directory. If there are multiple text blocks, the audio stream
        # will be combined into a single file.
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                s3.upload_fileobj(stream, BUCKET_NAME, f"{note_id}.mp3")
    
    s3.put_object_acl(
        ACL='public-read',
        Bucket=BUCKET_NAME,
        Key=f"{note_id}.mp3")

    location = s3.get_bucket_location(Bucket=BUCKET_NAME)
    region = location['LocationConstraint']
    
    if region is None:
        url_begining = "https://s3.amazonaws.com/"
    else:
        url_begining = "https://s3-" + str(region) + ".amazonaws.com/" \
    
    url = url_begining \
            + str(BUCKET_NAME) \
            + "/" \
            + str(note_id) \
            + ".mp3"

    table.update_item(
        Key={'id':note_id},
        UpdateExpression="SET #statusAtt = :statusValue, #urlAtt = :urlValue",
        ExpressionAttributeValues={':statusValue': 'UPDATED', ':urlValue': url},
        ExpressionAttributeNames={'#statusAtt': 'status', '#urlAtt': 'url'},
    )