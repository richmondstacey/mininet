#!/usr/bin/env python
"""Setup tools parameters."""

import os

from setuptools import setup
from os.path import join

from mirror_net import __version__

MODNAME = DIST_NAME = 'mirror_net'
RELATIVE_DIR = os.path.dirname(__file__)
SCRIPTS = [join('bin', filename) for filename in ['mn']]


def _read_requirements() -> list:
    """Read the requirements.txt file."""
    with open(os.path.join(RELATIVE_DIR, 'mirror_net/requirements.txt'), 'rt') as file:
        requires = file.readlines()
    return requires


setup(
    name=DIST_NAME,
    version=__version__,
    description='Realtime Network Simulator based upon Mininet and Kathara',
    author='Rich Stacey',
    packages=['mirror_net'],
    python_requires='>3.8.0',
    license='BSD',
    install_requires=_read_requirements(),
    scripts=SCRIPTS,
)
