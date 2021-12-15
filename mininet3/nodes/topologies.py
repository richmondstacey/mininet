"""Topology node types."""

import abc
import logging

from mininet3.nodes.base import Node

logger = logging.getLogger(__name__)


class Topology(Node, metaclass=abc.ABCMeta):
    """Base class for all Topology types."""

    def __init__(
            self,
            switch_type: str = 'ovs',
            host_type: str = 'cfs',
            controller_type: str = 'default',
            link_type: str = 'default',
            interface_type: str = 'default',
    ) -> None:
        """Build the topology based upon given types."""
        self.switch_type = switch_type
        self.host_type = host_type
        self.controller_type = controller_type
        self.link_type = link_type
        self.interface_type = interface_type
        self.hosts = {}
        self.links = {}
        self.switches = {}
        self.build()

    def build(self) -> None:
        """Custom logic goes here for how to build the topology."""
        raise NotImplementedError('No logic implemented to build the topology.')

    def start(self) -> None:
        """Start the whole topology by starting all individual nodes and links."""
        # TODO: Do this in parallel/async?
        for name, host in self.hosts.items():
            logger.info(f'Starting host {name}.')
            host.start()
        for name, switch in self.switches.items():
            logger.info(f'Starting switch {name}.')
            switch.start()
        for name, link in self.links.items():
            logger.info(f'Starting link {name}.')
            link.start()


class LinearTopology(Topology):
    """Placeholder."""


class MinimalTopology(Topology):
    """Placeholder."""


class ReversedTopology(Topology):
    """Placeholder."""


class SingleTopology(Topology):
    """Placeholder."""


class TorusTopology(Topology):
    """Placeholder."""


class TreeTopology(Topology):
    """Placeholder."""


TOPOLOGY_TYPES = {
    'default': Topology,
    'linear': LinearTopology,
    'minimal': MinimalTopology,
    'reversed': ReversedTopology,
    'single': SingleTopology,
    'torus': TorusTopology,
    'Tree': TreeTopology,
}
