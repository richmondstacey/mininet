"""Network emulation."""
# TODO: Add constructors from JSON, YAML, NEO4J, etc.

import logging

from typing import Union

from mininet3.core import nodes
from mininet3.core import topology

logger = logging.getLogger(__name__)

DEPLOYMENT_TYPES = (
    'local',
    # TODO:
    # 'remote',  # SSH deployment
    # 'docker',
    # 'docker-swarm',
    # 'kubernetes',
    # 'aws-ec2',
    # 'aws-ecs',
    # 'aws-eks',
    # 'custom',
)


class Mininet3:  # pylint: disable=too-many-instance-attributes
    """Mininet Network Emulator for Python3."""

    def __init__(  # pylint: disable=too-many-arguments
            self,
            deployment_type: str = 'local',
            topology_type: str = 'default',
            switch_type: str = 'default',
            host_type: str = 'default',
            controller_type: str = 'default',
            link_type: str = 'default',
            interface_type: str = 'default',
            **kwargs
    ) -> None:
        """Create the emulated network.

        Args:
            topology_type: The topology type. See: mn3.TOPOLOGY_CHOICES
            switch_type: The default switch type. See: mn3.SWITCH_CHOICES
            host_type: The default host type. See: mn3.HOST_CHOICES
            controller_type: The default controller type. See: mn3.CONTROLLER_CHOICES
            link_type: The default link type. See: mn3.LINK_CHOICES
            interface_type: the default interface type. See: mn3.INTERFACE_CHOICES

        Keyword Args:
            ip_base: The base IP address for all devices. Default: 10.0.0.x
            set_host_macs: Automatically assign MAC addresses to hosts.
            static_arp: Set all-pairs static ARP.
            pin_cpus: Pin hosts to real CPU cores. This requires CPULimitedHost host_type.
            listen_port: The listening port to bind.
            sw_wait_sec: How many seconds to wait for switches to connect (or don't wait if set to None/False/0).
            # TODO: inNamespace support for port mappings?
        """
        if deployment_type not in DEPLOYMENT_TYPES:
            raise ValueError(f'Invalid deployment type "{deployment_type}" was given.')
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
        topology_cls = topology.get_topology_by_name(topology_type)
        self.topology: topology.Topology = topology_cls()

    async def _async_add_node(self, name: str, node_type: str, node_cls: Union[str, nodes.Node]) -> None:
        """Add a new node to the topology asynchronously."""
        await self.topology.async_add_node(name=name, node_type=node_type, node_cls=node_cls)

    def _add_node(self, name: str, node_type: str, node_cls: Union[str, nodes.Node]) -> None:
        """Add a new node to the topology."""
        self.topology.add_node(name=name, node_type=node_type, node_cls=node_cls)

    async def _async_remove_node(self, name: str, node_type: str) -> None:
        """Remove a node from the topology by name and type asynchronously."""
        await self.topology.async_remove_node(name=name, node_type=node_type)

    def _remove_node(self, name: str, node_type: str) -> None:
        """Remove a node from the topology by name and type."""
        self.topology.remove_node(name=name, node_type=node_type)

    async def async_start(self) -> None:
        """Start Mininet asynchronously."""
        await self.topology.async_build()
        await self.topology.async_start()

    def start(self) -> None:
        """Start the Mininet simulator."""
        logger.info('Starting the simulated network.')
        self.topology.build()
        self.topology.start()

    async def async_add_host(self, name: str, host_type: Union[str, nodes.Host] = None) -> None:
        """Add a new host to the network topology.

        Args:
            name: The name to assign to the new host. Must be unique.
            host_type: A custom type of host to use. Otherwise, it will use self.host_type.
        """
        await self._async_add_node(name, 'host', host_type)

    def add_host(self, name: str, host_type: Union[str, nodes.Host] = None) -> None:
        """Add a new host to the network topology.

        Args:
            name: The name to assign to the new host. Must be unique.
            host_type: A custom type of host to use. Otherwise, it will use self.host_type.
        """
        self._add_node(name, 'host', host_type)

    async def async_add_link(self, name: str, link_type: Union[str, nodes.Link] = None) -> None:
        """Add a new link to the network topology asynchronously.

        Args:
            name: The name to assign to the new link. Must be unique.
            link_type: A custom type of link to use. Otherwise, it will use self.link_type.
        """
        await self._async_add_node(name, 'link', link_type)

    def add_link(self, name: str, link_type: Union[str, nodes.Link] = None) -> None:
        """Add a new link to the network topology.

        Args:
            name: The name to assign to the new link. Must be unique.
            link_type: A custom type of link to use. Otherwise, it will use self.link_type.
        """
        self._add_node(name, 'link', link_type)

    async def async_add_switch(self, name: str, switch_type: Union[str, nodes.Switch] = None) -> None:
        """Add a new switch to the network topology asynchronously.

        Args:
            name: The name to assign to the new switch. Must be unique.
            switch_type: A custom type of switch to use. Otherwise, it will use self.switch_type.
        """
        await self._async_add_node(name, 'switch', switch_type)

    def add_switch(self, name: str, switch_type: Union[str, nodes.Switch] = None) -> None:
        """Add a new switch to the network topology.

        Args:
            name: The name to assign to the new switch. Must be unique.
            switch_type: A custom type of switch to use. Otherwise, it will use self.switch_type.
        """
        self._add_node(name, 'switch', switch_type)

    async def async_remove_host(self, name: str) -> None:
        """Remove an existing host by name asynchronously.

        Args:
            name: The name of the host to remove.

        Raises:
            KeyError: If the host name was not found.
        """
        await self._async_remove_node(name, 'host')

    def remove_host(self, name: str) -> None:
        """Remove an existing host by name.

        Args:
            name: The name of the host to remove.

        Raises:
            KeyError: If the host name was not found.
        """
        self._remove_node(name, 'host')

    async def async_remove_link(self, name: str) -> None:
        """Remove an existing link by name asynchronously.

        Args:
            name: The name of the link to remove.

        Raises:
            KeyError: If the link name was not found.
        """
        await self._async_remove_node(name, 'link')

    def remove_link(self, name: str) -> None:
        """Remove an existing link by name.

        Args:
            name: The name of the link to remove.

        Raises:
            KeyError: If the link name was not found.
        """
        self._remove_node(name, 'link')

    async def async_remove_switch(self, name: str) -> None:
        """Remove an existing switch by name asynchronously.

        Args:
            name: The name of the switch to remove.

        Raises:
            KeyError: If the switch name was not found.
        """
        await self._async_remove_node(name, 'switch')

    def remove_switch(self, name: str) -> None:
        """Remove an existing switch by name.

        Args:
            name: The name of the switch to remove.

        Raises:
            KeyError: If the switch name was not found.
        """
        self._remove_node(name, 'switch')
