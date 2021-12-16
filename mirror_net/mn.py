#!/usr/bin/env python3
"""Mininet CLI for python3."""

import argparse
import asyncio
import importlib
import ipaddress
import logging
import os

from mirror_net import __version__
from mirror_net.core.controller_lib import Controller, CONTROLLER_TYPES
from mirror_net.core.host_lib import Host, HOST_TYPES
from mirror_net.core.link_lib import Link, LINK_TYPES
from mirror_net.core.network_lib import MirrorNet
from mirror_net.core.switch_lib import Switch, SWITCH_TYPES
from mirror_net.core.topology_lib import Topology, TOPOLOGY_TYPES

# TODO: Status update instead of printing everything to screen?

logger = logging.getLogger(__name__)
REL_DIR = os.path.dirname(os.path.abspath(__file__))
USE_ASYNC = os.getenv('USE_ASYNC', 'false').lower() == 'true'
VERBOSITY_TYPES = (
    'CRITICAL',
    'ERROR',
    'WARN',
    'INFO',
    'DEBUG',
)
NAT_HELP = """Adds a NAT to the topology that connects Mininet hosts to the physical network.
Warning: This may route any traffic on the machine that uses Mininet's IP subnet into the Mininet network.
If you need to change Mininet's IP subnet, use the --ip-base option.
"""


def _is_valid_file(filename: str) -> str:
    """Validate that the given file path exists."""
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(f'The filename: {filename} was not found.')
    return filename


def get_args() -> argparse.Namespace:
    """Collect user arguments.

    Returns:
        args: The user arguments.
    """
    # TODO: Load custom assets to update options for argparse?!
    parser = argparse.ArgumentParser(
        prog='mn',
        description='The mn utility creates a Mininet simulated network from the command line. '
                    'It can create parametrized topologies, invoke the Mininet CLI, and run tests.',
    )
    parser.add_argument('-S', '--switch', choices=SWITCH_TYPES.keys(), default='default')
    parser.add_argument('-H', '--host', choices=HOST_TYPES.keys(), default='default')
    parser.add_argument('-C', '--controller', choices=CONTROLLER_TYPES.keys(), default='default')
    parser.add_argument('-L', '--link', choices=LINK_TYPES.keys(), default='default')
    parser.add_argument('-T', '--topology', choices=TOPOLOGY_TYPES.keys(), default='default')
    parser.add_argument('--list', action='store_true', help='List all assets (including custom) and exit.')
    parser.add_argument('-c', '--clean', action='store_true', help='Clean up the mininet topology and exit.')
    custom = parser.add_mutually_exclusive_group()
    custom.add_argument('--custom-files', nargs='*', default=[], help='Read custom assets from .py file(s).', type=_is_valid_file)
    # TODO: Additional arguments needed for credentials, etc.
    # custom.add_argument('--custom-s3', nargs='+', help='Read custom assets from S3.')
    # TODO: Add support to read from Databases?
    parser.add_argument('-x', '--xterms', action='store_true', help='Spawn xterms for each node.')
    parser.add_argument('-i', '--ip-base', help='Base IP address for hosts.', type=ipaddress.ip_address)
    parser.add_argument('-M', '--set-host-macs', action='store_true', help='Automatically set host MAC addresses.')
    parser.add_argument('-A', '--static-arp', action='store_true', help='Enable static ARP.')
    parser.add_argument('-v', '--verbosity', choices=VERBOSITY_TYPES, default='INFO')
    parser.add_argument('--listen-port', type=int, help='Base port for passive switch listening.')
    parser.add_argument('--no-listen-port', action='store_true', help="Don't use passive switch listening.")
    parser.add_argument('--pre', help='CLI script to run before tests.', type=_is_valid_file)
    parser.add_argument('--post', help='CLI script to run after tests.', type=_is_valid_file)
    parser.add_argument('--pin-cpus', action='store_true', help='Pin hosts to CPU cores (requires --host cfs or --host rt).')
    parser.add_argument('--nat', action='store_true', help=NAT_HELP)
    parser.add_argument('--sw-wait-sec', type=int, default=0, help='How many seconds to wait for switches to connect.')
    parser.add_argument('--version', action='store_true', help='Print the version and exit.')
    deployment = parser.add_mutually_exclusive_group()
    deployment.add_argument('--docker', action='store_true', help='Deploy Mininet in Docker containers.')
    # TODO: Additional arguments needed for credentials, etc.
    # deployment.add_argument('--docker-swarm', action='store_true', help='Deploy Mininet as a Docker swarm service.')
    # deployment.add_argument('--kubernetes', action='store_true', help='Deploy Mininet on Kubernetes.')
    # deployment.add_argument('--aws-ec2', action='store_true', help='Deploy Mininet on AWS EC2.')
    # deployment.add_argument('--aws-ecs', action='store_true', help='Deploy Mininet on AWS ECS.')
    # deployment.add_argument('--aws-eks', action='store_true', help='Deploy Mininet on AWS EKS.')
    args = parser.parse_args()
    return args


def load_custom_assets(asset_paths: list) -> None:
    """Load custom classes, parameters, etc."""
    logger.info(f'Loading custom assets from {asset_paths}.')
    asset_paths = [
        os.path.join(os.path.dirname(REL_DIR), 'custom'),  # Include the built-in custom folder.
        *asset_paths
    ]
    for path in asset_paths:
        if os.path.isfile(path):
            files = [path]
        else:
            files = os.listdir(path)
        for file in files:
            if not file.endswith('.py') or file.startswith('_'):
                continue
            # Convert the file path into a module path, remove the parent directory (mininet).
            file_path = os.path.join(path, file)
            file_path = file_path.split('mininet', 1)[-1]
            module_path = file_path.replace(os.sep, '.').rsplit('.', 1)[0].lstrip('.')
            # Load all of these modules into memory for subclass registry to pick them up.
            importlib.import_module(module_path)
            logger.debug(f'Loaded custom assets from: {path}.')

    # Update the registries:
    CONTROLLER_TYPES.update(Controller.subclasses)
    HOST_TYPES.update(Host.subclasses)
    LINK_TYPES.update(Link.subclasses)
    SWITCH_TYPES.update(Switch.subclasses)
    TOPOLOGY_TYPES.update(Topology.subclasses)


def list_assets() -> None:
    """Print out a listing of all assets to the screen."""
    print('\nControllers:')
    print('\n'.join(CONTROLLER_TYPES.keys()))
    print('\nHosts:')
    print('\n'.join(HOST_TYPES.keys()))
    print('\nLinks:')
    print('\n'.join(LINK_TYPES.keys()))
    print('\nSwitches:')
    print('\n'.join(SWITCH_TYPES.keys()))
    print('\nTopologies:')
    print('\n'.join(TOPOLOGY_TYPES.keys()))


def run_cleanup(deployment_type: str = 'local') -> None:
    """Cleanup the Mininet network."""
    # TODO: Add logic here to clean up the old topology.
    logger.info('Cleaning up the Mininet network.')
    # Currently, this just runs pgrep and pkill -9 to all services.
    # TODO: Find a safer/cleaner method to cleaning up.
    # TODO: This also depends upon the deployment method used.


def main() -> None:
    """Collect user arguments and run the Mininet CLI."""
    args = get_args()
    logger.setLevel(args.verbosity.upper())
    # TODO: Add support for other deployment types.
    deployment_type = 'docker' if args.docker else 'local'
    if args.version:
        print(__version__)
    elif args.clean:
        run_cleanup(deployment_type=deployment_type)
    elif args.list:
        load_custom_assets(args.custom_files)
        list_assets()
    else:
        try:
            load_custom_assets(args.custom_files)
            network = MirrorNet(
                deployment_type=deployment_type,
                topology_type=args.topology,
                switch_type=args.switch,
                host_type=args.host,
                controller_type=args.controller,
                link_type=args.link,
                interface_type=args.interface,
                ip_base=args.ip_base,
                set_host_macs=args.set_host_macs,
                static_arp=args.static_arp,
                pin_cpus=args.pin_cpus,
                listen_port=args.listen_port,
                sw_wait_sec=args.sw_wait_sec,
            )
            if USE_ASYNC:
                asyncio.run(network.async_start())
            else:
                network.start()
        except KeyboardInterrupt:
            logger.warning('Stopping Mininet...')
        except Exception as error:  # pylint: disable=broad-except
            logger.exception(error)
            raise
        finally:
            run_cleanup(deployment_type=deployment_type)


if __name__ == '__main__':
    main()
