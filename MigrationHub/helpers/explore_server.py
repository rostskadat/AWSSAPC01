#!/usr/bin/env python
"""
Dump all computers from AD, look them up with a DNS request and then generate a dump that can be imported into Migration Hub
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from functools import partial
from os.path import dirname, join, abspath, exists, expanduser, isdir
from os import mkdir
from jinja2 import Environment, FileSystemLoader
import csv
from fabric.connection import Connection
from invoke.exceptions import UnexpectedExit
import logging
import sys

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def explore_server(args):
    """Explore the Computers

    Args:
        args (namespace): the args found on the command line.
    """
    if not exists(abspath(args.server_list)):
        logger.error("Invalid server-list: no such file {}".format(args.server_list))
        return 1

    servers = []
    with open(args.server_list) as f:
        server_reader = csv.DictReader(f)
        for server in server_reader:
            servers.append(server)

    if not exists(abspath(args.script)):
        logger.error("Invalid script: no such file {}".format(args.script))
        return 1
    with open(args.script) as f:
        script = '\n'.join(f.readlines())
    if not script:
        logger.error("Invalid script: no content detected")
        return 1

    logger.debug("Found {} servers".format(len(servers)))
    i = 0
    for server in servers:
        hostname = server['Hostname']
        username = server['Username'] if 'Username' in server and server['Username'] != '' else args.username
        key_filename = server['SshKey'] if 'SshKey' in server and server['SshKey'] != '' else args.ssh_key
        sudo_user = server['SudoUser'] if 'SudoUser' in server and server['SudoUser'] != '' else args.sudo_user

        if not hostname or not username or not key_filename:
            logger.error("Invalid Server {}: either missing username ({}) or key ({})".format(hostname, username, key_filename))
            continue

        k= {'key_filename': abspath(expanduser(key_filename)) }
        logger.info("Connecting to {}@{} w/ {}".format(hostname, username, key_filename))
        try:
            with Connection(hostname, username, connect_kwargs=k) as connection:
                run_kwargs = {}
                if sudo_user is None:
                    result = connection.run(script, **run_kwargs, hide=True)
                else:
                    run_kwargs['user'] = sudo_user
                    result = connection.sudo(script, **run_kwargs, hide=True)
        except UnexpectedExit as e:
            result = e.result
        if result.ok:
            output_dir = abspath(expanduser(args.output_dir))
            if not isdir(output_dir):
                mkdir(output_dir)
            output = join(output_dir, hostname + '.txt')
            with open(output, "w") as f:
                f.write(result.stdout)
        else:
            logger.error("Exploring of Server {} failed: {}".format(hostname, result.stderr))
        i = i + 1
        if args.limit != -1 and i >= args.limit:
            break

    return 0


def parse_command_line():
    parser = ArgumentParser(
        prog='explore_server', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--server-list', help='The file containing all the servers to explore. I.e. servers.csv', required=False, default="explore_server_list.csv")
    parser.add_argument(
        '--username', help='The unix user to use when connecting. Can be overriden in the server-list file', required=False)
    parser.add_argument(
        '--ssh-key', help='The SSH Key to use when connecting. Can be overriden in the server-list file', required=False)
    parser.add_argument(
        '--sudo-user', help='The unix user to use when executing the explore command. Can be overriden in the server-list file', required=False, default=None)
    parser.add_argument(
        '--script', help='The bash script to use when exploring', required=False, default='explore_server_script.sh')
    parser.add_argument(
        '--output-dir', help='The directory where the exploring data should be stored', required=False, default='data')
    parser.add_argument(
        '--limit', type=int, help='The max number of computer to explore', required=False, default=5)
    parser.set_defaults(func=explore_server)
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
