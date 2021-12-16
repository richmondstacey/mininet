"""Node types and helper utilities."""

from typing import Type, Union

from mininet3.core.nodes.controllers import Controller, CONTROLLER_TYPES
from mininet3.core.nodes.hosts import Host, HOST_TYPES
from mininet3.core.nodes.interfaces import Interface, INTERFACE_TYPES
from mininet3.core.nodes.links import Link, LINK_TYPES
from mininet3.core.nodes.base import Node
from mininet3.core.nodes.switches import Switch, SWITCH_TYPES

NODES_BY_TYPE = {
    'controller': CONTROLLER_TYPES,
    'host': HOST_TYPES,
    'interface': INTERFACE_TYPES,
    'link': LINK_TYPES,
    'switch': SWITCH_TYPES,
}


def get_cls_by_name(
        name: str,
        node_type: str,
) -> Union[Type[Node], Type[Host], Type[Link], Type[Switch]]:
    """Get the node class based upon its name and type.

    Args:
        name: The name of the node class.
        node_type: The type of node. Choices: controller, host, interface, link, switch, or topology.

    Returns:
        node_cls: The Node class type, if found.

    Raises:
        ValueError: if the node class type or node name was not found.
    """
    if node_type not in NODES_BY_TYPE:
        raise ValueError(f'Invalid node type "{node_type}" requested.')
    if name not in NODES_BY_TYPE[node_type]:
        raise ValueError(f'No {node_type} named "{name}" was found.')
    node_cls = NODES_BY_TYPE[node_type][name]
    return node_cls


__all__ = (
    'get_cls_by_name',
    'NODES_BY_TYPE',
    'Controller',
    'CONTROLLER_TYPES',
    'Host',
    'HOST_TYPES',
    'Interface',
    'INTERFACE_TYPES',
    'Link',
    'LINK_TYPES',
    'Node',
    'Switch',
    'SWITCH_TYPES',
)
