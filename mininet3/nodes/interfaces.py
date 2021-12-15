"""Interface node types."""

from mininet3.nodes.base import Node


class Interface(Node):
    """Base class for all Interface types."""


INTERFACE_TYPES = {
    'default': Interface,
}
