import json
import logging
import requests

def lambda_handler(event, context):
    print(event)
    return {
        'status': '302',
        'statusDescription': 'Found',
        'headers': {
            'location': [{
                'key': 'Location',
                'value': 'http://docs.aws.amazon.com/lambda/latest/dg/lambda-edge.html',
            }],
        },
    }
