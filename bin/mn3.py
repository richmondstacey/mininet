#!/usr/bin/env python3
"""Mininet CLI for python3."""

import argparse
import ipaddress
import logging
import os

from mininet3.network import Mininet3
from mininet3.nodes import CONTROLLER_TYPES, HOST_TYPES, INTERFACE_TYPES, LINK_TYPES, SWITCH_TYPES, TOPOLOGY_TYPES

# TODO: Status update instead of printing everything to screen?

logger = logging.getLogger(__name__)
VERSION = '3.0.0'  # TODO: Use the shared version.
VERBOSITY_TYPES = (
    'critical',
    'error',
    'warn',
    'info',
    'debug',
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
    parser = argparse.ArgumentParser(
        prog='mn',
        description='The mn utility creates a Mininet simulated network from the command line. '
                    'It can create parametrized topologies, invoke the Mininet CLI, and run tests.',
    )
    parser.add_argument('-S', '--switch', choices=SWITCH_TYPES.keys(), default='ovs')
    parser.add_argument('-H', '--host', choices=HOST_TYPES.keys(), default='cfs')
    parser.add_argument('-C', '--controller', choices=CONTROLLER_TYPES.keys(), default='default')
    parser.add_argument('-L', '--link', choices=LINK_TYPES.keys(), default='default')
    parser.add_argument('-T', '--topology', choices=TOPOLOGY_TYPES.keys(), default='linear')
    parser.add_argument('-I', '--interface', choices=INTERFACE_TYPES.keys(), default='default')
    parser.add_argument('-c', '--clean', action='store_true', help='Clean up the mininet topology and exit.')
    parser.add_argument('--custom', nargs='+', help='Read custom classes/params from .py file(s).', type=_is_valid_file)
    parser.add_argument('-x', '--xterms', action='store_true', help='Spawn xterms for each node.')
    parser.add_argument('-i', '--ip-base', help='Base IP address for hosts.', type=ipaddress.ip_address)
    parser.add_argument('-M', '--set-host-macs', action='store_true', help='Automatically set host MAC addresses.')
    parser.add_argument('-A', '--static-arp', action='store_true', help='Enable static ARP.')
    parser.add_argument('-v', '--verbosity', choices=VERBOSITY_TYPES)
    parser.add_argument('--listen-port', type=int, help='Base port for passive switch listening.')
    parser.add_argument('--no-listen-port', action='store_true', help="Don't use passive switch listening.")
    parser.add_argument('--pre', help='CLI script to run before tests.', type=_is_valid_file)
    parser.add_argument('--post', help='CLI script to run after tests.', type=_is_valid_file)
    parser.add_argument('--pin', action='store_true', help='Pin hosts to CPU cores (requires --host cfs or --host rt).')
    parser.add_argument('--nat', action='store_true', help=NAT_HELP)
    parser.add_argument('--sw-wait-sec', type=int, default=0, help='How many seconds to wait for switches to connect.')
    parser.add_argument('--version', action='store_true', help='Print the version and exit.')
    args = parser.parse_args()
    return args


def load_custom_assets(asset_paths: list) -> None:
    """Load custom classes, parameters, etc."""
    # TODO: Add these to the nodes registry dynamically.
    logger.info(f'Loading custom assets from {asset_paths}.')


def run_cleanup() -> None:
    """Cleanup the Mininet network."""
    # TODO: Add logic here to clean up the old topology.
    logger.info('Cleaning up the Mininet network.')


def main() -> None:
    """Collect user arguments and run the Mininet CLI."""
    args = get_args()
    if args.version:
        print(VERSION)
    elif args.clean:
        run_cleanup()
    else:
        try:
            if args.custom:
                load_custom_assets(args.custom)
            mn = Mininet3(
                topology_type=args.topology,
                switch_type=args.switch,
                host_type=args.host,
                controller_type=args.controller,
                link_type=args.link,
                interface_type=args.interface,
            )
            mn.start()
        except KeyboardInterrupt:
            logger.warning('Stopping Mininet...')
            run_cleanup()
        except Exception as error:  # pylint: disable=broad-except
            logger.exception(error)
            raise
        finally:
            run_cleanup()


if __name__ == '__main__':
    main()
