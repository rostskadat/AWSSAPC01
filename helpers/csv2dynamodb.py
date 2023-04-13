#!/usr/bin/env python
"""
Upload a CSV File to a DynamoDB Table.

SYNOPSIS:

# Load the funds.csv file into MyTable, using the ISIN_FONDO as the key.
?> csv2dynamodb.py --table-name MyTable --filename resources/funds.csv --schema resources/funds-schema.json --table-key-source ISIN_FONDO

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

def _from_DATE(column_name: str, date_format: str, value:str):
    """Convert a Oracle DATE to a datetime object
    """
    if value and value != '':
        return datetime.datetime.strptime(value, date_format)
    return None

def _from_NUMBER(column_name: str, value:str):
    """Convert a Oracle NUMBER to a float
    """
    if value and value != '':
        return float(value)
    return None

class PandasSerieConverter():

    def converter(self, record):
        for k, v in record.items():
            if self._is_nan(v):
                record[k] = None                
            elif self._is_float(v):
                record[k] = Decimal(v)
            elif self._is_datetime(v):
                record[k] = v.isoformat()
        return record

    def _is_nan(self, value):
        return True if isinstance(value, float) and math.isnan(value) else False
        
    def _is_float(self, value):
        return True if isinstance(value, float) else False

    def _is_datetime(self, value):
        return True if isinstance(value, datetime.datetime) else False

#
# The SCHEMA is json result of the query:
# SELECT '"'||COLUMN_NAME||'": "'||DATA_TYPE||'",' AS COL_SCHEMA FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = ':TABLE_NAME' ORDER BY COLUMN_ID ASC
#
def _parse_schema(schema, date_format):
    (names, dtype, converters) = (None, None, None)
    with open(schema) as f:
        json_dtype = json.load(f)
        names = list(json_dtype.keys())
        dtype = {}
        converters = {}
        for column_name, column_type in json_dtype.items():
            if column_type == 'DATE':
                converters[column_name] = partial(_from_DATE, column_name, date_format)
            elif column_type == 'VARCHAR2' or column_type == 'CHAR' :
                dtype[column_name] = 'str'
            elif column_type == 'NUMBER':
                converters[column_name] = partial(_from_NUMBER, column_name)
    return (names, dtype, converters)

def csv2dynamodb(args):
    """Upload a CSV File to a DynamoDB Table

    Args:
        args (namespace): the args found on the command line.
    """
    if not isfile(args.filename):
        raise ValueError("Invalid --filename argument: %s no such file", args.filename)
    
    logger.info("Loading cvs file '%s' ... ", abspath(args.filename))
    names = None
    dtype = None
    converters = None
    if args.schema:
        if not isfile(args.schema):
            raise ValueError("Invalid --schema argument: %s no such file", args.schema)
        (names, dtype, converters) = _parse_schema(args.schema, args.date_format)
    logger.debug("converters=%s", converters)
    df = pd.read_csv(
        args.filename, 
        delimiter=args.delimiter, 
        quotechar=args.quotechar, 
        encoding=args.encoding,
        header=0 if names else None,
        names=names,
        dtype=dtype,
        converters=converters,
        error_bad_lines=False, 
        warn_bad_lines=args.debug,
        low_memory=False,
        engine = 'c'
        )
    logger.info("Sample data:\n%s", df.head())
    # NOTE: that we only return ISO_8601 as this is the format used by
    #   DynamoDB to store dates        
    #return datetime.datetime.strptime(value, date_format).strftime("%Y-%m-%d'T'%H:%M:%S+00:00")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(args.table_name)
    converter = PandasSerieConverter()
    with table.batch_writer() as batch:
        count = len(df)
        intervals = 100
        step = max(int(count / intervals), 1)
        for index, row in df.iterrows():
            item = converter.converter(row.to_dict())
            if args.table_key != args.table_key_source and args.table_key not in item:
                item[args.table_key] = item[args.table_key_source]
            if int(index % step) == 0:
                percent = ("(%d%%) " % (int(index / step) * (100/intervals))) if step > 1 else ""
                logger.info("Loading record %d/%d %s...", index + 1, count, percent)
            batch.put_item(Item=item)
        logger.info("Loaded %d / %d records", index + 1, count)

def parse_command_line():
    parser = ArgumentParser(
        prog='csv2dynamodb', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--table-name', help='The DynamoDB to insert into', required=True)
    parser.add_argument(
        '--table-key', help='The attribute name that serves as the DynamoDB Key. Default to "id"', required=False, default="id")
    parser.add_argument(
        '--table-key-source', help='The column name that serves as the DynamoDB Key. Default to "id"', required=False, default="id")
    parser.add_argument(
        '--filename', help='The CSV filename to load', required=True)
    parser.add_argument(
        '--delimiter', help='The CSV delimiter. Default to ","', required=False, default=',')
    parser.add_argument(
        '--schema', help='The schema for the table, in the form { COLUMN_NAME: COLUMN_TYPE }', required=False, default=None)
    parser.add_argument(
        '--date-format', help='The date format to convert string to date. As per datetime.datetime.strptime', required=False, default="%Y/%m/%d %H:%M:%S")
    parser.add_argument(
        '--quotechar', help='The CSV quote character. Default to "', required=False, default='"')
    parser.add_argument(
        '--encoding', help='The CSV filename encoding. Default to "utf-8"', required=False, default='utf-8')
    parser.set_defaults(func=csv2dynamodb)
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
