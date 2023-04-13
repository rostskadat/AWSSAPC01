#!/usr/bin/env python
"""
Truncate DynamoDB Table

Ref: https://stackoverflow.com/questions/28521631/empty-a-dynamodb-table-with-boto

"""
from argparse import ArgumentParser, RawTextHelpFormatter
from functools import partial
from os.path import dirname, join, abspath, isfile
from decimal import Decimal
import datetime
import logging
import os
import sys
import boto3
from boto3.dynamodb.types import TypeSerializer
import json
import math
import time
import uuid
import pandas as pd 

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def dynamodb_truncate_table(args):
    """Truncate DynamoDB Table

    Args:
        args (namespace): the args found on the command line.
    """
    if "table_name" not in args:
        raise ValueError("Missing --table-name argument")
    
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table(args.table_name)
    
    #get the table keys
    tableKeyNames = [key.get("AttributeName") for key in table.key_schema]

    """
    NOTE: there are reserved attributes for key names, please see https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html
    if a hash or range key is in the reserved word list, you will need to use the ExpressionAttributeNames parameter
    described at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.scan
    """

    #Only retrieve the keys for each item in the table (minimize data transfer)
    ProjectionExpression = ", ".join(tableKeyNames)
    
    logger.info("Fetching keys ...")
    response = table.scan(ProjectionExpression=ProjectionExpression)
    data = response.get('Items')
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=ProjectionExpression, 
            ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        
    logger.info("Found %d items", len(data))

    with table.batch_writer() as batch:
        count = len(data)
        intervals = 100
        step = max(int(count / intervals), 1)
        index = 0
        for each in data:
            if int(index % step) == 0:
                percent = ("(%d%%) " % (int(index / step) * (100/intervals))) if step > 1 else ""
                logger.info("Deleting record %d/%d %s...", index + 1, count, percent)
            batch.delete_item(Key={key: each[key] for key in tableKeyNames})
            index += 1
        logger.info("Deleted %d / %d records", index + 1, count)

def parse_command_line():
    parser = ArgumentParser(
        prog='dynamodb_truncate_table', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--table-name', help='The DynamoDB to insert into', required=True)
    parser.set_defaults(func=dynamodb_truncate_table)
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
