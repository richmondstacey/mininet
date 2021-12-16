"""Topology node types."""

import abc
import logging

from typing import Type, Union

from mininet3.core import nodes

logger = logging.getLogger(__name__)


class Topology(metaclass=abc.ABCMeta):  # pylint: disable=too-many-instance-attributes
    """Base class for all Topology types."""

    def __init__(  # pylint: disable=too-many-arguments
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

    async def __aenter__(self):
        """Build and start the network."""
        await self.async_build()
        await self.async_start()

    def __enter__(self):
        """Build and start the network."""
        self.build()
        self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Stop the network."""
        await self.async_stop()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Stop the network."""
        self.stop()

    async def async_build(self) -> None:
        """Build the topology asynchronously."""
        raise NotImplementedError('No logic implemented to build the topology.')

    def build(self) -> None:
        """Build the topology by adding the nodes and links."""

    async def async_start(self) -> None:
        """Start the topology asynchronously."""
        for name, host in self.hosts.items():
            await host.async_start()
        for name, switch in self.switches.items():
            await switch.async_start()
        for name, link in self.links.items():
            await link.async_start()

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

    async def async_stop(self) -> None:
        """Stop the topology asynchronously."""
        for name, host in self.hosts.items():
            await host.async_stop()
        for name, switch in self.switches.items():
            await switch.async_stop()
        for name, link in self.links.items():
            await link.async_stop()

    def stop(self) -> None:
        """Stop the whole topology by stopping all individual nodes and links."""
        # TODO: Do this in parallel/async?
        for name, host in self.hosts.items():
            logger.info(f'Stopping host {name}.')
            host.stop()
        for name, switch in self.switches.items():
            logger.info(f'Stopping switch {name}.')
            switch.stop()
        for name, link in self.links.items():
            logger.info(f'Stopping link {name}.')
            link.stop()

    async def async_add_node(self, name: str, node_type: str, node_cls: Union[str, nodes.Node]) -> None:
        """Add a new node to the topology asynchronously."""
        if node_type not in ('hosts', 'links', 'switches'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if isinstance(node_cls, str):
            node_cls = nodes.get_cls_by_name(name, node_type)
        node = node_cls()
        getattr(self, node_type)[name] = node
        await node.async_start()

    def add_node(self, name: str, node_type: str, node_cls: Union[str, nodes.Node]) -> None:
        """Add a new node to the topology."""
        if node_type not in ('hosts', 'links', 'switches'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if isinstance(node_cls, str):
            node_cls = nodes.get_cls_by_name(name, node_type)
        node = node_cls()
        getattr(self, node_type)[name] = node
        node.start()

    async def async_remove_node(self, name: str, node_type: str) -> None:
        """Remove a node from the topology by name and type asynchronously."""
        if node_type not in ('host', 'link', 'switch'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if name not in getattr(self, node_type):
            raise KeyError(f'Failed to delete node. A {node_type} named "{name}" was not found in the network.')
        node = getattr(self, node_type).pop(name)
        await node.async_stop()

    def remove_node(self, name: str, node_type: str) -> None:
        """Remove a node from the topology by name and type."""
        if node_type not in ('host', 'link', 'switch'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if name not in getattr(self, node_type):
            raise KeyError(f'Failed to delete node. A {node_type} named "{name}" was not found in the network.')
        node = getattr(self, node_type).pop(name)
        node.stop()

    async def async_add_host(self, name: str, host_type: Union[str, nodes.Host] = None) -> None:
        """Add a new host to the network topology.

        Args:
            name: The name to assign to the new host. Must be unique.
            host_type: A custom type of host to use. Otherwise, it will use self.host_type.
        """
        await self.async_add_node(name, 'host', host_type)

    def add_host(self, name: str, host_type: Union[str, nodes.Host] = None) -> None:
        """Add a new host to the network topology.

        Args:
            name: The name to assign to the new host. Must be unique.
            host_type: A custom type of host to use. Otherwise, it will use self.host_type.
        """
        self.add_node(name, 'host', host_type)

    async def async_add_link(self, name: str, link_type: Union[str, nodes.Link] = None) -> None:
        """Add a new link to the network topology asynchronously.

        Args:
            name: The name to assign to the new link. Must be unique.
            link_type: A custom type of link to use. Otherwise, it will use self.link_type.
        """
        await self.async_add_node(name, 'link', link_type)

    def add_link(self, name: str, link_type: Union[str, nodes.Link] = None) -> None:
        """Add a new link to the network topology.

        Args:
            name: The name to assign to the new link. Must be unique.
            link_type: A custom type of link to use. Otherwise, it will use self.link_type.
        """
        self.add_node(name, 'link', link_type)

    async def async_add_switch(self, name: str, switch_type: Union[str, nodes.Switch] = None) -> None:
        """Add a new switch to the network topology asynchronously.

        Args:
            name: The name to assign to the new switch. Must be unique.
            switch_type: A custom type of switch to use. Otherwise, it will use self.switch_type.
        """
        await self.async_add_node(name, 'switch', switch_type)

    def add_switch(self, name: str, switch_type: Union[str, nodes.Switch] = None) -> None:
        """Add a new switch to the network topology.

        Args:
            name: The name to assign to the new switch. Must be unique.
            switch_type: A custom type of switch to use. Otherwise, it will use self.switch_type.
        """
        self.add_node(name, 'switch', switch_type)

    async def async_remove_host(self, name: str) -> None:
        """Remove an existing host by name asynchronously.

        Args:
            name: The name of the host to remove.

        Raises:
            KeyError: If the host name was not found.
        """
        await self.async_remove_node(name, 'host')

    def remove_host(self, name: str) -> None:
        """Remove an existing host by name.

        Args:
            name: The name of the host to remove.

        Raises:
            KeyError: If the host name was not found.
        """
        self.remove_node(name, 'host')

    async def async_remove_link(self, name: str) -> None:
        """Remove an existing link by name asynchronously.

        Args:
            name: The name of the link to remove.

        Raises:
            KeyError: If the link name was not found.
        """
        await self.async_remove_node(name, 'link')

    def remove_link(self, name: str) -> None:
        """Remove an existing link by name.

        Args:
            name: The name of the link to remove.

        Raises:
            KeyError: If the link name was not found.
        """
        self.remove_node(name, 'link')

    async def async_remove_switch(self, name: str) -> None:
        """Remove an existing switch by name asynchronously.

        Args:
            name: The name of the switch to remove.

        Raises:
            KeyError: If the switch name was not found.
        """
        await self.async_remove_node(name, 'switch')

    def remove_switch(self, name: str) -> None:
        """Remove an existing switch by name.

        Args:
            name: The name of the switch to remove.

        Raises:
            KeyError: If the switch name was not found.
        """
        self.remove_node(name, 'switch')


# class LinearTopology(Topology):
#     """Placeholder."""
#
#
# class MinimalTopology(Topology):
#     """Placeholder."""
#
#
# class ReversedTopology(Topology):
#     """Placeholder."""
#
#
# class SingleTopology(Topology):
#     """Placeholder."""
#
#
# class TorusTopology(Topology):
#     """Placeholder."""
#
#
# class TreeTopology(Topology):
#     """Placeholder."""


TOPOLOGY_TYPES = {
    'default': Topology,
    # 'linear': LinearTopology,
    # 'minimal': MinimalTopology,
    # 'reversed': ReversedTopology,
    # 'single': SingleTopology,
    # 'torus': TorusTopology,
    # 'Tree': TreeTopology,
}


def get_topology_by_name(topology_name: str) -> Type[Topology]:
    """Get a topology by name.

    Args:
        topology_name: The name of the topology to get.

    Returns:
        topology_cls: The topology type class.
    """
    topology_cls = TOPOLOGY_TYPES.get(topology_name)
    if topology_cls is None:
        raise ValueError(f'Invalid topology type "{topology_name}" was requested.')
    return topology_cls
