"""Switch node types."""

from mininet3.nodes.base import Node


class Switch(Node):
    """Base class for all Switch types."""


class IVSSwitch(Switch):
    """IVS Switch placeholder."""


class LXBRSwitch(Switch):
    """LXBR Switch placeholder."""


class OVSSwitch(Switch):
    """OVS Switch placeholder."""


class OVSBRSwitch(Switch):
    """OVS-BR Switch placeholder."""


class OVSKSwitch(Switch):
    """OVS-K Switch placeholder."""


class UserSwitch(Switch):
    """User Switch placeholder."""


SWITCH_TYPES = {
    'default': Switch,
    'ivs': IVSSwitch,
    'lxbr': LXBRSwitch,
    'ovs': OVSSwitch,
    'ovsbr': OVSBRSwitch,
    'ovsk': OVSKSwitch,
    'user': UserSwitch,
}
