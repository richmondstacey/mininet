"""OpenVSwitch + Ryu controller."""

from mirror_net.core.controller_lib import DockerController
from mirror_net.core.switch_lib import DockerSwitch


class OpenflowController(DockerController):
    """Base class for a Ryu Openflow Controller."""

    command = 'touch keepalive && less keepalive'
    image = 'kathara/sdn'


class OpenflowSwitch(DockerSwitch):
    """Base class for a Ryu Openflow Switch."""

    command = 'touch keepalive && less keepalive'
    image = 'kathara/sdn'
