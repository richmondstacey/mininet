"""Controller node types."""

from mininet3.core.node_lib import Node, DockerNode


class Controller(Node):
    """Base controller type."""

    subclasses = {}

    def __init_subclass__(cls, **kwargs) -> None:
        """Register subclasses."""
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__name__] = cls


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
