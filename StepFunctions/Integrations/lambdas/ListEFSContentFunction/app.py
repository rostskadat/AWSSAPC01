import json
import os

OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '/mnt/efs')

def lambda_handler(event, context):
    avro_files = os.listdir(OUTPUT_DIR)
    return {
        "statusCode": 200,
        "headers": {
            # In order to configure CORS while using Lambda Proxy integration 
            # it is important to add the following header (no set by
            # APIGateway... )
            # "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json" 
        },
        "body": {
            "avro_files": avro_files,
            "length": len(avro_files)
        }
    }
