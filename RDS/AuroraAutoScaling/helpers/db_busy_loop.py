#!/usr/bin/env python
"""
Execute an SQL on the MYSQL DB

SYNOPSIS:

"""
from argparse import ArgumentParser, RawTextHelpFormatter
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from os.path import isfile
import boto3
import logging
import mysql.connector
import socket
import sys

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def execute_sql(args, index):
    logger.debug(f"T{index} | Connecting to {args.user}@{args.host}:{args.port}/{args.database} ... ")
    connection = mysql.connector.connect(
        host=args.host,
        user=args.user,
        password=args.password,
        database=args.database
    )
    cursor = connection.cursor()
    if args.sql_file:
        with open(args.sql_file) as f:
            sql_statements = f.read()
    else:
        sql_statements = args.sql
    execution_results = []
    for result in cursor.execute(sql_statements, multi=True):
        if result.with_rows:
            execution_result = result.fetchall()
            logger.info(f"T{index} | Rows produced by statement '{result.statement}': {execution_result}")
        else:
            execution_result = result.rowcount
            logger.info(f"T{index} | Number of rows affected by statement '{result.statement}': {execution_result}")
        execution_results.append(execution_result)
    connection.close()
    return execution_results

def db_busy_loop(args):
    """Execute the given SQL on the database

    Args:
        args (namespace): the args found on the command line.
    """
    if not args.sql_file and not args.sql:
        raise ValueError(f"At least one of 'sql-file' or 'sql' argument must be defined")
    if args.sql_file and args.sql:
        raise ValueError(f"At most one of 'sql-file' or 'sql' argument can be defined")
    if args.sql_file and not isfile(args.sql_file):
        raise ValueError(f"Invalid 'sql-file' argument: no such file")
    if args.sql and len(args.sql) <= 10:
        raise ValueError(f"Invalid 'sql' argument: is it a valid SQL statement?")

    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        future_to_sql = { executor.submit(execute_sql, args, index): index for index in range(args.nb_executions)}
        for future in as_completed(future_to_sql):
            index = future_to_sql[future]
            try:
                execution_results = future.result()
                logger.debug(f"T{index} | {execution_results}")
            except Exception as e:
                logger.error('%r generated an exception: %s' % (index, e))
    logging.debug("All done")

def parse_command_line():
    parser = ArgumentParser(
        prog='db_busy_loop', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--host', help='The MySQL Host. Default to localhost', required=False, default="localhost")
    parser.add_argument(
        '--port', type=int, help='The MYSQL Port Number. Default to 3306', required=False, default=3306)
    parser.add_argument(
        '--user', help='The user to connect with', required=True)
    parser.add_argument(
        '--password', help='The password to connect with', required=True)
    parser.add_argument(
        '--database', help='The database to connect to', required=True)
    parser.add_argument(
        '--sql-file', help='The path of the sql file to execute', required=False, default=None)
    parser.add_argument(
        '--sql', help='The sql statement to execute', required=False, default=None)
    parser.add_argument(
        '--max-workers', type=int, help='The number of the workers. Allow to simulate parrallel connections', required=False, default=1)
    parser.add_argument(
        '--nb-executions', type=int, help='The number of time to execute the SQL statement', required=False, default=1)
    parser.set_defaults(func=db_busy_loop)
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
