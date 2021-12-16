"""Host node types."""

from mininet3.core.node_lib import Node, DockerNode


class Host(Node):
    """Base class for all Host types."""


class DockerHost(DockerNode, Host):
    """Base class for launching a host within a Docker container."""


class UbuntuHost(DockerHost):
    """Base class for an Ubuntu 20.04 host."""

    command = 'touch keepalive && less keepalive'
    image = 'ubuntu:20.04'


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
    'ubuntu': UbuntuHost,
    # 'cfs': CFSHost,
    # 'proc': ProcHost,
    # 'rt': RTHost,
}
