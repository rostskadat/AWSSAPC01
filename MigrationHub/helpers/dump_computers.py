#!/usr/bin/env python
"""
Dump all computers from AD, look them up with a DNS request and then generate a dump that can be imported into Migration Hub
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from functools import partial
from os.path import dirname, join, abspath, exists
from jinja2 import Environment, FileSystemLoader
from ldap3 import Server, Connection, SAFE_SYNC
from nslookup import Nslookup
import datetime
import logging
import sys
import boto3

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def dump_computers(args):
    """Dump all object of type Computers from AD

    Args:
        args (namespace): the args found on the command line.
    """
    if exists(abspath(args.import_template)):
        template = Environment(loader=FileSystemLoader(searchpath="./")).get_template(args.import_template)

    try:
        logger.debug("Connecting to LDAP Server {} ...".format(args.ldap_url))
        server = Server(args.ldap_url)
        conn = Connection(server, args.bind_dn, args.bind_password, client_strategy=SAFE_SYNC, auto_bind=True)
        if not conn:
            logger.error("Failed to login. Check your credentials and retry.")
            return 1
        logger.debug("Searching for computers w/ {} ...".format(args.search_filter))
        status, result, response, _ = conn.search(args.search_base, args.search_filter, attributes=['name', 'dNSHostName', 'objectGUID', 'operatingSystem', 'operatingSystemVersion'])
        if not status:
            logger.error("Failed to search {} from {}. Check your parameters and retry.".format(args.search_filter, args.search_base))
            return 1
        hostnames = {}
        for entry in response:
            if entry['type'] == 'searchResEntry':
                hostnames[entry['attributes']['dNSHostName']] = entry['attributes']
        logger.debug("Found {} hostnames. Looking up IP addresses ...".format(len(hostnames.keys())))
        dns_query = Nslookup()
        computers = []
        i = 0
        # vm-{{computer.ExternalId}},vm-00000000-0000-0000-0000-000000000000
        for hostname, entry in hostnames.items():
            if hostname:
                ips_record = dns_query.dns_lookup(hostname)
                primary_ip = ips_record.answer[0]
                if primary_ip:
                    computers.append({
                        'ExternalId': entry['name'],
                        'IPAddress': primary_ip,
                        'MACAddress': '00:00:00:00:00:00',
                        'HostName': hostname,
                        'OS_Name': entry['operatingSystem'],
                        'OS_Version': entry['operatingSystemVersion'],
                    })
                i = i + 1
                if args.limit != -1 and i >= args.limit:
                    break
        if args.output:
            logger.debug("Generating CSV file {} ...".format(args.output))
            with open(args.output, "w") as fh:
                fh.write(template.render({'computers': computers}))
        else:
            print(template.render({'computers': computers}))
    except Exception as e:
        logger.error(e)
        return 1
    return 0


def parse_command_line():
    parser = ArgumentParser(
        prog='dump_computers', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--ldap-url', help='The URL of the LDAP Server. i.e afb1windc01p.allfunds.bank', required=True)
    parser.add_argument(
        '--bind-dn', help='The DN to use when connecting. i.e CVS.LDAP.RO', required=True)
    parser.add_argument(
        '--bind-password', help='The password to use when connecting. i.e. aGz.280.323', required=True)
    parser.add_argument(
        '--search-base', help='The LDAP search base. i.e. DC=allfunds,DC=bank', required=False, default='DC=allfunds,DC=bank')
    parser.add_argument(
        '--search-filter', help='The LDAP search filter. i.e. (objectclass=computer)', required=False, default='(&(objectclass=computer)(cn=ESPLW*))')
    parser.add_argument(
        '--import-template', help='The CSV template file to use when writing the inventory', required=False, default='import_template.csv')
    parser.add_argument(
        '--output', help='The file to write the inventory to', required=False, default=None)
    parser.add_argument(
        '--limit', type=int, help='The max number of computer to export', required=False, default=-1)
    parser.set_defaults(func=dump_computers)
    return parser.parse_args()


def main():
    args = parse_command_line()
    try:
        if args.debug:
            logger.setLevel(logging.DEBUG)
        return args.func(args)
    except Exception as e:
        logging.error(e, exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
