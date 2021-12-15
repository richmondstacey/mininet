"""Network emulation."""

# TODO: Add constructors from JSON, YAML, NEO4J, etc.

import logging

from typing import Union

from mininet3 import nodes

logger = logging.getLogger(__name__)


class Mininet3:
    """Mininet Network Emulator for Python3."""

    def __init__(
            self,
            topology_type: str = 'linear',
            switch_type: str = 'ovs',
            host_type: str = 'cfs',
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
        self.switch_type = switch_type
        self.host_type = host_type
        self.controller_type = controller_type
        self.link_type = link_type
        self.interface_type = interface_type
        self.ip_base = kwargs.get('ip_base', '10.0.0.0')
        self.set_mac_addresses = kwargs.get('set_mac_addresses', True)
        self.static_arp = kwargs.get('static_arp', True)
        self.pin_cpus = kwargs.get('pin_cpus', False)
        self.listen_port = kwargs.get('listen_port', 8000)
        self.sw_wait_sec = kwargs.get('sw_wait_sec', 60)
        topology_cls = nodes.get_cls_by_name(topology_type, 'topology')
        self.topology: nodes.Topology = topology_cls()

    def _add_node(self, name: str, node_type: str, node_cls: Union[str, nodes.Node]) -> None:
        """Add a new node to the topology."""
        if node_type not in ('hosts', 'links', 'switches'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if isinstance(node_cls, str):
            node_cls = nodes.get_cls_by_name(name, node_type)
        node = node_cls()
        getattr(self.topology, node_type)[name] = node

    def _remove_node(self, name: str, node_type: str) -> None:
        """Remove a node from the topology by name and type."""
        if node_type not in ('host', 'link', 'switch'):
            raise ValueError(f'Invalid Node Type "{node_type}" was specified.')
        if name not in getattr(self.topology, node_type):
            raise KeyError(f'Failed to delete node. A {node_type} named "{name}" was not found in the network.')
        getattr(self.topology, node_type).pop(name)

    def start(self) -> None:
        """Start the Mininet simulator."""
        logger.info('Starting the simulated network.')
        self.topology.start()

    def add_host(self, name: str, host_type: Union[str, nodes.Host] = None) -> None:
        """Add a new host to the network topology.

        Args:
            name: The name to assign to the new host. Must be unique.
            host_type: A custom type of host to use. Otherwise, it will use self.host_type.
        """
        self._add_node(name, 'host', host_type)

    def add_link(self, name: str, link_type: Union[str, nodes.Link] = None) -> None:
        """Add a new link to the network topology.

        Args:
            name: The name to assign to the new link. Must be unique.
            link_type: A custom type of link to use. Otherwise, it will use self.link_type.
        """
        self._add_node(name, 'link', link_type)

    def add_switch(self, name: str, switch_type: Union[str, nodes.Switch] = None) -> None:
        """Add a new switch to the network topology.

        Args:
            name: The name to assign to the new switch. Must be unique.
            switch_type: A custom type of switch to use. Otherwise, it will use self.switch_type.
        """
        self._add_node(name, 'switch', switch_type)

    def remove_host(self, name: str) -> None:
        """Remove an existing host by name.

        Args:
            name: The name of the host to remove.

        Raises:
            KeyError: If the host name was not found.
        """
        self._remove_node(name, 'host')

    def remove_link(self, name: str) -> None:
        """Remove an existing link by name.

        Args:
            name: The name of the link to remove.

        Raises:
            KeyError: If the link name was not found.
        """
        self._remove_node(name, 'link')

    def remove_switch(self, name: str) -> None:
        """Remove an existing switch by name.

        Args:
            name: The name of the switch to remove.

        Raises:
            KeyError: If the switch name was not found.
        """
        self._remove_node(name, 'switch')
