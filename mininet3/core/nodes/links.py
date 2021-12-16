"""Link types."""

from mininet3.core.nodes.base import Node


class Link(Node):
    """Base class for all Link types."""

#
# class OVSLink(Link):
#     """OVS Link placeholder."""
#
#
# class TCULink(Link):
#     """TCU Link placeholder."""


LINK_TYPES = {
    'default': Link,
    # 'ovs': OVSLink,
    # 'tcu': TCULink,
}
