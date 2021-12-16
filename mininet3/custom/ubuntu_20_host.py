"""Ubuntu 20.04 Alpine Host."""

from mininet3.core.host_lib import DockerHost


class Ubuntu20AlpineHost(DockerHost):
    """Base class for an Ubuntu 20.04 host."""

    command = 'touch keepalive && less keepalive'
    image = 'ubuntu:20.04-alpine'
