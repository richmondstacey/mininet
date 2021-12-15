"""Controller node types."""

from mininet3.nodes.base import Node


class Controller(Node):
    """Base controller type."""


class NOXController(Controller):
    """NOX Controller placeholder."""


class OVSCController(Controller):
    """OVSC Controller placeholder."""


class REFController(Controller):
    """Ref Controller placeholder."""


class RemoteController(Controller):
    """Remote Controller placeholder."""


class RyuController(Controller):
    """Ryu Controller placeholder."""


CONTROLLER_TYPES = {
    'default': Controller,
    'nox': NOXController,
    'ovsc': OVSCController,
    'ref': REFController,
    'remote': RemoteController,
    'ryu': RyuController,
}
