"""Host node types."""

from mininet3.nodes.base import Node


class Host(Node):
    """Base class for all Host types."""


class CFSHost(Host):
    """CFS Host placeholder."""


class ProcHost(Host):
    """Proc Host placeholder."""


class RTHost(Host):
    """RT Host placeholder."""


HOST_TYPES = {
    'cfs': CFSHost,
    'proc': ProcHost,
    'rt': RTHost,
}
