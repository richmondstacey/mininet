"""Host node types."""

from mininet3.core.nodes.base import Node


class Host(Node):
    """Base class for all Host types."""


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
    # 'cfs': CFSHost,
    # 'proc': ProcHost,
    # 'rt': RTHost,
}
