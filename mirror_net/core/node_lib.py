"""Base Node type and helpers."""

import abc
import ipaddress
import logging

import docker

from pyroute2 import NDB

logger = logging.getLogger(__name__)


class Node(metaclass=abc.ABCMeta):
    """The base network node type."""

    def __init__(
            self,
            num_interfaces: int = 1,
            base_ip_address: str = '10.0.0.0',
            subnet_cidr: int = 24,
            **kwargs,
    ) -> None:
        """Initialize all interfaces for the node."""
        self.network = NDB()
        self.available_addresses = ipaddress.ip_network(f'{base_ip_address}/{subnet_cidr}').hosts()
        self.interfaces = {index: self.add_interface(index) for index in range(num_interfaces)}

    def generate_ip(self) -> str:
        """Generate an IP address within the subnet range.

        Yields:
            address: An IP address from the subnet range.
        """
        address = next(self.available_addresses)
        return address

    def add_interface(
            self,
            index: int,
            ip_address: str = None,
            subnet_cidr: int = 24,
    ):
        """Add a new interface to the node."""
        if not ip_address:
            ip_address = self.generate_ip()
        # TODO: Generate MAC address?
        # TODO: Bandwidth, delay, jitter: tc qdisc add
        # https://pypi.org/project/tcconfig/
        iface = self.network.interfaces.create(
            ifname=f'veth{index}',
            kind='veth',
            # TODO: What goes here for peer?
            # peer={'ifname': 'eth0', 'net_ns_fd': 'testns'},
        )
        iface.set('state', 'up')
        # TODO: Does this use prefixlen or mask?
        iface.add_ip(address=ip_address, prefixlen=subnet_cidr)
        iface.commit()
        return iface

    def delete_interface(self, index: int) -> None:
        """Delete an interface by index."""
        # TODO: Add logic here.

    def list_interfaces(self) -> list:
        """List all interfaces on the node."""
        interfaces = [dict(iface) for iface in self.network.interfaces.summary()]
        return interfaces

    async def async_start(self) -> None:
        """Start running the node asynchronously."""
        raise NotImplementedError('Must be implemented by each sub-class type.')

    def start(self) -> None:
        """Start running the node."""
        raise NotImplementedError('Must be implemented by each sub-class type.')

    async def async_stop(self) -> None:
        """Stop running the node asynchronously."""
        raise NotImplementedError('Must be implemented by each sub-class type.')

    def stop(self) -> None:
        """Stop the node."""
        raise NotImplementedError('Must be implemented by each sub-class type.')


class DockerNode(Node):
    """A network Node which runs within its own Docker container."""

    command: str = None
    image: str = None

    def __init__(self, image: str = None, command: str = None, **kwargs) -> None:
        """Add docker container/image parameters."""
        super().__init__(**kwargs)
        self.image = image or self.image
        self.command = command or self.command
        self.container_id = None

    async def async_start(self) -> None:
        """Start the host container asynchronously."""
        # TODO: Do this via async docker calls?
        self.start()

    def start(self) -> None:
        """Start the Host container."""
        if not self.image or not self.command:
            raise ValueError(f'Cannot start Docker container. Missing image and/or command.')
        docker_client = docker.from_env()
        logger.info(f'Starting Docker container with image {self.image} and command: {self.command}')
        container = docker_client.containers.run(image=self.image, detach=True, command=self.command)
        self.container_id = container.id
        logger.info(f'New Docker container ID {self.container_id}.')

    async def async_stop(self) -> None:
        """Start the host container asynchronously."""
        # TODO: Do this via async docker calls?
        self.stop()

    def stop(self) -> None:
        """Stop the Host container."""
        docker_client = docker.from_env()
        logger.warning(f'Stopping Docker container with ID {self.container_id}.')
        container = docker_client.containers.get(self.container_id)
        container.stop()
