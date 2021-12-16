"""Topology node types."""

import abc
import logging

from typing import Type, Union

from mininet3.core import host_lib
from mininet3.core import link_lib
from mininet3.core import node_lib
from mininet3.core import switch_lib

logger = logging.getLogger(__name__)


class Topology(metaclass=abc.ABCMeta):  # pylint: disable=too-many-instance-attributes
    """Base class for all Topology types."""

    def __init__(  # pylint: disable=too-many-arguments
            self,
            deployment_type: str = 'default',
            switch_type: str = 'default',
            host_type: str = 'default',
            controller_type: str = 'default',
            link_type: str = 'default',
            interface_type: str = 'default',
            **kwargs
    ) -> None:
        """Build the topology based upon given types.

        Args:
            deployment_type: The deployment type to use for the topology.
            switch_type: The type of switch to deploy by default.
            host_type: The type of host to deploy by default.
            controller_type: The type of controller to deploy by default.
            link_type: The type of link to deploy by default.
            interface_type: The type of interface to use by default.

        Keyword Args:
            ip_base: The base IP address for all devices. Default: 10.0.0.x
            set_host_macs: Automatically assign MAC addresses to hosts.
            static_arp: Set all-pairs static ARP.
            pin_cpus: Pin hosts to real CPU cores. This requires CPULimitedHost host_type.
            listen_port: The listening port to bind.
            sw_wait_sec: How many seconds to wait for switches to connect (or don't wait if set to None/False/0).
            # TODO: inNamespace support for port mappings?
        """
        self.deployment_type = deployment_type
        self.switch_type = switch_type
        self.host_type = host_type
        self.controller_type = controller_type
        self.link_type = link_type
        self.interface_type = interface_type
        # TODO: Subnet for ip base?
        self.ip_base = kwargs.get('ip_base', '10.0.0.0')
        self.set_host_macs = kwargs.get('set_host_macs', True)
        self.static_arp = kwargs.get('static_arp', True)
        self.pin_cpus = kwargs.get('pin_cpus', False)
        self.listen_port = kwargs.get('listen_port', 8000)
        self.sw_wait_sec = kwargs.get('sw_wait_sec', 60)
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
        # TODO: Implement async logic here.
        self.build()

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
        for name, host in self.hosts.items():
            logger.info(f'Stopping host {name}.')
            host.stop()
        for name, switch in self.switches.items():
            logger.info(f'Stopping switch {name}.')
            switch.stop()
        for name, link in self.links.items():
            logger.info(f'Stopping link {name}.')
            link.stop()

    @staticmethod
    def get_link_cls(name: str) -> Type[link_lib.Link]:
        """Get a link type by name."""
        cls = link_lib.LINK_TYPES.get(name)
        if cls is None:
            raise ValueError(f'Unknown Link type "{name}" was requested.')
        return cls

    @staticmethod
    def get_node_cls(name: str) -> Union[Type[host_lib.Host], Type[switch_lib.Switch]]:
        """Get a node type by name."""
        cls = host_lib.HOST_TYPES.get(name, switch_lib.SWITCH_TYPES.get(name))
        if cls is None:
            raise ValueError(f'Unknown Switch type "{name}" was requested.')
        return cls

    async def async_add_node(self, name: str, node_type: str, node_cls: Union[str, node_lib.Node], **kwargs) -> None:
        """Add a new node to the topology asynchronously."""
        if node_type not in ('controllers', 'hosts', 'switches'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if node_cls is None:
            if node_type == 'hosts':
                node_cls = self.host_type
            elif node_type == 'switches':
                node_cls = self.switch_type
            else:
                node_cls = self.controller_type
        if isinstance(node_cls, str):
            node_cls = self.get_node_cls(node_cls)
        node = node_cls(**kwargs)
        getattr(self, node_type)[name] = node
        await node.async_start()

    def add_node(self, name: str, node_type: str, node_cls: Union[str, node_lib.Node], **kwargs) -> None:
        """Add a new node to the topology."""
        if node_type not in ('controllers', 'hosts', 'switches'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if node_cls is None:
            if node_type == 'hosts':
                node_cls = self.host_type
            elif node_type == 'switches':
                node_cls = self.switch_type
            else:
                node_cls = self.controller_type
        if isinstance(node_cls, str):
            node_cls = self.get_node_cls(node_cls)
        node = node_cls(**kwargs)
        getattr(self, node_type)[name] = node
        node.start()

    async def async_remove_node(self, name: str, node_type: str) -> None:
        """Remove a node from the topology by name and type asynchronously."""
        if node_type not in ('hosts', 'links', 'switches'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if name not in getattr(self, node_type):
            raise KeyError(f'Failed to delete node. A {node_type} named "{name}" was not found in the network.')
        node = getattr(self, node_type).pop(name)
        await node.async_stop()

    def remove_node(self, name: str, node_type: str) -> None:
        """Remove a node from the topology by name and type."""
        if node_type not in ('hosts', 'links', 'switches'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if name not in getattr(self, node_type):
            raise KeyError(f'Failed to delete node. A {node_type} named "{name}" was not found in the network.')
        node = getattr(self, node_type).pop(name)
        node.stop()

    async def async_add_host(self, name: str, host_type: Union[str, host_lib.Host] = None, **kwargs) -> None:
        """Add a new host to the network topology.

        Args:
            name: The name to assign to the new host. Must be unique.
            host_type: A custom type of host to use. Otherwise, it will use self.host_type.
        """
        await self.async_add_node(name, 'hosts', host_type, **kwargs)

    def add_host(self, name: str, host_type: Union[str, host_lib.Host] = None, **kwargs) -> None:
        """Add a new host to the network topology.

        Args:
            name: The name to assign to the new host. Must be unique.
            host_type: A custom type of host to use. Otherwise, it will use self.host_type.
        """
        self.add_node(name, 'hosts', host_type, **kwargs)

    async def async_add_link(self, name: str, link_type: Union[str, link_lib.Link] = None, **kwargs) -> None:
        """Add a new link to the network topology asynchronously.

        Args:
            name: The name to assign to the new link. Must be unique.
            link_type: A custom type of link to use. Otherwise, it will use self.link_type.
        """
        await self.async_add_node(name, 'links', link_type, **kwargs)

    def get_node_by_name(self, name: str) -> Union[host_lib.Host, switch_lib.Switch]:
        """Get a node by name.

        Args:
            name: The name of the node to get.

        Returns:
            node: The node, if found.

        Raises:
            KeyError: If the node is not found.
        """
        node = self.hosts.get(name, self.switches.get(name))
        if node is None:
            raise KeyError(f'The node "{name}" does not exist in the topology.')
        return node

    def add_link(self, name: str, src_port: str, dst_port: str, link_type: Union[str, link_lib.Link] = None, **kwargs) -> None:
        """Add a new link to the network topology.

        Args:
            name: The name to assign to the new link. Must be unique.
            src_port: The source of the link (port is required, e.g. h1.0).
            dst_port: The destination of the link (port is required, e.g. s1.0)
            link_type: A custom type of link to use. Otherwise, it will use self.link_type.
        """
        # TODO: Configure bandwidth and delay.
        # TODO: Configure interface types.
        src, src_port = src_port.rsplit('.', 1)  # host1.0 -> host1, 0
        src_node = self.get_node_by_name(src)
        dst, dst_port = dst_port.rsplit('.', 1)  # host1.0 -> host1, 0
        dst_node = self.get_node_by_name(dst)
        src_node.interfaces[src_port] = dst_port
        dst_node.interfaces[dst_port] = src_port
        link_cls = self.get_link_cls(link_type)
        link = link_cls(**kwargs)
        self.links[name] = link

    async def async_add_switch(self, name: str, switch_type: Union[str, switch_lib.Switch] = None, **kwargs) -> None:
        """Add a new switch to the network topology asynchronously.

        Args:
            name: The name to assign to the new switch. Must be unique.
            switch_type: A custom type of switch to use. Otherwise, it will use self.switch_type.
        """
        await self.async_add_node(name, 'switches', switch_type, **kwargs)

    def add_switch(self, name: str, switch_type: Union[str, switch_lib.Switch] = None, **kwargs) -> None:
        """Add a new switch to the network topology.

        Args:
            name: The name to assign to the new switch. Must be unique.
            switch_type: A custom type of switch to use. Otherwise, it will use self.switch_type.
        """
        self.add_node(name, 'switches', switch_type, **kwargs)

    async def async_remove_host(self, name: str) -> None:
        """Remove an existing host by name asynchronously.

        Args:
            name: The name of the host to remove.

        Raises:
            KeyError: If the host name was not found.
        """
        await self.async_remove_node(name, 'hosts')

    def remove_host(self, name: str) -> None:
        """Remove an existing host by name.

        Args:
            name: The name of the host to remove.

        Raises:
            KeyError: If the host name was not found.
        """
        self.remove_node(name, 'hosts')

    async def async_remove_link(self, name: str) -> None:
        """Remove an existing link by name asynchronously.

        Args:
            name: The name of the link to remove.

        Raises:
            KeyError: If the link name was not found.
        """
        # TODO: Do this async.
        self.remove_link(name)

    def remove_link(self, name: str) -> None:
        """Remove an existing link by name.

        Args:
            name: The name of the link to remove.

        Raises:
            KeyError: If the link name was not found.
        """
        link = self.links.pop(name, None)
        if link is None:
            raise KeyError(f'Failed to remove link "{name}". It was not found.')
        link.stop()
        src = self.get_node_by_name(link.src)
        dst = self.get_node_by_name(link.dst)
        src.interfaces[src] = None
        dst.interfaces[dst] = None

    async def async_remove_switch(self, name: str) -> None:
        """Remove an existing switch by name asynchronously.

        Args:
            name: The name of the switch to remove.

        Raises:
            KeyError: If the switch name was not found.
        """
        await self.async_remove_node(name, 'switches')

    def remove_switch(self, name: str) -> None:
        """Remove an existing switch by name.

        Args:
            name: The name of the switch to remove.

        Raises:
            KeyError: If the switch name was not found.
        """
        self.remove_node(name, 'switches')


class LinearTopology(Topology):
    """Linear Topology with 2 switches and 1 host on each switch.

    H1 - S1 = S2 - H2
    """

    def build(self) -> None:
        """Build a linear topology."""
        self.add_host('h1')
        self.add_host('h2')
        self.add_switch('s1')
        self.add_switch('s2')
        self.add_link('h1 to s1', 'h1.0', 's1.0')
        self.add_link('h2 to s2', 'h2.0', 's2.0')
        self.add_link('s1-s2 trunc', 's1.1', 's2.1')


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
    'linear': LinearTopology,
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
