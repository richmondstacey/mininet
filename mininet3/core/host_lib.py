"""Host node types."""

from mininet3.core.node_lib import Node, DockerNode


class Host(Node):
    """Base class for all Host types."""

    subclasses = {}

    def __init_subclass__(cls, **kwargs) -> None:
        """Register subclasses."""
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__name__] = cls


class DockerHost(DockerNode, Host):
    """Base class for launching a host within a Docker container."""


# class CFSHost(Host):
#     """CFS Host placeholder."""
#
#
# class ProcHost(Host):
#     """Proc Host placeholder."""
#
#
# class RTHost(Host):
#     """RT Host placeholder."""


HOST_TYPES = {
    'default': Host,
    'docker': DockerHost,
    # 'cfs': CFSHost,
    # 'proc': ProcHost,
    # 'rt': RTHost,
}
