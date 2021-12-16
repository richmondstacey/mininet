"""Mininet Network emulation."""

# TODO: Add topology constructors from: JSON, YAML, GraphDB, etc.

import logging

from mininet3.core import topology_lib

logger = logging.getLogger(__name__)

DEPLOYMENT_TYPES = (
    'local',
    'docker',
    # TODO:
    # 'remote',  # SSH deployment
    # 'docker-swarm',
    # 'kubernetes',
    # 'aws-ec2',
    # 'aws-ecs',
    # 'aws-eks',
    # 'custom',
)


class Mininet3:
    """Mininet Network Emulator for Python3."""

    def __init__(self, deployment_type: str = 'local', topology_type: str = 'default', **kwargs) -> None:
        """Create the emulated network.

        Args:
            deployment_type: The type of deployment to run Mininet in. See: DEPLOYMENT_TYPES
            topology_type: The topology type to deploy in Mininet.
        """
        if deployment_type not in DEPLOYMENT_TYPES:
            raise ValueError(f'Invalid deployment type "{deployment_type}" was given.')
        self.deployment_type = deployment_type
        topology_cls = topology_lib.get_topology_by_name(topology_type)
        self.topology: topology_lib.Topology = topology_cls(deployment_type=deployment_type, **kwargs)

    async def async_start(self) -> None:
        """Start Mininet asynchronously."""
        await self.topology.async_build()
        await self.topology.async_start()

    def start(self) -> None:
        """Start the Mininet simulator."""
        logger.info('Starting the simulated network.')
        self.topology.build()
        self.topology.start()
