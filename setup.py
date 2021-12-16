#!/usr/bin/env python
"""Setup tools parameters."""

import os

from setuptools import setup
from os.path import join

from mininet.net import VERSION

MODNAME = DIST_NAME = 'mininet'
RELATIVE_DIR = os.path.dirname(__file__)
SCRIPTS = [join('bin', filename) for filename in ['mn']]


def _read_requirements() -> list:
    """Read the requirements.txt file."""
    with open(os.path.join(RELATIVE_DIR, 'mininet3/requirements.txt'), 'rt') as file:
        requires = file.readlines()
    return requires


setup(
    name=DIST_NAME,
    version=VERSION,
    description='Process-based OpenFlow emulator',
    author='Bob Lantz',
    author_email='rlantz@cs.stanford.edu',
    packages=['mininet', 'mininet.examples'],
    python_requires='>3.8.0',
    long_description="""
        Mininet is a network emulator which uses lightweight
        virtualization to create virtual networks for rapid
        prototyping of Software-Defined Network (SDN) designs
        using OpenFlow. http://mininet.org
        """,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: System :: Emulators",
    ],
    keywords='networking emulator protocol Internet OpenFlow SDN',
    license='BSD',
    install_requires=_read_requirements(),
    scripts=SCRIPTS,
)
