"""Base Node type and helpers."""

import abc
import logging

import docker

from mininet3.core.interface_lib import INTERFACE_TYPES

logger = logging.getLogger(__name__)


class Node(metaclass=abc.ABCMeta):
    """The base network node type."""

    def __init__(self, interface_type: str = 'default', num_interfaces: int = 1, **kwargs) -> None:
        """Initialize all interfaces for the node."""
        iface_cls = INTERFACE_TYPES.get(interface_type)
        if iface_cls is None:
            raise ValueError(f'Invalid interface type "{interface_type}" was requested.')
        self.interfaces = {index: iface_cls() for index in range(num_interfaces)}

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
