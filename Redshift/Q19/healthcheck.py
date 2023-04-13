#!/usr/bin/python3

import psycopg2

hostname = 'redshiftq19-cluster-gjnjx6entqst.cr6dcdipbnus.eu-west-1.redshift.amazonaws.com'
port = 5439
username = 'admin'
password = 'Passw0rd'
database = 'dev'


def do_view(conn):
    """Create the view."""    
    try:
        cur = conn.cursor()
        cur.execute("CREATE VIEW DUAL AS SELECT 'X' AS DUMMY;")
    except Exception:
        pass


def do_query(conn):
    """Execute dummy query."""
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM DUAL;")
    for x in cur.fetchall():
        print(f"DUAL={x[0]}")


print("Using psycopg2...")
connection = None
try:
    connection = psycopg2.connect(
        host=hostname,
        port=port,
        user=username,
        password=password,
        dbname=database)
    do_view(connection)
    do_query(connection)
finally:
    if connection:
        connection.close()
