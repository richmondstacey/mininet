"""Switch node types."""

from mininet3.core.node_lib import Node, DockerNode


class Switch(Node):
    """Base class for all Switch types."""


class DockerSwitch(DockerNode, Switch):
    """Base class for launching a switch within a Docker container."""


# class IVSSwitch(Switch):
#     """IVS Switch placeholder."""
#
#
# class LXBRSwitch(Switch):
#     """LXBR Switch placeholder."""
#
#
# class OVSSwitch(Switch):
#     """OVS Switch placeholder."""
#
#
# class OVSBRSwitch(Switch):
#     """OVS-BR Switch placeholder."""
#
#
# class OVSKSwitch(Switch):
#     """OVS-K Switch placeholder."""
#
#
# class UserSwitch(Switch):
#     """User Switch placeholder."""


SWITCH_TYPES = {
    'default': Switch,
    'docker': DockerSwitch,
    # 'ivs': IVSSwitch,
    # 'lxbr': LXBRSwitch,
    # 'ovs': OVSSwitch,
    # 'ovsbr': OVSBRSwitch,
    # 'ovsk': OVSKSwitch,
    # 'user': UserSwitch,
}
