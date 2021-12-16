"""Controller node types."""

from mininet3.core.node_lib import Node, DockerNode


class Controller(Node):
    """Base controller type."""


class DockerController(DockerNode, Controller):
    """Base class for launching a controller within a Docker container."""


# class NOXController(Controller):
#     """NOX Controller placeholder."""
#
#
# class OVSCController(Controller):
#     """OVSC Controller placeholder."""
#
#
# class REFController(Controller):
#     """Ref Controller placeholder."""
#
#
# class RemoteController(Controller):
#     """Remote Controller placeholder."""
#
#
# class RyuController(Controller):
#     """Ryu Controller placeholder."""


CONTROLLER_TYPES = {
    'default': Controller,
    'docker': DockerController,
    # 'nox': NOXController,
    # 'ovsc': OVSCController,
    # 'ref': REFController,
    # 'remote': RemoteController,
    # 'ryu': RyuController,
}
