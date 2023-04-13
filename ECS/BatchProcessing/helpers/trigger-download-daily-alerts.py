#!/usr/bin/env python
"""
Trigger the given ECS task and override its command line parameters
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import sys
import boto3

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def trigger_download_daily_alerts(args):
    ecs = boto3.client('ecs')
    
    # logger.info("Checking CapacityProvider ...")
    # response = ecs.describe_capacity_providers(capacityProviders=[args.capacity_provider])
    # print (response)


    response = ecs.run_task(
        # capacityProviderStrategy=[{
        #     "capacityProvider": args.capacity_provider,
        #     "weight": 1,
        #     "base": 1
        # }],
        cluster=args.cluster,
        taskDefinition=args.task_definition,
        overrides={
            "containerOverrides": [{
                "name": args.container_name,
                "command": args.command.split()
            }]
        }
    )
    logger.info(response)


def parse_command_line():
    parser = ArgumentParser(
        prog='trigger_download_daily_alerts', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--profile', help='The profile to use to call the sts service', required=False, default=None)
    parser.add_argument(
        '--cluster', help='The short name or full Amazon Resource Name (ARN) of the cluster on which to run your task', required=True)
    parser.add_argument(
        '--task-definition', help='The family and revision (family:revision) or full ARN of the task definition to run', required=True)
    # parser.add_argument(
    #     '--capacity-provider', help='The short name of the capacity provider.', required=False, default="")
    parser.add_argument(
        '--container-name', help='The name of the container that receives the override', required=True)
    parser.add_argument(
        '--command', help='The command to send to the container that overrides the default command from the Docker image or the task definition', required=True)
    parser.set_defaults(func=trigger_download_daily_alerts)
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
