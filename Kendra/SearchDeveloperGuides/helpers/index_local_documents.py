#!/usr/bin/env python
"""
Implements a Kendra Custom Datasource to index local document
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from os import walk
from os.path import join, abspath, expanduser
from datetime import datetime
import logging
import sys
import boto3


logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

CONTENT_TYPES = {
    'pdf': 'PDF',
    'html': 'HTML',
    'htm': 'HTML',
    'xhtml': 'HTML',
    'doc': 'MS_WORD',
    'docx': 'MS_WORD',
    'txt': 'PLAIN_TEXT',
    'ppt': 'PPT'
}

#bat
#doc
#DOC
#docx
#graphml
#html
#java
#mpp
#msg
#odg
#odt
#pdf
#PDF
#ppt
#pptx
#py
#rar
#sh
#sql
#txt
#vbs
#xdb
#xls
#xlsm
#xlsx
#XLSX
#xml
#yaml
#zargo


def _upload_local_documents(kendra, index_id, datasource_id, execution_id,root_dir, includes):
    for root, _, files in walk(abspath(expanduser(root_dir))):
        for basename in files:
            if not basename.lower().endswith(includes):
                continue
            file_to_index = join(root, basename)
            logger.info("Sending file %s to Index %s ...", file_to_index, index_id)
            with open(file_to_index, 'rb') as fd:
                document = {
                    'Id': str(file_to_index),
                    'Attributes': [
                        {'Key': '_data_source_id', 'Value': {'StringValue': datasource_id} }, 
                        {'Key': '_data_source_sync_job_execution_id', 'Value': {'StringValue': str(execution_id)} },
                        {'Key': '_index_time', 'Value': {'DateValue': datetime.now()} },
                        ],
                    'ContentType': CONTENT_TYPES[includes],
                    'Blob': fd.read()
                }
                kendra.batch_put_document(IndexId = index_id, Documents = [document])


def index_local_documents(args):
    """Send local document to the Kendra index

    Args:
        args (namespace): the args found on the command line.
    """
    kendra = boto3.client('kendra')
    
    if not args.includes in CONTENT_TYPES:
        logger.error("Invalid '--includes' parameter: '%s' is not a recognised extention", args.includes)
        return

    if not args.execution_id:
        result = kendra.start_data_source_sync_job(IndexId = args.index_id, Id = args.datasource_id)
        execution_id = result['ExecutionId']
        logger.info("Started Sync job with Execution Id '%s' ...", execution_id)
    else:
        execution_id = args.execution_id
    try:
        _upload_local_documents(kendra, args.index_id, args.id, execution_id, args.root_dir, args.includes)
    except Exception as e:
        logger.error(str(e))
    finally:
        kendra.stop_data_source_sync_job(IndexId = args.index_id, Id = args.id)


def parse_command_line():
    parser = ArgumentParser(
        prog='index_local_documents', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--index-id', help='The id of the Kendra Index', required=True)
    parser.add_argument(
        '--id', help='The id of the Custom Datasource', required=True)
    parser.add_argument(
        '--execution-id', help='The id of the Custom Datasource Sync job', required=False, default=None)
    parser.add_argument(
        '--root-dir', help='The path where the file to index are located', required=True)
    parser.add_argument(
        '--includes', help='The extention of file to include', required=False, default='pdf')
    parser.set_defaults(func=index_local_documents)
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
