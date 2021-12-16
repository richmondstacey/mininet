"""Behavioral Model (BMv2) P4 controller."""

from mirror_net.core.controller_lib import DockerController
from mirror_net.core.switch_lib import DockerSwitch


class BMv2P4Controller(DockerController):
    """Base class for a P4 Controller."""

    command = 'touch keepalive && less keepalive'
    image = 'kathara/p4'


class BMv2Switch(DockerSwitch):
    """Base class for BMv2 Switch."""

    command = 'touch keepalive && less keepalive'
    image = 'kathara/p4'
