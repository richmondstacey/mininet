"""Base Node type and helpers."""

import abc


class Node(metaclass=abc.ABCMeta):
    """The base network node type."""

    def start(self) -> None:
        """Start running the topology."""
        raise NotImplementedError('Must be implemented by each sub-class type.')
