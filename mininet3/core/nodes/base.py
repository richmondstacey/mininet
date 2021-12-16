"""Base Node type and helpers."""

import abc


class Node(metaclass=abc.ABCMeta):
    """The base network node type."""

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
